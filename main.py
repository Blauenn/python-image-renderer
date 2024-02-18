import os
import tkinter
from tkinter import filedialog, font

from get_exif_data import get_exif_data
from file_export import file_export

app = tkinter.Tk()
app.title("Python image renderer")

file_name = "No file has been selected"

print_info = {
    "lens_focal_length": "0mm",
    "make": "Camera",
    "model": "Model",

    "iso": "0",
    "shutter_speed": "0",
    "aperture": "0",

    "date": "01.01.2024",
    "venue": "",
    "venue_extra": "",

    "facebook": "",
    "instagram": "",
}


def file_prompt(print_info):
    global file_name
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[
                                           ("Image Files", "*.jpg;*.png")])
    if file_path:
        file_name = os.path.basename(file_path)
        label_file_name.config(text=file_name)

        lens_focal_length, make, model, date, iso, shutter, aperture = get_exif_data(
            file_path)
        print_info["lens_focal_length"] = f"{str(lens_focal_length)}mm"
        print_info["make"] = str(make).capitalize()
        print_info["model"] = str(model)
        print_info["iso"] = str(iso)
        print_info["shutter_speed"] = f"{str(shutter)}s"
        print_info["aperture"] = f"f/{str(aperture)}"
        print_info["date"] = str(date)

        label_focal_length.config(text=print_info["lens_focal_length"])
        label_make.config(text=print_info["make"])
        label_model.config(text=print_info["model"])
        label_iso.config(text=print_info["iso"])
        label_shutter_speed.config(text=print_info["shutter_speed"])
        label_aperture.config(text=print_info["aperture"])
        label_date.config(text=print_info["date"])
    else:
        print("No file given")
        return None


montserrat_font = font.Font(family="Montserrat")
app.option_add("*Font", montserrat_font)

label_file_name = tkinter.Label(app, text=file_name, font="Montserrat 16 bold", padx=10, pady=10)

label_focal_length = tkinter.Label(
    app, text=print_info["lens_focal_length"], padx=10)
label_make = tkinter.Label(
    app, text=print_info["make"], padx=10)
label_model = tkinter.Label(
    app, text=print_info["model"], padx=10)
label_iso = tkinter.Label(
    app, text=print_info["iso"], padx=10)
label_shutter_speed = tkinter.Label(
    app, text=print_info["shutter_speed"], padx=10)
label_aperture = tkinter.Label(
    app, text=print_info["aperture"], padx=10)
label_date = tkinter.Label(
    app, text=print_info["date"], padx=10)

button_image_prompt = tkinter.Button(
    app, text="Select an image", padx=4, pady=2, command=lambda: file_prompt(print_info))
button_image_export = tkinter.Button(
    app, text="Export value as .txt", padx=4, pady=2, command=lambda: file_export(file_name, print_info))

# --- #

label_file_name.pack(anchor="nw")

label_focal_length.pack(anchor="nw")
label_make.pack(anchor="nw")
label_model.pack(anchor="nw")
label_iso.pack(anchor="nw")
label_shutter_speed.pack(anchor="nw")
label_aperture.pack(anchor="nw")
label_date.pack(anchor="nw")

button_image_prompt.pack(anchor="nw")
button_image_export.pack(anchor="nw")

app.mainloop()
