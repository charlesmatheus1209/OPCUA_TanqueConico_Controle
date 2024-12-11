import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import threading
import time

# Parâmetros do sistema
r1 = 1
R1 = 2
H1 = 2
gama1 = 1
qo1 = 0

r2 = 1
R2 = 2
H2 = 2
gama2 = 1
qo2 = 0

r3 = 1
R3 = 2
H3 = 2
gama3 = 1
qo3 = 0


# Variável global para a força
global_force = {"Qi1": 0.0, "Qi2": 0.0, "Qi3": 0.0}

# Função para representar o sistema em forma de equações de estado
def sistema_massa_mola_amortecedor(t, h):
    h1, h2, h3 = h 

    raio1 = (r1 + ((R1-r1)/H1) * h1)
    raio2 = (r2 + ((R2-r2)/H2) * h2)
    raio3 = (r3 + ((R3-r3)/H3) * h3)
    
    qi2 = global_force["Qi2"]
    qi3 = global_force["Qi3"]

    if(h1 <= 0):
        h1 = 0
        qo1 = 0
        qi2 = 0
    else:
        qo1 = gama1*np.sqrt(h1)
    
    if(h2 <= 0):
        h2 = 0
        qo2 = 0
        qi3 = 0
    else:
        qo2 = gama2*np.sqrt(h2)

    if(h3 <= 0):
        h3 = 0
        qo3 = 0
    else:
        qo3 = gama3*np.sqrt(h3)

    
    # print(f"qo1: {qo1}")
    # print(f"qo2: {qo2}")
    # print(f"qo3: {qo3}")

    dh1_dt = (global_force["Qi1"] - qo1 - qi2) / (np.pi * raio1 * raio1 )
    dh2_dt = (qi2 - qo2 - qi3) / (np.pi * raio2 * raio2 )
    dh3_dt = (qi3 - qo3) / (np.pi * raio3 * raio3 )
    return [dh1_dt, dh2_dt, dh3_dt]

# Função para capturar entrada do usuário
def capturar_entrada():
    global global_force
    while True:
        try:
            nova_qi1 = float(input("Digite o novo valor da vazão qi1 (m³/h): "))
            nova_qi2 = float(input("Digite o novo valor da vazão qi2 (m³/h): "))
            nova_qi3 = float(input("Digite o novo valor da vazão qi3 (m³/h): "))

            global_force["Qi1"] = nova_qi1
            global_force["Qi2"] = nova_qi2
            global_force["Qi3"] = nova_qi3
        except ValueError:
            print("Por favor, insira um valor numérico.")

# Função principal para a simulação
def simular_sistema():
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

    while True:
        # Resolver o sistema de equações diferenciais
        solucao = solve_ivp(
            sistema_massa_mola_amortecedor,
            [tempo_inicial, tempo_final],
            condicoes_iniciais,
            t_eval=np.linspace(tempo_inicial, tempo_final, 10)
        )

        # Atualizar as condições iniciais para o próximo intervalo
        for j in range(len(solucao.y)):
            for i in range(len(solucao.y[j])):
                if(solucao.y[j][i] < 0):
                    solucao.y[j][i] = 0

        condicoes_iniciais = [solucao.y[0][-1], solucao.y[1][-1], solucao.y[2][-1]]
        tempo_inicial = tempo_final
        tempo_final += dt

        # Salvar os resultados
        historico_tempo.extend(solucao.t)
        historico_niveis[0].extend(solucao.y[0])
        historico_niveis[1].extend(solucao.y[1])
        historico_niveis[2].extend(solucao.y[2])

        
        # Exibir os últimos resultados no console
        print(f"Tempo: {solucao.t[-1]:.2f}s, Nível 1: {solucao.y[0][-1]:.4f}m, Nível 2: {solucao.y[1][-1]:.4f}m, Nível 3: {solucao.y[2][-1]:.4f}m, Vazao i1: {global_force['Qi1']:.2f}m, Vazao i2: {global_force['Qi2']:.2f}m, Vazao i3: {global_force['Qi3']:.2f}m")
        
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

# Configurar e iniciar as threads
if __name__ == "__main__":
    # Thread para entrada do usuário
    thread_entrada = threading.Thread(target=capturar_entrada, daemon=True)
    thread_entrada.start()

    # Simulação do sistema
    simular_sistema()
