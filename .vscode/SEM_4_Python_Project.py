from tkinter import *
import tkinter.messagebox as tmsg
from tkinter import filedialog, font
from tkinter import colorchooser
import win32print
import win32api                             #to print file.


root = Tk()
root.title("NOTEPAD!!")
root.wm_iconbitmap("icon.ico")
root.geometry("1200x680")

#Variable for open file name
global open_status_name
open_status_name = False             #not important but still     but good practice

#Selected text
global selected
selected = False



#Creating new file function
def new_file():
    my_text.delete("1.0", END)          #deletes previous text
    root.title("New File - NOTEPAD!!")  #updates previous title
    status_bar.config(text="New File")  #updates status bar

    global open_status_name
    open_status_name = False 

#Creating Open file function
def open_file():
    my_text.delete("1.0", END)  #deletes previous text
    #Grab Filename
    text_file = filedialog.askopenfilename(initialdir="D:/Chirag/", title="Open File", filetypes=(("Text Files", "*.txt"), ("python Files", "*.py"), ("All Files", "*.*")))
    
    #Check to see if there is file Name
    if text_file:
        #Making file name global so we can access it later
        global open_status_name
        open_status_name = text_file
    #Update status bar
    name = text_file
    status_bar.config(text=f"{name}")  
    name = name.replace("D:/Chirag/", "")   # Replacing file directory with the file name
    root.title(f"{name} - NOTEPAD!!")      

    #open File
    text_file = open(text_file, "r")   #to read the content of the file
    content = text_file.read()

    #Add file content to text box
    my_text.insert(END, content)

    #Close opened file
    text_file.close()   #opened file will close if we open New File

# Creating Save As File function
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="D:/Chirag/", title="Save File", filetypes=(("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")))
    #to check whether file name is available
    if text_file:
        #Upadating status bar
        name = text_file
        status_bar.config(text="Saved" f"{name}")
        name = name.replace("D:/Chirag/", "")
        root.title(f"{name} - NOTEPAD!!") 

        #Saving the file in directory
        text_file = open(text_file, "w")
        text_file.write(my_text.get(1.0, END))
        text_file.close()   #close the file


#Creating Save File function
def save_file():
    global open_status_name   # if the file is available we are saving it directly...
    if open_status_name:
        #Saving the file
        text_file = open(open_status_name, "w")
        text_file.write(my_text.get(1.0, END))
        text_file.close()   #close the file

        #Creating message box to get message of the FILE IS SAVED...
        message = tmsg.showinfo("File Saved", f"{open_status_name} is Saved Successfully !")

        status_bar.config(text=f"Saved:{open_status_name}")
    else:                   # if the name is not available we are following SaveAs functionality...
        save_as_file()

#Cut Text()
def cut_text(event):
    global selected
    #Event binding so to see whether we press keyboard shortcuts.
    if event:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():      # to see if the text is selected or not
            # Grabing selected text from text box
            selected = my_text.selection_get()
            #Deleting selected text from text box    ....because it is imp to do
            #Selected text has tag "sel"
            my_text.delete(SEL_FIRST, SEL_LAST)              #first aplabet to last alphabet and everything in between...
            #to clear the previous copied text from clipboard
            root.clipboard_clear()
            root.clipboard_append(selected)   #appending selected text to clipboard
        

#Copy Text
def copy_text(event):
    global selected
    #Event binding so to see whether we press keyboard shortcuts.
    if event:
        selected = root.clipboard_get()
    
    if my_text.selection_get():
        # Grabing selected text from text box
        selected = my_text.selection_get()
    #to clear the previous copied text from clipboard
        root.clipboard_clear()
        root.clipboard_append(selected)   #appending selected text to clipboard

#Paste text
def paste_text(event):
    global selected
    #Event binding so to see whether we press keyboard shortcuts.
    if event:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)

#Bold text
def bold_func():           #we will select the tag, which we want to make bold 
    #Create our font
    bold_font = font.Font(my_text, my_text.cget("font"))    
    bold_font.configure(weight="bold")
    #Configure the tag
    my_text.tag_configure("bold", font=bold_font)

    #define current tags
    current_tags = my_text.tag_names(SEL_FIRST)
    #if the selected text is not bold it will make it bold and it selected text is bold already then it will unbold it
    if "bold" in current_tags:
        my_text.tag_remove("bold", SEL_FIRST, SEL_LAST)    
    else:
        my_text.tag_add("bold", SEL_FIRST, SEL_LAST)

