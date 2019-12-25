import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

class Patch:
    x = 0
    y = 0
    width = 0
    height = 0
    is_fit = False

    def __init__(self, x, y, width, height, is_fit):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_fit = is_fit

    def __repr__(self):
        return 'Patch({},{},{},{}.{})'.format(self.x, self.y , self.width, self.height, self.is_fit)



class AutoCrop:
    crop_size = 0
    threshold = 50
    stride = -1

    def __init__(self, crop_size=215, threshold=50, stride=-1):
        self.crop_size = crop_size
        self.threshold = threshold
        if stride <= 0:
            self.stride = self.crop_size
        else:
            self.stride = stride

    def crop(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        # N = 8
        # kernel = np.ones((N, N), np.float32) / N**2
        # gray = cv2.filter2D(gray, -1, kernel)

        ret, mask = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY_INV)

        # plt.imshow(mask)
        # plt.show()
        patches = self.get_cropping_area(img, mask)
        patches_img = []
        for index, patch in enumerate(patches) :
            cropped = img[patch.x: (patch.x + patch.width), patch.y: (patch.y + patch.height)]
            patches_img.append(cropped)
        return patches_img


    def get_cropping_area(self, img, mask):
        width, height, _ = img.shape
        patches = []
        is_fit = False
        i=0
        pixel_y = 0
        while True:
            pixel_x = 0
            while True:
                if pixel_x + self.crop_size > width:
                    break

                count_white = cv2.countNonZero(
                    mask[pixel_x:(pixel_x + self.crop_size), pixel_y:(pixel_y + self.crop_size)])
                ratio = count_white / self.crop_size ** 2
                if ratio > 0.95:
                    patch = Patch(pixel_x, pixel_y, self.crop_size, self.crop_size, True)
                    print(str(i) + ': ' + repr(patch))
                    i += 1
                    patches.append(patch)
                    # plt.imshow(mask[pixel_y:(pixel_y + self.crop_size), pixel_x:(pixel_x + self.crop_size)])
                    # plt.show()

                pixel_x += self.stride

            if pixel_y + self.crop_size > height:
                break
            pixel_y += self.stride

        return patches

def cropAllFilesInDirectory(input_dir, naming_func, output_dir=None):
    AP = AutoCrop(256, 250, 40)
    for root, dirs, files in os.walk(input_dir):
        for file_index, file in enumerate(files):
            extension = os.path.splitext(file)
            if extension[1] == '.tif':
                file_path = os.path.join(root, file)
                img = cv2.imread(file_path)
                patches = AP.crop(img)
                for index, patch in enumerate(patches):
                    new_file_name = naming_func(file_path, index)
                    if output_dir is None:
                        cv2.imwrite(os.path.join(root, new_file_name), patch)
                    else:
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        cv2.imwrite(os.path.join(output_dir, new_file_name), patch)

class FunctionFileNaming:
    files_class = None


    def __init__(self, files_class):
        self.files_class = files_class

    def __call__(self, file_path, index):
        dir_path, file = os.path.split(file_path)
        dir_arr = dir_path.split(r'/')
        file_name, file_ext = os.path.splitext(file)
        if dir_arr[-1] == '':
            dir_arr.pop(len(dir_arr)-1)
        return dir_arr[-1] + '_' + str(index) + file_ext

if __name__ == "__main__":
    input_dir = r'/home/itamarg/Pictures/bigAnnotations2Crop'
    naming_func = FunctionFileNaming('')
    output_dir = r'/home/itamarg/Pictures/PDL1_Cropped/PDL1_patches'
    cropAllFilesInDirectory(input_dir, naming_func, output_dir)