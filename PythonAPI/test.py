# took from: https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoDemo.ipynb

import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
from pycocotools.coco import COCO
import os

dir = r'/home/itamarg/Downloads/'
file = r'via_export_coco.json'
file_path = os.path.join(dir, file)
coco = COCO(file_path)


# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))

nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

catIds = coco.getCatIds(catNms=['pos', 'neg'])
imgIds = coco.getImgIds(catIds=catIds)
img = coco.loadImgs(int(imgIds[0]))[0]

img_path = r'/home/itamarg/Pictures/DataMaskRCNN/MOD_1M16_19.06.2019_12.02.59 - Annotation 3.png'

I = io.imread(img_path)
plt.axis('off')
plt.imshow(I)
plt.show()

plt.imshow(I); plt.axis('off')
annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
anns = coco.loadAnns(annIds)
coco.showAnns(anns)

