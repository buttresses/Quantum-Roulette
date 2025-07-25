import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageSequenc


class LoadingScreen(tk.Toplevel):
    def __init__(self, master=None, gif_path="loading.gif", duration=500, on_done=None):
        super().__init__(master)
        self.title("Loading...")
        self.geometry("400x300")
        self.configure(bg="black")
        self.attributes("-alpha", 0.5)
        self.on_done = on_done

        self.frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA"))
                       for frame in ImageSequence.Iterator(Image.open(gif_path))]

        self.label = tk.Label(self, bg="black")
        self.label.pack(expand=True)

        self.frame_index = 0
        self.animate()
        self.after(duration, self.finish)

    def animate(self):
        frame = self.frames[self.frame_index]
        self.label.config(image=frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.animate)

    def finish(self):
        self.destroy()
        if self.on_done:
            self.on_done()


# Qiskit quantum random number generator
#QISKIT CODE (This is Charmaine's)

#Quantum teleportation algorithm

from qiskit import QuantumCircuit
from qiskit import ClassicalRegister, QuantumRegister
import random
import numpy as np
from numpy import pi


#Entangle two qubits, create bell state using hadamard and CNOT
q1 = QuantumRegister(1, "Q")
q2 = QuantumRegister(1, "A") #Alice needs 2 qubits
q3 = QuantumRegister(1, "B") #Bob needs 1 qubit that is entangled

cr = ClassicalRegister(3, 'c')
qc = QuantumCircuit(q1,q2,q3,cr)


#Entangle q2 and q3 qubits above using a hadamard and CNOT gate (to create the first bell state)
qc.h(q2)
qc.cx(q2, q3)

#Generate a random state using q1 by rotating the vector on the Bloch sphere (u rotation gate)
np.random.seed(42) #fixing seed for repeatibility
theta = np.random.uniform(0.0, 1.0) * np.pi    #from 0 to pi
varphi = np.random.uniform(0.0, 2.0) * np.pi    #from 0 to 2*pi

#If you don't want it to be random use this code:
#theta = input("Choose a theta")
#varphi = input("Choose varphi")

#qc.u(theta, varphi, 0.0, q1)


#Entangle this with alice qubits
qc.cx(q1, q2)
qc.h(q1)


#Measure the qubits
qc.measure(q2, cr[1])
qc.measure(q1, cr[0])

#Conditional logic
with qc.if_test((cr[1], 1)):
    qc.x(q2)
with qc.if_test((cr[0], 1)):
    qc.z(q2)

#print(qc)

"""Quantum random number generator"""

# Qiskit quantum random number generator
def quantum_random_number(num_bits=6):
    """Generate a quantum random number between 1 and 38 for roulette"""
    try:
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector
        
        random_decimal = 39
        while random_decimal < 1 or random_decimal > 38:
            qc = QuantumCircuit(num_bits)
            for i in range(num_bits):
                qc.h(i)
            # Get the statevector (superposition)
            state = Statevector.from_instruction(qc)
            # Get probabilities for all basis states
            probs = state.probabilities_dict()
            # Randomly sample one bitstring based on quantum probabilities
            bitstrings = list(probs.keys())
            chosen = random.choices(bitstrings, weights=probs.values())[0]
            random_decimal = int(chosen, 2)
            return random_decimal



def get_roulette_color(number):
    """Determine the color based on roulette number"""
    if number in (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36):
        return "Red"
    elif number in (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35):
        return "Black"
    else:  # 0 (37) and 00 (38)
        return "Green"


def on_start():
    global roulette_final_color, roulette_number, player_money, player_bet_choice
    
    # CAPTURE THE BET CHOICE HERE before anything else
    player_bet_choice = bet_color_choice.get()
    
    # Get quantum random number
    roulette_number = quantum_random_number(6)
    roulette_final_color = get_roulette_color(roulette_number)
    
    # Validate betting amount
    bet = betting_amount_var.get()
    try:
        bet_int = int(bet)
        if bet_int <= 0:
            raise ValueError
    except ValueError:
        if hasattr(root, 'children'):
            result_label.config(text="Please enter a valid positive integer for betting amount.", fg="red")
        return

    # Set initial player money if this is the first game
    if player_money == 0:
        player_money = bet_int
    
    LoadingScreen(root, "loading.gif", duration=1500, on_done=open_display_screen)


