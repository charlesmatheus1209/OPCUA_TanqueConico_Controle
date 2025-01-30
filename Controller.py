import sys
import time
from opcua import Client
import socket
import threading
import time

global_values = {"l1":0,
                 "l2":0,
                 "l3":0,
                 "q1":0,
                 "q2":0,
                 "q3":0,
                 "sp1":0,
                 "sp2":0,
                 "sp2":0
                }




class TCPServer:
    def __init__(self, host="0.0.0.0", port=12345):
        self.host = host
        self.port = port
        self.setpoints = [0.0, 0.0, 0.0]  # Setpoints iniciais
        self.lock = threading.Lock()

    def encode_dict_to_string(self, dictionary):
        # Cria a string concatenando as chaves e valores, separando com ';' entre pares
        encoded_string = ";".join(f"{key}={value}" for key, value in dictionary.items())
        return encoded_string

    def decode_string_to_dict(self, encoded_string):
        pairs = encoded_string.split(";")    
        decoded_dict = {pair.split("=")[0]: float(pair.split("=")[1]) for pair in pairs}    
        return decoded_dict

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break
                print(f"Recebido: {data}")

                # Parse the setpoints
                try:
                    if('GET' in data):
                        global_values["sp1"] = self.get_setpoints()[0]
                        global_values["sp2"] = self.get_setpoints()[1]
                        global_values["sp3"] = self.get_setpoints()[2]
                        
                        client_socket.sendall(self.encode_dict_to_string(global_values).encode("utf-8"))
                    else:
                        decoded = self.decode_string_to_dict(data)
                        self.setpoints = [decoded["sp1"], decoded["sp2"], decoded["sp3"]]
                        global_values["sp1"] = decoded["sp1"]
                        global_values["sp2"] = decoded["sp2"]
                        global_values["sp3"] = decoded["sp3"]
                            
                except ValueError:
                    client_socket.sendall("Erro: Enviar apenas números separados por vírgula.\n".encode("utf-8"))
        except Exception as ex:
            print(f"Erro ao lidar com cliente: {ex}")
        finally:
            client_socket.close()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Servidor TCP iniciado em {self.host}:{self.port}")

        try:
            while True:
                client_socket, addr = server.accept()
                print(f"Conexão aceita de {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Servidor encerrado.")
        finally:
            server.close()

    def get_setpoints(self):
        with self.lock:
            return self.setpoints

class OPCUAConnection:
    def __init__(self, url):
        self.url = url
        self.connect_opcua()

    def connect_opcua(self):
        try:
            self.client = Client(self.url)
            self.client.connect()
            print("Connected to OPC UA server")
        except Exception as ex:
            print(f"Error connecting to OPC UA server: {ex}")
            sys.exit(1)

    def get_value(self, node_id):
        try:
            node = self.client.get_node(node_id)
            return node.get_value()
        except Exception as ex:
            print(f"Error reading value from node {node_id}: {ex}")
            sys.exit(1)

    def set_value(self, node_id, value):
        try:
            node = self.client.get_node(node_id)
            node.set_value(value)
        except Exception as ex:
            print(f"Error writting value from node {node_id}: {ex}")
            sys.exit(1)


class ControladorSegundoGrauTCP:
    def __init__(self, opcua_connection, tcp_server):
        self.opcua = opcua_connection
        self.tcp_server = tcp_server
        self.kp = 2
        self.ki = 0.5
        self.kd = 1.0
        self.erro_anterior = [0.0, 0.0, 0.0]
        self.integral = [0.0, 0.0, 0.0]

    def executar(self):
        while True:
            try:
                # Obter níveis do OPC
                nivel_atual = [
                    self.opcua.get_value("ns=3;i=1013"),
                    self.opcua.get_value("ns=3;i=1014"),
                    self.opcua.get_value("ns=3;i=1015"),
                ]

                global_values["l1"] = nivel_atual[0]
                global_values["l2"] = nivel_atual[1]
                global_values["l3"] = nivel_atual[2]

                # Obter setpoints do servidor TCP
                setpoints = self.tcp_server.get_setpoints()

                # Controlador PID
                vazoes = []
                for i in range(3):
                    erro = setpoints[i] - nivel_atual[i]
                    self.integral[i] += erro
                    derivativo = erro - self.erro_anterior[i]
                    vazao = self.kp * erro + self.ki * self.integral[i] + self.kd * derivativo
                    vazoes.append(max(0.0, vazao))  # Garantir que a vazão não seja negativa
                    self.erro_anterior[i] = erro
                    # print(vazoes)

                # Limitando as vazões à 3m3
                for i in range(3):
                    if vazoes[i] >= 6:
                        vazoes[i] = 6

                # Enviar vazões para o OPC
                self.opcua.set_value("ns=3;i=1009", vazoes[0])
                self.opcua.set_value("ns=3;i=1010", vazoes[1])
                self.opcua.set_value("ns=3;i=1011", vazoes[2])

                self.opcua.set_value("ns=3;i=1016", setpoints[0])
                self.opcua.set_value("ns=3;i=1017", setpoints[1])
                self.opcua.set_value("ns=3;i=1018", setpoints[2])


                global_values["q1"] = vazoes[0]
                global_values["q2"] = vazoes[1]
                global_values["q3"] = vazoes[2]

                # print(f"Setpoints: {setpoints}, Níveis: {nivel_atual}, Vazões: {vazoes}")
                print(global_values)
                time.sleep(0.5)
            except Exception as ex:
                print(f"Erro no controlador: {ex}")
                break


if __name__ == "__main__":
    try:
        # Iniciar o servidor TCP
        tcp_server = TCPServer()
        tcp_thread = threading.Thread(target=tcp_server.start_server, daemon=True)
        tcp_thread.start()

        # Conectar ao OPC UA
        url = "opc.tcp://127.0.0.1:53530/OPCUA/SimulationServer"
        opcua_connection = OPCUAConnection(url)

        # Iniciar o controlador
        controlador = ControladorSegundoGrauTCP(opcua_connection, tcp_server)
        controlador.executar()
    except KeyboardInterrupt:
        print("Encerrando aplicação.")
