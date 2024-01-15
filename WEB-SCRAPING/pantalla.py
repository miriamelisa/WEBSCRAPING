import tkinter as tk
from c_interfaz.gui_app import Frame, barra_menu

def main():
    root = tk.Tk()
    root.title('WEBSCRAPING')
    root.resizable(False,False)
    root.geometry("700x600")


    barra_menu(root)

    
    app=Frame(root=root)
    app.campos_scraping()
    root.mainloop()

    
if __name__ == '__main__':
    main()
