import os
import subprocess
from colorama import init, Fore
import minecraft_launcher_lib

class MinecraftManager:
    title_dreamless = Fore.RED + """
        ·▄▄▄▄  ▄▄▄  ▄▄▄ . ▄▄▄· • ▌ ▄ ·. ▄▄▌  ▄▄▄ ..▄▄ · .▄▄ · 
        ██▪ ██ ▀▄ █·▀▄.▀·▐█ ▀█ ·██ ▐███▪██•  ▀▄.▀·▐█ ▀. ▐█ ▀. 
        ▐█· ▐█▌▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ▐█ ▌▐▌▐█·██▪  ▐▀▀▪▄▄▀▀▀█▄▄▀▀▀█▄
        ██. ██ ▐█•█▌▐█▄▄▌▐█ ▪▐▌██ ██▌▐█▌▐█▌▐▌▐█▄▄▌▐█▄▪▐█▐█▄▪▐█
        ▀▀▀▀▀• .▀  ▀ ▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀.▀▀▀  ▀▀▀  ▀▀▀▀  ▀▀▀▀ 
                                                by: Aaron v.0.1
    """ + Fore.RESET

    menu_options = """
    1. Run Minecraft
    2. Install Minecraft
    3. List Installed Versions
    4. Exit
    """
    def __init__(self):
        self.file_path = 'configuration.txt'
        self.information = []
        self.current_max = 0
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()


    def read_configuration(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    self.information = [line.strip() for line in file]
        except Exception as e:
            print(f"Error reading configuration file: {e}")

    def write_configuration(self, username, ram):
        try:
            with open(self.file_path, 'w') as file:
                file.write(username + '\n')
                file.write(str(ram) + '\n')
        except Exception as e:
            print(f"Error writing to configuration file: {e}")

    def set_status(self, status):
        print(status)

    def set_progress(self, progress):
        if self.current_max != 0:
            print(f"{progress}/{self.current_max}")

    def set_max(self, new_max):
        self.current_max = new_max

    def list_installed_versions(self):
        try:
            versions_path = os.path.join(self.minecraft_directory, 'versions')
            if os.path.exists(versions_path):
                installed_versions = [version for version in os.listdir(versions_path) if os.path.isdir(os.path.join(versions_path, version))]
                if installed_versions:
                    print("Installed Minecraft Versions:")
                    for version in installed_versions:
                        print(f" - {version}")
                else:
                    print("No Minecraft versions installed.")
            else:
                print("Minecraft versions directory not found.")
        except Exception as e:
            print(f"Error listing installed versions: {e}")

    def run_minecraft(self):
        try:
            mine_user = input("Enter your Minecraft username: ")
            version = input("Enter the Minecraft version to run: ")
            ram = f"-Xmx{input('Enter the amount of RAM in GB (e.g., 4):')}G"

            options = {
                'username': mine_user,
                'uuid': '',
                'token': '',
                'jvArguments': [ram, ram],
                'launcherVersion': "0.0.2"
            }

            self.write_configuration(mine_user, ram)
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, self.minecraft_directory, options)
            subprocess.run(minecraft_command)
        except Exception as e:
            print(f"Error running Minecraft: {e}")

    def install_version(self):
        try:
            versionMC = input("Enter the Minecraft version to install: ")
            if versionMC:
                minecraft_launcher_lib.install.install_minecraft_version(versionMC, self.minecraft_directory, callback=self.callback)
                print(f'Installed version {versionMC}')
            else:
                print('No version entered')
        except Exception as e:
            print(f"Error installing Minecraft version: {e}")

    def Dreamless(self):
        try:
            user_pc = os.getlogin()

            while True:
                print(self.title_dreamless)
                print(self.menu_options)

                option = input(f"{Fore.CYAN}{user_pc}{Fore.RESET} >> ")
                if option == "1":
                    self.run_minecraft()
                elif option == "2":
                    self.install_version()
                elif option == "3":
                    self.list_installed_versions()
                    input("Press Enter to continue...")
                elif option == "4":
                    break
                else:
                    print("Invalid option. Please select a valid option.")
        except Exception as e:
            print(f"Error in Dreamless: {e}")

if __name__ == "__main__":
    minecraft_manager = MinecraftManager()
    minecraft_manager.read_configuration()
    minecraft_manager.Dreamless()
