# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018 Jeff Maggio, Nathan Dileas, Ryan Hartzell
import numpy as np
from PIL import Image
from .error_checking import dtype_type_check
from .imports import import_opencv
cv2 = import_opencv()

def normalize_and_bin(src, max_count=255, cast_type=np.uint8):
    """normalizes and bins an image

    normalizes and bins the bins the input image to a given bit depth
    and max_count

    Args:
        src (np.ndarray): input image
        max_count (int,float): max value in output image
        cast_type (numpy.dtype): np.dtype the final array is casted to

    Returns:
        np.ndarray: normalized and binned image

    """
    assert isinstance(src, np.ndarray), "'src' must be np.ndarray"
    assert isinstance(max_count, (int, float)), "'max_count' must be number"
    dtype_type_check(cast_type)

    img = norm_ab(src, 0, max_count).astype(cast_type)
    return img


def quick_image_view(img, normalize_and_bin=False, title="quick view image"):
    """
    quickly displays the image using a PIL Image Viewer
    (which uses ImageMagick over X11 -- this will work over ssh)

    Args:
        img (np.ndarray): input image you want to view
        normalize_and_bin (bool, optional): Defaults to False
            boolean value indicating whether or not to normalize
            and bin the image
        title (str, optional): title for the image window.
            Default is 'quick view image'

    Returns:
        None
    """
    assert isinstance(img, np.ndarray), "'img' must be a np array or subclass"
    assert isinstance(normalize_and_bin, int), "'normalize_and_bin' must be int"
    assert isinstance(title, str), "'title' must be a string"

    if normalize_and_bin:
        img = norm_ab(img, 0, 255)

    if len(img.shape) > 2:
        img = np.flip(img, 2)

    img = img.astype(np.uint8)
    img = Image.fromarray(img)
    img.show(title)


def number_image(img, num):
    """Adds a number to the corner of an image

    Args:
        img (np.ndarray): image
        num (int,str): number to put in the corner of the image

    Returns:
        np.ndarray: numbered image
    """
    r,c,b,_ = dimensions(img)
    loc = int( min(r,c) * .95 )
    color = (255,255,255)
    if np.mean(img[int(.9*r):r,int(.9*c):c]) > 128:
        color = (0,0,0)

    img = cv2.putText(img,
                        text=str(num),
                        org=(loc,loc),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=.5,
                        color=color,
                        thickness=2,
                        bottomLeftOrigin=False)

    return img

def centroid(img):
    """finds the centroid of the given image img

    Args:
        img (np.ndarray):
            input img to find the centroid of
    Returns:
        tuple: centroid of the input image (height,width)

    Example:
        >>> import imagepypelines as ip
        >>> lenna_centroid = centroid( ip.lenna() )
    """
    assert isinstance(img, np.ndarray), "'img' must be a np array or subclass"

    centroid = img.shape[0]//2, img.shape[1]//2
    return centroid


def frame_size(img):
    """return the height and width of a given img

    Args:
        img (np.ndarray): input img to find frame_size of

    Returns:
        tuple: frame_size, height and width of the input img

    Example:
        >>> import imagepypelines as ip
        >>> lenna_framesize = frame_size( ip.lenna() )
    """
    assert isinstance(img, np.ndarray), "'img' must be a np array or subclass"

    frame_size = img.shape[0], img.shape[1]
    return frame_size


def dimensions(img, return_as_dict=False):
    """
    function which returns the dimensions and data_type of a given image

    Args:
        img (np.ndarray): input image
        return_as_dict (bool): whether or not to return a dictionary.
            Default is False

    Returns:
        tuple: dimensions of the form (rows, cols, bands, dtype)

    Example:
        >>> import imagepypelines as ip
        >>> dims = dimensions( ip.lenna() )
    """
    assert isinstance(img, np.ndarray), "'img' must be a np array or subclass"

    rows = img.shape[0]
    cols = img.shape[1]
    if img.ndim == 3:
        bands = img.shape[2]
    else:
        bands = 1
    dims = (rows, cols, bands, img.dtype)

    if return_as_dict:
        dims = dict(zip(('rows','cols','bands','dtype'), dims))

    return dims

def norm_01(img):
    """ Normalize img to the range [0, 1], inclusive.

    Args:
        img (np.ndarray): image to normalize, can be any dtype.

    Returns:
        np.ndarray: normalized image, dtype=np.float64
    """
    assert isinstance(img, np.ndarray), "'img' must be a np array or subclass"

    img_out = img.astype(np.float64)
    img_out = (img_out - img_out.min()) / (img_out.max() - img_out.min())

    return img_out


def norm_ab(img, a, b):
    """ Normalize img to the range [a, b], inclusive. Float output by default.

    If a < b, then the histogram will just be scaled and shifted.
    If b > a, then the histogram will be flipped left-right, scaled, and shifted.

    Args:
        img (np.ndarray): image to normalize, can be any dtype.
        a (float): one end of range
        b (float): other end of range

    Returns:
        np.ndarray: normalized image, dtype=np.float64
    """
    assert isinstance(img, np.ndarray), "'img' must be a np array or subclass"

    img_out = norm_01(img)
    # scale to the extent of the range, then shift to match
    img_out = (img_out * (b - a)) + a

    return img_out


def norm_dtype(img, dtype=np.uint8):
    """ Normalize img to the range [dtype_min, dtype_max].

    Can be used to prepare images for file output.
    Equivalent to a 0% histogram stretch.
    Works by converting to float64, then stretching/shifting, then quantizing.

    Args:
        img (np.ndarray): image to normalize, can be any dtype.
        dtype (np dtype): integer datatype to normalize to.

    Returns:
        np.ndarray: normalized image, dtype=dtype
    """
    assert isinstance(img, np.ndarray), "'img' must be a np array or subclass"

    dtype_info = np.iinfo(dtype)

    return norm_ab(img, dtype_info.min, dtype_info.max).astype(dtype)
