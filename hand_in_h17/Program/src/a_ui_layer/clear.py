from os import system, name

def clear():
   """Clears terminal, for cleaning up UI.
   Code from https://www.tutorialspoint.com/how-to-clear-python-shell#:~:text=The%20commands%20used%20to%20clear,shell%20are%20cls%20and%20clear."""
   # for windows
   if name == 'nt':
    _ = system('cls')

   # for mac and linux
   else:
    _ = system('clear')