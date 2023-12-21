import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import *
import urllib3 
from io import BytesIO
from tkinter import *
from PIL import Image, ImageTk

#for pokemon, make a global list
#if the pokemon is already displayed, prevent it from displaying again

img_ref = None #this is to help with the image error
global_image_list = [] # making an empty global image list
shit = [] #dont like this

class dexEntry(Toplevel):

    def __init__(Pokemon, master = None):
            
        super().__init__(master = master)
        Pokemon.title("Pokedex Entry")
        Pokemon.geometry("512x364")
        Pokemon.resizable(width=False, height=False)
        
        # Create Window Canvas
        my_canvas = Canvas(Pokemon, width=512, height=364, bd=0, highlightthickness=0)
        my_canvas.pack(fill="both", expand=True)
        
        # Set Pokedex Entry background
        bg = PhotoImage(file="Pokedex Screen.png")
        image = Image.open("Pokedex Screen.png")
        resize_image = image.resize((512, 364))
        img = PIL.ImageTk.PhotoImage(resize_image)
        c = my_canvas.create_image(0, 0, image=img, anchor="nw")
        
        def add_image_to_gshit(image):
            global shit
            shit.append(image)

        add_image_to_gshit(img)
        
        #Pokemon Information
        pokemon_info = my_canvas.create_text(345, 60, text=f" ", font=("Rockwell", 12), fill= "black")
        pokemon_image = my_canvas.create_image(200,15)
        pokemon_types = my_canvas.create_text(315, 95, text=f" ", font=("Rockwell", 12), fill= "black")
        pokemon_height = my_canvas.create_text(340, 185, text=f" ", font=("Rockwell", 12), fill= "black")
        pokemon_weight = my_canvas.create_text(340, 215, text=f" ", font=("Rockwell", 12), fill= "black")
        pokemon_basestats = my_canvas.create_text(256, 300, text=f" ", font=("Rockwell", 15), fill= "black")

        def add_image_to_global_list(image):
            global global_image_list
            global_image_list.append(image)

        def load_pokemon(Pokemon_Entry):
            try: 
                pokemon = pypokedex.get(name=Pokemon_Entry.get())
                http = urllib3.PoolManager()
                response = http.request('GET', pokemon.sprites.front.get('default'))
                if response.status == 200:
                    image = PIL.Image.open(BytesIO(response.data))
                    resize_image = image.resize((300, 300))
                    img = PIL.ImageTk.PhotoImage(resize_image)
                    
                    # global img_ref1
                    # img_ref1 = img
                    add_image_to_global_list(img)

                    my_canvas.itemconfig(pokemon_image, image=img)
                    my_canvas.itemconfig(pokemon_info, text=f"{pokemon.dex} - {pokemon.name}".title())
                    my_canvas.itemconfig(pokemon_types, text=" - ".join([t for t in pokemon.types]).title())
                    my_canvas.itemconfig(pokemon_height, text=f"Height: {pokemon.height}0 cm")
                    my_canvas.itemconfig(pokemon_weight, text=f"Weight: {pokemon.weight}00 g")
                    my_canvas.itemconfig(pokemon_basestats, text=f"HP: {pokemon.base_stats.hp} - Attack: {pokemon.base_stats.attack} - Defense: {pokemon.base_stats.defense} - Special Attack: {pokemon.base_stats.sp_atk} - Special Defense: {pokemon.base_stats.sp_def} - Speed: {pokemon.base_stats.speed}")
                else: 
                    # Handle unsuccessful response
                    my_canvas.itemconfig(pokemon_info, text="Failed to fetch Sprite.")
                    print("Failed to fetch the image from the API")

            except pypokedex.exceptions.PyPokedexHTTPError as e: #this is the error message that this api returns if it didnt find the pokemon it was looking for
    
                error_message = "The requested Pokémon was not found!"
                my_canvas.itemconfig(pokemon_info, text=error_message, font=("Rockwell", 20), fill="red")
                print(e)

            except Exception as e: #if an error occurred and who on earth knows what it was, just tell the user an error occurred

                my_canvas.itemconfig(pokemon_info, text="An error occurred.", font=("Rockwell", 20), fill= "red")
                print(e)

        load_pokemon(Pokemon_Entry)
        
Home = tk.Tk()
Home.geometry("360x640")
Home.resizable(width=False, height=False)
Home.title("Python Pokedex")

# Create Main Window Canvas
my_canvas = Canvas(Home, width=360, height=640, bd=0, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)

# Set Pokedex background
bg = PhotoImage(file="Home.png")
image = Image.open("Home.png")
resize_image = image.resize((360, 640))
img = PIL.ImageTk.PhotoImage(resize_image)
c = my_canvas.create_image(0, 0, image=img, anchor="nw")

#Add Texts
title_text = my_canvas.create_text(180, 290, text="Python Pokedex", font=("Rockwell", 25), fill="black")
subtitle_text = my_canvas.create_text(180, 320, text="Created by JCPandaz", font=("Rockwell", 12), fill="red")
my_canvas.create_text(180, 420, text="Enter Name or Pokedex #", font=("Rockwell", 18), fill= "black")
#Add Entry box
Pokemon_Entry = Entry(Home, font=("Rockwell", 24), width=15, fg="black", bd=2)
Pokemon_window=my_canvas.create_window(180,460, window=Pokemon_Entry)
#Add Button
#Load_Button = Button(Home, text= "LOAD POKEMON", font=("Rockwell", 20), width = 18, command=NewWindow(Pokemon_Entry))
#load_btn_window = my_canvas.create_window(180,578, window=Load_Button)
btn = Button(Home, text= "LOAD POKEMON", font=("Rockwell", 20), width = 18, command = dexEntry)
load_btn_window = my_canvas.create_window(180,578, window=btn)
#btn.bind("<Button>", lambda e: NewWindow(Home))


Home.mainloop()
