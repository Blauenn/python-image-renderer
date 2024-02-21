from datetime import datetime
from PIL import Image, ExifTags

lens_focal_length = ""
make = ""
model = ""
shot_focal_length = ""
iso = ""
shutter = ""
aperture = ""
date = ""

def apex_to_aperture(apex_value):
    return round(2 ** (apex_value / 2), 4)


def get_exif_data(file_path):
    global lens_focal_length, make, model, shot_focal_length, iso, shutter, aperture, date
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "LensSpecification" and isinstance(value, tuple):
                    min_length, max_length, _, _ = value
                    if min_length == max_length:
                        lens_focal_length = f"{int(min_length)}mm"
                    else:
                        lens_focal_length = f"{
                            int(min_length)}-{int(max_length)}mm"
                elif tag_name == "Make":
                    make = value.capitalize()
                elif tag_name == "Model":
                    if value == "ILCE-5100":
                        model = "A5100"
                    elif value == "ILCE-7M3":
                        model = "A7 III"
                    elif value == "ILCE-7M4":
                        model = "A7 IV"
                    else:
                        model = value
                elif tag_name == "FocalLength":
                    shot_focal_length = f"{int(value)}mm"
                elif tag_name == "ISOSpeedRatings":
                    iso = value
                elif tag_name == "ExposureTime":
                    shutter = f"1/{int(1/value)}s"
                elif tag_name == "ApertureValue":
                    aperture = f"f/{apex_to_aperture(value)}"
                elif tag_name == "DateTime":
                    date = datetime.strptime(
                        value, "%Y:%m:%d %H:%M:%S").strftime("%d.%m.%Y")
    except Exception as e:
        print(f"Error opening image: {e}")

    return lens_focal_length, make, model, shot_focal_length, iso, shutter, aperture, date
