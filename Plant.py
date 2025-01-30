import sys
import time
import threading
from opcua import Client
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Shared variables
global_flow = {"Qi1": 0.0, "Qi2": 0.0, "Qi3": 0.0}
global_level = {"l1": 0.0, "l2": 0.0, "l3": 0.0}
stop_process = False
lock = threading.Lock()

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

class Plant:
    
    def __init__(self):
        # Plant Params
        self.r1 = 1
        self.R1 = 2
        self.H1 = 2
        self.gama1 = 1
        self.qo1 = 0

        self.r2 = 1
        self.R2 = 2
        self.H2 = 2
        self.gama2 = 1
        self.qo2 = 0

        self.r3 = 1
        self.R3 = 2
        self.H3 = 2
        self.gama3 = 1
        self.qo3 = 0

    def sistema_massa_mola_amortecedor(self,t, h):
        h1, h2, h3 = h 

        raio1 = (self.r1 + ((self.R1-self.r1)/self.H1) * h1)
        raio2 = (self.r2 + ((self.R2-self.r2)/self.H2) * h2)
        raio3 = (self.r3 + ((self.R3-self.r3)/self.H3) * h3)
        
        with lock:
            qi2 = global_flow["Qi2"]
            qi3 = global_flow["Qi3"]

        if(h1 <= 0):
            h1 = 0
            qo1 = 0
            qi2 = 0
        else:
            qo1 = self.gama1*np.sqrt(h1)
        
        if(h2 <= 0):
            h2 = 0
            qo2 = 0
            qi3 = 0
        else:
            qo2 = self.gama2*np.sqrt(h2)

        if(h3 <= 0):
            h3 = 0
            qo3 = 0
        else:
            qo3 = self.gama3*np.sqrt(h3)

        dh1_dt = (global_flow["Qi1"] - qo1 - qi2) / (np.pi * raio1 * raio1 )
        dh2_dt = (qi2 - qo2 - qi3) / (np.pi * raio2 * raio2 )
        dh3_dt = (qi3 - qo3) / (np.pi * raio3 * raio3 )
        return [dh1_dt, dh2_dt, dh3_dt]

    def simular_sistema(self):
        # Condições iniciais
        h1 = 0.0  # altura 1 inicial (m)
        h2 = 0.0  # altura 2 inicial (m)
        h3 = 0.0  # altura 3 inicial (m)
        condicoes_iniciais = [h1, h2, h3]

        # Tempo inicial da simulação
        tempo_inicial = 0.0
        tempo_final = 0.1  # Simular em pequenos intervalos
        dt = 0.1          # Passo do tempo

        # Dados para plotar
        historico_tempo = []
        historico_niveis = [[],[],[]]

        print("Iniciando a simulação. Altere a força a qualquer momento.")

        while not stop_process:
            # Resolver o sistema de equações diferenciais
            solucao = solve_ivp(
                self.sistema_massa_mola_amortecedor,
                [tempo_inicial, tempo_final],
                condicoes_iniciais,
                t_eval=np.linspace(tempo_inicial, tempo_final, 10)
            )

            # Atualizar as condições iniciais para o próximo intervalo
            for j in range(len(solucao.y)):
                for i in range(len(solucao.y[j])):
                    if(solucao.y[j][i] < 0):
                        solucao.y[j][i] = 0

            solucao.y[0][solucao.y[0] > self.H1] = self.H1
            solucao.y[1][solucao.y[1] > self.H2] = self.H2
            solucao.y[2][solucao.y[2] > self.H3] = self.H3

            condicoes_iniciais = [solucao.y[0][-1], solucao.y[1][-1], solucao.y[2][-1]]
            tempo_inicial = tempo_final
            tempo_final += dt

            # Salvar os resultados
            historico_tempo.extend(solucao.t)
            historico_niveis[0].extend(solucao.y[0])
            historico_niveis[1].extend(solucao.y[1])
            historico_niveis[2].extend(solucao.y[2])

            
            # Exibir os últimos resultados no console
            print(f"Tempo: {solucao.t[-1]:.2f}s, Nível 1: {solucao.y[0][-1]:.4f}m, Nível 2: {solucao.y[1][-1]:.4f}m, Nível 3: {solucao.y[2][-1]:.4f}m, Vazao i1: {global_flow['Qi1']:.2f}m, Vazao i2: {global_flow['Qi2']:.2f}m, Vazao i3: {global_flow['Qi3']:.2f}m")
            
            with lock:
                global_level['l1'] = solucao.y[0][-1]
                global_level['l2'] = solucao.y[1][-1]
                global_level['l3'] = solucao.y[2][-1]


            # Pausa para simular tempo real
            time.sleep(dt)

            # Atualizar o gráfico
            plt.clf()
            plt.plot(historico_tempo, historico_niveis[0], label="Nível 1", color="blue")
            plt.plot(historico_tempo, historico_niveis[1], label="Nível 2", color="green")
            plt.plot(historico_tempo, historico_niveis[2], label="Nível 3", color="red")
            plt.xlabel("Tempo (s)")
            plt.ylabel("Nivel (m)")
            plt.title("Tanque Cônico")
            plt.legend()
            plt.grid()
            plt.pause(0.01)

def opc_interface():
    global stop_process
    url = "opc.tcp://127.0.0.1:53530/OPCUA/SimulationServer"
    opcua = OPCUAConnection(url)

    while not stop_process:
        try:
            with lock:
                opcua.set_value("ns=3;i=1013", global_level["l1"])
                opcua.set_value("ns=3;i=1014", global_level["l2"])
                opcua.set_value("ns=3;i=1015", global_level["l3"])

                global_flow["Qi1"] = opcua.get_value("ns=3;i=1009")
                global_flow["Qi2"] = opcua.get_value("ns=3;i=1010")
                global_flow["Qi3"] = opcua.get_value("ns=3;i=1011")
            
            flag_value = opcua.get_value("ns=3;i=1012")
            print(f"Flag value: {flag_value}")
            print(f"Global flow: {global_flow}")

            if flag_value == 1:
                stop_process = True

            time.sleep(1)
        except Exception as ex:
            print(f"Error in reading_input_values: {ex}")
            break

if __name__ == "__main__":
    try:
        opc_thread = threading.Thread(target=opc_interface, daemon=True)
        opc_thread.start()

        plant = Plant()
        plant.simular_sistema()

        print("Process stopped.")
    except KeyboardInterrupt:
        print("Interrupted by user.")
        stop_process = True
    finally:
        if opc_thread.is_alive():
            opc_thread.join()
