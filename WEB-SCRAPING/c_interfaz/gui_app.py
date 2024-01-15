import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import requests
from bs4 import BeautifulSoup
from tkinter import scrolledtext

def salir(root):
    respuesta = messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?")
    if respuesta:
        root.destroy()
def barra_menu(root):
    barra_menu=tk.Menu(root)
    root.config(menu=barra_menu,width=300, height=300)

    menu_inicio=tk.Menu(barra_menu,tearoff=0)
    barra_menu.add_cascade(label='Inicio',menu=menu_inicio)

    menu_inicio.add_command(label='Introduce la URL')
    menu_inicio.add_command(label='Buscador')
    
    barra_menu.add_cascade(label='Salir',command=lambda: salir(root))
    

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root,width=350, height=400)
        self.root=root
        self.pack()
        self.campos_scraping()
        self.conexion = sqlite3.connect('scraping3.db')
        self.crear_bbdd(self.conexion)
        self.tabla_url()
        self.mostrar_datos_iniciales()
    
        
        
    
    def campos_scraping(self):
        self.label_url = tk.Label(self, text='Introducir URL: ', height=2, width=20)
        self.label_url.config(font=('Arial', 12, 'bold'), foreground='black')
        self.label_url.grid(row=0, column=0)

        self.label_BUSQUEDA = tk.Label(self, text='Busqueda: ', height=2, width=20)
        self.label_BUSQUEDA.config(font=('Arial', 12, 'bold'), foreground='black')
        self.label_BUSQUEDA.grid(row=2, column=0)
