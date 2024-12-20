"""
Class containing the UI and game logic for Guess the Number game.
"""
import re, random
import tkinter as tk
from PIL import Image, ImageTk
import pyglet # used for custom font import
pyglet.options['win32_gdi_font'] = True # use GDI font renderer for pyglet, this is was tkinter uses

class GameWindow:

    def __init__(self):
        """
        Initializes and opens the game window for the class instance.
        """
        # background color
        self.bg_color = "#8442f5"

        # add custom font
        pyglet.font.add_file("BagelFatOne-Regular.ttf") # font name = "Bagel Fat One"

        # window setup
        self.window = tk.Tk()
        self.window.title("Guess the Number")
        self.window.iconbitmap("Images/question_mark_small.ico")
        self.window.geometry("900x600")
        self.window.resizable(False, False)
        self.window.config(bg=self.bg_color)

        # widgets
        # -top menu
        menu_bar = tk.Menu(self.window)
        options = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game Options", menu=options)
        options.add_command(label="New Game", command=self.back_to_menu)
        options.add_command(label="Exit", command=self.window.destroy)
        self.window.config(menu=menu_bar)

        # -game title
        self.game_title = tk.Label(self.window,
                                   bg=self.bg_color,
                                   text="Guess the Number!",
                                   font=("Bagel Fat One", 36),
                                   pady=25
                                   ).pack()
        # -question mark/answer reveal
        self.answer = tk.Label(self.window,
                               bg=self.bg_color,
                               text="?",
                               font=("Bagel Fat One", 65)
                               )
        self.answer.pack()
        
        # defaults to main menu on open
        self.menu = self.main_menu()

    def back_to_menu(self):
        """
        Resets game window back to the main menu.
        """
        try:
            game_frame = self.window.nametowidget("game_frame")
        except:
            pass
        else:
            game_frame.destroy()
            self.window.nametowidget("game_message").destroy()
            self.answer.config(text="?")
            self.menu = self.main_menu()

    def main_menu(self):
        """
        Displays the game's main menu in the window.

        Returns:
            menu (widget): Frame widget containing the menu widgets.
        """
        menu = tk.Frame(self.window,
                        bg=self.bg_color,
                        padx=0,
                        pady=0
                        )
        menu.pack(pady=10)

        # menu buttons
        self.create_button(menu, "Easy", lambda dif="easy": self.gameplay(dif)).pack(pady=8)
        self.create_button(menu, "Intermediate", lambda dif="inter": self.gameplay(dif)).pack(pady=8)
        self.create_button(menu, "Hard", lambda dif="hard": self.gameplay(dif)).pack(pady=8)
        self.create_button(menu, "Exit Game", self.window.destroy).pack(pady=8)
        
        return menu

    def gameplay(self, difficulty):
        """
        Displays game frame to the window and handles all gameplay logic.

        Parameters:
            difficulty (str): Possible values: ["easy", "inter", "hard"] - Setting that determines the range of values the answer number can be in
            and the number of guesses the user will receive.
        """
        def entry_validation(entry_text):
            """
            Ensures entry text consists of only digits and has a max
            length of 3 characters.

            Parameters:
                entry_text (entry text obj): Object representing the text entered into the entry box. 
            """
            # allow only numbers for input
            if re.search(r"[^0-9]", entry_text.get()):
                entry_text.set(entry_text.get()[:-1])
            # limit input to 3 characters
            if len(entry_text.get()) > 3:
                entry_text.set(entry_text.get()[:3])

        def toggle_hints():
            """
            Toggles the hint check box between checked for hints on and displaying the hint below
            the entry box, and unchecked and removing the hint from below the entry box.
            """
            # hints off and turning on
            if hint_checkbox.image == checkbox_unchecked:
                hint_checkbox.config(image=checkbox_checked)
                hint_checkbox.image = checkbox_checked
                hint_text.pack()
            # hints on and turning off
            elif hint_checkbox.image == checkbox_checked:
                hint_checkbox.config(image=checkbox_unchecked)
                hint_checkbox.image = checkbox_unchecked
                hint_text.pack_forget()

        def get_upper_bound():
            """
            Determines the upper bound for possible winning number.

            Returns:
                (int): The upper bound value.
            """
            if difficulty == "easy":
                upper_bound = 10
            elif difficulty == "inter":
                upper_bound = 50
            else:
                upper_bound = 100
            
            return upper_bound

        def generate_number(upper_bound):
            """
            Generates a random number between 1 and the given upper bound, inclusive.

            Returns:
                (int): The number the user is trying to guess.
            """
            return random.randrange(1, upper_bound + 1)

        def get_lives():
            """
            Determines the number of lives based on the set difficulty of the game.
            Easy: 3
            Intermediate: 5
            Hard: 8

            Returns:
                (int): The number of guesses the user will have.
            """
            if difficulty == "easy":
                return 3
            elif difficulty == "inter":
                return 5
            else:
                return 8

        def set_hint():
            """
            Changes the hint text to inform the user whether their guess was higher or lower
            than the winning number.
            """
            if guess.get() == winning_num:
                hint_text.config(text="Your guess is correct!")
            elif int(guess.get()) < int(winning_num):
                hint_text.config(text="Your guess is too low.")
            else:
                hint_text.config(text="Your guess is too high.")

        def evaluate_guess():
            """
            Handles the game state based on whether the user's guess was correct or incorrect
            and how many lives they had remaining.
            """
            # guess is blank
            if guess.get() == "":
                pass
            # guess is correct
            elif guess.get() == winning_num:
                set_hint()
                reveal_number()
                set_game_message("You Win!", "#5beb34")
                entry_box.config(state="disabled")
                submit_button.config(state="disabled")
                options_frame.place(x=260, y=220)
            # guess is incorrect
            else:
                set_hint()
                lives_left = int(lives["text"][-1]) - 1
                lives.config(text=lives["text"][:-1] + str(lives_left)) # reduce lives by 1
                # -no lives remaining
                if lives_left == 0:
                    reveal_number()
                    set_game_message("You Lost :(", "#c71818")
                    entry_box.config(state="disabled")
                    submit_button.config(state="disabled")
                    options_frame.place(x=260, y=220)
                # -lives remaining
                else:
                    guess.set("")   # clear entry box

        def reveal_number():
            """
            Changes the question mark to the winning number.
            """
            self.answer.config(text=winning_num)

        def set_game_message(text, color):
            """
            Sets the game message to the given text and font color.

            Parameters:
                text (str): Text the game message will be set to.
                color (str): Font color the text will be set to.
            """
            game_message_text.config(text=text, fg=color)

        # game variables
        upper_bound = get_upper_bound()
        winning_num = str(generate_number(upper_bound))
        num_lives = get_lives()

        # gameplay frame
        game_frame = tk.Frame(self.window,
                              width=500,
                              bg=self.bg_color,
                              name="game_frame"
                              )
        # guess box label
        entry_box_label = tk.Label(game_frame,
                                   bg=self.bg_color,
                                   text="Enter guess:",
                                   font=("Bagel Fat One", 16)
                                   )
        entry_box_label.pack(pady=8)
        
        # guess entry box
        guess = tk.StringVar()
        entry_box = tk.Entry(game_frame,
                             width=20,
                             font=("Arial", 24),
                             justify="center",
                             textvariable=guess
                             )
        entry_box.pack()
        guess.trace_add("write", lambda *args: entry_validation(guess))   # limit guess to 3 numerical chars
        entry_box.focus_set()
        
        # submit button
        submit_button = self.create_button(game_frame, "Enter Guess:", evaluate_guess)
        submit_button.pack(pady=10)
        self.window.bind("<Return>", lambda event: submit_button.invoke())

        # hint box --- Take text out of button, make label and put in small frame with button
        checkbox_unchecked = Image.open("Images/checkbox_unchecked.png")
        checkbox_unchecked = ImageTk.PhotoImage(checkbox_unchecked)
        checkbox_checked = Image.open("Images/checkbox_checked.png")
        checkbox_checked = ImageTk.PhotoImage(checkbox_checked)

        # hint box frame
        hint_box_frame = tk.Frame(game_frame,
                                  width=160,
                                  bg=self.bg_color
                                  )
        hint_box_frame.place(x=720, y=35)

        # hint box label
        hint_box_label = tk.Label(hint_box_frame,
                                  bg=self.bg_color,
                                  text="Hints",
                                  font=("Bagel Fat One", 24)
                                  )
        hint_box_label.grid(row=0, column=0)
        
        # hint check box
        hint_checkbox = tk.Button(hint_box_frame,
                             bg=self.bg_color,
                             activebackground=self.bg_color,
                             bd=0,
                             image=checkbox_unchecked,
                             command = toggle_hints
                             )
        hint_checkbox.image = checkbox_unchecked
        hint_checkbox.grid(row=0, column=1, padx=10)

        # hint text
        hint_text = tk.Label(game_frame,
                             bg = self.bg_color,
                             font = ("Bagel Fat One", 16)
                             )
        
        # remaining guesses
        lives = tk.Label(game_frame,
                         bg=self.bg_color,
                         text = "Guesses Remaining: " + str(num_lives),
                         font=("Bagel Fat One", 16)
                         )
        lives.place(x=20, y=285)

        # game message (display range, 'You Win!' / 'You Lost :(' )
        game_message = tk.Frame(self.window,
                                width=15,
                                bg=self.bg_color,
                                name="game_message"
                                )
        game_message_text = tk.Label(game_message,
                                     width=25,
                                     bg=self.bg_color,
                                     text="Number is between 1 and " + str(upper_bound),
                                     font=("Bagel Fat One", 20),
                                     justify="center"
                                     )
        game_message_text.pack()
        game_message.place(x=250, y=100)

        # end game options
        options_frame = tk.Frame(game_frame,
                                 bg=self.bg_color
                                 )
        self.create_button(options_frame, "Play Again", self.back_to_menu).pack(side="left", padx=10) # play again button
        self.create_button(options_frame, "Exit", self.window.destroy).pack(side="right", padx=10)      # exit button

        # display game frame
        self.menu.pack_forget()
        game_frame.pack(expand=True, fill="both")
        game_frame.pack_propagate(0)

    def create_button(self, parent, text, func):
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
        button = tk.Button(parent,
                           width=12,
                           height=0,
                           bd=5,
                           text=text,
                           font=("Bagel Fat One", 16),
                           compound="center",
                           padx=0,
                           pady=0,
                           cursor="hand2",
                           command=func
                           )

        return button
    
    def run(self):
        """
        Opens UI window and begins game execution.
        """
        self.window.mainloop()