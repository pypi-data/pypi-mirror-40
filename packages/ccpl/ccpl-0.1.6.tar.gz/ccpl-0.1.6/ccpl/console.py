import os

def clear():
    os.system('cls')

def prints(text="Spam, eggs and bacon, good sir!"):
    print('\r'+str(text))

if __name__ == '__main__':
    prints("This is the CCPL console module. For help on CCPL, run ccpl.help")