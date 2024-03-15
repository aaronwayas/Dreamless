import minecraft_launcher_lib as mclib
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import logging
import os


logging.basicConfig(filename="error.log", level=logging.ERROR)

usr_window = os.getlogin()
minecraft_directory = f"C:/Users/{usr_window}/AppData/Roaming/.minecraftLauncher"  # Directorio de Minecraft


def list_install_versions():
    list1 = mclib.utils.get_available_versions(minecraft_directory)
    release_versions = [
        version["id"] for version in list1 if version["type"] == "release"
    ]
    for version in release_versions:
        print(version)


def download_version():
    download_vrs = versions_to_install.get()

    if download_vrs:
        try:
            mclib.install.install_minecraft_version(download_vrs, minecraft_directory)
            logging.info("Downloaded successfully: %s", download_vrs)
            CTkMessagebox(
                title="Success", message="Downloaded successfully", icon="check"
            )
        except Exception as e:
            logging.error("Error downloading version %s: %s", download_vrs, str(e))
            CTkMessagebox(
                title="Error",
                message="Something went wrong!!!, show the log",
                icon="cancel",
            )
    else:
        logging.error("No version provided")
        CTkMessagebox(title="Error", message="No version provided", icon="cancel")


def Download():
    global versions_to_install

    window = ctk.CTk()
    window.geometry("788x448")
    window.configure(bg="#FFFFFF")
    window.title("Dreamless - Download")
    window._set_appearance_mode("light")
    window.iconbitmap("assets/images/icon.ico")
    canvas = ctk.CTkCanvas(
        window,
        bg="#FFFFFF",
        height=448,
        width=788,
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

    canvas.create_text(
        28.0,
        97.0,
        anchor="nw",
        text="Select a version to install",
        fill="#140C1C",
        font=("SplineSans Medium", 24 * -1),
    )

    # Obtener las versiones disponibles
    available_versions = mclib.utils.get_available_versions(minecraft_directory)
    release_versions = [
        version["id"] for version in available_versions if version["type"] == "release"
    ]

    versions_to_install = ctk.CTkComboBox(
        window,
        values=release_versions,
        bg_color="white",
        fg_color="#EDE8F2",
        text_color="#140C1C",
        width=508.0,
        height=45,
        font=("SplineSans Bold", 20),
        border_color="#EDE8F2",
        button_color="#EDE8F2",
        dropdown_fg_color="#EDE8F2",
        dropdown_text_color="#140C1C",
        dropdown_hover_color="#EDE8F2",
        dropdown_font=("SplineSans Bold", 14),
        corner_radius=15,
    )

    versions_to_install.place(x=28.0, y=140.0)

    install_button = ctk.CTkButton(
        window,
        command=download_version,
        width=480.0,
        text="Download",
        fg_color="#801AE5",
        hover_color="#A95EFF",
        bg_color="white",
        corner_radius=12.0,
        text_color="white",
        font=("SplineSans", 22),
        height=49.93934631347656,
    )
    install_button.place(
        x=28.0,
        y=206.0,
    )

    close_button = ctk.CTkButton(
        window,
        command=window.destroy,
        width=83.0,
        height=40.0,
        text="Close",
        text_color="black",
        fg_color="#EDE8F2",
        hover_color="#faf4ff",
        bg_color="white",
        corner_radius=18.0,
        font=("SplineSans", 14, "bold"),
    )
    close_button.place(
        x=660.0,
        y=391.0,
    )
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    # Si es así, llama a la función Download()
    Download()
