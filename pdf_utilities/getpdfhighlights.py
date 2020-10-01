# The fitz highlight code is
# based on https://stackoverflow.com/a/62859169/562769

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from typing import List, Tuple
import csv
import fitz  # install with 'pip install pymupdf'

root= tk.Tk()

def createGUI():
    
    print("Inside createGUI.")
    canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    canvas1.pack()

    label1 = tk.Label(root, text='\nPDF Highlight and\n Notes Extraction Tool', bg = 'lightsteelblue2')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(150, 20, window=label1)
    exitButton = tk.Button (root, text='       Exit Application     ',command=exitApplication, bg='brown', fg='white', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 230, window=exitButton)

    root.mainloop()

def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    return sentence


def handle_page(page):
    wordlist = page.getText("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

    highlights = []
    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights


def main(filepath: str) -> List:
    createGUI()
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return highlights

def exitApplication():
    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()



if __name__ == "__main__":
    print(main("C:\\Users\\mark_\\Dropbox\\Doctoral Studies\\Thesis\\Literature\\Static_Analysis\\SOSRepair-Expressive Semantic Search for Real-World Program Repair.pdf"))
    
