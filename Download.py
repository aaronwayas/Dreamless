import threading
import logging
import minecraft_launcher_lib as mclib
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import os
from validations import Cls_validations

class ClsDownload:
    
    def __init__(self):
        self.user_window = os.getlogin()
        self.minecraft_directory = f"C:/Users/{self.user_window}/AppData/Roaming/.minecraftLauncher"
        self.progressbar_visible = False

    def show_messagebox(self,title, message, icon, font_size=17):
            CTkMessagebox(
                title=title,
                message=message,
                icon=icon,  #  check, cancel, info, question, warning
                bg_color="#FFFFFF",
                text_color="#863bb4",
                font=("SplineSans Bold", font_size),
                fg_color="#FFFFFF",
                title_color="black",
                button_color="#801AE5",
                button_hover_color="#A95EFF",
            )

    def download_version(self,pantalla, tipo):
        if tipo == "vanilla" or tipo == "snapshot":
            download_vrs = versions_to_install.get()
            # Se establece el inicio del progressbar si hay algo que descargar
            if download_vrs:
                # Se cambia la visibilidad de la barra de progreso y se inicia
                self.progressbar_visible = True
                progressbar.place(
                    x=28.0,
                    y=263.0,
                )
                progressbar.start()
                try:
                    mclib.install.install_minecraft_version(download_vrs, self.minecraft_directory)
                    #logging.info("Downloaded successfully: %s", download_vrs)
                    self.show_messagebox("Success", "Downloaded successfully", "check")

                except Exception as e:
                    #logging.error("Error downloading version %s: %s", download_vrs, str(e))
                    self.show_messagebox("Error", "Error downloading version", "cancel")

                # Al finalizar la descarga, se detiene la barra de progreso y se oculta
                progressbar.stop()
                progressbar.place_forget()
                self.progressbar_visible = False
                self.actualizar_versiones(pantalla)
        else:
            download_vrs = versions_to_install.get()

            # Se establece el inicio del progressbar si hay algo que descargar
            if download_vrs:
                # Se cambia la visibilidad de la barra de progreso y se inicia
                self.progressbar_visible = True
                progressbar.place(
                    x=28.0,
                    y=263.0,
                )
                progressbar.start()

                try:
                    mclib.forge.install_forge_version(download_vrs, self.minecraft_directory)
                    #logging.info("Downloaded successfully: %s", download_vrs)
                    self.show_messagebox("Success", "Downloaded successfully", "check")

                except Exception as e:
                    #logging.error("Error downloading version %s: %s", download_vrs, str(e))
                    self.show_messagebox("Error", "Error downloading version", "cancel")

                # Al finalizar la descarga, se detiene la barra de progreso y se oculta
                progressbar.stop()
                progressbar.place_forget()
                self.progressbar_visible = False
                self.actualizar_versiones(pantalla)

    def thread_download(self,pantalla,tipo):
        thd_download = threading.Thread(target=self.download_version, args=(pantalla,tipo))
        thd_download.start()

    def saver_versiones_instaladas_forge(version):
        numero = str(version)[2:]
        ultima_terminacion = None
        ultima_version = None
        versiones_forge_instaladas = []
        for version_de_minecraft in mclib.forge.list_forge_versions():
            if int(numero) >= 10:
                if ultima_version != version_de_minecraft[0:6]:
                    if version_de_minecraft[2] == str(numero)[0] and ultima_terminacion != version_de_minecraft[5]:
                        if version_de_minecraft[3] == str(numero)[1]:
                            versiones_forge_instaladas.append(version_de_minecraft)
                            ultima_terminacion = version_de_minecraft[5]
                            ultima_version = version_de_minecraft[0:6]

            elif int(numero) >= 1 and version_de_minecraft[5] == '.' or version_de_minecraft[5] == '-':
                if ultima_version != version_de_minecraft[0:5]:
                    if version_de_minecraft[2] == str(numero):
                        versiones_forge_instaladas.append(version_de_minecraft)
                        ultima_terminacion = version_de_minecraft[4]
                        ultima_version = version_de_minecraft[0:5]

        return versiones_forge_instaladas

    def volver_a_llamar_download(self,tipo,pantalla_borrar):
        pantalla_borrar.destroy()
        self.Download(tipo)

    def ver_versiones_forge(self,pantalla,tipo,window,entry_version):

        global versions_to_install
        global progressbar
        global install_button
        if len(entry_version.get()) != 0:
            versions_to_install = ctk.CTkComboBox(
                window,
                values=self.saver_versiones_instaladas_forge(entry_version.get()),
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

            versions_to_install.place(x=28.0, y=290.0)
            
            install_button = ctk.CTkButton(
                window,
                command=lambda: self.thread_download(pantalla, tipo),
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
                y=350.0,
            )
            install_button.configure(state="disable")
        else:
            pass
 
    def Download(self,tipo):
        # Funcion para cambiar de descarga
        def cambiar_descarga(window,tipo_version,text,coord_y):
            cambiar_descarga = ctk.CTkButton(
                    window,
                    command=lambda: self.volver_a_llamar_download(tipo_version,window),
                    width=150.0,
                    text=text, # Forge, Vanilla, Snapshot
                    fg_color="#801AE5",
                    hover_color="#A95EFF",
                    bg_color="white",
                    corner_radius=12.0,
                    text_color="white",
                    font=("SplineSans", 22),
                    height=49.93934631347656,
                )

            cambiar_descarga.place(
                x=600.0,
                y=coord_y,
            )
       
        global versions_to_install
        global progressbar
        # Pantalla de Descarga
        window = ctk.CTk()
        pos_x = (window.winfo_screenwidth()//2)-(788//2)
        pos_y = (window.winfo_screenheight()//2)-(448//2)
        window.geometry("{}x{}+{}+{}".format(788,448,pos_x,pos_y))
        window.configure(bg="#FFFFFF")
        window.title(f"Dreamless - Download - {tipo}")
        window._set_appearance_mode("light")
        window.iconbitmap("assets/images/icon.ico")
        canvas = ctk.CTkCanvas(
            window,
            bg="#FFFFFF",
            height=700,
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

        canvas.create_text(
            28.0,
            97.0,
            anchor="nw",
            text="Select a version to install",
            fill="#140C1C",
            font=("SplineSans Medium", 24 * -1),
        )
        if tipo == 'vanilla':
            # Obtener las versiones disponibles
            available_versions = mclib.utils.get_available_versions(self.minecraft_directory)
            release_versions = [
                version["id"] for version in available_versions if version["type"] == "release"
            ]

            #botones para cambiar de descarga
            self.cambiar_descarga_vanilla_forge = cambiar_descarga(window,'forge','Forge',50.0)
            self.cambiar_descarga_vanilla_snapshot = cambiar_descarga(window,'snapshot','Snapshot',130.0)

        elif tipo == 'snapshot':
            # Reducir las snapshots a las mas nuevas de cada version
            available_versions = mclib.utils.get_available_versions(self.minecraft_directory)
            release_versions = []
            ultima_snapshot = None
            available_versions = mclib.utils.get_available_versions(self.minecraft_directory)
            for snapshots in available_versions:
                if snapshots['type'] == 'snapshot' and not ultima_snapshot == snapshots['id'][0:4]:
                    release_versions.append(snapshots["id"])
                    ultima_snapshot = snapshots['id'][0:4]
            
            #botones para cambiar de descarga
            self.cambiar_descarga_snapshot_vanilla = cambiar_descarga(window,'vanilla','Vanilla',50.0)
            self.cambiar_descarga_snapshot_forge = cambiar_descarga(window,'forge','Forge',130.0)
       
        elif tipo == 'forge':
            # botones para cambiar de descarga
            self.cambiar_descarga_forge_vanilla = cambiar_descarga(window,'vanilla','Vanilla',50.0)
            self.cambiar_descarga_forge_snapshot = cambiar_descarga(window,'snapshot','Snapshot',130.0)
            
        if tipo == 'snapshot' or tipo == 'vanilla':
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
                corner_radius=15
            )

            versions_to_install.place(x=28.0, y=140.0)

            install_button = ctk.CTkButton(
                window,
                command=lambda: self.thread_download(window, tipo),
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
        else:
            release_versions = []
            escoger_version = ctk.CTkEntry(
                window,
                bg_color="white",
                fg_color="#EDE8F2",
                text_color="#140C1C",
                width=508.0,
                height=45,
                font=("SplineSans Bold", 20),
                border_color="#EDE8F2",
                corner_radius=15
            )
            escoger_version.place(x=28.0, y=140.0)

            install_button = ctk.CTkButton(
                window,
                command=lambda: self.ver_versiones_forge(window,tipo,window,escoger_version),
                width=480.0,
                text="Search",
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

        
        global progressbar
        progressbar = ctk.CTkProgressBar(
            window,
            width=480.0,
            height=7,
            orientation='horizontal',
            corner_radius=20, 
            fg_color="#ede8f2",
            progress_color="#801AE5",
            bg_color="white",
            mode='indeterminate',
            determinate_speed=5,
            )

        progressbar.set(0)

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

    def actualizar_versiones(self,app):
        global versions 
        objValidatios = Cls_validations.minecraft_folder(self.minecraft_directory)

        if objValidatios == False:
            versions_installed = ["No versions installed"]
        else:
            versions_installed = [
                version["id"] for version in mclib.utils.get_installed_versions(self.minecraft_directory)
            ]

        versions = ctk.CTkComboBox(
        app,
        values=versions_installed,
        bg_color="white",
        fg_color="#EDE8F2",
        text_color="#140C1C",
        width=480.0,
        height=56,
        font=("SplineSans Bold", 20),
        border_color="#EDE8F2",
        button_color="#EDE8F2",
        dropdown_fg_color="#EDE8F2",
        dropdown_text_color="#140C1C",
        dropdown_hover_color="#EDE8F2",
        dropdown_font=("SplineSans Bold", 14),
        corner_radius=15,
        )

        versions.place(
            x=667.0,
            y=157.0,
        )

if __name__ == "__main__":
    downloader = ClsDownload()
    downloader.Download("vanilla")
