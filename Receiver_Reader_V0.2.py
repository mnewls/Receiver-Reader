from PIL import Image 
from tkinter import Button
import pytesseract 
import sys 
import tkinter as tk
from pdf2image import convert_from_path 
import os 
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk as itk

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def folder_in_func():

    #global input location - 
    # button and window prompt for loc

    global input_loc

    root.directory = filedialog.askdirectory()
    
    input_loc = root.directory

    tk.Label(root, text=input_loc).grid(row = 0, column = 2)
    

def folder_out_func():

    #global output location - 
    # button and window prompt for loc

    global output_loc

    root.directory = filedialog.askdirectory()
    
    output_loc = root.directory

    tk.Label(root, text=output_loc).grid(row = 1, column = 2)

def cleanup():

    #post run sequence cleanup

    os.chdir(input_loc)

    os.remove("File Names.txt")

    for filename in os.listdir(input_loc):

        if filename.endswith(".jpg"):

            os.remove(filename)    

def run_reader_prog():

    for filename in os.listdir(input_loc):
        
        if filename.endswith(".pdf"):

            #print(input_loc + "/" + filename)

            os.chdir(input_loc)

            # Path of the pdf 
            PDF_file = open(filename)
            ''' 
            Part #1 : Converting PDF to images 
            '''
            
            # Store all the pages of the PDF in a variable 
            pages = convert_from_path(PDF_file.name) 
            
            # Counter to store images of each page of PDF to image 
            image_counter = 1

            whole_pdf_in_image = []

            # Iterate through all the pages stored above 
            for page in pages: 
            
                # Declaring filename for each page of PDF as JPG 
                # For each page, filename will be: 
                # PDF page 1 -> page_1.jpg 
                # PDF page 2 -> page_2.jpg 
                # PDF page 3 -> page_3.jpg 
                # .... 
                # PDF page n -> page_n.jpg 
                filename = "page_"+str(image_counter)+".jpg"
                
                # Save the image of the page in system 
                page.save(filename, 'JPEG')

                im = Image.open(filename)

                whole_pdf_in_image.append(im)

                # Increment the counter to update filename 
                image_counter = image_counter + 1

            # Variable to get count of total number of pages 
            filelimit = image_counter-1

            # Creating a text file to write the file names
            outfile = "File Names.txt"
            
            # Open the file in append mode so that  
            f = open(outfile, "a") 
            
            # Iterate from 1 to total number of pages 
            for i in range(1, filelimit + 1): 
            
                # Set filename to recognize text from 
                # Again, these files will be: 
                # page_1.jpg 
                # page_2.jpg 
                # .... 
                # page_n.jpg 
                filename = "page_"+str(i)+".jpg"

                im = Image.open(filename)
                
                #cropping side for PN
                im_detect_PN = im.crop((1100,390,1260,440))

                #cropping top for RCV#
                im_detect_RCV = im.crop((640,180,800,240))
                
                    
                # Recognize the text as string in image using pytesserct  
                PN_im_to_text = str(((pytesseract.image_to_string(im_detect_PN))))

                RCV_im_to_text = str(((pytesseract.image_to_string(im_detect_RCV)))) 

                if PN_im_to_text != "" and RCV_im_to_text[0:3] == "RCV":

                    file_name = PN_im_to_text + ', ' + RCV_im_to_text +'.pdf'

                    path_to_save = output_loc +'/'+ file_name

                    #print(path_to_save)

                    whole_pdf_in_image[0].save(path_to_save, save_all = True, quality=100, append_images = whole_pdf_in_image[1:])


            
                # The recognized text is stored in variable text 
                # Any string processing may be applied on text 
                # Here, basic formatting has been done: 
                # In many PDFs, at line ending, if a word can't 
                # be written fully, a 'hyphen' is added. 
                # The rest of the word is written in the next line 
                # Eg: This is a sample text this word here GeeksF- 
                # orGeeks is half on first line, remaining on next. 
                # To remove this, we replace every '-\n' to ''.    
            
                # Finally, write the processed text to the file. 
                f.write(file_name + '\n')
            
            # Close the file after writing all the text. 
            f.close()
        else:
            print("error")
    
    cleanup()

#creating window to work with
root = tk.Tk()

#set window geometry
root.geometry("600x200")

img = Image.open(r'C:\Users\Michael\Desktop\Elbit files\Receipt Reader\Elbit_Logo.png')
img = img.resize((192,66), Image.ANTIALIAS)
photoImg = itk.PhotoImage(img)

background_label = tk.Label(root, image=photoImg)
background_label.place(relx = 1, rely = 1, anchor = 'se')

root.title("Non-Essential Receiver Reader")

#input folder label, and button
tk.Label(root, text="Input Folder").grid(row = 0, sticky = 'W')
Button(root, text="Input Folder", fg='blue', command=folder_in_func).grid(row = 0, column = 1, sticky = 'W')

#output folder label, and button
tk.Label(root, text="Output Folder").grid(row = 1, sticky = 'W')
Button(root, text="Output Folder", fg='blue', command=folder_out_func).grid(row = 1, column = 1, sticky = 'W')

Button(root, text="File My PDFs", fg='blue', command=run_reader_prog).grid(row = 2, column = 1, sticky = 'W')



root.grid_columnconfigure(0, pad=20)
root.grid_columnconfigure(1, pad=20)

root.grid_rowconfigure(0, pad=20)
root.grid_rowconfigure(1, pad=20)
root.grid_rowconfigure(2, pad=20)

root.mainloop()

#main loop to iterate through files

