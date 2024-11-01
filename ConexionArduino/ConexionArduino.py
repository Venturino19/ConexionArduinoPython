import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading


arduino_port = "COM1" 
baud_rate = 9600
arduino = None



def conectar():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2) 
        lbConection.config(text="Estado: Conectado", fg="green")
        messagebox.showinfo("Estado de conexion", "Conectado con exito. ")
        start_reading() #empieza  la lectura de arduino
    except serial.SerialException:
        messagebox.showerror("Error!", "No se pudo conectar al Arduino.")
    except serial.SerialException as e:
        messagebox.showerror("Error!", f"No se pudo conectar al Arduino: {e}")
    except Exception as e:
        messagebox.showerror("Error!", f"Hubo un error inesperado {e}")
        


#desconectar el Arduino
def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close() # ierra la conexion con el arduino
        lbConection.config(text="Estado de conexion: Desconectado", fg="red")
        messagebox.showinfo("Conecion", "Desconectado. ")
    else:
        messagebox.showwarning("Cuidado!", "No hay ninguna conexion establecida.")


def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimTemp.get()
            if limite.isdigit(): 
                arduino.write(f"{limite}\n".encode()) 
                messagebox.showinfo("Enviado", f"Limite de temperatura ({limite}C) enviado.")
            else:
                messagebox.showerror("Error", "Ingrese un valor numerico para el Limite. ")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el limite: {e}")
    else:
        messagebox.showwarning("Advertencia", "Conectese al Arduino antes de enviar el limite. ")

def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip() 
            if "Temperatura" in data: 
                temp_value = data.split(":")[1].strip().split(" ")[0]
                lbTemp.config(text=f"{temp_value} ℃")
            time.sleep(1)
        except Exception as e:
            print(f"Error leyendo datos: {e}")
            break

def start_reading():
    thread = threading. Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

root = tk.Tk()
root. title("COMPROBAR TEMPERATURA")
root.geometry("650x350")


lbTitleTemp = tk.Label(root, text="Temperatura Actual", font=("Calibri", 12))
lbTitleTemp.pack(pady=10)


lbTemp = tk.Label(root, text=" -- ℃", font=("Calibri", 24))
lbTemp.pack()


lbConection = tk.Label(root, text="Estado: Desconectado", fg="red", font=("Calibri", 10))
lbConection.pack(pady=5)


lbLimitTemp = tk.Label(root, text="Limite de Temperatura:")
lbLimitTemp.pack(pady=5)
tbLimTemp = tk.Entry(root, width=10)
tbLimTemp.pack(pady=5)


btnEnviar = tk. Button(root, text="Enviar Limite", command=enviar_limite, font=("Calibri", 10))
btnEnviar.pack(pady=5)

btnConectar = tk.Button(root, text="Conectar", command=conectar, font=("Calibri", 10))
btnConectar.pack(pady=5)


btnDesconectar = tk.Button(root, text="Desconectar", command=desconectar, font=("Calibri", 10))
btnDesconectar.pack(pady=5)

root.mainloop()
