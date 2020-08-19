import tkinter as tk
import tkinter.ttk as ttk

from twitter_image_dl.gui.main import Main

class AppGUI:
    """
    Root of the entire GUI structure
    """

    def __init__(self, bindings):
        self._bindings = bindings
        self._initializeWidgets()

    def _initializeWidgets(self):
        self._root = tk.Tk()
        self._mainframe = ttk.Frame(self._root)
        self._mainframe.grid(column=0, row=0)
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._main = Main(self._bindings, self._mainframe)
        self._main.grid(column=0, row=0, sticky='nsew')

    def start(self):
        self._root.mainloop()
