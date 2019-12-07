from PIL import Image, ImageFilter, ImageChops

cell = Image.open('/home/itamarg/Downloads/1M03_Default_Extended.tif')


cell_sharpen =cell.filter( ImageFilter.UnsharpMask(8) )
cell_diff = ImageChops.difference(cell, cell_sharpen)


cell_diff.show()