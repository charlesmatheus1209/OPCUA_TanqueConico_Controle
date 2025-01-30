# import tkinter as tk
# from tkinter import messagebox
# import socket
# import json
# import threading
# import time

# # Dicionário com valores globais para níveis, setpoints e vazões
# global_values = {"l1": 0, "l2": 0, "l3": 0, "q1": 0, "q2": 0, "q3": 0, "sp1": 0, "sp2": 0, "sp3": 0}

# def encode_dict_to_string(dictionary):
#     # Cria a string concatenando as chaves e valores, separando com ';' entre pares
#     encoded_string = ";".join(f"{key}={value}" for key, value in dictionary.items())
#     return encoded_string


# # Função para enviar os setpoints ao controlador via TCP
# def send_setpoints_to_controller():
#     try:
#         # Cria o dicionário com os setpoints
#         setpoints = {
#             "sp1": global_values['sp1'],
#             "sp2": global_values['sp2'],
#             "sp3": global_values['sp3']
#         }
        
#         # Converte o dicionário para uma string JSON
#         setpoints_json = encode_dict_to_string(setpoints)

#         # Conexão com o controlador
#         host = "127.0.0.1"  # IP do servidor (controlador)
#         port = 12345  # Porta do servidor (controlador)

#         # Cria o socket e envia os dados
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#             client_socket.connect((host, port))
#             client_socket.sendall(setpoints_json.encode('utf-8'))
            
#             # Recebe a resposta do controlador
#             response = client_socket.recv(1024).decode('utf-8')
#             return response
#     except Exception as e:
#         messagebox.showerror("Erro", f"Erro ao enviar setpoints: {e}")
#         return None

# def decode_string_to_dict(encoded_string):
#     pairs = encoded_string.split(";")    
#     decoded_dict = {pair.split("=")[0]: float(pair.split("=")[1]) for pair in pairs}    
#     return decoded_dict


# # Função para obter os dados do controlador via GET
# def get_data_from_controller():
#     try:
#         # Conexão com o controlador
#         host = "127.0.0.1"  # IP do servidor (controlador)
#         port = 12345  # Porta do servidor (controlador)

#         # Cria o socket e envia o pedido de dados (GET)
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#             client_socket.connect((host, port))
#             client_socket.sendall("GET".encode('utf-8'))  # Envia o pedido de dados
            
#             # Recebe a resposta do controlador
#             response = client_socket.recv(4096).decode('utf-8')
#             print(response)
#             # Converte a resposta de volta para um dicionário
#             data = decode_string_to_dict(response)
            
#             # Atualiza os valores globais
#             global_values['l1'] = data['l1']
#             global_values['l2'] = data['l2']
#             global_values['l3'] = data['l3']
#             global_values['q1'] = data['q1']
#             global_values['q2'] = data['q2']
#             global_values['q3'] = data['q3']
            
#             # Agenda a atualização da interface gráfica
#             root.after(0, update_display)
#     except Exception as e:
#         messagebox.showerror("Erro", f"Erro ao obter dados do controlador: {e}")


# # Função para atualizar a interface com os valores atuais
# def update_display():
#     # Atualiza os níveis e vazões
#     l1_label.config(text=f"Nível Tanque 1: {global_values['l1']} m")
#     l2_label.config(text=f"Nível Tanque 2: {global_values['l2']} m")
#     l3_label.config(text=f"Nível Tanque 3: {global_values['l3']} m")
    
#     q1_label.config(text=f"Vazão Tanque 1: {global_values['q1']} L/s")
#     q2_label.config(text=f"Vazão Tanque 2: {global_values['q2']} L/s")
#     q3_label.config(text=f"Vazão Tanque 3: {global_values['q3']} L/s")
    
#     # Atualiza os setpoints
#     sp1_label.config(text=f"Setpoint 1: {global_values['sp1']} m")
#     sp2_label.config(text=f"Setpoint 2: {global_values['sp2']} m")
#     sp3_label.config(text=f"Setpoint 3: {global_values['sp3']} m")
    
#     # Atualiza a altura dos tanques (nível) nos desenhos
#     update_tank_display()


# # Função para atualizar os setpoints a partir dos inputs
# def update_setpoints():
#     try:
#         # Obtém os valores inseridos nos campos de entrada
#         sp1 = float(sp1_entry.get())
#         sp2 = float(sp2_entry.get())
#         sp3 = float(sp3_entry.get())
        
