from PIL import Image
import os

def operate_function_on_files(func_to_operate, input_dir, is_file_to_operate):
    for root, dirs, files in os.walk(input_dir):
        for file_index, file in enumerate(files):
            if is_file_to_operate(root, file):
                func_to_operate(root, file)


class CheckFileExtention:
    extensionToFind = ""

    def __init__(self, extension):
        if not extension.startswith("."):
            extension = "." + extension
        self.extensionToFind = extension

    def __call__(self, root, file):
        _, extension = os.path.splitext(file)
        if extension == self.extensionToFind:
            return True
        return False


class TransformGivenImage:
    functions = []
    image = []

    def __init__(self, functions_list):
        self.functions = functions_list

    def __call__(self, root, file):
        file_path = os.path.join(root, file)
        self.image = Image.open(file_path)
        file_path = os.path.join(root, file)
        for function in self.functions:
            self.image = function(self.image, file_path)
        return self.image


class FunctionFileNamingByDirectory:
    files_class = None

    def __init__(self, files_class=None):
        self.files_class = files_class

    def __call__(self, file_path):
        dir_path, file = os.path.split(file_path)
        dir_arr = dir_path.split(r'/')
        if dir_arr[-1] == '':
            dir_arr.pop(len(dir_arr) - 1)
        if self.files_class is None:
            return dir_arr[-1]
        return self.files_class + '_' +  dir_arr[-1]


class FunctionSaveImage:
    extension = ""
    output_dir = ""
    renaming_function = None

    def __init__(self, output_dir, renaming_function=None, image_extension="png"):
        self.extension = image_extension
        self.output_dir = output_dir
        self.renaming_function = renaming_function

    def __call__(self, image, input_file_path):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        _, file_name = os.path.split(input_file_path)
        file_name, _ = os.path.splitext(file_name)
        file_name = self.renaming_function(input_file_path)
        file_name = str(file_name) + self.extension
        image.save(os.path.join(self.output_dir, file_name))
