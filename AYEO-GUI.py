from tkinter import *
import tkinter as tk
import random
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import simpledialog
import pygame
import json

class BingoGameApp:

    # Class representing the main Bingo game application
    def __init__(self, root, dimension):
        self.root = root
        self.root.title("Bingo Game")
        self.dimension = dimension
        self.count_user = 0
        self.count_computer = 0
        self.user_name = User_name
        self.root.iconbitmap('logo.ico')
        self.root.configure(background='light sea green')



        # Create frames for user and computer tables with added space
        self.user_frame = tk.Frame(self.root, padx=10,background='light sea green')
        self.user_frame.grid(row=0, column=0,padx=10)

        self.computer_frame = tk.Frame(self.root, padx=10,background='light sea green')
        self.computer_frame.grid(row=0, column=1,padx=10)

        # Create user and computer tables
        self.create_table(f"{self.user_name} Table", self.user_frame)
        self.create_table("Computer Table", self.computer_frame)

        # Score labels
        self.user_score_label = tk.Label(self.root, text=f"   {self.user_name}'s Score: ",background='light sea green' )
        self.user_score_label.grid(row=1, column=0,sticky=tk.W)

        self.computer_score_label = tk.Label(self.root, text="Computer's Score: ",background='light sea green')
        self.computer_score_label.grid(row=1, column=1,sticky=tk.W)

        # Set to store button values
        self.used_numbers = set()

        # User makes the first move
        self.user_play()

        # Create menu button
        menu_button = tk.Button(self.root, text="Menu", command=self.show_menu,background='white')
        menu_button.grid(row=2, column=0, columnspan=self.dimension, pady=10)

        # Menu variables
        self.menu_visible = False

        # Create menu popup
        self.menu_popup = tk.Toplevel(root)
        self.menu_popup.iconbitmap('logo.ico')
        self.menu_popup.title("Menu")
        self.menu_popup.withdraw()
        self.menu_popup.configure(background='light sea green')

        # Continue button in menu
        continue_button = tk.Button(self.menu_popup, text="Continue", command=self.hide_menu)
        continue_button.pack(pady=10)

        # Restart button in menu
        restart_button = tk.Button(self.menu_popup, text="Restart", command=self.restart_game)
        restart_button.pack(pady=5)

        # Quit button in menu
        quit_button = tk.Button(self.menu_popup, text="Quit", command=self.quit_game)
        quit_button.pack(pady=5)

    def show_menu(self):
        self.menu_visible = True
        self.menu_popup.deiconify()


    def hide_menu(self):
        self.menu_visible = False
        self.menu_popup.withdraw()


    def save_game_state(self):
        game_state_Computer = {
            "user_name": self.user_name,
            "dimension": self.dimension,
            "count_user": self.count_user,
            "count_computer": self.count_computer,
            "used_numbers": list(self.used_numbers)
        }

        with open("saved_game_state.json", "w") as file:
            json.dump(game_state_Computer, file)

        messagebox.showinfo('Save Game', 'Game state saved successfully.')

    def load_game_state(self):
        self.menu_popup.withdraw()
        try:
            with open("saved_game_state.json", "r") as file:
                game_state_computer = json.load(file)

            # Assuming your class has these attributes
            self.user_name = game_state_computer.get("user_name")
            self.dimension = game_state_computer.get("dimension")
            self.count_user = game_state_computer.get("count_user")
            self.count_computer = game_state_computer.get("count_computer")
            self.used_numbers = set(game_state_computer.get("used_numbers", []))

            self.user_frame.destroy()
            self.user_frame = tk.Frame(self.root, padx=10, background='light sea green')
            self.user_frame.grid(row=0, column=0, padx=10)
            self.create_table(f"{self.user_name}'s Table", self.user_frame, self.count_user)

            self.computer_frame.destroy()
            self.computer_frame = tk.Frame(self.root, padx=10, background='light sea green')
            self.computer_frame.grid(row=0, column=1, padx=10)
            self.create_table("Computer Table", self.computer_frame, self.count_computer)

            self.user_score_label = tk.Label(self.root, text=f"{self.user_name}'s Score: ",
                                             background='light sea green')
            self.user_score_label.grid(row=1, column=0, sticky="W")

            self.computer_score_label = tk.Label(self.root, text="Computer's Score: ", background='light sea green')
            self.computer_score_label.grid(row=1, column=1, sticky='W')

            # Update score labels
            self.user_score_label.config(text=f"   {self.user_name}'s Score:            ")
            self.computer_score_label.config(text='Computer score is:            ')

            self.menu_popup = tk.Toplevel(root)
            self.menu_popup.iconbitmap('logo.ico')
            self.menu_popup.title("Menu")
            self.menu_popup.withdraw()
            self.menu_popup.configure(background='light sea green')

            # Continue button in menu
            continue_button = tk.Button(self.menu_popup, text="Continue", command=self.hide_menu)
            continue_button.pack(pady=10)

            # Restart button in menu
            restart_button = tk.Button(self.menu_popup, text="Restart", command=self.restart_game)
            restart_button.pack(pady=5)

            save_button = tk.Button(self.menu_popup, text="Save", command=self.save_game_state)
            save_button.pack(pady=5)

            load = tk.Button(self.menu_popup, text="load", command=self.load_game_state)
            load.pack(pady=5)

            # Quit button in menu
            quit_button = tk.Button(self.menu_popup, text="Quit", command=self.quit_game)
            quit_button.pack(pady=5)

            messagebox.showinfo('Load Game', 'Game state loaded successfully.')

        except FileNotFoundError:
            messagebox.showinfo('Load Game', 'No saved game state found.')
        except json.JSONDecodeError:
            messagebox.showerror('Error', 'Error decoding saved game state.')


    def restart_game(self):
        confirm=messagebox.askyesno('Restart Game', 'Do you want to restart game?')
        if confirm:
            self.hide_menu()

            # Reset scores
            self.count_user = 0
            self.count_computer = 0

            # Clear used numbers
            self.used_numbers = set()

            # Destroy and create new user and computer tables
            self.user_frame.destroy()
            self.user_frame = tk.Frame(self.root, padx=10,background='light sea green')
            self.user_frame.grid(row=0, column=0, padx=10)
            self.create_table(f"{self.user_name}'s Table", self.user_frame)

            self.computer_frame.destroy()
            self.computer_frame = tk.Frame(self.root, padx=10,background='light sea green')
            self.computer_frame.grid(row=0, column=1, padx=10)
            self.create_table("Computer Table", self.computer_frame)

            self.user_score_label = tk.Label(self.root, text=f"{self.user_name}'s Score: ", background='light sea green')
            self.user_score_label.grid(row=1, column=0,sticky="W")

            self.computer_score_label = tk.Label(self.root, text="Computer's Score: ", background='light sea green')
            self.computer_score_label.grid(row=1, column=1,sticky='W')

            # Update score labels
            self.user_score_label.config(text=f"   {self.user_name}'s Score:            ")
            self.computer_score_label.config(text='Computer score is:            ')



    def quit_game(self):
        messagebox.askokcancel("Quit", "Are you sure you want to quit?")
        self.root.destroy()
        self.menu()

    def create_table(self, table_name, frame):
        tk.Label(frame, text=table_name,background='light sea green').grid(row=0, columnspan=self.dimension)
        table_frame = tk.Frame(frame)
        table_frame.grid(row=1, columnspan=self.dimension)

        # Generate random unique numbers for buttons
        numbers = random.sample(range(1, self.dimension ** 2 + 1), self.dimension ** 2)

        # Create buttons in a dimension x dimension grid
        buttons = [[None] * self.dimension for _ in range(self.dimension)]
        for i in range(self.dimension):
            for j in range(self.dimension):
                button_value = numbers[i * self.dimension + j]
                button = tk.Button(table_frame, text=str(button_value), width=5, height=2, command=lambda i=i, j=j, value=button_value: self.button_click(frame, i, j, value))
                button.grid(row=i, column=j)
                buttons[i][j] = button

        # Store the buttons in the frame
        frame.buttons = buttons

    def button_click(self, frame, i, j, value):
        user_button = frame.buttons[i][j]
        pygame.mixer.music.load('click.wav')
        pygame.mixer.music.play()
        computer_buttons = [button for row in self.computer_frame.buttons for button in row]

        if user_button.cget("text") != 'X':
            user_button.config(text='X', bg='red')

            # Update the corresponding button in the other player's table
            for row in self.computer_frame.buttons:
                for button in row:
                    if button.cget("text") == str(value) and button != user_button:
                        button.config(text='X', bg='red')
                        break

            # Add the used number to the set
            self.used_numbers.add(value)

            # Check for Bingo and update the score
            self.count_user += 1
            self.update_score(self.user_frame, self.count_user, self.user_score_label, f"{User_name}")
            self.update_score(self.computer_frame, self.count_computer, self.computer_score_label, "Computer")


            # Computer makes a move after a delay
            self.root.after(250, self.computer_play)

    def computer_play(self):
        # Simulate the computer's move
        available_numbers = set(range(1, self.dimension ** 2 + 1)) - self.used_numbers
        if available_numbers:
            computer_choice = random.choice(list(available_numbers))
            self.used_numbers.add(computer_choice)

            # Update the corresponding button in the computer's table
            for row in self.computer_frame.buttons:
                for button in row:
                    if button.cget("text") == str(computer_choice):
                        button.config(text='X', bg='red')
                        break

            # Update the corresponding button in the user's table
            for row in self.user_frame.buttons:
                for button in row:
                    if button.cget("text") == str(computer_choice):
                        button.config(text='X', bg='red')
                        break

            # Disable computer's buttons
            for row in self.computer_frame.buttons:
                for button in row:
                    button.config(state=tk.DISABLED)

            self.count_computer += 1
            self.update_score(self.computer_frame, self.count_computer, self.computer_score_label, "Computer")
            self.update_score(self.user_frame, self.count_user, self.user_score_label, f"{User_name}")

            # User makes the next move
            self.user_play()

    def update_score(self, frame, count, score_label, player_name):
        global computer_score, user_score
        count_lines = 0

        # Check for bingo in rows, columns, and diagonals
        for i in range(self.dimension):
            if all(frame.buttons[i][j].cget("text") == "X" for j in range(self.dimension)):
                count_lines += 1
            if all(frame.buttons[j][i].cget("text") == "X" for j in range(self.dimension)):
                count_lines += 1
        if all(frame.buttons[i][i].cget("text") == "X" for i in range(self.dimension)):
            count_lines += 1
        if all(frame.buttons[i][self.dimension - 1 - i].cget("text") == "X" for i in range(self.dimension)):
            count_lines += 1

        # Display the score based on the number of lines
        if count_lines >= 5:
            score = "BINGO"
            if player_name == self.user_name:
                pygame.mixer.music.load('win_sound.wav')
                pygame.mixer.music.play()
                messagebox.showinfo("BINGO", f"Congratulations  {player_name}!  You got BINGO!")
                self.root.destroy()
            else:
                pygame.mixer.music.load('Lose sound effects.wav')
                pygame.mixer.music.play()
                messagebox.showinfo("BINGO", "LOSER! Computer got BINGO!, You need to practice more")
                self.root.destroy()
            self.disable_all_buttons(frame)
        elif count_lines == 4:
            score = "BING     "
        elif count_lines == 3:
            score = "BIN      "
        elif count_lines == 2:
            score = "BI       "
        elif count_lines == 1:
            score = "B        "
        else:
            score = "         "

        score_label.config(text=f"{player_name}'s Score: {score}         ")
        return count_lines

    def disable_all_buttons(self, frame):
        for row in frame.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def user_play(self):
        # Enable user's buttons
        for row in self.user_frame.buttons:
            for button in row:
                button.config(state=tk.NORMAL)