#         # Atualiza os valores no dicionário global
#         global_values['sp1'] = sp1
#         global_values['sp2'] = sp2
#         global_values['sp3'] = sp3
        
#         # Envia os setpoints ao controlador
#         response = send_setpoints_to_controller()
        
#         if response:
#             messagebox.showinfo("Sucesso", f"Setpoints atualizados com sucesso!\nResposta do controlador: {response}")
#         else:
#             messagebox.showwarning("Aviso", "Falha ao comunicar com o controlador.")
        
#         # Atualiza a interface gráfica
#         update_display()
#     except ValueError:
#         messagebox.showerror("Erro", "Os setpoints devem ser números válidos!")


# # Função para desenhar os tanques e mostrar os níveis
# def update_tank_display():
#     # Desenha o tanque 1
#     canvas1.delete("all")
#     canvas1.create_rectangle(50, 50, 150, 250, outline="black", width=2)  # Corpo do tanque
#     canvas1.create_rectangle(50, 250 - global_values['l1'] * 100, 150, 250, fill="blue")  # Nível do tanque

#     # Desenha o tanque 2
#     canvas2.delete("all")
#     canvas2.create_rectangle(50, 50, 150, 250, outline="black", width=2)  # Corpo do tanque
#     canvas2.create_rectangle(50, 250 - global_values['l2'] * 100, 150, 250, fill="blue")  # Nível do tanque

#     # Desenha o tanque 3
#     canvas3.delete("all")
#     canvas3.create_rectangle(50, 50, 150, 250, outline="black", width=2)  # Corpo do tanque
#     canvas3.create_rectangle(50, 250 - global_values['l3'] * 100, 150, 250, fill="blue")  # Nível do tanque


# # Função para rodar a thread de atualização dos dados
# def start_data_thread():
#     while True:
#         get_data_from_controller()  # Obtém os dados do controlador
#         time.sleep(5)  # Espera 5 segundos antes de buscar novamente


# # Configurações iniciais da janela
# root = tk.Tk()
# root.title("Sistema Supervisório de Tanques")

# # Layout para mostrar os tanques, níveis e vazões
# frame_tanques = tk.Frame(root)
# frame_tanques.pack(padx=10, pady=10)

# # Tanque 1
# tanque1_label = tk.Label(frame_tanques, text="Tanque 1", font=("Arial", 14))
# tanque1_label.grid(row=0, column=0, padx=20)
# l1_label = tk.Label(frame_tanques, text="Nível Tanque 1: 0 m", font=("Arial", 12))
# l1_label.grid(row=1, column=0, pady=5)
# q1_label = tk.Label(frame_tanques, text="Vazão Tanque 1: 0 L/s", font=("Arial", 12))
# q1_label.grid(row=2, column=0, pady=5)
# sp1_label = tk.Label(frame_tanques, text="Setpoint 1: 0 m", font=("Arial", 12))
# sp1_label.grid(row=3, column=0, pady=5)

# canvas1 = tk.Canvas(frame_tanques, width=200, height=300, bg="white")
# canvas1.grid(row=4, column=0, pady=10)

# # Tanque 2
# tanque2_label = tk.Label(frame_tanques, text="Tanque 2", font=("Arial", 14))
# tanque2_label.grid(row=0, column=1, padx=20)
# l2_label = tk.Label(frame_tanques, text="Nível Tanque 2: 0 m", font=("Arial", 12))
# l2_label.grid(row=1, column=1, pady=5)
# q2_label = tk.Label(frame_tanques, text="Vazão Tanque 2: 0 L/s", font=("Arial", 12))
# q2_label.grid(row=2, column=1, pady=5)
# sp2_label = tk.Label(frame_tanques, text="Setpoint 2: 0 m", font=("Arial", 12))
# sp2_label.grid(row=3, column=1, pady=5)

# canvas2 = tk.Canvas(frame_tanques, width=200, height=300, bg="white")
# canvas2.grid(row=4, column=1, pady=10)

