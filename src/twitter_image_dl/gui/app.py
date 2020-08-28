import tkinter as tk
import tkinter.ttk as ttk

from twitter_image_dl.gui.main import MainPage
from twitter_image_dl.gui.settings_page import SettingsPage

class AppGUI:
    """
    Root of the entire GUI structure
    """

    def __init__(self, bindings):
        self._bindings = bindings
        self._initializeWidgets()
        self._main.lift()
        self._root.update()

    def _initializeWidgets(self):
        self._create_widgets()
        self._set_widget_geometry()
        self._bind_callbacks()

    def _create_widgets(self):
        self._root = tk.Tk()
        self._root.title('twitter image dl')
        self._mainframe = ttk.Frame(self._root)
        self._main = MainPage(self._bindings, self._mainframe)
        self._settings = SettingsPage(self._bindings, self._mainframe)

    def _set_widget_geometry(self):
        # self._root.geometry('400x600+50+50') # size, location of window on screen
        self._root.resizable(tk.FALSE, tk.FALSE)
        self._mainframe.grid(row=0, column=0)
        self._main.grid(row=0, column=0, sticky='nsew')
        self._settings.grid(row=0, column=0, sticky='nsew')

    def _bind_callbacks(self):
        self._main.set_settings_callback(lambda: self._settings.lift())
        self._settings.set_close_callback(lambda: self._main.lift())

    def start(self):
        self._root.mainloop()
