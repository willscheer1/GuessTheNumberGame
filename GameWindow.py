"""
Class containing the UI and game logic for Guess the Number game.
"""
import tkinter as tk
import pyglet # used for custom font import
pyglet.options['win32_gdi_font'] = True # use GDI font renderer for pyglet, this is was tkinter uses

class GameWindow:

    def __init__(self):
        """
        """
        # background color pallete
        self.bg_default = "#8442f5"
        self.bg_win = "#51f046"
        self.bg_lose = "#d43941"

        # add custom font
        pyglet.font.add_file("BagelFatOne-Regular.ttf") # font name = "Bagel Fat One"

        # window setup
        self.window = tk.Tk()
        self.window.title("Guess the Number")
        self.window.iconbitmap("Images/question_mark_small.ico")
        self.window.geometry("900x600")
        self.window.resizable(False, False)
        self.window.config(bg=self.bg_default)

        # widgets
        self.game_title = tk.Label(self.window,
                                   bg=self.bg_default,
                                   text="Guess the Number!",
                                   font=("Bagel Fat One", 36),
                                   pady=25
                                   ).pack()
        self.answer = tk.Label(self.window,
                               bg=self.bg_default,
                               text="?",
                               font=("Bagel Fat One", 65)
                               ).pack()
        
        # defaults to main menu on open
        self.main_menu()


    def main_menu(self):
        """
        """
        menu = tk.Frame(self.window,
                        bg=self.bg_default,
                        padx=0,
                        pady=0
                        )
        easy_button = self.create_button(menu, "Easy").pack(pady=10)
        intermediate_button = self.create_button(menu, "Intermediate").pack(pady=10)
        hard_button = self.create_button(menu, "Hard").pack(pady=10)
        menu.pack(pady=10)
        
    def create_button(self, parent, text, width=150, height=50, bd=5, function=None):
        """
        Creates a tkinter button.

        Parameters:
            parent (object):  Tkinter object the button will be placed in to.
            text (str): Text that appears inside the button.
            width (int): Width of the button.
            height (int): Height of the button.
            bd (int): Width of the button's border.
            function (function): Function called when the button is clicked.
        """
        pixel = tk.PhotoImage(width=1, height=1)    # placing image inside button allows button to be sized by pixels instead of character length
        button = tk.Button(parent,
                           image=pixel,
                           width=width,
                           height=height,
                           bd=bd,
                           text=text,
                           font=("Bagel Fat One", 16),
                           compound="center",
                           padx=0,
                           pady=0,
                           cursor="hand2"
                           )

        return button
    
    def run(self):
        """
        Opens UI window and begins game execution.
        """
        self.window.mainloop()