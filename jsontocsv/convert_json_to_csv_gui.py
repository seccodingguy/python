import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
#import pandas as pd
import csv
import json

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='File Conversion Tool', bg = 'lightsteelblue2')
label1.config(font=('helvetica', 20))
canvas1.create_window(150, 20, window=label1)

def getJSON ():
    #global read_file
    global json_data

    import_file_path = filedialog.askopenfilename()
    with open(import_file_path) as json_file:
        data = json.load(json_file)

    #vuln_data = data['vulnerabilities']
    element_to_convert = inputtxt.get("1.0", "end-1c")
    json_data = data[element_to_convert]
    #read_file = pd.read_json (import_file_path)
    
browseButton_JSON = tk.Button(text="      Import JSON File     ", command=getJSON, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 130, window=browseButton_JSON)
label_input = tk.Label(root, text='JSON Element to Convert', bg = 'lightsteelblue2')
label_input.config(font=('helvetica', 12))
canvas1.create_window(150, 55, window=label_input)
inputtxt = tk.Text(root, height = 1, width = 25, bg = "light yellow") 
canvas1.create_window(150,80,window=inputtxt)

def convertToCSV ():
    #global read_file
    global json_data

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')

    data_file = open(export_file_path, 'w') 
  
    # create the csv writer object 
    csv_writer = csv.writer(data_file) 
  
    # Counter variable used for writing  
    # headers to the CSV file 
    count = 0
  
    for element in json_data: 
        if count == 0: 
  
            # Writing headers of CSV file 
            header = element.keys() 
            csv_writer.writerow(header) 
            count += 1
        try:
            # Writing data of CSV file 
            csv_writer.writerow(element.values())
        finally:
            print('Error with Element: ')
            print(element)
            print('. Continuing with next element.\n') 
  
    data_file.close() 
    #read_file.to_csv (export_file_path, index = None, header=True)

saveAsButton_CSV = tk.Button(text='Convert JSON to CSV', command=convertToCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 180, window=saveAsButton_CSV)

def exitApplication():
    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()
     
exitButton = tk.Button (root, text='       Exit Application     ',command=exitApplication, bg='brown', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 230, window=exitButton)

root.mainloop()
