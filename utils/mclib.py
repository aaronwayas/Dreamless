import minecraft_launcher_lib as mclib
import os
import subprocess
import json


usr_window = os.getlogin()
minecraft_directory = f"C:/Users/{usr_window}/AppData/Roaming/.minecraftLauncher"


# obtener las versiones instaladas
def get_installed_versions(minecraft_directory: str, inverted: bool = False):
    versions_installed = [
        version["id"]
        for version in mclib.utils.get_installed_versions(minecraft_directory)
    ]

    def key_func(version):
        # Verificar si la versión contiene letras
        if any(char.isalpha() for char in version):
            # Extraer los primeros dígitos numéricos de la versión
            num_digits = next(
                (i for i, char in enumerate(version) if not char.isdigit()), None
            )
            if num_digits is not None:
                version = version[:num_digits]

        return tuple(map(int, version.split(".")))

    # Regresa las versiones ordenadas, de menor a mayor
    return sorted(versions_installed, key=key_func, reverse=inverted)


# obtener la configuracion
def get_config(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            config_data = json.load(file)
            return config_data.get("username"), config_data.get("ram")
    except Exception as e:
        print(f"Error reading config file: {e}")
        return None, None


# ejecutar minecraft
def run_minecraft(username: str, ram: str, version: str):
    if not username or not ram:
        print("Error: Missing username or ram in config file.")
        return False

    version = version

    options = {
        "username": username,
        "uuid": "",
        "token": "",
        "launcherVersion": "0.0.2",
    }
    options["jvmArguments"] = [f"-Xmx{ram}G", f"-Xms{ram}G"]
    minecraft_command = mclib.command.get_minecraft_command(
        version, minecraft_directory, options
    )
    subprocess.run(minecraft_command)


# escribir la configuracion
def write_config(file: str, username: str, ram: str):
    try:
        with open(file, "w") as file:
            json.dump({"username": username, "ram": ram}, file)

    except Exception as e:
        print(f"Error writing config file: {e}")


# obtener todas las versiones vanilla
def get_all_versions():
    return mclib.utils.get_version_list()


# descargar la version vanilla
def download_version(version: str, callback=None):
    try:
        mclib.install.install_minecraft_version(version, minecraft_directory, callback)
        print(f"Downloaded version: {version}")
        return True
    except Exception as e:
        print(f"Error downloading version: {e}")
        return False


def get_forge_version(version: str):
    return mclib.forge.find_forge_version(version)


def download_forge_version(version: str, callback=None):
    try:
        mclib.forge.install_forge_version(version, minecraft_directory, callback)
        print(f"Downloaded version: {version}")
        return True
    except Exception as e:
        print(f"Error downloading forge version: {e}")
        return False
