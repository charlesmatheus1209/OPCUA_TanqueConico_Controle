import socket
import threading
import time

def main():
    host = "127.0.0.1"  # IP do servidor (controlador)
    port = 12345        # Porta do servidor (controlador)
    
    print("Cliente para envio de setpoints iniciado.")
    print("Digite três valores de setpoint separados por vírgula (exemplo: 1.0,2.5,3.0).")
    print("Digite 'exit' para encerrar o programa.")

    while True:
        # Lê a entrada do terminal
        user_input = input("Setpoints: ")
        
        # Permite ao usuário encerrar o programa
        if user_input.lower() == "exit":
            print("Encerrando o cliente.")
            break

        try:
            # Valida e formata os setpoints
            setpoints = [float(x.strip()) for x in user_input.split(",")]
            if len(setpoints) != 3:
                print("Erro: Enviar exatamente 3 valores separados por vírgula.")
                continue
        except ValueError:
            print("Erro: Certifique-se de enviar apenas números separados por vírgula.")
            continue

        # Cria uma conexão com o servidor
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                # Envia os setpoints como uma string unida por vírgulas
                client_socket.sendall(",".join(map(str, setpoints)).encode("utf-8"))
                # Recebe a resposta do servidor
                response = client_socket.recv(1024).decode("utf-8")
                print(f"Resposta do servidor: {response}")
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar ao servidor. Verifique se ele está ativo.")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

def get_values_from_controller():
    host = "127.0.0.1"  
    port = 12345        
    
    while True:
        
        # Cria uma conexão com o servidor
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                # Envia os setpoints como uma string unida por vírgulas
                client_socket.sendall("GET".encode("utf-8"))
                # Recebe a resposta do servidor
                response = client_socket.recv(1024).decode("utf-8")
                print(f"Resposta do servidor: {decode_string_to_dict(response)}")
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar ao servidor. Verifique se ele está ativo.")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

        time.sleep(1)


def decode_string_to_dict(encoded_string):
    pairs = encoded_string.split(";")    
    decoded_dict = {pair.split("=")[0]: float(pair.split("=")[1]) for pair in pairs}    
    return decoded_dict

if __name__ == "__main__":
    get_values_thread = threading.Thread(target=get_values_from_controller, daemon=True)
    get_values_thread.start()
    
    main()
    get_values_thread.join()



