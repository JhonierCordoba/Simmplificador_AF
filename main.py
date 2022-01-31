import tkinter as tk
from tkinter import *
from tkinter import ttk



class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.geometry("800x600")

        self.entradal = tk.Label(self, text="Ingrese los valores de entrada separados por espacios:")
        self.entradal.grid(column=0, row=0, pady=10, padx=10, sticky="e")

        self.estadosl = tk.Label(self, text="Ingrese los valores de estado separados por espacios:")
        self.estadosl.grid(column=0, row=1, pady=10, padx=10, sticky="e")

        self.entrada = tk.Entry(self)
        self.grid_columnconfigure(1, weight=1)
        self.entrada.grid(column=1, row=0, pady=20, padx=10, sticky="ew")

        self.estados = tk.Entry(self)
        self.estados.grid(column=1, row=1, pady=20, padx=10, sticky="ew")

        self.boton = tk.Button(self, text="Ingresar automata",
                               command=lambda: self.read_automata(self.entrada.get(), self.estados.get()))
        self.boton.place(x=100, y=150)

    def read_automata(self, entrys, states):
        entradas = entrys.split()
        estados = states.split()
        transiciones = []
        deterministico = True
        if len(entradas) == 0 or len(estados) == 0:
            self.sintax("Tu automata carece de estados o valores de entrada, reformalo")
        for estado in estados:
            try:
                estado.index("]")
                n = estado.index("[")
            except:
                self.sintax("Error de sintaxis al ingresar los estados")
                return
            m = estados.index(estado)
            trancicion = estado[n + 1:-1].split(",")
            estados[m] = estado[:n]
            t = {}
            for entrada, trans in zip(entradas, trancicion):
                if trans[0] == "[" and trans[-1] == "]":
                    deterministico = False
                    trans = trans[1:-1].split(";")
                t[entrada] = trans
            transiciones.append(t)
        automata_finito = {}
        for estado, transicion in zip(estados, transiciones):
            automata_finito[estado] = transicion
        print(automata_finito)
        if not deterministico:
            automata_finito["*"] = {"*": "*"}
            primer_estado = list(automata_finito.keys())[0]
            automata_deterministico = {}
            self.recorrer_automata(automata_finito, automata_deterministico, primer_estado)
            print(automata_deterministico)

    def transformacion_deterministico(self, automata_no_deterministico):
        #Método muerto
        primer_estado = list(automata_no_deterministico.keys())[0]
        automata_deterministico = {}
        self.recorrer_automata(automata_no_deterministico, automata_deterministico, primer_estado)

    def recorrer_automata(self, automata_no_deterministico, automata_deterministico, estado):
        if estado in automata_deterministico:
            return
        transiciones = automata_no_deterministico[estado]
        automata_deterministico[estado] = {}
        # Recorrer transiciones
        for entrada in list(transiciones.keys()):
            if (type(transiciones[entrada]) == list):
                estado1 = transiciones[entrada][0]
                estado2 = transiciones[entrada][1]
                if (estado1 == estado2):
                    self.recorrer_automata(automata_no_deterministico, automata_deterministico, estado1)
                    automata_deterministico[estado] = automata_no_deterministico[estado]
                    continue
                nuevo_estado = [estado1, estado2]
                nuevo_estado.sort()
                nuevo_estado = "".join(nuevo_estado)
                # insertar transicion en el estado
                automata_deterministico[estado][entrada] = nuevo_estado
                self.recorrer_indeterminacion(automata_no_deterministico, automata_deterministico, transiciones[entrada], estado1, estado2)
            else:
                self.recorrer_automata(automata_no_deterministico, automata_deterministico, transiciones[entrada])
                automata_deterministico[estado][entrada] = automata_no_deterministico[estado][entrada]

    def recorrer_indeterminacion(self, automata_no_deterministico, automata_deterministico, estado, estado1, estado2):
        #Control de igualdad o contencion de otro estado
        if(estado1 == estado2):
            return
        elif estado2.__contains__(estado1):
            self.recorrer_automata(automata_no_deterministico, automata_deterministico, estado2)
            return
        elif estado1.__contains__(estado2):
            self.recorrer_automata(automata_no_deterministico, automata_deterministico, estado1)
            return
        #Control de estados indeterministicos
        if type(estado) == list:
            orden = [estado1, estado2]
            orden.sort()
            estado = "".join(orden)
        if type(estado1) == list:
            orden = [estado1[0], estado1[1]]
            orden.sort()
            estado = "".join(orden)
        if type(estado2) == list:
            orden = [estado2[0], estado2[1]]
            orden.sort()
            estado = "".join(orden)
        automata_deterministico[estado] = {}
        #Control de automatas repetidos
        if estado1 in list(automata_no_deterministico.keys()):
            transiciones1 = automata_no_deterministico[estado1]
        else:
            transiciones1 = automata_deterministico[estado1]
        if estado2 in list(automata_no_deterministico.keys()):
            transiciones2 = automata_no_deterministico[estado2]
        else:
            transiciones2 = automata_deterministico[estado2]
        #Recorrido de transiciones
        for entrada in list(transiciones1.keys()):
            if type(transiciones1[entrada]) == list:
                orden = [transiciones1[entrada][0], transiciones1[entrada][1]]
                orden.sort()
                transiciones1[entrada] = "".join(orden)
                self.recorrer_indeterminacion(automata_no_deterministico, automata_deterministico, transiciones1[entrada], transiciones1[entrada][0], transiciones1[entrada][1])
            if type(transiciones2[entrada]) == list:
                orden = [transiciones2[entrada][0], transiciones2[entrada][1]]
                orden.sort()
                transiciones2[entrada] = "".join(orden)
                self.recorrer_indeterminacion(automata_no_deterministico, automata_deterministico,transiciones2[entrada], transiciones2[entrada][0], transiciones2[entrada][1])
            nueva_transicion = [transiciones1[entrada], transiciones2[entrada]]
            #Control de asteriscos(Salidas)
            try:
                nueva_transicion.remove("*")
                nueva_transicion.sort()
            except:
                nueva_transicion.sort()
            nuevo_estado = "".join(nueva_transicion)
            # Control de uniones triples repetidas
            repetido = []
            for char in nuevo_estado:
                repetido.append(char)
            repetido.sort()
            repetido = "".join(repetido)
            if repetido in list(automata_deterministico.keys()):
                nuevo_estado = repetido
            #Control de transiciones iguales
            if (transiciones1[entrada] == transiciones2[entrada]):
                automata_deterministico[estado][entrada] = transiciones1[entrada]
            elif transiciones2[entrada].__contains__((transiciones1[entrada])):
                automata_deterministico[estado][entrada] = transiciones2[entrada]
            elif transiciones1[entrada].__contains__(transiciones2[entrada]):
                automata_deterministico[estado][entrada] = transiciones1[entrada]
            else:
                automata_deterministico[estado][entrada] = nuevo_estado
            #Recursividad
            if nuevo_estado not in list(automata_deterministico.keys()):
                self.recorrer_indeterminacion(automata_no_deterministico, automata_deterministico, nuevo_estado, transiciones1[entrada], transiciones2[entrada])

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