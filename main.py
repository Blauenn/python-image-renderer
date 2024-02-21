import os
import tkinter
from tkinter import font, filedialog
from PIL import Image, ImageTk

from get_exif_data import get_exif_data

# App setup #
app = tkinter.Tk()
app.title("Python image renderer")
app.geometry("900x600")
montserrat_font = font.Font(family="Montserrat")
app.option_add("*Font", montserrat_font)

image_label = None
file_name = tkinter.StringVar()
file_make = tkinter.StringVar()
file_model = tkinter.StringVar()
file_focal_length = tkinter.StringVar()
file_shot_focal_length = tkinter.StringVar()
file_camera = tkinter.StringVar()
file_iso = tkinter.StringVar()
file_shutter = tkinter.StringVar()
file_aperture = tkinter.StringVar()
file_date = tkinter.StringVar()

set_date = tkinter.StringVar()
set_venue = tkinter.StringVar()
set_venue_extras = tkinter.StringVar()

set_facebook = tkinter.StringVar()
set_instagram = tkinter.StringVar()


def display_image(file_path):
    global image_label, max_width

    original_image = Image.open(file_path)

    aspect_ratio = original_image.width / original_image.height

    new_width = min(original_image.width, 280)
    new_height = int(new_width / aspect_ratio)
    resized_image = original_image.resize(
        (new_width, new_height))

    image = ImageTk.PhotoImage(resized_image)

    if image_label:
        image_label.destroy()

    image_label = tkinter.Label(master=frame_information, image=image)
    image_label.image = image
    image_label.pack(side="right", padx=10)


def file_prompt():
    global file_name
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[
                                           ("Image Files", "*.jpg;*.png")])

    if file_path:
        file_name.set(os.path.basename(file_path))
        lens_focal_length, make, model, shot_focal_length, iso, shutter, aperture, date = get_exif_data(
            file_path)

        display_image(file_path)
        file_make.set(make)
        file_model.set(model)
        file_focal_length.set(lens_focal_length)
        file_shot_focal_length.set(shot_focal_length)
        file_camera.set(f"{make} {model} {lens_focal_length}")
        file_iso.set(iso)
        file_shutter.set(shutter)
        file_aperture.set(aperture)
        file_date.set(date)


def file_export():
    with open("export.txt", "w") as file:
        file.write(f"Camera : {file_make.get()} {file_model.get()}\n")
        file.write(f"Focal length : {file_focal_length.get()}\n")
        file.write(f"Shot at : {file_shot_focal_length.get()}\n")
        file.write(f"ISO : {file_iso.get()}\n")
        file.write(f"Shutter speed : {file_shutter.get()}\n")
        file.write(f"Aperture : {file_aperture.get()}\n")
        if set_date.get() != "":
            file.write(f"Date : {set_date.get()}\n")
            print("Date is typed")
        else:
            file.write(f"Date : {file_date.get()}\n")
        if set_venue.get() != "":
            file.write(f"Venue : {set_venue.get()} {set_venue_extras.get()}\n")
        if set_facebook.get() != "":
            file.write(f"Facebook : {set_facebook.get()}\n")
        if set_instagram.get() != "":
            file.write(f"Instagram : {set_instagram.get()}\n")


# Header #
frame_header = tkinter.Frame(master=app)
frame_header.pack(padx=10, pady=10, anchor="nw")
label_title = tkinter.Label(
    master=frame_header, text="Python image renderer", font="Montserrat 16 bold")
label_title.pack()

# Buttons #
frame_buttons = tkinter.Frame(master=app)
frame_buttons.pack(padx=10, pady=10, anchor="nw")
button_upload = tkinter.Button(
    master=frame_buttons, text="Image", command=file_prompt)
button_upload.pack(side="left")
button_export = tkinter.Button(
    master=frame_buttons, text="Export", command=file_export)
button_export.pack(side="left", padx=10)

# Information #
frame_information = tkinter.Frame(master=app)
frame_information.pack(padx=10, pady=10, anchor="nw")
# Image #
frame_image = tkinter.Frame(master=frame_information)
frame_image.pack(anchor="n")
# Camera #
frame_camera = tkinter.Frame(master=frame_information)
frame_camera.pack(side="right", anchor="n")
label_file_name = tkinter.Label(
    master=frame_camera, textvariable=file_name, font="Montserrat 16 bold")
label_file_name.pack(anchor="nw")
frame_camera_child = tkinter.Frame(master=frame_camera)
frame_camera_child.pack(anchor="nw", pady="4")
label_camera = tkinter.Label(
    master=frame_camera_child, textvariable=file_camera)
label_camera.pack(anchor="nw")
label_focal_length = tkinter.Label(
    master=frame_camera_child, textvariable=file_shot_focal_length)
label_focal_length.pack(anchor="nw")
label_iso = tkinter.Label(
    master=frame_camera_child, textvariable=file_iso)
label_iso.pack(anchor="nw")
label_shutter = tkinter.Label(
    master=frame_camera_child, textvariable=file_shutter)
label_shutter.pack(anchor="nw")
label_aperture = tkinter.Label(
    master=frame_camera_child, textvariable=file_aperture)
label_aperture.pack(anchor="nw")
# Date #
group_date = tkinter.Frame(master=frame_camera)
group_date.pack(anchor="nw")
label_date = tkinter.Label(
    master=group_date, text="Date :")
label_date.pack(side="left")
input_date = tkinter.Entry(master=group_date, textvariable=set_date)
input_date.pack(side="right", padx=8)
group_date = tkinter.Frame(master=frame_camera)
# Venue #
group_venue = tkinter.Frame(master=frame_camera)
group_venue.pack(anchor="nw", pady=4)
label_venue = tkinter.Label(
    master=group_venue, text="Venue :")
label_venue.pack(side="left")
input_venue = tkinter.Entry(master=group_venue, textvariable=set_venue)
input_venue.pack(side="right", padx=8)
# Venue extras #
group_venue_extras = tkinter.Frame(master=frame_camera)
group_venue_extras.pack(anchor="nw", pady=2)
label_venue_extras = tkinter.Label(
    master=group_venue_extras, text="Venue extras :")
label_venue_extras.pack(side="left")
input_venue_extras = tkinter.Entry(
    master=group_venue_extras, textvariable=set_venue_extras)
input_venue_extras.pack(side="right", padx=8)
# Facebook #
group_facebook = tkinter.Frame(master=frame_camera)
group_facebook.pack(anchor="nw", pady=4)
label_facebook = tkinter.Label(
    master=group_facebook, text="Facebook :")
label_facebook.pack(side="left")
input_facebook = tkinter.Entry(
    master=group_facebook, textvariable=set_facebook)
input_facebook.pack(side="right", padx=8)
# Instagram #
group_instagram = tkinter.Frame(master=frame_camera)
group_instagram.pack(anchor="nw", pady=2)
label_instagram = tkinter.Label(
    master=group_instagram, text="Instagram :")
label_instagram.pack(side="left")
input_instagram = tkinter.Entry(
    master=group_instagram, textvariable=set_instagram)
input_instagram.pack(side="right", padx=8)

app.mainloop()
