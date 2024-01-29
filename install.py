import os, time

title_dreamless = """
    ·▄▄▄▄  ▄▄▄  ▄▄▄ . ▄▄▄· • ▌ ▄ ·. ▄▄▌  ▄▄▄ ..▄▄ · .▄▄ · 
    ██▪ ██ ▀▄ █·▀▄.▀·▐█ ▀█ ·██ ▐███▪██•  ▀▄.▀·▐█ ▀. ▐█ ▀. 
    ▐█· ▐█▌▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ▐█ ▌▐▌▐█·██▪  ▐▀▀▪▄▄▀▀▀█▄▄▀▀▀█▄
    ██. ██ ▐█•█▌▐█▄▄▌▐█ ▪▐▌██ ██▌▐█▌▐█▌▐▌▐█▄▄▌▐█▄▪▐█▐█▄▪▐█
    ▀▀▀▀▀• .▀  ▀ ▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀.▀▀▀  ▀▀▀  ▀▀▀▀  ▀▀▀▀ 
                                                by: Aaron
"""

text1 = """
    Do you want to download dreamless?
    Press 1 for yes, and 2 for no

"""


def installDreamless():
    os.system('cls')
    print(title_dreamless)
    print(text1)
    
    while True:
        input1 = input(">> ")
        
        if input1 == "1":
            os.system('cls')
            print(title_dreamless)
            print("Now downloading...")
            time.sleep(2)
            os.system('pip install -r Dreamless/requirements.txt')
            print("")
            input("note: Press enter to exit")
            break
        elif input1 == "2":
            os.system('cls')
            print(title_dreamless)
            print("Ok, bye")
            time.sleep(1)
            break
        else:
            print("Invalid option. Please select a valid option.")
            
installDreamless()