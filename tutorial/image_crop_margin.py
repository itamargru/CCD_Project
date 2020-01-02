from PIL import Image, ImageChops
import utiles_image_manipulation as utiles
import os
import cv2


def cropImageWhite(im, path=None):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    # Bounding box given as a 4-tuple defining the left, upper, right, and lower pixel coordinates.
    # If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


if __name__ == "__main__":

    root_path = r'/home/itamarg/Pictures/BigPatches'
    output_dir = r'/home/itamarg/Pictures/DataMaskRCNN'

    rename_file = utiles.FunctionFileNamingByDirectory("MOD")
    save_image = utiles.FunctionSaveImage(output_dir, rename_file, ".png")
    is_file_tiff = utiles.CheckFileExtention(".tif")
    functions_to_operate = [cropImageWhite, save_image]
    image_transform = utiles.TransformGivenImage(functions_to_operate)
    utiles.operate_function_on_files(image_transform, root_path, is_file_tiff)

