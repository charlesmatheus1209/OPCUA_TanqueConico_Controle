import time
from opcua import Client
from datetime import datetime

# Configurações do cliente OPC UA
url = "opc.tcp://127.0.0.1:53530/OPCUA/SimulationServer"  # Substitua pelo endereço do seu servidor
client = Client(url)

# Lista de variáveis para leitura
variable_ids = [f"ns=3;i={i}" for i in range(1009, 1019)]  # De 1009 até 1018

# Nome do arquivo para salvar os valores
output_file = "mes.txt"

try:
    # Conectar ao servidor OPC UA
    client.connect()
    print("Conectado ao servidor OPC UA.")

    # Abrir arquivo para gravação
    with open(output_file, "a") as file:
        file.write("Leitura contínua de valores OPC UA\n")
        file.write(f"Data de início: {datetime.now()}\n\n")

        # Loop infinito para leitura contínua
        while True:
            try:
                # Capturar data e hora da leitura
                timestamp = datetime.now()

                # Coletar valores das variáveis
                values = []
                for var_id in variable_ids:
                    try:
                        node = client.get_node(var_id)
                        value = node.get_value()
                        values.append(value)
                    except Exception as e:
                        values.append(f"Erro: {e}")

                # Escrever valores no arquivo
                linha = f"{timestamp}: " + ", ".join([f"{v}" for v in values]) + "\n"
                file.write(linha)
                file.flush()  # Garantir que os dados sejam gravados imediatamente
                print(f"Valores registrados: {linha.strip()}")

                # Esperar 10 segundos antes da próxima leitura
                time.sleep(10)

            except KeyboardInterrupt:
                print("Leitura interrompida pelo usuário.")
                break

except Exception as e:
    print(f"Erro ao conectar ou durante a execução: {e}")

finally:
    # Desconectar do servidor OPC UA
    client.disconnect()
    print("Desconectado do servidor OPC UA.")
