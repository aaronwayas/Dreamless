import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    title_dreamless = """
        ·▄▄▄▄  ▄▄▄  ▄▄▄ . ▄▄▄· • ▌ ▄ ·. ▄▄▌  ▄▄▄ ..▄▄ · .▄▄ · 
        ██▪ ██ ▀▄ █·▀▄.▀·▐█ ▀█ ·██ ▐███▪██•  ▀▄.▀·▐█ ▀. ▐█ ▀. 
        ▐█· ▐█▌▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ▐█ ▌▐▌▐█·██▪  ▐▀▀▪▄▄▀▀▀█▄▄▀▀▀█▄
        ██. ██ ▐█•█▌▐█▄▄▌▐█ ▪▐▌██ ██▌▐█▌▐█▌▐▌▐█▄▄▌▐█▄▪▐█▐█▄▪▐█
        ▀▀▀▀▀• .▀  ▀ ▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀.▀▀▀  ▀▀▀  ▀▀▀▀  ▀▀▀▀ 
                                                    by: Aaron
    """
    print(title_dreamless)

def download_dreamless():
    print("Do you want to download Dreamless?")
    print("Press 1 for yes, and 2 for no")

    while True:
        choice = input(">> ")

        if choice == "1":
            clear_screen()
            print_title()
            print("Now downloading...")
            time.sleep(0.5)

            try:
                os.system('pip install minecraft_launcher_lib')
                os.system('pip install colorama')
                print("\nPress enter to execute Dreamless.")
                input()
                os.system('python Dreamless/main.py')
            except Exception as e:
                print(f"An error occurred: {e}")

            break

        elif choice == "2":
            clear_screen()
            print_title()
            print("Ok, bye.")
            time.sleep(1)
            break

        else:
            print("Invalid option. Please select a valid option.")

if __name__ == "__main__":
    clear_screen()
    print_title()
    download_dreamless()
