import customtkinter as ctk
from tkinter import Canvas
import json
from CTkMessagebox import CTkMessagebox


def read_json(user, ram):
    try:
        with open("config.json") as f_json:
            data = json.load(f_json)
        username = data.get("username", "")
        gbram = data.get("ram", "")
        if username and gbram:
            user.insert(0, str(username))
            ram.set(str(gbram))
    except FileNotFoundError:
        # Si el archivo no existe, se crea con valores predeterminados
        config_data = {"username": "", "ram": ""}
        with open("config.json", "w") as file:
            json.dump(config_data, file, indent=4)
    except Exception as e:
        print(f"Error reading configuration file: {e}")
   

def save_config():
    try:
        if not username_entry.get() or not ram_combo.get():
            CTkMessagebox(
                title="Error",
                message="Please fill in all fields",
                icon="cancel",
                bg_color="#FFFFFF",
                text_color="#863bb4",
                font=("SplineSans Bold", 17),
                fg_color="#FFFFFF",
                title_color="black",
                button_color="#801AE5",
                button_hover_color="#A95EFF",
            )
            return

        config_data = {"username": username_entry.get(), "ram": str(ram_combo.get())}
        with open("config.json", "w") as file:
            json.dump(config_data, file, indent=4)
        CTkMessagebox(
            title="Success",
            message="Settings saved successfully",
            icon="check",
            bg_color="#FFFFFF",
            text_color="#863bb4",
            font=("SplineSans Bold", 17),
            fg_color="#FFFFFF",
            title_color="black",
            button_color="#801AE5",
            button_hover_color="#A95EFF",
        )

    except Exception as e:
        print(f"Error writing to configuration file: {e}")


def Settings():
    global username_entry
    global ram_combo

    settings_window = ctk.CTk()
    pos_x = (settings_window.winfo_screenwidth()//2)-(788//2)
    pos_y = (settings_window.winfo_screenheight()//2)-(448//2)
    settings_window.geometry("{}x{}+{}+{}".format(788,448,pos_x,pos_y))
    settings_window.configure(bg="#FFFFFF")
    settings_window.title("Dreamless - Settings")
    settings_window._set_appearance_mode("light")
    settings_window.iconbitmap("assets/images/icon.ico")

    canvas = Canvas(
        settings_window,
        bg="#FFFFFF",
        height=900,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        28.0,
        14.0,
        anchor="nw",
        text="Dreamless",
        fill="#140C1C",
        font=("SplineSans Bold", 18 * -1),
    )
    canvas.create_rectangle(
        -1.0, 46.0, 456.02740478515625, 47.0, fill="#E5E8EB", outline=""
    )
    username_entry = ctk.CTkEntry(
        settings_window,
        placeholder_text="Enter your username",
        placeholder_text_color="#703ba6",
        font=("SplineSans", 14),
        width=300,
        height=40,
        fg_color="#f5f0fa",
        border_color="#d9c7eb",
        text_color="black",
        border_width=1,
        corner_radius=12,
        bg_color="#FFFFFF",
    )

    username_entry.place(relx=0.225, rely=0.3, anchor="center")

    ram_combo = ctk.CTkComboBox(
        settings_window,
        values=["2GB", "4GB", "6GB", "8GB"],
        font=("SplineSans", 14),
        width=300,
        height=40,
        fg_color="#f5f0fa",
        border_color="#d9c7eb",
        text_color="#703ba6",
        border_width=1,
        corner_radius=12,
        bg_color="#FFFFFF",
        dropdown_fg_color="#f5f0fa",
        dropdown_font=("SplineSans", 13),
        dropdown_text_color="#703ba6",
        button_color="#f5f0fa",
        button_hover_color="#d9c7eb",
        dropdown_hover_color="#d9c7eb",
    )

    ram_combo.place(relx=0.225, rely=0.4, anchor="center")

    canvas.create_text(
        28.0,
        77.0,
        anchor="nw",
        text="Settings",
        fill="#140C1C",
        font=("SplineSans Medium", 24 * -1),
    )
    save_button = ctk.CTkButton(
        settings_window,
        font=("SplineSans", 14, "bold"),
        text="Save",
        command=save_config,
        corner_radius=12,
        fg_color="#801AE5",
        text_color="#FAF7FC",
        bg_color="#FFFFFF",
        width=97.83000183105469,
        height=40.0,
        hover_color="#ac1cff",
    )
    save_button.place(x=660.0, y=391.0)

    close_button = ctk.CTkButton(
        settings_window,
        font=("SplineSans", 14, "bold"),
        text="Close",
        command=lambda: settings_window.destroy(),
        corner_radius=18,
        bg_color="#FFFFFF",
        fg_color="#EDE8F2",
        text_color="#140D1C",
        width=83.0,
        height=40.0,
        hover_color="#faf4ff",
    )
    close_button.place(
        x=555.0,
        y=391.0,
    )

    read_json(username_entry, ram_combo)

    settings_window.resizable(False, False)
    settings_window.mainloop()



if __name__ == "__main__":
    Settings()
  
