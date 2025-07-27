# from PIL import Image
# import piexif
#
# def extract_exif(path):
#     try:
#         img = Image.open(path)
#         exif_dict = piexif.load(img.info['exif'])
#         for ifd_name in exif_dict:
#             print(f"\n-- {ifd_name} --")
#             for tag in exif_dict[ifd_name]:
#                 try:
#                     tag_name = piexif.TAGS[ifd_name][tag]["name"]
#                     value = exif_dict[ifd_name][tag]
#                     print(f"{tag_name}: {value}")
#                 except KeyError:
#                     continue
#     except KeyError:
#         print("No EXIF data found in this image.")
#     except Exception as e:
#         print(f"Error: {e}")
#
# # Example usage
# extract_exif("/home/kavita/LegalExpose/Camera/Camera.jpg")  # Replace with your file name

from PIL import Image
import piexif

def extract_exif(path):
    try:
        img = Image.open(path)
        exif_dict = piexif.load(img.info['exif'])
        exif_data = {}

        for ifd_name in exif_dict:
            for tag in exif_dict[ifd_name]:
                try:
                    tag_name = piexif.TAGS[ifd_name][tag]["name"]
                    value = exif_dict[ifd_name][tag]
                    exif_data[f"{ifd_name}::{tag_name}"] = value
                except KeyError:
                    continue

        return exif_data

    except KeyError:
        print("No EXIF data found in this image.")
        return {}

    except Exception as e:
        print(f"Error: {e}")
        return {}