class BingoGameApp_vsfriend:
    def __init__(self, root, dimension, user_name, friend_name):
        self.root = root
        self.root.title("Bingo Game")
        self.dimension = dimension
        self.count_user = 0
        self.count_friend = 0
        self.user_name = user_name
        self.friend_name = friend_name
        self.root.iconbitmap('logo.ico')
        self.root.configure(bg='light sea green')


        self.turn_label = tk.Label(self.root, text="Turn: User", background='light sea green')
        self.turn_label.grid(row=2, column=0, sticky=tk.W)

        # Create frames for user and friend tables
        self.user_frame = tk.Frame(self.root, padx=10,bg='light sea green')
        self.user_frame.grid(row=0, column=0, padx=10)

        self.friend_frame = tk.Frame(self.root, padx=10,bg='light sea green')
        self.friend_frame.grid(row=0, column=1, padx=10)

        # Create user and friend tables
        self.create_table(f"{self.user_name}'s Table", self.user_frame, self.count_user)
        self.create_table(f"{self.friend_name}'s Table", self.friend_frame, self.count_friend)

        # Score labels
        self.user_score_label = tk.Label(self.root, text=f"{self.user_name}'s Score: ",bg='light sea green')
        self.user_score_label.grid(row=1, column=0, sticky="w")

        self.friend_score_label = tk.Label(self.root, text=f"{self.friend_name}'s Score: ",bg='light sea green')
        self.friend_score_label.grid(row=1, column=1, sticky="w")

        # Set to store button values
        self.used_numbers = set()

        # Initialize the current player (1 for user, 2 for friend)
        self.current_player = 1

        # User makes the first move
        self.user_play()

        # Create menu button
        menu_button = tk.Button(self.root, text="Menu", command=self.show_menu)
        menu_button.grid(row=2, column=0, columnspan=self.dimension)

        # Menu variables
        self.menu_visible = False

        # Create menu popup
        self.menu_popup = tk.Toplevel(root)
        self.menu_popup.iconbitmap('logo.ico')
        self.menu_popup.config(bg='light sea green')
        self.menu_popup.title("Menu")
        self.menu_popup.withdraw()

        # Continue button in menu
        continue_button = tk.Button(self.menu_popup, text="Continue", command=self.hide_menu)
        continue_button.pack(pady=10)

        # Restart button in menu
        restart_button = tk.Button(self.menu_popup, text="Restart", command=self.restart_game)
        restart_button.pack(pady=5)

        # Quit button in menu
        quit_button = tk.Button(self.menu_popup, text="Quit", command=self.quit_game)
        quit_button.pack(pady=5)

    def show_menu(self):
        self.menu_visible = True
        self.menu_popup.deiconify()

    def hide_menu(self):
        self.menu_visible = False
        self.menu_popup.withdraw()

    def restart_game(self):
        confirm=messagebox.askyesno('Restart Game', 'Do you want to restart game?')
        if confirm :
            self.hide_menu()

            # Reset scores
            self.count_user = 0
            self.count_friend = 0

            # Clear used numbers
            self.used_numbers = set()

            # Destroy and create new user and friend tables
            self.user_frame.destroy()
            self.user_frame = tk.Frame(self.root, padx=10,bg='light sea green')
            self.user_frame.grid(row=0, column=0, padx=10)
            self.create_table(f"{self.user_name}'s Table", self.user_frame, self.count_user)

            self.friend_frame.destroy()
            self.friend_frame = tk.Frame(self.root, padx=10,bg='light sea green')
            self.friend_frame.grid(row=0, column=1, padx=10)
            self.create_table(f"{self.friend_name}'s Table", self.friend_frame, self.count_friend)

            # Score labels
            self.user_score_label = tk.Label(self.root, text=f"{self.user_name}'s Score: ", bg='light sea green')
            self.user_score_label.grid(row=1, column=0, sticky="w")

            self.friend_score_label = tk.Label(self.root, text=f"{self.friend_name}'s Score: ", bg='light sea green')
            self.friend_score_label.grid(row=1, column=1, sticky="w")

            # Update score labels
            self.user_score_label.config(text=f"{self.user_name}'s Score:                    ")
            self.friend_score_label.config(text=f"{self.friend_name}'s Score:                ")

    def update_turn_label(self, player_name):
        self.turn_label.config(text=f"Turn: {player_name}")

    def save_game_state(self):
        game_state_friend = {
            "user_name": self.user_name,
            "friend_name": self.friend_name,
            "dimension": self.dimension,
            "count_user": self.count_user,
            'count_friend': self.count_friend,
            "used_numbers": list(self.used_numbers),
        }

        file_path = "saved_game_state.json"
        with open(file_path, "w") as file:
            json.dump(game_state_friend, file)

        messagebox.showinfo('Save Game', f'Game state saved successfully.')

    def load_game_state(self):
        try:
            file_path = "saved_game_state.json"
            with open(file_path, "r") as file:
                loaded_state = json.load(file)

            # Set the loaded state to resume the game
            self.user_name = loaded_state["user_name"]
            self.friend_name = loaded_state["friend_name"]
            self.dimension = loaded_state["dimension"]
            self.count_user = loaded_state["count_user"]
            self.count_friend = loaded_state["count_friend"]
            self.used_numbers = set(loaded_state["used_numbers"])

            # Destroy and recreate frames and tables
            self.user_frame.destroy()
            self.user_frame = tk.Frame(self.root, padx=10, bg='light sea green')
            self.user_frame.grid(row=0, column=0, padx=10)
            self.create_table(f"{self.user_name}'s Table", self.user_frame, self.count_user)

            self.friend_frame.destroy()
            self.friend_frame = tk.Frame(self.root, padx=10, bg='light sea green')
            self.friend_frame.grid(row=0, column=1, padx=10)
            self.create_table(f"{self.friend_name}'s Table", self.friend_frame, self.count_friend)

            # Update score labels
            self.update_score(self.user_frame, self.count_user, self.user_score_label, self.user_name)
            self.update_score(self.friend_frame, self.count_friend, self.friend_score_label, self.friend_name)

            messagebox.showinfo('Load Game', f'Game state loaded successfully from: {file_path}')
        except FileNotFoundError:
            messagebox.showerror('Load Game', 'No saved game state found.')
        except Exception as e:
            messagebox.showerror('Load Game', f'Error loading game state: {e}')

    def quit_game(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()
            self.menu()

    def create_table(self, table_name, frame, count):
        tk.Label(frame, text=table_name,bg='light sea green').grid(row=0, columnspan=self.dimension)
        table_frame = tk.Frame(frame,bg='light sea green')
        table_frame.grid(row=1, columnspan=self.dimension)

        # Generate random unique numbers for buttons
        numbers = random.sample(range(1, self.dimension ** 2 + 1), self.dimension ** 2)

        # Create buttons in a dimension x dimension grid
        buttons = [[None] * self.dimension for _ in range(self.dimension)]
        for i in range(self.dimension):
            for j in range(self.dimension):
                button_value = numbers[i * self.dimension + j]
                button = tk.Button(table_frame, text=str(button_value), width=5, height=2,command=lambda i=i, j=j, value=button_value: self.button_click(frame, i, j, value))
                button.grid(row=i, column=j)
                buttons[i][j] = button

        # Store the buttons in the frame
        frame.buttons = buttons

    def button_click(self, frame, i, j, value):
        pygame.mixer.music.load('click.wav')
        pygame.mixer.music.play()
        user_button = frame.buttons[i][j]

        # Check if the current player is allowed to play
        if (
            (self.current_player == 1 and frame == self.friend_frame)
            or (self.current_player == 2 and frame == self.user_frame)
        ):
            messagebox.showinfo("Invalid Move", "It's not your turn.")
            return

        if user_button.cget("text") == str(value):
            user_button.config(text='X', bg='red')

            # Update the corresponding button in the opponent's table
            for row in self.friend_frame.buttons:
                for button in row:
                    if button.cget("text") == str(value):
                        button.config(text='X', bg='red')

            # Update the corresponding button in the user's table
            for row in self.user_frame.buttons:
                for button in row:
                    if button.cget("text") == str(value):
                        button.config(text='X', bg='red')

            # Add the used number to the set
            self.used_numbers.add(value)

            # Check for Bingo and update the score
            self.update_score(self.user_frame, self.count_user, self.user_score_label, self.user_name)
            self.update_score(self.friend_frame, self.count_friend, self.friend_score_label, self.friend_name)

            # Check for game over
            self.check_game_result()

            # Switch turns between user and friend
            self.current_player = 3 - self.current_player

            # Perform the next move based on the current player
            if self.current_player == 1:
                self.update_turn_label(self.user_name)
                self.user_play()
            elif self.current_player == 2:
                self.friend_play()
                self.update_turn_label(self.friend_name)


    def update_score(self, frame, count, score_label, player_name):
        count_lines = self.count_lines(frame)

        # Display the score based on the number of lines
        if count_lines == 0:
            score = ""
        elif count_lines == 1:
            score = "B             "
        elif count_lines == 2:
            score = "BI            "
        elif count_lines == 3:
            score = "BIN           "
        elif count_lines == 4:
            score = "BING          "
        elif count_lines == 5:
            score = "BINGO         "
        else:
            score = "              "

        score_label.config(text=f"{player_name}'s Score: {score}            ")

    def count_lines(self, frame):
        count_lines = 0

        # Check for bingo in rows, columns, and diagonals
        for i in range(self.dimension):
            if all(self.get_button_text(frame, i, j) == 'X' for j in range(self.dimension)):
                count_lines += 1
            if all(self.get_button_text(frame, j, i) == 'X' for j in range(self.dimension)):
                count_lines += 1

        if all(self.get_button_text(frame, i, i) == 'X' for i in range(self.dimension)):
            count_lines += 1

        if all(self.get_button_text(frame, i, self.dimension - 1 - i) == 'X' for i in range(self.dimension)):
            count_lines += 1

        return count_lines

    def get_button_text(self, frame, i, j):
        # Check if the button is within the frame boundaries
        if 0 <= i < self.dimension and 0 <= j < self.dimension:
            return str(frame.buttons[i][j].cget("text"))
        else:
            return ''

    def check_game_result(self):
        count_user_lines = self.count_lines(self.user_frame)
        count_friend_lines = self.count_lines(self.friend_frame)

        if count_user_lines == 5 and count_friend_lines == 5:
            pygame.mixer.music.load('Lose sound effects.wav')
            pygame.mixer.music.play()
            messagebox.showinfo("Game Over", "It's a draw! Both players got BINGO! Game Over!")
            self.root.destroy()

        elif count_user_lines == 5:
            pygame.mixer.music.load('win_sound.wav')
            pygame.mixer.music.play()
            messagebox.showinfo("Congratulations", f"Congratulations {self.user_name}! {self.friend_name} ,you need to practice more. ")
            self.root.destroy()

        elif count_friend_lines == 5:
            pygame.mixer.music.load('win_sound.wav')
            pygame.mixer.music.play()
            messagebox.showinfo("Congratulations", f"Congratulations {self.friend_name}! You got BINGO! {self.user_name} ,you need to practice more.")
            self.root.destroy()


    def user_play(self):
        # Enable user's buttons
        for row in self.user_frame.buttons:
            for button in row:
                button.config(state=tk.NORMAL)
                self.update_turn_label(self.user_name)

    def friend_play(self):
        # Disable user's buttons
        for row in self.user_frame.buttons:
            for button in row:
                button.config(state=tk.DISABLED)
                self.update_turn_label(self.friend_name)

        # Automatically pick a number for the friend
        available_numbers = set(range(1, self.dimension ** 2 + 1)) - self.used_numbers
        chosen_number = random.choice(list(available_numbers))
        self.button_click(self.friend_frame, (chosen_number - 1) // self.dimension, (chosen_number - 1) % self.dimension, chosen_number)

        # Check for game over
        self.check_game_result()

        # Update scores and continue with the game
        self.update_score(self.user_frame, self.count_user, self.user_score_label, self.user_name)
        self.update_score(self.friend_frame, self.count_friend, self.friend_score_label, self.friend_name)
        self.user_play()


class SoundApp:
    def __init__(self, root):
        self.root = root
        pygame.init()
        pygame.mixer.init()

        self.mute_image = PhotoImage(file="mute.png")
        self.speaker_image = PhotoImage(file="speaker.png")



        # Load the sound file using pygame.mixer.Sound
        self.sound = pygame.mixer.Sound('game_voice.wav')

        # Create a single button to control the sound
        self.play_button = tk.Button(root, image=self.mute_image, command=self.toggle_sound, font=("Arial", 5), fg="white",
                                     bg="light sea green")
        self.play_button.place(relx=0.3535, rely=0.873, anchor=tk.CENTER)

        # Flag to track the state of the sound (playing or stopped)
        self.sound_playing = True

        # Check for sound end every 100 milliseconds
        self.root.after(100, self.check_sound_end)

    def toggle_sound(self):
        if self.sound_playing:
            print('toggle sound button')
            pygame.mixer.music.load('click.wav')
            pygame.mixer.music.play()
            # If the sound is playing, stop it
            self.sound.stop()
            self.play_button.config(image=self.speaker_image)
        else:
            print('toggle sound button')
            pygame.mixer.music.load('click.wav')
            pygame.mixer.music.play()
            # If the sound is stopped, play it
            self.sound.play()
            self.play_button.config(image=self.mute_image)

        # Toggle the sound state
        self.sound_playing = not self.sound_playing

    def check_sound_end(self):
        if pygame.mixer.get_busy() == 0 and self.sound_playing:
            # The sound has finished, restart it
            self.sound.play()

        # Check for sound end every 100 milliseconds
        self.root.after(100, self.check_sound_end)


def dimensions():
    global dimension_value
    Default_dim = messagebox.askyesno('Game Options', 'Do you want to play with default dimensions (5x5)?')
    if Default_dim == 1:
        print('dimension is default (5)')
        dimension_value = 5
    else:
        print('dimensions is custom')
        while True:
            custom = simpledialog.askinteger("Custom Dimensions", "Enter the size of the grid:")
            if custom is not None and 5 <= custom <= 12:
                dimension_value = custom
                break
            else:
                messagebox.showerror("Invalid Dimensions", "Please enter a valid dimension between 5 and 12.")

    BingoGameApp(tk.Tk(), dimension_value)
    print('Game initated vs Friend')

def dimensions_friend():
    global dimension_value
    x = messagebox.askyesno('Game Options', 'Do you want to play with default dimensions (5x5)?')
    if x == 1:
        print('dimension is default (5)')
        dimension_value = 5
    else:
        print('dimensions is custom')
        while True:

            custom = simpledialog.askinteger("Custom Dimensions", "Enter the size of the grid:")
            if custom is not None and 5 <= custom <= 12:
                dimension_value = custom
                break
            else:
                messagebox.showerror("Invalid Dimensions", "Please enter a valid dimension between 5 and 12.")

    BingoGameApp_vsfriend(tk.Tk(), dimension_value, User_name, friend_name_value)
    print('Game initated vs Friend')

def load_game():
    print('Load button enterd')
    messagebox.showinfo("Game", "not availabe right now  ")


def friend_name():
    global friend_name_value, User_name, dimension_value
    input_window = tk.Toplevel()
    input_window.title("Game Options")
    input_window.iconbitmap('logo.ico')

    def store_name():
        pygame.mixer.music.load('click.wav')
        pygame.mixer.music.play()
        global friend_name_value
        friend_name_value = Entry_name.get()
        print('Friend name: ', friend_name_value)
        dimensions_friend()
        input_window.destroy()

    label_name = tk.Label(input_window, text="Enter your friend's name:", font=("Helvetica", 12, 'bold'), fg='dark cyan')
    Entry_name = tk.Entry(input_window,font='Helvetica')
    button_name = tk.Button(input_window, text="submit", font=("Helvetica", 12, 'bold'), command=store_name, fg='dark cyan')
    button_name.grid(row=2, column=3)
    label_name.grid(row=1, column=1)
    Entry_name.grid(row=1, column=2)

def Com_friend():
    pygame.mixer.music.load('click.wav')
    pygame.mixer.music.play()
    global friend_name_value,User_name
    input_window = tk.Toplevel()
    input_window.title("Game Options")
    input_window.iconbitmap('logo.ico')

    def store_com():
        print('play vs Computer')
        pygame.mixer.music.load('click.wav')
        pygame.mixer.music.play()
        input_window.destroy()
        dimensions()
    def store_friend():
        print('play vs Friend')
        pygame.mixer.music.load('click.wav')
        pygame.mixer.music.play()
        input_window.destroy()
        friend_name()

    label_name = tk.Label(input_window, text=(f"Hi! {User_name} play against computer or friend:"), font=("Helvetica", 12, 'bold'), fg='dark cyan')
    button_friend = tk.Button(input_window, text="Friend", font=("Helvetica", 12, 'bold'), command=store_friend, fg='dark cyan')
    button_computer = tk.Button(input_window, text="Computer", font=("Helvetica", 12, 'bold'), command=store_com, fg='dark cyan')

    label_name.grid(row=0, column=1)
    button_friend.grid(row=1, column=0)
    button_computer.grid(row=1, column=3)

def Get_name():
    pygame.mixer.music.load('click.wav')
    pygame.mixer.music.play()
    global User_name
    input_window = tk.Toplevel()
    input_window.title("Game Options")
    input_window.iconbitmap('logo.ico')

    def on_submit():
        pygame.mixer.music.load('click.wav')
        pygame.mixer.music.play()
        global User_name
        User_name = user_name_var.get()
        print('User Name: ', User_name)
        input_window.destroy()
        Com_friend()

    user_name_var = tk.StringVar()
    label_name = tk.Label(input_window, text="Enter your name:", font=("Helvetica", 12, 'bold'), fg='dark cyan')
    User_name = tk.Entry(input_window, font=("Helvetica"),textvariable=user_name_var)
    button_name = tk.Button(input_window, text="submit", font=("Helvetica", 12, 'bold'), fg='dark cyan', command=on_submit)
    button_name.grid(row=2, column=3)
    label_name.grid(row=1, column=1)
    User_name.grid(row=1, column=2)

    return User_name

def menu():
    root = tk.Tk()
    root.title("play Bingo")
    root.attributes("-fullscreen", True)
    root.iconbitmap('logo.ico')
    bg_image = Image.open("ayeo_front.png")
    bg_image= bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    image = ImageTk.PhotoImage(bg_image)
    label_bg = tk.Label(root, image=image)
    label_bg.place(x=0, y=0 ,relwidth=1, relheight=1)
    label_bg.pack(side=tk.TOP)

    sound_app=SoundApp(root)

    start = tk.Button(root, text="      Start      ", font=("Arial", 30), fg="white",bg="light sea green", command=Get_name)
    instructions = tk.Button(root, text=" instructions ", font=("Arial", 30), fg="white", bg="light sea green", command=info)
    Load_game = tk.Button(root, text="Load Game", font=("Arial", 30), fg="white", bg="light sea green", command=load_game)
    Quit = tk.Button(root, text="      Quit      ", font=("Arial", 30 ), fg="white", bg="light sea green", command=root.quit)

    start.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    instructions.place(relx=0.5, rely=0.53, anchor=tk.CENTER)
    Load_game.place(relx=0.5, rely=0.66, anchor=tk.CENTER)
    Quit.place(relx=0.5, rely=0.79, anchor=tk.CENTER)

    root.mainloop()


def info():
    print('info button clicked')
    pygame.mixer.music.load('click.wav')
    pygame.mixer.music.play()
    game_instructions = """
        Bingo Game Instructions:

    1. Start the Game:
       - Click the "Start" button to initiate the Bingo game.
       - Enter your name when prompted.

    2. Game Options:
       - Choose to play against a friend or the computer.
       - If playing against a friend, enter your friend's name.
       - If playing against the computer, the game will start with default dimensions (5x5) unless you choose custom dimensions(should be between 5 to 12) .

    3. Game Setup:
       - Bingo cards for both players (User and Friend/Computer) will be generated with random numbers.
       - Each player has grid of unique numbers on their card.

    4. Gameplay:
       - Players take turns marking numbers on their cards.
       - Click on a number to mark it with an 'X'. The corresponding number on the opponent's card will also be marked.
       - The game alternates between the User and the Friend/Computer.

    5. Winning Patterns:
       - The goal is to complete a row, column, or diagonal on your Bingo card.
       - The game recognizes and displays the score based on the number of completed lines (B, BI, BIN, BING, BINGO).
       - The first player to achieve BINGO wins the game.

    6. Game Over:
       - The game ends when a player achieves BINGO.
       - A message will be displayed announcing the winner (You or Your Friend/Computer).

    7. Menu Options:
       - Click the "Menu" button to access additional options:
          - **Continue:** Resume the game.
          - **Restart:** Start a new game with the same players.
          - **Quit:** Exit the game.

    8. Load Game:
       - Click "Load Game" to check if a previous game is saved.

    9. Quit:
       - Click "Quit" to exit the game at any time.

    Enjoy playing Bingo with your friend or against the computer!
    """

    messagebox.showinfo("info", game_instructions)


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('game_voice.wav')
menu()
