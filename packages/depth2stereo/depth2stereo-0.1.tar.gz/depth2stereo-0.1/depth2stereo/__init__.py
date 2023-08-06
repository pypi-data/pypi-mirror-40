import os
from PIL import Image
import numpy as np
from scipy import misc
import subprocess
from skimage.transform import warp_coords, warp
from skimage.io import imsave, imread
from scipy.ndimage import map_coordinates
from shutil import copyfile

left_path = "temp/left.jpg"
right_path = "temp/right.jpg"
stereo_path = "temp/stereo.jpg"


def _get_percent(rgb):
    return float(rgb[0])/255

def _create_one_eye_image(is_left, input_path, depth_path, distortion_rate):
    warped_image = _get_warped_image(is_left, input_path, depth_path, distortion_rate)
    o_path = _get_one_eye_image_path(is_left)
    imsave(o_path, warped_image)

def _get_one_eye_image_path(is_left):
    if(is_left): return left_path
    return right_path

def _get_warped_image(is_left, single_photo, depth_map, distortion_rate):
    image = np.array(single_photo)
    shifted = _get_shifted_coords2(depth_map, is_left, distortion_rate)
    def shift_function(xy):
        return shifted
    coords = warp_coords(shift_function, image.shape)
    warped_image = map_coordinates(image, coords, prefilter=False)
    return warped_image

def _get_shifted_coords2(im, is_left, distortion_rate):
    #distortion_rate = 5
    after = []
    depth_pix = np.array(im)
    w, h = im.size
    if is_left: distortion_rate*=-1
    rows = w
    cols = h
    i = 0
    #todo refactor/performance
    for y in range(0, rows):
        for x in range(0, cols):
            i+=1
            depth = depth_pix[x,y]
            depth = _get_percent(depth)
            magic_number = 800
            move_by_x_pixels = 1/depth * distortion_rate * (w+h)/magic_number
            target_position_y = y-move_by_x_pixels
            after.append([target_position_y,x])
    after = np.array(after).astype(np.float64)
    return after
     

def _merge_left_and_right():
    os.system("convert +append "+left_path+" "+right_path+" "+stereo_path)

#returns PIL Image
#i => input image as PIL Image
#d -> depth map as PIL Image
#distortion rate -> warping rate, ideally value between 0 to 2 (float)
def generate_stereo_pair(i, d, distortion_rate):
    mkdir("temp")
    _create_one_eye_image(True, i, d, distortion_rate)
    _create_one_eye_image(False, i, d, distortion_rate)
    _merge_left_and_right()
    return Image.open(stereo_path)
    
    

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
