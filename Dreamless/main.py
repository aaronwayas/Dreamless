import minecraft_launcher_lib
import os
from colorama import init, Fore
import subprocess

file_path = 'configuration.txt'
information = []

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

if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            information.append(line)
else:
    with open(file_path, 'w') as file:
        file.write(' ')

user_window = os.environ["USERNAME"]
user_pc = os.getlogin()
minecraft_directory = f"C:/Users/{user_window}/AppData/Roaming/.minecraft"

def list_installed_versions():
    versions_path = os.path.join(minecraft_directory, 'versions')
    
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



def run_minecraft():
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

    with open(file_path, 'w') as file:
        file.writelines(mine_user)
        file.writelines(str(ram))

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
    subprocess.run(minecraft_command)

def install_normal_versions():
    version = input("Enter the Minecraft version to install: ")
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)
        print(f'Installed version {version}')
    else:
        print('No version entered')

def menu():
    while True:
        os.system('cls')
        print(title_dreamless)
        print(menu_options)
        choice = input(f"{Fore.CYAN}{user_pc}{Fore.RESET} >> ")

        if choice == "1":
            run_minecraft()
        elif choice == "2":
            install_normal_versions()
        elif choice == "3":
            list_installed_versions()
            input("Press Enter to continue...")
        elif choice == "4":
            break
        else:
            print("Invalid option. Please select a valid option.")

menu()
