from colorama import init as colorama_init
from colorama import Fore, Back, Style

class BootScreen:
    def __init__(self) -> None:
        colorama_init()
        print(Style.BRIGHT, Fore.BLUE, end='')
        print("""
  _                              ____                   _ _ 
 (_)_ __ ___   __ _  __ _  ___  |___ \    __ _ ___  ___(_(_)
 | | '_ ` _ \ / _` |/ _` |/ _ \   __) |  / _` / __|/ __| | |
 | | | | | | | (_| | (_| |  __/  / __/  | (_| \__ | (__| | |
 |_|_| |_| |_|\__,_|\__, |\___| |_____|  \__,_|___/\___|_|_|
                    |___/                                    
                                author: FFFFFF-base16       
                                        2021 (c)            
""")
        print(Style.RESET_ALL, end='')
        return