def open_display_screen():
    # Set the betting amount right before opening display screen
    global next_bet_amount
    if next_bet_amount:
        betting_amount_var.set(next_bet_amount)
        next_bet_amount = ""  # Clear it after use
    DisplayScreen(root)


class DisplayScreen(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Result Screen")
        self.geometry("600x450")
        self.configure(bg="#ffffff")

        # Show what the player actually bet (not editable radio buttons)
        color_label = tk.Label(self, text="Your bet was:", font=("Arial", 16), bg="#ffffff")
        color_label.pack()
        
        # Show the actual bet choice (no radio buttons needed here)
        bet_display = tk.Label(self, text=player_bet_choice, font=("Arial", 16, "bold"), 
                              fg=player_bet_choice.lower() if player_bet_choice != "Green" else "green", 
                              bg="#ffffff")
        bet_display.pack(pady=(5, 15))

        #Determine if you won or not
        bet_str = betting_amount_var.get()
        
        try:
            bet_amount = int(bet_str)
            if bet_amount <= 0:
                raise ValueError
        except ValueError:
            # If betting amount is invalid, close this window and return to main
            self.destroy()
            return
            
        global player_money
        
        # USE THE STORED BET CHOICE, NOT THE RADIO BUTTONS
        if roulette_final_color == player_bet_choice:
            displayedToUser="WON!"
            result_color = "green"
            player_won = True
            if player_bet_choice == "Green":
                winnings = bet_amount * 35
            else:
                winnings = bet_amount * 2
            player_money = player_money - bet_amount + winnings  # Subtract bet, add winnings
        else:
            displayedToUser = "lost ):"
            result_color = "red"
            player_won = False
            player_money = player_money - bet_amount  # Just subtract the bet amount

        # Show the actual roulette result
        roulette_result_label = tk.Label(self, text=f"Roulette landed on: {roulette_number} ({roulette_final_color})", 
                                        font=("Arial", 14), bg="#ffffff", 
                                        fg=roulette_final_color.lower() if roulette_final_color != "Green" else "green")
        roulette_result_label.pack(pady=10)

        # Top result label
        result_label = tk.Label(self, text=(("You have " + displayedToUser)), font=("Arial", 32, "bold"), bg="#ffffff", fg=result_color)
        result_label.pack(pady=(30, 20))
        
        # Frame for input and "Remaining:" label
        input_frame = tk.Frame(self, bg="#ffffff")
        input_frame.pack(pady=10)

        # Input label and entry
        input_label = tk.Label(input_frame, text="Input your bet amount", font=("Arial", 16), bg="#ffffff")
        input_label.grid(row=0, column=0, sticky="w", padx=10)

        self.input_var = tk.StringVar()
        input_entry = tk.Entry(input_frame, textvariable=self.input_var, font=("Arial", 16),
                               bg="#f0f0f0", highlightthickness=2, highlightbackground="#999999", relief="flat",
                               width=15, justify="center")
        input_entry.grid(row=1, column=0, padx=10, pady=5)

        # "Remaining:" label
        self.remaining_label = tk.Label(input_frame, text=f"Remaining: ${player_money}", font=("Helvetica", 14),
                                        bg="#ffffff", anchor="w", width=20)
        self.remaining_label.grid(row=1, column=1, padx=10)

        # Bottom buttons
        button_frame = tk.Frame(self, bg="#ffffff")
        button_frame.pack(fill="x", side="bottom", pady=20, padx=20)

        return_button = tk.Button(button_frame, text="Return", font=("Arial", 14), bg="gray", fg="white",
                                  command=self.close)
        return_button.pack(side="right", padx=10)

        # Only show play again button if player won
        if player_won:
            play_again_button = tk.Button(button_frame, text="Play Again!", font=("Arial", 14), bg="green", fg="white",
                                          command=self.play_again)
            play_again_button.pack(side="right", padx=10)

    def close(self):
        self.destroy()

    def play_again(self):
        # Update betting amount with new input if provided
        new_bet = self.input_var.get().strip()
        
        if new_bet:
            try:
                new_bet_int = int(new_bet)
                if new_bet_int > 0:
                    # Store the bet amount before destroying the window
                    global next_bet_amount
                    next_bet_amount = new_bet
                else:
                    return
            except ValueError:
                return
        else:
            # If no new bet entered, use current betting amount
            current_bet = betting_amount_var.get()
            if current_bet:
                next_bet_amount = current_bet
            else:
                return
        
        self.destroy()
        
        # Start new game - the betting amount will be set in open_display_screen
        LoadingScreen(root, "loading.gif", duration=500, on_done=open_display_screen)
        betting_amount_var.set("")


# Global variables
roulette_final_color = ""
roulette_number = 0
player_money = 0  # Track player's total money
next_bet_amount = ""  # Store next bet amount
player_bet_choice = ""  # Store the actual bet choice

# Main window
root = tk.Tk()
root.title("Quantum Roulette")
root.geometry("600x500")
root.configure(bg="#d3d3d3")
root.iconbitmap("icon.ico")


# Initialize variables after root is created
bet_color_choice = tk.StringVar(value="Red")
betting_amount_var = tk.StringVar()

# Title
title_label = tk.Label(root, text="Welcome to Quantum Roulette!", font=("Arial", 24, "bold"), bg="#d3d3d3")
title_label.pack(pady=20)

# Logo
image = PhotoImage(file="logo.png")
image = image.subsample(2, 2)
label = tk.Label(root, image=image, bg="#d3d3d3")
label.pack()

# Explanation
explain_label = tk.Label(root, text="Determines the roulette result using true randomness and fairness!",
                        font=("Times New Roman", 15), bg="#d3d3d3")
explain_label.pack(pady=5)

# Betting amount input
bet_label = tk.Label(root, text="Initial betting amount", font=("Arial", 14), bg="#d3d3d3")
bet_label.pack(pady=(20, 0))
bet_entry = tk.Entry(root, textvariable=betting_amount_var, font=("Arial", 14), justify="center")
bet_entry.pack(pady=(5, 10))

# Color selection
color_select_label = tk.Label(root, text="Select your bet:", font=("Arial", 14), bg="#d3d3d3")
color_select_label.pack()

color_radio_frame = tk.Frame(root, bg="#d3d3d3")
color_radio_frame.pack(pady=(0, 20))

tk.Radiobutton(color_radio_frame, text="Red", variable=bet_color_choice, value="Red", font=("Arial", 12), fg="red", bg="#d3d3d3").pack(side="left", padx=10)
tk.Radiobutton(color_radio_frame, text="Black", variable=bet_color_choice, value="Black", font=("Arial", 12), fg="black", bg="#d3d3d3").pack(side="left", padx=10)
tk.Radiobutton(color_radio_frame, text="0 / 00", variable=bet_color_choice, value="Green", font=("Arial", 12), fg="green", bg="#d3d3d3").pack(side="left", padx=10)

# Result display area
result_label = tk.Label(root, text="", font=("Arial", 12), bg="#d3d3d3")
result_label.pack(pady=5)

start_button = tk.Button(root, text="Start", font=("Arial", 21), bg="green", fg="white", command=on_start)
start_button.place(x=200, y=430, width=200, height=35)  # adjust x/y if needed


# Remove the instructions at bottom
if __name__ == "__main__":
    root.mainloop()
#Non-Qiskit stuff coded by Laith Al-Wir (: + Claude AI (Saved me fr). Qiskit coded by Charmaine
#Idk who'd be reading this, maybe someone in my group Charmaine, Vish, or Turki; maybe a professor; maybe a TA. Maybe a future student. Who
