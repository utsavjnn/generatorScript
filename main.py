from PIL import Image
from IPython.display import display
import random
import json
import os

CLASSES_AFFECTING_APPEARANCE = ["WALKING", "RUNNING", "LIFESTYLE", "ALL PURPOSE", "GYM", "BADMINTON", "TENNIS", "SOCCER",
                                "BASKETBALL"] # not sure what all we supporting in start hence the name
TYPES = ["BASIC", "ATHLETE", "PRO ATHLETE", "LEGEND", "SPECIAL EDITION"]
#LEVELS MAYBE IDK
SNEAKER_PARTS = ["LATERAL BASE", "MEDIAL BASE", "LINING", "LATERAL WEBBING", "MEDICAL WEBBING", "LACE", "MIDSOLE",
                 "MIDSOLE TOPLINE", "LOGO", "MEDIAL MIDSOLE ICON", "HEEL LOGO", "TONGUE LABEL"]

SNEAKER_DATA_PATH = "/Users/utsavjn/Desktop/fitmint/nftGenerator/sneaker_data" #change accordingly.
OUTPUT_PATH = "/Users/utsavjn/Desktop/fitmint/nftGenerator/sneaker_output"
#LOCAL IMAGES OR CLOUD OR WHATEVER LINKS TO IMAGES TO BE STORED IN DICT FOR FURTHER OVERLAY

# FOR OUR PURPOSE I THINK WE JUST WANT ALL COMBINATIONS OF SNEAKERS POSSIBLE AND THEIR IPFS/ORACLE URIs

#params(format) --> {
#                       final_name: "xyz"  -> final stored file name will be xyz.png
#                       class: "walking" -> one class --> assuming one sneaker can have only one class
#                       type: "athlete"
#                       sneaker_parts:["LATERAL BASE"...]
#                    }

def create_image(params):
    final_name = params['final_name'].replace(" ", "_")
    class_ = params['class']
    type_ = params['type']
    sneaker_parts = params['sneaker_parts']

    class_image = os.path.join(SNEAKER_DATA_PATH, "classes_affecting_appearance", "{}.png".format(class_.replace(" ", "_").lower()))
    if not os.path.isfile(class_image):
        print("CLASS IMAGE DOESNT EXIST")
        return
    type_image = os.path.join(SNEAKER_DATA_PATH, "types", "{}.png".format(type_.replace(" ", "_").lower()))
    if not os.path.isfile(type_image):
        print("TYPE IMAGE DOESNT EXIST")
        return
    sneaker_parts_images = []
    for part in sneaker_parts:
        part_image = os.path.join(SNEAKER_DATA_PATH, "sneaker_parts", "{}.png".format(part.replace(" ", "_").lower()))
        if not os.path.isfile(part_image):
            print("PART IMAGE DOESNT EXIST", part)
            return
        sneaker_parts_images.append(part_image)

    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    output_file_path = os.path.join(OUTPUT_PATH, "{}.png".format(final_name))
    if os.path.isfile(output_file_path):
        print("SNEAKER WITH THIS FILENAME ALREADY EXISTS", final_name)
        return
    class_img = Image.open(class_image).convert("RGBA")
    type_img = Image.open(type_image).convert("RGBA")
    sneaker_parts_imgs = [Image.open(img).convert("RGBA") for img in sneaker_parts_images]

    composite = Image.alpha_composite(class_img, type_img)
    for part_img in sneaker_parts_imgs:
        composite = Image.alpha_composite(composite, part_img)

    rgb_im = composite.convert("RGB")
    rgb_im.save(output_file_path)

def create_combinations():
# right now only assuming one part per sneaker TODO: Later
    print("---GENERATION STARTED---")
    for class_ in CLASSES_AFFECTING_APPEARANCE:
        for type_ in TYPES:
            for part in SNEAKER_PARTS:
                create_image({
                    "final_name": "{}_{}_{}".format(class_, type_, part),
                    "class": class_,
                    "type": type_,
                    "sneaker_parts": [part,]
                })
    print("---GENERATION FINISHED---")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_combinations()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
