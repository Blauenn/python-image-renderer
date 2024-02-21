import os
import tkinter
from tkinter import font, filedialog
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageTk, ImageDraw, ImageFont

from get_exif_data import get_exif_data

# App setup #
app = tkinter.Tk()
app.title("Python image renderer")
app.geometry("900x600")
montserrat_font = font.Font(family="Montserrat")
app.option_add("*Font", montserrat_font)

file_path = ""

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
    global file_path, file_name
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

        input_date.delete(0, tkinter.END)
        input_date.insert(0, date)


# def file_export():
#     with open("export.txt", "w") as file:
#         file.write(f"Camera : {file_make.get()} {file_model.get()}\n")
#         file.write(f"Focal length : {file_focal_length.get()}\n")
#         file.write(f"Shot at : {file_shot_focal_length.get()}\n")
#         file.write(f"ISO : {file_iso.get()}\n")
#         file.write(f"Shutter speed : {file_shutter.get()}\n")
#         file.write(f"Aperture : {file_aperture.get()}\n")
#         if set_date.get() != "":
#             file.write(f"Date : {set_date.get()}\n")
#             print("Date is typed")
#         else:
#             file.write(f"Date : {file_date.get()}\n")
#         if set_venue.get() != "":
#             file.write(f"Venue : {set_venue.get()} {set_venue_extras.get()}\n")
#         if set_facebook.get() != "":
#             file.write(f"Facebook : {set_facebook.get()}\n")
#         if set_instagram.get() != "":
#             file.write(f"Instagram : {set_instagram.get()}\n")

