import minecraft_launcher_lib as mclib
from tkinter import PhotoImage
import customtkinter as ctk
import SettingsMc
import subprocess
import webbrowser
import Download
import json
import os
# se importa la clase de las validaciones 
from validations import Cls_validations
from Download import ClsDownload


app = ctk.CTk()
# Obtener longitudes de la pantalla 
scr_width = app.winfo_screenwidth()-150
scr_height = app.winfo_screenheight()-120

#se obtienen las posiciones X y Y
pos_x = (app.winfo_screenwidth()//2)-(scr_width//2)
pos_y = (app.winfo_screenheight()//2)-(scr_height//2)


# Se le resta -150 al ancho que tenga la pantalla y -120 al alto para centrar 
# app.geometry("{}x{}+{}+{}".format(scr_width-150,scr_height-120,pos_x,pos_y))
app.geometry("{}x{}+{}+{}".format(scr_width,scr_height,pos_x,pos_y))

app.title("Dreamless")
app._set_appearance_mode("light")
app.config(bg="#FFFFFF")
app.iconbitmap("assets/images/icon.ico")


# Functions

usr_window = os.getlogin()    
minecraft_directory = f"C:/Users/{usr_window}/AppData/Roaming/.minecraftLauncher"
# se crea un objeto de la clase que valida la existencia de la carpeta
objValidatios = Cls_validations.minecraft_folder(minecraft_directory)

if objValidatios == False:
    versions_installed = ["No versions installed"]
else:
    versions_installed = [
        version["id"] for version in mclib.utils.get_installed_versions(minecraft_directory)
    ]

def read_config_file(filename):
    try:
        with open(filename, "r") as file:
            config_data = json.load(file)
            return config_data.get("username"), config_data.get("ram")
    except Exception as e:
        print(f"Error reading config file: {e}")
        return None, None


def run_minecraft():
    try:
        mine_user, ram = read_config_file("config.json")
        if not mine_user or not ram:
            print("Error: Missing username or ram in config file.")
            return

        version = Download.versions.get()

        options = {
            "username": mine_user,
            "uuid": "",
            "token": "",
            "launcherVersion": "0.0.2",
        }
        options["jvmArguments"] = [f"-Xmx{ram}G", f"-Xms{ram}G"]
        minecraft_command = mclib.command.get_minecraft_command(
            version, minecraft_directory, options
        )
        subprocess.run(minecraft_command)
    except Exception as e:
        print(f"Error running Minecraft: {e}")


# Canvas

canvas = ctk.CTkCanvas(
    app,
    bg="#FFFFFF",
    height=900,
    width=2280,
)

canvas.place(x=-2, y=-2)

# Buttons and Canvas

download_label = ctk.CTkLabel(
    app,
    text="Download",
    text_color="black",
    bg_color="#FFFFFF",
    font=("SplineSans", 17, "bold"),
    cursor="hand2",
)

download_label.place(relx=0.55, rely=0.063, anchor="center")

download_label.bind("<Button-1>", lambda event: Download.Download(app,'forge'))

settings_label = ctk.CTkLabel(
    app,
    text="Settings",
    text_color="black",
    bg_color="#FFFFFF",
    font=("SplineSans", 17, "bold"),
    cursor="hand2",
)

settings_label.place(relx=0.65, rely=0.063, anchor="center")
settings_label.bind("<Button-1>", lambda event: SettingsMc.Settings())

buy_minecraft_label = ctk.CTkLabel(
    app,
    text="Buy Minecraft",
    text_color="black",
    bg_color="#FFFFFF",
    font=("SplineSans", 12, "bold"),
    cursor="hand2",
)

buy_minecraft_label.place(
    x=667.0,
    y=285.0,
)
buy_minecraft_label.bind("<Button-1>", lambda event: webbrowser.open("https://www.minecraft.net/es-es/store/minecraft-java-bedrock-edition-pc"))

feedback = ctk.CTkButton(
    app,
    font=("SplineSans", 14),
    text="Feedback",
    command=lambda: webbrowser.open("https://github.com/aaronwayas/Dreamless"),
    corner_radius=12,
    fg_color="#801AE5",
    bg_color="white",
    text_color="white",
    width=97.83000183105469,
    height=40.0,
    hover_color="#9d1cff",
)
feedback.place(
    x=955.0,
    y=31.0,
)

help_button = ctk.CTkButton(
    app,
    command=lambda: webbrowser.open("https://discord.gg/tarfQNevpf"),
    width=20.0,
    height=40.0,
    text="Help",
    text_color="black",
    font=("SplineSans", 14, "bold"),
    corner_radius=20,
    fg_color="#EDE8F2",
    bg_color="white",
    hover_color="#faf4ff",
)
help_button.place(
    x=1067.0,
    y=31.0,
)

play_button = ctk.CTkButton(
    app,
    command=run_minecraft,
    width=480.0,
    height=54.5999755859375,
    text="Play",
    text_color="white",
    bg_color="white",
    fg_color="#801AE5",
    corner_radius=12,
    font=("SplineSans", 24, "bold"),
    hover_color="#9d1cff",
)
play_button.place(
    x=667.0,
    y=235.0,
)

Download.actualizar_versiones(app)

image_image_1 = PhotoImage(file="assets/images/image_1.png")
image_1 = canvas.create_image(331.0, 367.0, image=image_image_1)

canvas.create_text(
    240.0,
    384.0,
    anchor="nw",
    text="Play Minecraft totally free",
    fill="#FFFFFF",
    font=("SplineSans Medium", 14 * -1, "bold"),
)

canvas.create_text(
    156.0,
    300.0,
    anchor="nw",
    text="Welcome to Minecraft",
    fill="#FFFFFF",
    font=("SplineSans Bold", 36 * -1, "bold"),
)

canvas.create_text(
    142.0,
    40.0,
    anchor="nw",
    text="Dreamless",
    fill="#140C1C",
    font=("SplineSans Bold", 19 * -1, "bold"),
)

canvas.create_rectangle(87.0, 70.0, 544.0274047851562, 71.0, fill="#E5E8EB", outline="")

canvas.create_text(
    670.0,
    127.0,
    anchor="nw",
    text="Version",
    fill="#140C1C",
    font=("SplineSans Medium", 16 * -1),
)


app.resizable(False, False)
app.mainloop()
