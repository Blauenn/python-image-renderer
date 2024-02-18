from datetime import datetime
from PIL import Image, ExifTags

from apex_convert import apex_to_aperture

lens_focal_length = ""
make = ""
model = ""
date = ""
iso = ""
shutter = ""
aperture = ""


def get_exif_data(file_path):
    global lens_focal_length, make, model, date, iso, shutter, aperture
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "LensSpecification" and isinstance(value, tuple):
                    min_length, max_length, _, _ = value
                    if min_length == max_length:
                        lens_focal_length = int(min_length)
                    else:
                        lens_focal_length = f"{
                            int(min_length)}-{int(max_length)}mm"
                elif tag_name == "Make":
                    make = value
                elif tag_name == "Model":
                    model = value
                elif tag_name == "ISOSpeedRatings":
                    iso = value
                elif tag_name == "ExposureTime":
                    shutter = f"1/{int(1/value)}"
                elif tag_name == "ApertureValue":
                    aperture = apex_to_aperture(value)
                elif tag_name == "DateTime":
                    date = datetime.strptime(
                        value, "%Y:%m:%d %H:%M:%S").strftime("%d.%m.%Y")
    except Exception as e:
        print(f"Error opening image: {e}")

    return lens_focal_length, make, model, date, iso, shutter, aperture
