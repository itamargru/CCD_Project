from PIL import Image, ImageFilter, ImageChops
import os


def hpfOnCellImage():
    cell = Image.open('/home/itamarg/Downloads/1M03_Default_Extended.tif')

    cell_sharpen = cell.filter(ImageFilter.UnsharpMask(8))
    cell_diff = ImageChops.difference(cell, cell_sharpen)

    cell_diff.show()

def cropImageWhite(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    # Bounding box given as a 4-tuple defining the left, upper, right, and lower pixel coordinates.
    # If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def cropAllFilesInDirectory(root, files):
    for file in files:
        extension = os.path.splitext(file)
        if extension[1] == '.tif':
            file_path = os.path.join(root, file)
            im = Image.open(file_path)
            cropped = cropImageWhite(im)
            new_file_name = 'crp_' + file
            cropped.save(os.path.join(root, new_file_name))


if __name__ == "__main__":
    root_path = r'/home/itamarg/Pictures/CCD'
    for root, dirs, files in os.walk(root_path):
        cropAllFilesInDirectory(root, files)
