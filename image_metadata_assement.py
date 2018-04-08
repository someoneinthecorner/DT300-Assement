from tkinter import *
import tkinter.messagebox
import csv

class Image:
    def __init__(self, image_id, filename, file_extension, owner, licence_type, resolution):
        self.image_id = image_id
        self.filename = filename #separate filename and extension as extension will be chosen from drop down list to prevent user entering file extension wrong
        self.file_extension = file_extension 
        self.owner = owner #one field rather than fn ln to allow usernames and companies to own images
        self.licence_type = licence_type
        self.resolution = resolution

    def get_image_id(self):
        return self.image_id

    def get_filename(self):
        return self.filename

    def get_file_extension(self):
        return self.file_extension

    def get_owner(self):
        return self.owner

    def get_licence_type(self):
        return self.licence_type

    def get_resolution(self):
        return self.resolution

class GUI:
    def __init__(self):
        window = Tk()
        window.title("Image Metadata Entry")
        window.minsize(width=400, height=400)

        self.ready_to_write = False
        self.recordlist = []

        # Label and field for each entry field
        
        image_id_label = Label(window, text="Enter image id")
        image_id_label.pack()
        self.image_id_field = Entry(window)
        self.image_id_field.pack()

        filename_label = Label(window, text="Enter filename:")
        filename_label.pack()
        self.filename_field = Entry(window)
        self.filename_field.pack()

        file_extension_label = Label(window, text='File extension:')
        file_extension_label.pack()
        self.file_extension_field = StringVar()
        # make sure this is enough file extensions
        OptionMenu(window, self.file_extension_field, ".jpg", ".png", ".gif").pack()

        owner_label = Label(window, text="Enter file owner:")
        owner_label.pack()
        self.owner_field = Entry(window)
        self.owner_field.pack()

        licence_type_label = Label(window, text='Licence type:')
        licence_type_label.pack()
        self.licence_type_field = StringVar()
        # make sure the lisences are correct and in best format for user to pick
        OptionMenu(window, self.licence_type_field, "Attribution alone", "Attribution + ShareAlike", "Attribution + Noncommercial", "Attribution + NoDerivatives", "Attribution + Noncommercial + ShareAlike", "Attribution + Noncommercial + NoDerivatives").pack()

        resolution_label = Label(window, text="Enter image resolution:")
        resolution_label.pack()
        self.resolution_field = Entry(window)
        self.resolution_field.pack()

        # Button for submtting entered records
        button_label = Label(window, text="Press to enter data")
        button_label.pack()
        button = Button(window, text='Submit', command=self.doSubmit)
        button.pack()

        # Button for writing to csv
        button_label1 = Label(window, text='Convert Records to csv')
        button_label1.pack()
        button1 = Button(window, text='write to csv', command=self.writetocsv)
        button1.pack()
        
        window.mainloop() 
        
    def doSubmit(self):

        if len(self.image_id_field.get()) >1 or len(self.filename_field.get()) > 1 or len(self.file_extension_field.get()) > 1 or len(self.owner_field.get()) > 1 or len(self.licence_type_field.get()) > 1 or len(self.resolution_field.get()) > 1:
            try:
                validate_resolution = int(self.resolution_field.get())
                self.recordlist.append(Image(self.image_id_field.get(), self.filename_field.get(), self.file_extension_field.get(), self.owner_field.get(), self.licence_type_field.get(), self.resolution_field.get()))
                self.ready_to_write = True
                tkinter.messagebox.showinfo("Submission succesful", "Image metadata validated")

                self.image_id_field.delete(0, END) #deletes text entry in fields. Dropdown menus stay the same as are likely to be the same when entering multiple image entries
                self.filename_field.delete(0, END)
                self.owner_field.delete(0, END)
                self.resolution_field.delete(0, END)             
            except:
                tkinter.messagebox.showwarning("Error", "Make sure image resolution is numerical")
        else:
            tkinter.messagebox.showwarning("Error", "Please enter values for all fields")

    def writetocsv(self): #add if else for if has been validated
        file_name = "images.csv"

        if self.ready_to_write == True:
            ofile = open(file_name, "w")
            writer = csv.writer(ofile, delimiter=",")#, lineterminator="\n")
            for record in self.recordlist:
                writer.writerow([record.get_image_id(), record.get_filename(), record.get_file_extension(), record.get_owner(), record.get_licence_type(), record.get_resolution()])
                ofile.close()
                tkinter.messagebox.showinfo("file generated", "file generated") # change to say file name
        else:
            tkinter.messagebox.showwarning("Error", "You need to validate your data before writing to csv")

        ready_to_write = False

# Main routine
GUI() 
