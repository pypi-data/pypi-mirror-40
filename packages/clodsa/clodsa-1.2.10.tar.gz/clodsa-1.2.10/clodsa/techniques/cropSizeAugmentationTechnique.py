from technique import AlteringTechnique
import cv2

class cropSizeAugmentationTechnique(AlteringTechnique):

    # percentage is a value between 0 and 1
    # startFrom indicates the starting point of the cropping,
    # the possible values are TOPLEFT, TOPRIGHT, BOTTOMLEFT,
    # BOTTOMRIGHT, and CENTER
    def __init__(self,parameters):
        AlteringTechnique.__init__(self, parameters)
        if 'x' in parameters.keys():
            self.x = int(parameters["x"])
        else:
            raise NameError("Provide x value")
        if 'y' in parameters.keys():
            self.y = int(parameters["y"])
        else:
            raise NameError("Provide y value")
        if 'width' in parameters.keys():
            self.width = int(parameters["width"])
        else:
            raise NameError("Provide width value")
        if 'height' in parameters.keys():
            self.height = int(parameters["height"])
        else:
            raise NameError("Provide height value")


    def apply(self, image):
        crop = image[self.y:self.y+self.height, self.x:self.x+self.width]
        return crop


# Example
# technique = cropAugmentationTechnique(0.5,'TOPRIGHT')
# image = cv2.imread("LPR1.jpg")
# cv2.imshow("original",image)
# cv2.imshow("new",technique.apply(image))
# cv2.waitKey(0)