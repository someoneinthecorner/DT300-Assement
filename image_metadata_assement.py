"""
Program: Write image metadata to csv
Author: Zoe Kaufman
Purpose: To collect image metadata and append to a csv file that can be uploaded to a mysql database
"""

from tkinter import *
import tkinter.messagebox
import csv
import re

class Image:
    def __init__(self, image_id, filename, file_extension, owner, licence_type, resolution):
        self.image_id = image_id
        self.filename = filename # separate filename and extension as extension will be chosen from drop down list to prevent user entering file extension wrong
        self.file_extension = file_extension 
        self.owner = owner # one field rather than fn ln to allow usernames and companies to own images
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
        window.minsize(width=275, height=350)
        background_colour = "#e6f3f4" # Light blue background colour can be changed here
        window.configure(background=background_colour)

        self.ready_to_write = False
        self.recordlist = [] # list of records to be written to csv that gets cleared once written to csv
        self.id_list = [] #list of id's that doesn't get deleted when written to csv so can check for duplicates

        # Label and field for each entry field
        # Labels are right aligned in gui to make it easier to see which label goes with which field
        
        title_label = Label(window, text="Image Metadata Entry", pady = 10, font = ("5"), bg = background_colour)
        title_label.grid(row = 0, column = 0, columnspan = 2)
        
        image_id_label = Label(window, text="Image ID:", pady = 10, padx = 10, bg = background_colour)
        image_id_label.grid(row = 1, column = 0, sticky = E)
        self.image_id_field = Entry(window)
        self.image_id_field.grid(row = 1, column = 1)
        self.image_id_field.focus()

        filename_label = Label(window, text="Filename:", pady = 10, padx = 10, bg = background_colour)
        filename_label.grid(row = 2, column = 0, sticky = E)
        self.filename_field = Entry(window)
        self.filename_field.grid(row = 2, column = 1)

        # drop down menu used as only small set of image file extensions are actually used, and dropdown menus don't require validation
        file_extension_label = Label(window, text='File extension:', pady = 10, padx = 10, bg = background_colour)
        file_extension_label.grid(row = 3, column = 0, sticky = E)
        self.file_extension_field = StringVar()
        OptionMenu(window, self.file_extension_field, ".jpg", ".png", ".gif", ".tiff").grid(row = 3, column = 1) # File extesions that I or someone in our class would use as brief states it could be used in our database assesment

        owner_label = Label(window, text="File owner:", pady = 10, padx = 10, bg = background_colour)
        owner_label.grid(row = 4, column = 0, sticky = E)
        self.owner_field = Entry(window)
        self.owner_field.grid(row = 4, column = 1)

        # drop down menu used as user needs to enter only these, and dropdown menus don't require validation
        licence_type_label = Label(window, text='Licence type:', pady = 10, padx = 10, bg = background_colour)
        licence_type_label.grid(row = 5, column = 0, sticky = E)
        self.licence_type_field = StringVar()
        OptionMenu(window, self.licence_type_field, "Attribution alone", "Attribution + ShareAlike", "Attribution + Noncommercial", "Attribution + NoDerivatives", "Attribution + Noncommercial + ShareAlike", "Attribution + Noncommercial + NoDerivatives").grid(row = 5, column = 1)

        resolution_label = Label(window, text="Resolution (ppi):", pady = 10, padx = 10, bg = background_colour)
        resolution_label.grid(row = 6, column = 0, sticky = E)
        self.resolution_field = Entry(window)
        self.resolution_field.grid(row = 6, column = 1)

        # set at the start of program as defult as is the most likely answer for each
        self.file_extension_field.set(".jpg")
        self.licence_type_field.set("Attribution alone")

        # Button for writing to csv
        button1 = Button(window, text='Write to csv', command=self.writetocsv)
        button1.grid(row = 7, column = 0)

        # Button for submtting entered records
        button = Button(window, text='Submit Data', command=self.doSubmit)
        button.grid(row = 7, column = 1)
             
        window.mainloop() 
        
    def doSubmit(self):
        ready_to_validate = True

        # Checks for duplicate records
        for i in range (0, len(self.id_list)):
            if self.image_id_field.get() == self.id_list[i]:
                tkinter.messagebox.showwarning("Duplicate Image ID", "Please choose another unique image ID.")
                ready_to_validate = False

        # checks that image resolution is an integer greater than zero
        try:
            resolution = int(self.resolution_field.get())
            if resolution < 1:
               tkinter.messagebox.showwarning("Error", "Make sure image resolution is greater than zero")
               ready_to_validate = False
        except:
            tkinter.messagebox.showwarning("Error", "Make sure image resolution is numerical")
            ready_to_validate = False

        # makes sure there are only numbers. letters and underscores
        if not re.match("^[a-zA-Z0-9_]+$", self.filename_field.get()):
            tkinter.messagebox.showwarning("Error", "Please make sure filename contains only numbers, letters and underscores")
            ready_to_validate = False            
        
        # checks that there is info in each field and if resolution is an integer not less than one
        if ready_to_validate == True:
            if len(self.image_id_field.get()) > 0 and len(self.filename_field.get()) > 0 and len(self.file_extension_field.get()) > 0 and len(self.owner_field.get()) > 0 and len(self.licence_type_field.get()) > 0 and len(self.resolution_field.get()) > 0:
                self.recordlist.append(Image(self.image_id_field.get(), self.filename_field.get(), self.file_extension_field.get(), self.owner_field.get(), self.licence_type_field.get(), self.resolution_field.get()))
                self.id_list.append(self.image_id_field.get())
                self.ready_to_write = True
                tkinter.messagebox.showinfo("Submission succesful", "Image metadata validated")

                self.image_id_field.delete(0, END) #deletes text entry in fields. Dropdown menus stay the same as are likely to be the same when entering multiple image records
                self.filename_field.delete(0, END)
                self.owner_field.delete(0, END)
                self.resolution_field.delete(0, END)
                self.image_id_field.focus()
            else:
                tkinter.messagebox.showwarning("Error", "Please enter values for all fields")

    def writetocsv(self):
        file_name = "images.csv"

        if self.ready_to_write == True:
            ofile = open(file_name, "a") # Append so if someone writes to csv and wants to add more data they can without losing everything
            writer = csv.writer(ofile, delimiter=",", lineterminator="\n")
            for record in self.recordlist:
                writer.writerow([record.get_image_id(), record.get_filename(), record.get_file_extension(), record.get_owner(), record.get_licence_type(), record.get_resolution()])
            ofile.close()
            tkinter.messagebox.showinfo("file generated", "file generated")
            self.recordlist = []
        else:
            tkinter.messagebox.showwarning("Error", "You need to validate your data before writing to csv")

        self.ready_to_write = False

# Main routine
GUI() 