# # Tanque 3
# tanque3_label = tk.Label(frame_tanques, text="Tanque 3", font=("Arial", 14))
# tanque3_label.grid(row=0, column=2, padx=20)
# l3_label = tk.Label(frame_tanques, text="Nível Tanque 3: 0 m", font=("Arial", 12))
# l3_label.grid(row=1, column=2, pady=5)
# q3_label = tk.Label(frame_tanques, text="Vazão Tanque 3: 0 L/s", font=("Arial", 12))
# q3_label.grid(row=2, column=2, pady=5)
# sp3_label = tk.Label(frame_tanques, text="Setpoint 3: 0 m", font=("Arial", 12))
# sp3_label.grid(row=3, column=2, pady=5)

# canvas3 = tk.Canvas(frame_tanques, width=200, height=300, bg="white")
# canvas3.grid(row=4, column=2, pady=10)

# # Configura a interface para atualização dos setpoints
# frame_setpoints = tk.Frame(root)
# frame_setpoints.pack(padx=10, pady=10)

# sp1_entry = tk.Entry(frame_setpoints, width=5)
# sp1_entry.grid(row=0, column=0, padx=5, pady=5)
# sp2_entry = tk.Entry(frame_setpoints, width=5)
# sp2_entry.grid(row=0, column=1, padx=5, pady=5)
# sp3_entry = tk.Entry(frame_setpoints, width=5)
# sp3_entry.grid(row=0, column=2, padx=5, pady=5)

# update_button = tk.Button(frame_setpoints, text="Atualizar Setpoints", command=update_setpoints)
# update_button.grid(row=1, column=0, columnspan=3, pady=10)

# # Thread para atualização contínua dos dados
# data_thread = threading.Thread(target=start_data_thread, daemon=True)
# data_thread.start()

# # Inicia o loop da interface
# root.mainloop()
import tkinter as tk
from tkinter import messagebox
import socket
import threading
import time

# Dicionário com valores globais para níveis, setpoints e vazões
global_values = {"l1": 0, "l2": 0, "l3": 0, "q1": 0, "q2": 0, "q3": 0, "sp1": 0, "sp2": 0, "sp3": 0}

# Funções auxiliares para codificação e decodificação de dados
def encode_dict_to_string(dictionary):
    return ";".join(f"{key}={value}" for key, value in dictionary.items())

def decode_string_to_dict(encoded_string):
    pairs = encoded_string.split(";")
    return {pair.split("=")[0]: float(pair.split("=")[1]) for pair in pairs}

