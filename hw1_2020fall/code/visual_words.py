import os
import multiprocessing
from os.path import join, isfile

import numpy as np
from PIL import Image
import scipy.ndimage
import scipy.signal
import skimage.color
from enum import Enum

class Filter(Enum):
  """ 
    Enum containing the types of filters types available
  """
  GAUSSIAN = 1
  LOG = 2
  DOG_X = 3
  DOG_Y = 4

def get_response(img, ftype, scale):
  """
    Gets a filter response
    [input]
    ------
      * img: an array corresponding to one channel of an image
      * ftype: type of filter to apply to img
      * scale: sigma of the filter
    [output]
    --------
      * response of the same size as img 
  """
  if ftype == Filter.GAUSSIAN:
    return scipy.ndimage.gaussian_filter(img, scale, order=0, mode='reflect')
  elif ftype == Filter.LOG:
    return scipy.ndimage.gaussian_laplace(img, scale, mode='reflect')
  elif ftype == Filter.DOG_X:
    r1 = scipy.ndimage.gaussian_filter1d(img, scale, axis=1)
    r2 = scipy.ndimage.gaussian_filter1d(img, 2*scale, axis=1)
    return r2 - r1
  elif ftype == Filter.DOG_Y:
    r1 = scipy.ndimage.gaussian_filter1d(img, scale, axis=0)
    r2 = scipy.ndimage.gaussian_filter1d(img, 2*scale, axis=0)
    return r2 - r1

def extract_filter_responses(opts, img):
  '''
    Extracts the filter responses for the given image.

    [input]
    * opts    : options
    * img    : numpy.ndarray of shape (H,W) or (H,W,3)
    [output]
    * filter_responses: numpy.ndarray of shape (H,W,3F)
  '''
  # Check if the image is floating point type and in range [0, 1]
  # Solve this later
  if img.dtype != np.float32:
      if img.dtype.kind == 'u':
          img = img.astype(np.float32) / np.iinfo(img.dtype).max
      # ---- TODO : handle this later
      else:
          print("Unsupported conversion")
          return 0

  # Check if image is grayscale, if so, convert it into three channel image
  if len(img.shape) == 2:
    img = np.array([img, img, img])
    img = np.moveaxis(img, 0, 2)

  # Convert image from RGB to Lab
  img = skimage.color.rgb2lab(img)
  
  filter_scales = opts.filter_scales
  filter_responses = np.ones(
    (img.shape[0], img.shape[1], len(Filter) * len(filter_scales) * img.shape[2]))
  
  i = 0
  for fscale in filter_scales:
    for ftype in Filter:
      for c in range(img.shape[2]):
        filter_responses[:, :, i] = get_response(img[:, :, c], ftype, fscale)
        i += 1
        
  return filter_responses


def compute_dictionary_one_image(args):
    '''
    Extracts a random subset of filter responses of an image and save it to disk
    This is a worker function called by compute_dictionary

    Your are free to make your own interface based on how you implement compute_dictionary
    '''

    # ----- TODO -----
    pass


def compute_dictionary(opts, n_worker=1):
    '''
    Creates the dictionary of visual words by clustering using k-means.

    [input]
    * opts         : options
    * n_worker     : number of workers to process in parallel

    [saved]
    * dictionary : numpy.ndarray of shape (K,3F)
    '''

    data_dir = opts.data_dir
    feat_dir = opts.feat_dir
    out_dir = opts.out_dir
    K = opts.K

    train_files = open(join(data_dir, 'train_files.txt')).read().splitlines()
    # ----- TODO -----
    pass

    # example code snippet to save the dictionary
    # np.save(join(out_dir, 'dictionary.npy'), dictionary)


def get_visual_words(opts, img, dictionary):
    '''
    Compute visual words mapping for the given img using the dictionary of visual words.

    [input]
    * opts    : options
    * img    : numpy.ndarray of shape (H,W) or (H,W,3)

    [output]
    * wordmap: numpy.ndarray of shape (H,W)
    '''

    # ----- TODO -----
    pass
