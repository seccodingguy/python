# The fitz highlight code is
# based on https://stackoverflow.com/a/62859169/562769

import os

import os.path
from os import path

import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from typing import List, Tuple
import csv
import fitz  # install with 'pip install pymupdf'

root= tk.Tk()
replaceCSV = tk.IntVar()

replace = False

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
    counter = 0
    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            highlight = _parse_highlight(annot, wordlist)
            comment = annot.info["content"]
            highlights.append(_parse_highlight(annot, wordlist))
            highlights.append(comment)
        annot = annot.next
    return highlights

def main(filepath: str) -> List:
    global replace
    created = False
    if path.isfile(inputcsvtxt.get("1.0","end-1c")):
        if replace:
            data_file = open(inputcsvtxt.get("1.0","end-1c"), 'w', encoding='utf-8')
            replace = False
        else:
            data_file = open(inputcsvtxt.get("1.0","end-1c"), 'a', encoding='utf-8')
    else:
        data_file = open(inputcsvtxt.get("1.0","end-1c"), 'w', encoding='utf-8')
        created = True
        

    csv_writer = csv.writer(data_file)
    
    if created:
        header = ["Comment","Note","File"]
        csv_writer.writerow(header)

    doc = fitz.open(filepath)
    
    for page in doc:
        references = handle_page(page)
        length = len(references)
        i = 0
        if length > 0:
            while i < (length-1):
                csv_writer.writerow([references[i].encode('utf-8'),references[i+1].encode('utf-8'),filepath.encode('utf-8')])
                i += 2
       

def getPDFFiles():
    print("Saving to " + inputcsvtxt.get("1.0","end-1c"))
    rootpath = inputtxt.get("1.0","end-1c")
    for subdir, dirs, files in os.walk(rootpath):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".pdf") or filepath.endswith(".PDF"):
                print (filepath)
                main(filepath)
    print("Done!")


def getPDFilePath():
    import_file_path = filedialog.askdirectory()
    inputtxt.insert("end-1c",import_file_path)

def exitApplication():
    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()

def saveToCSVFile():
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    inputcsvtxt.insert("end-1c",export_file_path)
    print(export_file_path)
    #getPDFFiles(inputtxt.get("1.0","end-1c"))

def setReplaceVariable():
    global replace
    if replaceCSV.get() == 1:
        replace = True
    else:
        replace = False
        
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

browseButton_CSV = tk.Button(text="Create CSV", command=getPDFFiles, bg='green', fg='white', font=('helvetica', 10, 'bold'))
canvas1.create_window(100, 180, window=browseButton_CSV)

c1 = tk.Checkbutton(root, text='Replace CSV?', variable=replaceCSV, onvalue=1, offvalue=0, command=setReplaceVariable)
canvas1.create_window(100,140,window=c1)

root.mainloop()

