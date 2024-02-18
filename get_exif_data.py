from PIL import Image, ExifTags
from apex_convert import apex_to_aperture


def get_exif_data(file_path):
    global iso_value, shutter_value, aperture_value
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "ISOSpeedRatings":
                    iso_value = value
                elif tag_name == "ExposureTime":
                    shutter_value = f"1/{int(1/value)}"
                elif tag_name == "ApertureValue":
                    aperture_value = apex_to_aperture(value)
    except Exception as e:
        print(f"Error opening image: {e}")

    return iso_value, shutter_value, aperture_value
