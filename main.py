import tkinter as tk
from tkinter import *
from tkinter import ttk



class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.geometry("800x600")
        self.text = tk.StringVar(value=("Esto es un texto largo de ejemplo "
                                        "para Stackoverflow."
                                        "Esto es un texto largo de ejemplo "
                                        "para Stackoverflow."))

        self.entradal = tk.Label(self, text="Ingrese los valores de entrada separados por espacios:")
        self.entradal.grid(column=0, row=0, pady=10, padx=10, sticky="e")

        self.estadosl = tk.Label(self, text="Ingrese los valores de estado separados por espacios:")
        self.estadosl.grid(column=0, row=1, pady=10, padx=10, sticky="e")

        self.entrada = tk.Entry(self)
        self.grid_columnconfigure(1, weight=1)
        self.entrada.grid(column=1, row=0, pady=20, padx=10,sticky="ew")

        self.estados = tk.Entry(self)
        self.estados.grid(column=1, row=1, pady=20, padx=10, sticky="ew")

        self.boton = tk.Button(self, text="Ingresar automata", command = lambda: self.read_automata(self.entrada.get(), self.estados.get()))
        self.boton.place(x= 100, y= 150)

    def read_automata(self, entrys, states):
        entradas = entrys.split()
        estados = states.split()
        tranciciones = []
        if len(entradas) == 0 or len(estados) == 0:
            self.sintax("Tu automata carece de estados o valores de entrada, reformalo")

        for estado in estados:
            try:
                estado.index("]")
                n = estado.index("[")
            except:
                self.sintax("Error de sitanxis al ingresar los estados")
                return
            m = estados.index(estado)
            trancicion = estado[n+1:len(estado)-1].split(",")
            estados[m] = estado[:n]
            t = {}
            for entrada, trans in zip(entradas, trancicion):
                t[entrada] = trans
            tranciciones.append(t)
        automnata_finito = {}
        for estado, trancicion in zip(estados, tranciciones):
            automnata_finito[estado] = trancicion
        print(automnata_finito)


    def sintax(self, text):
        top = Toplevel(self)
        top.geometry("360x150")
        top.title("Ops!!")
        Label(top, text=text).place(x=10, y=50)

    def on_label_resize(self,  event):
        event.widget["wraplength"] = event.width

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(600, 600)
    app = Application(root)
    app.pack(expand=True, fill='both')
    root.mainloop()