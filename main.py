import tkinter
import os
from tkinter import filedialog
from get_exif_data import get_exif_data

app = tkinter.Tk()
app.title("Python image renderer")
app.geometry("300x150")

file_name = ""
iso_value = "No file chosen"
shutter_value = "No file chosen"
aperture_value = "No file chosen"


def update_labels(file_name, iso, shutter, aperture):
    label_name.config(text=file_name)
    label_ISO.config(text=f"ISO : {iso}")
    label_shutter.config(text=f"Shutter speed : {shutter}s")
    label_aperture.config(text=f"Aperture : f/{aperture}")


def file_prompt():
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[
                                           ("Image Files", "*.jpg;*.png")])
    if file_path:
        file_name = os.path.basename(file_path)
        iso, shutter, aperture = get_exif_data(file_path)
        update_labels(file_name, iso, shutter, aperture)
    else:
        print("No file given")


label_name = tkinter.Label(app, text="No file chosen")
label_ISO = tkinter.Label(app, text=f"ISO : {iso_value}")
label_shutter = tkinter.Label(app, text=f"Shutter speed : {shutter_value}s")
label_aperture = tkinter.Label(app, text=f"Aperture : {aperture_value}")
button = tkinter.Button(app, text="Image", command=file_prompt)

label_name.pack()
label_ISO.pack()
label_shutter.pack()
label_aperture.pack()
button.pack()

app.mainloop()