######ENTRYS
        self.url=tk.StringVar()
        self.entry_url = tk.Entry(self,width=50,textvariable=self.url)
        self.entry_url.config(font=('Arial', 10), foreground='black')
        self.entry_url.grid(row=1, column=0,columnspan=3)

        self.bsq=tk.StringVar()
        self.entry_busqueda = tk.Entry(self,width=50,textvariable=self.bsq)
        self.entry_busqueda.config(font=('Arial', 10), foreground='black')
        self.entry_busqueda.grid(row=4, column=0,columnspan=3)
        #####BOTONESS
        self.boton_guardar=tk.Button(self,text="Guardar Datos",command=self.guardar_datos)
        self.boton_guardar.config(width=15,font=('Arial',12,'bold'),
        fg='white',bg='blue',cursor='hand2')
        self.boton_guardar.grid(row=5,column=0,padx=10,pady=10)

        self.boton_buscar=tk.Button(self,text="Buscar",command=self.buscar)
        self.boton_buscar.config(width=15,font=('Arial',12,'bold'),
        fg='white',bg='green',cursor='hand2')
        self.boton_buscar.grid(row=5,column=1,padx=10,pady=10)

        self.boton_borrar=tk.Button(self,text="Limpiar",command=self.borrar)
        self.boton_borrar.config(width=15,font=('Arial',12,'bold'),
        fg='white',bg='red',cursor='hand2')
        self.boton_borrar.grid(row=5,column=2,padx=10,pady=10)

        self.texto_scroll = scrolledtext.ScrolledText(self, width=33, height=10)
        self.texto_scroll.grid(row=7,column=1,padx=10,pady=10)


    def borrar(self):
        self.url.set('')
        self.bsq.set('')
        self.campo_texto.delete(1.0, tk.END)


    def guardar_datos(self):
        url = self.url.get()
        if url:
            conexion = sqlite3.connect('scraping3.db')
            cursor = conexion.cursor()
            url_existente = cursor.execute('SELECT id FROM urls WHERE url = ?', (url,)).fetchone()
            if not url_existente:
                contenido = requests.get(url)
                soup = BeautifulSoup(contenido.text, "html.parser")
                datos_h1 = [h1.get_text() for h1 in soup.find_all("h1")]
                datos_h2 = [h2.get_text() for h2 in soup.find_all("h2")]
                datos_p = [p.get_text() for p in soup.find_all("p")]
                datos_a = [a.get_text() for a in soup.find_all("a")]
                datos_address = [address.get_text() for address in soup.find_all("address")]
                datos_img = [img['src'] for img in soup.find_all("img", src=True)]

                
                cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
                url_id = cursor.lastrowid

                for titulo in datos_h1:
                    cursor.execute('INSERT INTO titulos (url_id, titulo) VALUES (?, ?)', (url_id, titulo))
                for subtitulo in datos_h2:
                    cursor.execute('INSERT INTO subtitulos (url_id, subtitulo) VALUES (?, ?)', (url_id, subtitulo))
                for parrafo in datos_p:
                    cursor.execute('INSERT INTO parrafos (url_id, parrafo) VALUES (?, ?)', (url_id, parrafo))
                for direccion in datos_address:
                    cursor.execute('INSERT INTO direcciones (url_id, direccion) VALUES (?, ?)', (url_id, direccion))
                for src in datos_img:
                    cursor.execute('INSERT INTO imagenes (url_id, src) VALUES (?, ?)', (url_id, src))

                conexion.commit()
                conexion.close()

                self.actualizar_tabla()
                messagebox.showinfo("Guardado", "Datos guardados en la base de datos.")
            
            else:
                messagebox.showwarning("Error", "Puede que la URL ya se encuentre regustrada o debes introduce una URL válida.")
            self.url.set('')
            self.campo_texto.delete(1.0, tk.END)
            self.bsq.set('')
        
    def crear_bbdd(self,conexion):
        conexion.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL
        )
        ''')

        conexion.execute('''
        CREATE TABLE IF NOT EXISTS titulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            titulo TEXT NOT NULL,
            FOREIGN KEY (url_id) REFERENCES urls (id)
        )
        ''')

        conexion.execute('''
        CREATE TABLE IF NOT EXISTS subtitulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            subtitulo TEXT NOT NULL,
            FOREIGN KEY (url_id) REFERENCES urls (id)
        )
        ''')

        conexion.execute('''
        CREATE TABLE IF NOT EXISTS parrafos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            parrafo TEXT NOT NULL,
            FOREIGN KEY (url_id) REFERENCES urls (id)
        )
        ''')

        conexion.execute('''
        CREATE TABLE IF NOT EXISTS direcciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            direccion TEXT NOT NULL,
            FOREIGN KEY (url_id) REFERENCES urls (id)
        )
        ''')

        conexion.execute('''
        CREATE TABLE IF NOT EXISTS imagenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            src TEXT NOT NULL,
            FOREIGN KEY (url_id) REFERENCES urls (id)
        )
        ''')
        conexion.commit()

    def habilitar_campos(self):
        self.entry_busqueda.config(state='normal')
        self.entry_url.config(state='normal')
        self.boton_buscar.config(state='normal')
        self.boton_guardar.config(state='normal')

    def desabilitar_campos(self):
        self.entry_busqueda.config(state='disable')
        self.entry_url.config(state='disable')
        self.boton_buscar.config(state='disable')
        self.boton_guardar.config(state='disable')

    def mostrar_datos_iniciales(self):
        conexion = sqlite3.connect('scraping3.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='urls'")
        tabla_urls_existente = cursor.fetchone()
        if not tabla_urls_existente:
            self.crear_bbdd(conexion)

        cursor.execute('SELECT * FROM urls')
        urls = cursor.fetchall()

        for url in urls:
            self.tabla.insert('', 0, text=url[0], values=(url[1]))
        conexion.close()

    def tabla_url(self):
        self.tabla=ttk.Treeview(self,column=('URL'))
        self.tabla.grid(row=6,column=0,columnspan=3)
        self.tabla.heading('#0',text='ID')
        self.tabla.heading('#1',text='URL')
        self.tabla.column('#0', width=50)
        self.tabla.column('#1', width=250) 

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.mostrar_datos_iniciales()

    def crear_campo_texto(self):
        self.campo_texto = scrolledtext.ScrolledText(self, width=50, height=10)
        self.campo_texto.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
    
    def buscar(self):
        print('buscar')
    def mostrar_busqueda(self):
        print('mostrar buscar')




        
