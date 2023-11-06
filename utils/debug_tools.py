# ==========================================================+
# Author: Gabriel Bento                                     #
#                                                           #
# Purpose:                                                  #
# I often need to use one/or more function ins this module  #
# So I'm gonna create them here for debug purposes.         #
# ==========================================================+

def save_text(filename: str, text: str):
    """Saves a string content into a file."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def read_file(filename: str) -> str:
    """Reads a file."""
    with open(filename, 'r') as file:
        return file.read()