def file_export():
    global file_path
    if file_path:
        # Get EXIF data and image dimensions
        lens_focal_length, make, model, shot_focal_length, iso, shutter, aperture, date = get_exif_data(
            file_path)

        # Open the image using PIL
        image = Image.open(file_path)

        # Determine if the image is vertical or horizontal
        width, height = image.size
        if height > width:  # Vertical image
            new_height = 1960
            new_width = int((new_height / height) * width)
        else:  # Horizontal image
            new_width = 2400
            new_height = int((new_width / width) * height)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Create a 3840x1080 canvas
        canvas_width = 3840
        canvas_height = 2160
        canvas = Image.new("RGB", (canvas_width, canvas_height), "#FFFFFF")

        # Calculate the position to center the image on the canvas
        x_offset = (canvas_width - new_width) // 2
        y_offset = (canvas_height - new_height) // 2

        # Paste the resized image onto the canvas
        canvas.paste(resized_image, (x_offset, y_offset))

        font_regular = ImageFont.FreeTypeFont(
            "assets/fonts/Montserrat/Montserrat-Regular.ttf", 60)
        font_regular_72 = ImageFont.FreeTypeFont(
            "assets/fonts/Montserrat/Montserrat-Regular.ttf", 72)
        font_bold_56 = ImageFont.FreeTypeFont(
            "assets/fonts/Montserrat/Montserrat-Bold.ttf", 56)
        font_bold = ImageFont.FreeTypeFont(
            "assets/fonts/Montserrat/Montserrat-Bold.ttf", 72)

        # Draw text on the canvas
        draw = ImageDraw.Draw(canvas)

        # Camera information
        draw.text((x_offset - 60, y_offset + 20), lens_focal_length,
                  fill="black", font=font_regular, anchor="rt")
        draw.text((x_offset - 60, y_offset + 150), make,
                  fill="black", font=font_bold, anchor="rt")
        draw.text((x_offset - 60, y_offset + 260), model,
                  fill="black", font=font_bold, anchor="rt")

        # Camera settings
        if (lens_focal_length != shot_focal_length):
            draw.text((x_offset - 60, new_height - 410), str(shot_focal_length),
                      fill="black", font=font_bold, anchor="rt")
        draw.text((x_offset - 60, new_height - 280), f"ISO {str(iso)}",
                  fill="black", font=font_bold, anchor="rt")
        draw.text((x_offset - 60, new_height - 150), shutter,
                  fill="black", font=font_bold, anchor="rt")
        draw.text((x_offset - 60, new_height - 20), aperture,
                  fill="black", font=font_bold, anchor="rt")

        # Event information
        if (input_date.get() != ""):
            draw.text((x_offset + new_width + 60, y_offset + 20), input_date.get(),
                      fill="black", font=font_regular)
        else:
            draw.text((x_offset + new_width + 60, y_offset + 20), file_date.get(),
                      fill="black", font=font_regular)
        venue_text = input_venue.get("1.0", "end-1c")
        venue_lines = venue_text.split("\n")
        for i, line in enumerate(venue_lines):
            y_position = y_offset + 150 + i * 110
            draw.text((x_offset + new_width + 60, y_position), line,
                      fill="black", font=font_bold)
        final_y_position = y_offset + 150 + len(venue_lines) * 110
        draw.text((x_offset + new_width + 60, final_y_position),
                  input_venue_extras.get(), fill="black", font=font_regular_72)

        # Contact information
        original_facebook_logo = Image.open(
            "assets/images/Facebook.png").convert("RGBA")
        bg_facebook_logo = Image.new(
            "RGBA", original_facebook_logo.size, (255, 255, 255, 0))
        no_bg_facebook_logo = Image.alpha_composite(
            bg_facebook_logo, original_facebook_logo)
        facebook_logo = no_bg_facebook_logo.resize((100, 100))
        original_instagram_logo = Image.open(
            "assets/images/Instagram.png").convert("RGBA")
        bg_instagram_logo = Image.new(
            "RGBA", original_instagram_logo.size, (255, 255, 255, 0))
        no_bg_instagram_logo = Image.alpha_composite(
            bg_instagram_logo, original_instagram_logo)
        instagram_logo = no_bg_instagram_logo.resize((100, 100))

        # Facebook
        facebook_text = input_facebook.get("1.0", "end-1c")
        if (facebook_text != ""):
            canvas.paste(facebook_logo, (x_offset + new_width +
                                         60, new_height - 20), facebook_logo)
            facebook_lines = facebook_text.split("\n")
            if (len(facebook_lines) == 1):
                draw.text((x_offset + new_width + 60 + 100 + 40, new_height),
                          facebook_text, fill="black", font=font_bold_56)
            else:
                draw.text((x_offset + new_width + 60 + 100 + 40, new_height - 40),
                          facebook_text, fill="black", font=font_bold_56)

        # Instagram
        if (input_instagram.get() != ""):
            if (facebook_text != ""):
                canvas.paste(instagram_logo, (x_offset + new_width +
                                              60, new_height - 200), instagram_logo)
                draw.text((x_offset + new_width + 60 + 100 + 40, new_height - 200 + 15),
                          input_instagram.get(), fill="black", font=font_bold_56)
            else:
                canvas.paste(instagram_logo, (x_offset + new_width +
                                              60, new_height - 20), instagram_logo)
                draw.text((x_offset + new_width + 60 + 100 + 40, new_height),
                          input_instagram.get(), fill="black", font=font_bold_56)

        # Save the result
        canvas.save("output_image.jpg")


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
input_date = tkinter.Entry(master=group_date)
input_date.pack(side="right", padx=8)
group_date = tkinter.Frame(master=frame_camera)
# Venue #
group_venue = tkinter.Frame(master=frame_camera)
group_venue.pack(anchor="nw", pady=4)
label_venue = tkinter.Label(
    master=group_venue, text="Venue :")
label_venue.pack(side="left")
input_venue = tkinter.Text(master=group_venue, height=4, width=40, wrap="word")
input_venue.pack(side="right", padx=8)
# Venue extras #
group_venue_extras = tkinter.Frame(master=frame_camera)
group_venue_extras.pack(anchor="nw", pady=2)
label_venue_extras = tkinter.Label(
    master=group_venue_extras, text="Venue extras :")
label_venue_extras.pack(side="left")
input_venue_extras = tkinter.Entry(
    master=group_venue_extras)
input_venue_extras.pack(side="right", padx=8)
# Facebook #
group_facebook = tkinter.Frame(master=frame_camera)
group_facebook.pack(anchor="nw", pady=4)
label_facebook = tkinter.Label(
    master=group_facebook, text="Facebook :")
label_facebook.pack(side="left")
input_facebook = tkinter.Text(
    master=group_facebook, height=2, width=40, wrap="word")
input_facebook.pack(side="right", padx=8)
# Instagram #
group_instagram = tkinter.Frame(master=frame_camera)
group_instagram.pack(anchor="nw", pady=2)
label_instagram = tkinter.Label(
    master=group_instagram, text="Instagram :")
label_instagram.pack(side="left")
input_instagram = tkinter.Entry(master=group_instagram)
input_instagram.pack(side="right", padx=8)

app.mainloop()
