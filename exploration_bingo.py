import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os

def start(root,choice,game_type,games,resources):

    # destroy the starter window
    root.destroy()

    # Pull JSON input from corresponding game JSON chosen
    with open(os.path.join(games, f"{choice}.json"), 'r') as f:
        data = json.load(f)
    
    # Load JSON input
    possible_challenges = data["challenges"]

    # Function to handle button click
    def on_button_click(i, j):
        # Update the clicked button to green and reveal text around it
        buttons[i][j].config(bg=data['button_color'], text=grid[i][j])
        
        # Reveal surrounding buttons if within bounds
        if i > 0:  # Top
            buttons[i-1][j].config(text=grid[i-1][j])
        if i < 4:  # Bottom
            buttons[i+1][j].config(text=grid[i+1][j])
        if j > 0:  # Left
            buttons[i][j-1].config(text=grid[i][j-1])
        if j < 4:  # Right
            buttons[i][j+1].config(text=grid[i][j+1])

    # Create main window
    root = tk.Tk()
    root.title("Exploration Bingo")


    # Grid size
    grid_size = 5

    # Create a 5x5 grid of buttons and randomly assign texts
    buttons = []
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]

    # Shuffle and assign the possible texts randomly to the grid
    random.shuffle(possible_challenges)
    index = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if i == 2 and j == 2:  # Center button
                grid[i][j] = "Begin Here"  # Change the center button text to "Begin Here"
            else:
                grid[i][j] = possible_challenges[index]  # Assign a random challenge for all other buttons
                index += 1

    # Set the button size and scaling factor (adjust if too big for your resolution)
    button_width = 14 
    button_height = 7

    # Configure grid to resize with window
    for i in range(grid_size):
        root.grid_rowconfigure(i, weight=1, uniform="equal")
        root.grid_columnconfigure(i, weight=1, uniform="equal")

    # Create header labels for "ROGUE" BINGO letters
    header_labels = ['R', 'O', 'G', 'U', 'E']
    for j in range(grid_size):
        label = tk.Label(root, text=header_labels[j], font=(data['font'], 120, "bold"))
        label.grid(row=0, column=j, sticky="nsew", padx=10, pady=5)

    # Load the image for the center button
    image = Image.open(os.path.join(resources, data['icon']))  # Grab the game's image file
    image = image.resize((100, 100), Image.NEAREST)  # Resize to fit button size
    photo = ImageTk.PhotoImage(image)

    # Create buttons and place them in the grid
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            if game_type == "Exploration":
            # Initialize the button with invisible text (empty string) for all except center
                button = tk.Button(root, text="", width=button_width, height=button_height,
                                   font=(data['font'], 12),  # Font size is kept at 12 (can be adjusted)
                                   command=lambda i=i, j=j: on_button_click(i, j),
                                   wraplength=100,  # Set wraplength to control the text wrapping
                                   justify="center", anchor="center")  # Center the text
            else:
                button = tk.Button(root, text=grid[i][j], width=button_width, height=button_height,
                                   font=(data['font'], 12),  # Font size is kept at 12 (can be adjusted)
                                   command=lambda i=i, j=j: on_button_click(i, j),
                                   wraplength=100,  # Set wraplength to control the text wrapping
                                   justify="center", anchor="center")  # Center the text
            button.grid(row=i+1, column=j, sticky="nsew")  # Place buttons below the header
            row.append(button)
        buttons.append(row)
    
    # Make the center button visible with the icon for the game
    buttons[2][2].config(image=photo, bg="lightgray")

    # Start the main loop
    root.mainloop()
    
def main():

    # Create window with game choices

    root = tk.Tk()
    root.title("Choose your game")
    root.geometry("500x360")

    # Set strings for starter box
    
    text_var = tk.StringVar()
    text_var2 = tk.StringVar()

    text_var.set("Welcome to Roguelike Exploration Bingo!\n")
    text_var2.set("Start by choosing your game in the drop down below and then begin the Bingo game. Choose your game type, Exploration or Regular Bingo.\n\nOnce it loads, you'll start by clicking the center icon. Once you complete an adjacent challenge, new challenges will appear.\nTry to get 5 in a row vertical, horizontal, or diagonal!\n\nIf you want to add new bingo boards for other games, you can add them to the games and resources folders found in the working directory of the script. Use the existing files as examples.\n")

    label = tk.Label(root, 
                     textvariable=text_var, 
                     anchor=tk.CENTER,       
                     font=("Arial", 12, 'underline'), 
                     justify=tk.CENTER,    
                     wraplength=450         
                    )
    label2 = tk.Label(root, 
                     textvariable=text_var2, 
                     anchor=tk.CENTER,       
                     font=("Arial", 12), 
                     justify=tk.CENTER,    
                     relief=tk.RAISED,                
                     wraplength=450         
                    )
    label.pack()
    label2.pack()
    
    # Get current working directory of the script
    current_directory = os.getcwd()
    games = os.path.join(current_directory, 'games')
    resources = os.path.join(current_directory, 'resources')

    # set the OptionsMenu button for game selection
    variable = tk.StringVar(root)
    options = []
    for f in  os.listdir(games):
        options.append(f.split('.json')[0])
    variable.set('Please choose a game') # set default value          
    w = tk.OptionMenu(root, variable, *options)
    w.pack()

    variable2 = tk.StringVar(root)
    options2 = ['Exploration', 'Regular']
    variable2.set(options2[0]) # set default value          
    w2 = tk.OptionMenu(root, variable2, *options2)
    w2.pack()

    # set button for Starting the Bingo Game
    
    button = tk.Button(root, text="Start Bingo Board", command=lambda: start(root,variable.get(),variable2.get(),games,resources))
    button.pack()
    root.mainloop()

    

if __name__ == "__main__":
    main()
