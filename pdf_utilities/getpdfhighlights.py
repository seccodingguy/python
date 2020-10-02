# The fitz highlight code is
# based on https://stackoverflow.com/a/62859169/562769

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from typing import List, Tuple
import csv
import fitz  # install with 'pip install pymupdf'

root= tk.Tk()

def getPDFilePath():
    import_file_path = filedialog.askdirectory()
    inputtxt.insert("end-1c",import_file_path)

def exitApplication():
    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()

def saveToCSVFile():
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    print(export_file_path)
    inputcsvtxt.insert = ("end-1c",export_file_path)
       
canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='\nPDF Highlight and\n Notes Extraction Tool', bg = 'lightsteelblue2')
label1.config(font=('helvetica', 14))
canvas1.create_window(150, 20, window=label1)
exitButton = tk.Button (root, text='       Exit Application     ',command=exitApplication, bg='brown', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 230, window=exitButton)

browseButton_PDF = tk.Button(text="PDF Location", command=getPDFilePath, bg='green', fg='white', font=('helvetica', 10, 'bold'))
canvas1.create_window(60, 80, window=browseButton_PDF)
inputtxt = tk.Text(root, height = 1, width = 20, bg = "light yellow") 
canvas1.create_window(200,80,window=inputtxt)

browseButton_CSV = tk.Button(text="CSV Output", command=saveToCSVFile, bg='green', fg='white', font=('helvetica', 10, 'bold'))
canvas1.create_window(60, 110, window=browseButton_CSV)
inputcsvtxt = tk.Text(root, height = 1, width = 20, bg = "light yellow") 
canvas1.create_window(200,110,window=inputcsvtxt)

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
    #createGUI()
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return highlights


def getPDFFiles():
    for subdir, dirs, files in os.walk(import_file_path):
        for file in files:
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".pdf"):
                print (filepath)

if __name__ == "__main__":
    print(main("C:\\Users\\mark_\\Dropbox\\Doctoral Studies\\Thesis\\Literature\\Static_Analysis\\SOSRepair-Expressive Semantic Search for Real-World Program Repair.pdf"))
    
