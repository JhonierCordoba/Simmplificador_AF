import tkinter as tk
from tkinter import *
from tkinter import ttk
from itertools import product



class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.geometry("800x600")

        self.automata_ingresado = {}
        self.automata_deterministico_ingresado = {}
        self.automata_simplificado = {}
        self.secuencia = ""

        self.entradal = tk.Label(self, text="Ingrese los valores de entrada separados por espacios:")
        self.entradal.grid(column=0, row=0, pady=10, padx=10, sticky="e")

        self.estadosl = tk.Label(self, text="Ingrese los valores de estado separados por espacios:")
        self.estadosl.grid(column=0, row=1, pady=10, padx=10, sticky="e")

        self.estadosl = tk.Label(self, text="Ingrese los valores de aceptación o rechazo(0 ó 1) separados por espacios:")
        self.estadosl.grid(column=0, row=2, pady=10, padx=10, sticky="e")

        self.entrada = tk.Entry(self)
        self.grid_columnconfigure(1, weight=1)
        self.entrada.grid(column=1, row=0, pady=20, padx=10, sticky="ew")

        self.estados = tk.Entry(self)
        self.estados.grid(column=1, row=1, pady=20, padx=10, sticky="ew")

        self.salidas = tk.Entry(self)
        self.salidas.grid(column=1, row=2, pady=20, padx=10, sticky="ew")

        self.boton = tk.Button(self, text="Ingresar automata",
                               command=lambda: self.read_automata(self.entrada.get(), self.estados.get(), self.salidas.get()))
        self.boton.place(x=150, y=170)

    def read_automata(self, entrys, states, exits):
        entradas = entrys.split()
        estados = states.split()
        salidas = exits.split()
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
        automata_finito["*"] = {est: "*" for est in entradas}
        print(automata_finito)
        #Mostrar el automata inicial
        self.automata_ingresado = automata_finito
        self.automataLabel = tk.Label(self, text="El automata que ingresó es:" + str(self.automata_ingresado))
        self.automataLabel.place(x=10, y=200)

        # Convertir automata a deterministico si es necesario, remover estados extraños
        primer_estado = list(automata_finito.keys())[0]
        automata_deterministico = {}
        self.recorrer_automata(automata_finito, automata_deterministico, primer_estado)
        if "*" in automata_deterministico.keys():
            automata_deterministico.pop("*")
        salidas_no_deterministicas = [0 for x in automata_deterministico]
        for estado in list(automata_deterministico.keys()):
            i = list(automata_deterministico.keys()).index(estado)
            for estado_no_deterministico in automata_finito:
                y = list(automata_finito.keys()).index(estado_no_deterministico)
                if estado_no_deterministico in estado and salidas_no_deterministicas[i] == 0 and salidas[y] == "1":
                    salidas_no_deterministicas[i] = 1
        salidas = salidas_no_deterministicas
        self.automata_ingresado = automata_deterministico
        print(salidas)

        #eliminar estado nulo
        for fila in self.automata_ingresado:
            self.automata_ingresado[fila]["*"] = salidas.pop(0)
        print(self.automata_ingresado)

        # Mostar automata deterministico
        if not deterministico:
            self.deterministico = tk.Label(self, text="convertido a deterministico: " + str(self.automata_ingresado))
            self.deterministico.place(x=10, y=220)

        #simplificar
        self.automata_simplificado = self.simplificacion_estados_equivalentes()


        # WIP leer secuencia


        self.ingresarSecuencia = tk.Button(self, text="Simplificar automata",
                               command=lambda: self.mostrar_simplificado())
        self.ingresarSecuencia.place(x=150, y=260)


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
                unique = ""
                for char in nuevo_estado:
                    if char not in unique:
                        unique += char
                nuevo_estado = unique
                automata_deterministico[estado][entrada] = nuevo_estado
            #Recursividad
            if nuevo_estado not in list(automata_deterministico.keys()):
                self.recorrer_indeterminacion(automata_no_deterministico, automata_deterministico, nuevo_estado, transiciones1[entrada], transiciones2[entrada])

    def simplificacion_estados_equivalentes(self):
        aceptacion = []
        rechazo = []
        aceptacion_grupos = {}
        rechazo_grupos = {}
        nombre_primer_estado = list(self.automata_ingresado.keys())[0]
        estado_inicial = self.automata_ingresado[list(self.automata_ingresado.keys())[0]]

        for i in self.automata_ingresado:
            if self.automata_ingresado[i]["*"] == 1:
                aceptacion.append(i)
            else:
                rechazo.append(i)

        r = [0, 1]
        grupos = list(product(r, repeat=len(estado_inicial) - 1))
        print(grupos)
        print("-"*100)
        for i in list(grupos):
            aceptacion_grupos[i] = []
            rechazo_grupos[i] = []


        for estado in self.automata_ingresado:
            salidas = ()
            for transicion in list(self.automata_ingresado[estado].values()):
                if transicion != "*":
                    salidas += (self.automata_ingresado[transicion]["*"],) if type(transicion) != int else ()
                else:
                    salidas += ("*",)
            if estado in aceptacion:
                if salidas in aceptacion_grupos:
                    aceptacion_grupos[salidas].append(estado)
                else:
                    aceptacion_grupos[salidas] = estado
            else:
                if salidas in rechazo_grupos:
                    rechazo_grupos[salidas].append(estado)
                else:
                    rechazo_grupos[salidas] = estado

        grupos = []
        for i in aceptacion_grupos:
            if len(aceptacion_grupos[i]) > 0:
                grupos.append(aceptacion_grupos[i])
        for i in rechazo_grupos:
            if len(rechazo_grupos[i]) > 0:
                grupos.append(rechazo_grupos[i])

        print(grupos)
        print("-"*100)
        automata_simplificado = self.crear_simplificacion(nombre_primer_estado, grupos, {})
        for estado in automata_simplificado:
            print(estado)
            if estado in ["".join(valor) for valor in rechazo]:
                print("sep")
                automata_simplificado[estado]["*"] = 0
            else:
                automata_simplificado[estado]["*"] = 1
        print(automata_simplificado)
        return automata_simplificado

    def crear_simplificacion(self, estado, grupos, automata_simplificado):
        union = ""
        for estados in grupos:
            if estado in estados:
                union = "".join(estados)
                break
        if union in automata_simplificado or estado is None:
            return
        automata_simplificado[union] = {}
        estado_actual = self.automata_ingresado[estado]
        for entrada in list(estado_actual.keys()):
            if entrada != "*":
                automata_simplificado[union][entrada] = self.union(self.automata_ingresado[estado][entrada], grupos)
                self.crear_simplificacion(estado_actual[entrada], grupos, automata_simplificado)
        print(automata_simplificado)
        return automata_simplificado

    def union(self, estado, grupos):
        for estados in grupos:
            if estado in estados:
                union = "".join(estados)
                return union

    def mostrar_simplificado(self):
        self.simplificado = tk.Label(self, text="El automata simplificado:" + str(self.automata_simplificado))
        self.simplificado.place(x=10, y=300)
        self.ingreseSecuencia = tk.Label(self, text="ingrese la secuencia que desea leer: ")
        self.ingreseSecuencia.place(x=10, y=320)
        self.secuenciaEntry = tk.Entry(self)
        self.secuenciaEntry.place(x=310, y=320)
        nombre_primer_estado = list(self.automata_simplificado.keys())[0]
        self.ingresarSecuencia = tk.Button(self, text="Ingresar secuencia",
                                           command=lambda: self.leer_secuencia(nombre_primer_estado, 0))
        self.ingresarSecuencia.place(x=150, y=340)

    def leer_secuencia(self, estado, posicion):
        self.secuencia = self.secuenciaEntry.get()
        if posicion == len(self.secuencia) or self.automata_simplificado[estado][self.secuencia[posicion]] == "*":
            if self.automata_simplificado[estado]["*"] == 1:
                final = "aceptacion"
            else:
                final = "rechazo"
            self.simplificado = tk.Label(self, text="se terminó de leer el automata con un estado de: " + final)
            self.simplificado.place(x=50, y=380, width=700)
            return

        self.simplificado = tk.Label(self, text="estado actual: " + str(estado))
        self.simplificado.place(x=50, y=380, width = 700)
        self.ingreseSecuencia = tk.Label(self, text="siguiente entrada: " + self.secuencia[posicion])
        self.ingreseSecuencia.place(x=10, y=400, width= 700)
        self.ingresarSecuencia = tk.Button(self, text="Ingresar secuencia",
                                           command=lambda: self.leer_secuencia(self.automata_simplificado[estado][self.secuencia[posicion]], posicion+1))
        self.ingresarSecuencia.place(x=150, y=440)

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