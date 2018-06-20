#import the necessary modules
import freenect
import cv2
import numpy as np


#funcao para pegar imagem RGB do kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#funcao para pegar a imagem profundidade do kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    #serve para suavizar a captura da profundidade
    #Limitamos o depth para 1023, removendo objetos 
    #muitos distantes e ruidos.
    np.clip(array, 0, 2**10 - 1, array)
    array >>= 2
    #Transforma o array em 8 bit array
    array = array.astype(np.uint8)
    return array
 
if __name__ == "__main__":

    while 1:

        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()
        # print '\n'
        #display RGB image
        cv2.imshow('RGB image',frame)
        #display depth image
        cv2.imshow('Depth image',depth)
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()