# Função para enviar os setpoints ao controlador via TCP
def send_setpoints_to_controller():
    try:
        setpoints = {"sp1": global_values['sp1'], "sp2": global_values['sp2'], "sp3": global_values['sp3']}
        setpoints_json = encode_dict_to_string(setpoints)
        host, port = "127.0.0.1", 12345

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(setpoints_json.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar setpoints: {e}")
        return None

# Função para obter os dados do controlador via TCP
def get_data_from_controller():
    try:
        host, port = "127.0.0.1", 12345
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall("GET".encode('utf-8'))
            response = client_socket.recv(4096).decode('utf-8')
            data = decode_string_to_dict(response)

            global_values.update(data)
            root.after(0, update_display)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter dados do controlador: {e}")

# Função para atualizar a interface com os valores atuais
def update_display():
    l1_label.config(text=f"Nível Tanque 1: {global_values['l1']:.2f} m")
    l2_label.config(text=f"Nível Tanque 2: {global_values['l2']:.2f} m")
    l3_label.config(text=f"Nível Tanque 3: {global_values['l3']:.2f} m")

    q1_label.config(text=f"Vazão Tanque 1: {global_values['q1']:.2f} L/s")
    q2_label.config(text=f"Vazão Tanque 2: {global_values['q2']:.2f} L/s")
    q3_label.config(text=f"Vazão Tanque 3: {global_values['q3']:.2f} L/s")

    sp1_label.config(text=f"Setpoint 1: {global_values['sp1']:.2f} m")
    sp2_label.config(text=f"Setpoint 2: {global_values['sp2']:.2f} m")
    sp3_label.config(text=f"Setpoint 3: {global_values['sp3']:.2f} m")

    update_tank_display()

# Função para atualizar os setpoints
def update_setpoints():
    try:
        global_values['sp1'] = float(sp1_entry.get())
        global_values['sp2'] = float(sp2_entry.get())
        global_values['sp3'] = float(sp3_entry.get())

        threading.Thread(target=send_setpoints_to_controller, daemon=True).start()
        update_display()
    except ValueError:
        messagebox.showerror("Erro", "Os setpoints devem ser números válidos!")

# Função para desenhar os tanques e níveis
def update_tank_display():
    canvas1.delete("all")
    canvas1.create_rectangle(50, 50, 150, 250, outline="black", width=2)
    canvas1.create_rectangle(50, 250 - global_values['l1'] * 100, 150, 250, fill="blue")

    canvas2.delete("all")
    canvas2.create_rectangle(50, 50, 150, 250, outline="black", width=2)
    canvas2.create_rectangle(50, 250 - global_values['l2'] * 100, 150, 250, fill="blue")

    canvas3.delete("all")
    canvas3.create_rectangle(50, 50, 150, 250, outline="black", width=2)
    canvas3.create_rectangle(50, 250 - global_values['l3'] * 100, 150, 250, fill="blue")

# Thread para comunicação contínua
def communication_thread():
    while True:
        get_data_from_controller()
        time.sleep(5)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Sistema Supervisório de Tanques")

frame_tanques = tk.Frame(root)
frame_tanques.pack(padx=10, pady=10)

# Tanque 1
tanque1_label = tk.Label(frame_tanques, text="Tanque 1", font=("Arial", 14))
tanque1_label.grid(row=0, column=0, padx=20)
l1_label = tk.Label(frame_tanques, text="Nível Tanque 1: 0 m", font=("Arial", 12))
l1_label.grid(row=1, column=0, pady=5)
q1_label = tk.Label(frame_tanques, text="Vazão Tanque 1: 0 L/s", font=("Arial", 12))
q1_label.grid(row=2, column=0, pady=5)
sp1_label = tk.Label(frame_tanques, text="Setpoint 1: 0 m", font=("Arial", 12))
sp1_label.grid(row=3, column=0, pady=5)
canvas1 = tk.Canvas(frame_tanques, width=200, height=300, bg="white")
canvas1.grid(row=4, column=0, pady=10)

# Tanque 2
tanque2_label = tk.Label(frame_tanques, text="Tanque 2", font=("Arial", 14))
tanque2_label.grid(row=0, column=1, padx=20)
l2_label = tk.Label(frame_tanques, text="Nível Tanque 2: 0 m", font=("Arial", 12))
l2_label.grid(row=1, column=1, pady=5)
q2_label = tk.Label(frame_tanques, text="Vazão Tanque 2: 0 L/s", font=("Arial", 12))
q2_label.grid(row=2, column=1, pady=5)
sp2_label = tk.Label(frame_tanques, text="Setpoint 2: 0 m", font=("Arial", 12))
sp2_label.grid(row=3, column=1, pady=5)
canvas2 = tk.Canvas(frame_tanques, width=200, height=300, bg="white")
canvas2.grid(row=4, column=1, pady=10)

# Tanque 3
tanque3_label = tk.Label(frame_tanques, text="Tanque 3", font=("Arial", 14))
tanque3_label.grid(row=0, column=2, padx=20)
l3_label = tk.Label(frame_tanques, text="Nível Tanque 3: 0 m", font=("Arial", 12))
l3_label.grid(row=1, column=2, pady=5)
q3_label = tk.Label(frame_tanques, text="Vazão Tanque 3: 0 L/s", font=("Arial", 12))
q3_label.grid(row=2, column=2, pady=5)
sp3_label = tk.Label(frame_tanques, text="Setpoint 3: 0 m", font=("Arial", 12))
sp3_label.grid(row=3, column=2, pady=5)
canvas3 = tk.Canvas(frame_tanques, width=200, height=300, bg="white")
canvas3.grid(row=4, column=2, pady=10)

frame_setpoints = tk.Frame(root)
frame_setpoints.pack(padx=10, pady=10)

sp1_entry = tk.Entry(frame_setpoints, width=5)
sp1_entry.grid(row=0, column=0, padx=5, pady=5)
sp2_entry = tk.Entry(frame_setpoints, width=5)
sp2_entry.grid(row=0, column=1, padx=5, pady=5)
sp3_entry = tk.Entry(frame_setpoints, width=5)
sp3_entry.grid(row=0, column=2, padx=5, pady=5)

update_button = tk.Button(frame_setpoints, text="Atualizar Setpoints", command=update_setpoints)
update_button.grid(row=1, column=0, columnspan=3, pady=10)

# Inicia a thread de comunicação
threading.Thread(target=communication_thread, daemon=True).start()

# Inicia o loop da interface gráfica
root.mainloop()