#Italics text
def italics_func():
    #Create our font
    italics_font = font.Font(my_text, my_text.cget("font"))    
    italics_font.configure(slant="italic")
    #Configure the tag
    my_text.tag_configure("italic", font=italics_font)

    #define current tags
    current_tags = my_text.tag_names(SEL_FIRST)
    #if the selected text is not bold it will make it bold and it selected text is bold already then it will unbold it
    if "italic" in current_tags:
        my_text.tag_remove("italic", SEL_FIRST, SEL_LAST)    
    else:
        my_text.tag_add("italic", SEL_FIRST, SEL_LAST)

#Change selected text Color
def text_color():
    #Pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        #Create our font
        color_font = font.Font(my_text, my_text.cget("font"))    
        #Configure the tag
        my_text.tag_configure("colored", font=color_font, foreground=my_color)

        #define current tags
        current_tags = my_text.tag_names(SEL_FIRST)
        #if the selected text is not bold it will make it bold and it selected text is bold already then it will unbold it
        if "colored" in current_tags:
            my_text.tag_remove("colored", SEL_FIRST, SEL_LAST)    
        else:
            my_text.tag_add("colored", SEL_FIRST, SEL_LAST)

    
#Change background color
def  background_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)

#Change all text color
def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)

#About Us
def aboutus_info():
    message = tmsg.showinfo("Our group project team members.", "Chirag Sonavale (19104B0046)\nAnuj Gargote (19104B0047)\nPranjal Gaikwad (19104B0018)")


#Print file
def print_file():
    printer_name = win32print.GetDefaultPrinter()
    status_bar.config(text=printer_name)                  #just to see default printer
     
    #Grab a file
    file_to_print = filedialog.askopenfilename(initialdir="D:/Chirag/", title="Open File", filetypes=(("Text Files", "*.txt"), ("python Files", "*.py"), ("All Files", "*.*")))

    if file_to_print:
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)







#Creating toolbar Frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

#Creating main frame
f1 = Frame(root)
f1.pack(pady=5)
#Creating scroll bar on right side for text Box
text_scroll = Scrollbar(f1)
text_scroll.pack(side=RIGHT, fill=Y)
#Creating scrol bar at botoom side in horizontal direction for text Box
hor_scroll = Scrollbar(f1, orient="horizontal")
hor_scroll.pack(side=BOTTOM, fill=X)

#Creating Text Box
my_text = Text(f1, width=125, height=28, font=("TimesNewRoman", 16), selectbackground="silver", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
my_text.pack()
#Configure our scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)
#Create MenuBar
my_menu = Menu(root)
root.config(menu=my_menu)
#Add file Menu
file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu= file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="SaveAs", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Print File", command=print_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
#Add Edit Menu

edit_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Edit", menu= edit_menu)
edit_menu.add_command(label="Cut       (Ctrl+x)", command=lambda: cut_text(False))
edit_menu.add_command(label="Copy    (Ctrl+c)", command=lambda: copy_text(False))
edit_menu.add_command(label="Paste    (Ctrl+v)", command=lambda: paste_text(False))
edit_menu.add_separator()
edit_menu.add_command(label="Undo    (Ctrl+z)", command=my_text.edit_undo)    #inbuilt in tkinter
edit_menu.add_command(label="Redo    (Ctrl+y)", command=my_text.edit_redo)

#Add Color Menu
color_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Colors", menu= color_menu)
color_menu.add_command(label="Selected Text Color", command=text_color)
color_menu.add_command(label="All Text Color", command=all_text_color)
color_menu.add_command(label="Background Color", command=background_color)

#About Us
aboutus_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="About Us", menu= aboutus_menu)
aboutus_menu.add_command(label="Our Project Team", command=aboutus_info)


#Add Satus bar to BOTTOM
status_bar = Label(root, text="Ready",font=("Arial", 12), anchor=NW)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

#Edit event bindings
root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)

#Create buttons in toolbar

#Bold button
bold_button = Button(toolbar_frame, text="Bold", command=bold_func)
bold_button.grid(row=0, column=0, sticky=W, padx=5)
#Italics Button
italics_button = Button(toolbar_frame, text="Italics", command=italics_func)
italics_button.grid(row=0, column=1, padx=5)
#Undo/Redo button
undo_button = Button(toolbar_frame, text="Undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)

redo_button = Button(toolbar_frame, text="Redo", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

#color text
color_text_button = Button(toolbar_frame, text="Text Color", command=text_color)
color_text_button.grid(row=0, column=4, padx=5)



root.mainloop()
