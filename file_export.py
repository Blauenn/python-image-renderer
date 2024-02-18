def file_export(file_name, print_info):
    with open("example.txt", "w") as file:
        file.write(f"File name : {file_name}\n")
        file.write("\n")
        file.write(f"Focal length : {print_info["lens_focal_length"]}\n")
        file.write(f"Make : {str(print_info["make"]).capitalize()}\n")
        file.write(f"Model : {print_info["model"]}\n")
        file.write("\n")
        file.write(f"ISO : {print_info["iso"]}\n")
        file.write(f"Shutter speed : {print_info["shutter_speed"]}\n")
        file.write(f"Aperture : {print_info["aperture"]}\n")
        file.write("\n")
        file.write(f"Date : {print_info["date"]}\n")
        if print_info["venue"] != "":
            file.write(f"Event : {print_info["venue"]} {
                print_info["venue_extra"]}\n")
        file.write("\n")
        if print_info["facebook"] != "":
            file.write(f"Facebook : {print_info["facebook"]}\n")
        if print_info["instagram"] != "":
            file.write(f"Instagram : {print_info["instagram"]}\n")
