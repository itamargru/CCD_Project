from PIL import Image, ImageFilter, ImageChops
import os
import cv2


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

def cropAllFilesInDirectory(input_dir, naming_func, output_dir = None):
    for root, dirs, files in os.walk(input_dir):
        for file_index, file in enumerate(files):
            extension = os.path.splitext(file)
            if extension[1] == '.tif':
                file_path = os.path.join(root, file)
                im = Image.open(file_path)
                cropped = cropImageWhite(im)
                new_file_name =  naming_func(file_path)#'crp_' +str(dir_index) + str(file_index) + '_' + file
                if output_dir == None:
                    cropped.save(os.path.join(root, new_file_name))
                else:
                    cropped.save(os.path.join(output_dir, new_file_name))

class FunctionFileNaming:
    files_class = None

    def FunctionFileNaming(self, files_class):
        self.files_class = files_class

    def __call__(self, file_path):
        dir_path, file = os.path.split(file_path)
        dir_arr = dir_path.split('//')
        if(dir_arr[-1] == ''):
            dir_arr.pop(len(dir_arr)-1)
        return file_path + '_' + dir_arr[-1] + '_' + file


def extractPatchesOutOfImage(image):
    im = cv2.imread()
    thresh = cv2.threshold(im,0,255,cv2.THRESH_BINARY)
    

if __name__ == "__main__":
    root_path = r'/home/itamarg/Pictures/CCD'
    output_dir = r'/home/itamarg/Pictures/'

    positive = 'POS'
    pos_dir = output_dir + positive + '_PDL1'
    positiveNaming = FunctionFileNaming(positive)
    cropAllFilesInDirectory(root_path, positiveNaming, output_dir=pos_dir)

    negative = 'NEG'
    neg_dir = output_dir + negative + '_PDL1'
    negativeNaming = FunctionFileNaming(negative)
    cropAllFilesInDirectory(root_path, negativeNaming, output_dir=neg_dir)




