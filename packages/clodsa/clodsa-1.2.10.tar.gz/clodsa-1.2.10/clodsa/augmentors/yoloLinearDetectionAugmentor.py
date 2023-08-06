from iaugmentor import IAugmentor
from imutils import paths
import os
import cv2
from sklearn.externals.joblib import Parallel, delayed
import xml.etree.ElementTree as ET
from utils import prettify



def readAndGenerateImage(outputPath, generators, i_and_imagePath):

    (i, imagePath) = i_and_imagePath
    image = cv2.imread(imagePath)
    (hI, wI) = image.shape[:2]
    name = imagePath.split(os.path.sep)[-1]
    labelPath = '/'.join(imagePath.split(os.path.sep)[:-1]) + "/"+name[0:name.rfind(".")] + ".txt"
    lines = [line.rstrip('\n') for line in open(labelPath)]
    #if(len(objects)<1):
    #    raise Exception("The xml should contain at least one object")
    boxes = []
    if lines != ['']:
        for line in lines:
            components = line.split(" ")
            category = components[0]
            x  = int(float(components[1])*wI - float(components[3])*wI/2)
            y = int(float(components[2])*hI - float(components[4])*hI/2)
            h = int(float(components[4])*hI)
            w = int(float(components[3])*wI)
            boxes.append((category, (x, y, w, h)))
    for (j, generator) in enumerate(generators):
        (newimage, newboxes) = generator.applyForDetection(image, boxes)
        (hI, wI) = newimage.shape[:2]

        if newboxes is not None:
            cv2.imwrite(outputPath + "/" + str(i) + "_" + str(j) + "_" + name,
                        newimage)


            file = open(outputPath + "/" + str(i) + "_" + str(j) + "_" + name[0:name.rfind(".")]+".txt", "w")
            for box in newboxes:
                (category, (x, y, wb, hb)) = box
                file.write(category + " " + str(float(x+wb/2)/wI) + " " + str(float(y+hb/2)/hI) + " " + str(float(wb)/wI) + " " + str(float(hb)/hI)+ "\n")
            file.close()
        else:
            file = open(outputPath + "/" + str(i) + "_" + str(j) + "_" + name[0:name.rfind(".")] + ".txt", "w")
            file.close()


    #
# # This class serves to generate images for a detection
# # problem where all the images in the given folder using the JPG format, and the labels
# # are given in the same folder with the same name and using the YOLO format.
# # Example:
# # - Folder
# # |- image1.jpg
# # |- image1.txt
# # |- image2.jpg
# # |- image2.txt
# # |- ...
# #
#
class yoloLinearDetectionAugmentor:

    def __init__(self,inputPath,parameters):
        IAugmentor.__init__(self)
        self.inputPath = inputPath
        # output path represents the folder where the images will be stored
        if parameters["outputPath"]:
            self.outputPath = parameters["outputPath"]
        else:
            raise ValueError("You should provide an output path in the parameters")

        self.generators = []

    def addGenerator(self, generator):
        self.generators.append(generator)

    def readImagesAndAnnotations(self):
        self.imagePaths = list(paths.list_files(self.inputPath,validExts=(".jpg", ".jpeg")))
        self.labelPaths = list(paths.list_files(self.inputPath,validExts=(".txt")))
        if (len(self.imagePaths) != len(self.labelPaths)):
            raise Exception("The number of images is different to the number of annotations")

    def applyAugmentation(self):
        self.readImagesAndAnnotations()
        Parallel(n_jobs=-1)(delayed(readAndGenerateImage)(self.outputPath,self.generators,x) for x in enumerate(self.imagePaths))


#
# # Example
# augmentor = yoloLinearDetectionAugmentor(
#     "/home/joheras/datasets/estomas-yolo/",
#     {"outputPath": "/home/joheras/datasets/estomas-yolo/"}
# )
#
# from ..techniques.averageBlurringAugmentationTechnique import averageBlurringAugmentationTechnique
# from techniques.bilateralBlurringAugmentationTechnique import bilateralBlurringAugmentationTechnique
# from techniques.gaussianNoiseAugmentationTechnique import gaussianNoiseAugmentationTechnique
# from techniques.rotateAugmentationTechnique import rotateAugmentationTechnique
# from ..techniques.flipAugmentationTechnique import flipAugmentationTechnique
# from techniques.noneAugmentationTechnique import noneAugmentationTechnique
# from generator import Generator
# import time
# augmentor.addGenerator(Generator(noneAugmentationTechnique()))
# augmentor.addGenerator(Generator(averageBlurringAugmentationTechnique()))
# augmentor.addGenerator(Generator(bilateralBlurringAugmentationTechnique()))
# augmentor.addGenerator(Generator(gaussianNoiseAugmentationTechnique()))
# augmentor.addGenerator(Generator(rotateAugmentationTechnique()))
# augmentor.addGenerator(Generator(flipAugmentationTechnique()))
# start = time.time()
# augmentor.applyAugmentation()
# end = time.time()
# print(end - start)
