
from PIL import Image
import pandas as pd
import skimage
import os

class CVConfig():
    '''
    Define your constants below.

    DIRECTORY_PATH - directory that contains your .tif bestFocus images (usually the bestFocus folder)
    CHANNEL_PATH - path to your channels file (usually called channelNames.txt). Only used for tif images with more than 3 channels, or 4D TIF images.
    NUCLEAR_CHANNEL_NAME - name of nuclear stain (corresponding to channelNames.txt).  Case sensitive.  Only used for tif images with more than 3 channels, or 4D TIF images.
    GROWTH_PIXELS - number of pixels from which to grow out from the nucleus to define a cell boundary.  Change based on tissue types.
    OUTPUT_METHOD - (imagej_text_file, statistics, visual_image_output, visual_overlay_output, all)
    BOOST - multiplier with which to boost the pixels of the nuclear stain before inference
    MODEL_DIRECTORY - path to save logs to (not important)
    MODEL_PATH - path that contains your .h5 saved weights file for the model
    OVERLAP - amount of pixels overlap with which to run the stitching algorithm. Must be divisible by 2, and should be > cell diameter
    INCREASE_FACTOR - Amount with which to boost the size of the image. 2.5X works quite well after training on the Kaggle dataset.

    ---------OUTPUT PATHS-------------
    IMAGEJ_OUTPUT_PATH - path to output imagej .txt files
    QUANTIFICATION_OUTPUT_PATH - path to output .csv and .fcs quantifications
    VISUAL_OUTPUT_PATH - path to output visual masks as pngs.

    Note:  Unfortunately, ImageJ provides no way to export to the .roi file format needed to import into ImageJ.  Additionally, we can't
    use numpy in ImageJ scripts.  Thus, we need to write to file and read in (using the included imagej.py script) using the ImageJ
    scripter if we pick output to imagej_text_file
    '''
    # Change these!
    target = '/media/TitanRAID/CHRISTIAN/COLLABORATIONS/XIANGYUE_ZHANG/20190613_6spleens_mc_processed'

    root = os.path.dirname(os.path.realpath(__file__))

    # target = 
    DIRECTORY_PATH = os.path.join(target, 'bestFocus')
    CHANNEL_PATH = os.path.join(target, 'channelNames.txt')
    NUCLEAR_CHANNEL_NAME = 'DRAQ5'
    GROWTH_PIXELS = 0
    OUTPUT_METHOD = 'all'
    BOOST = 'auto'

    # Usually not changed
    MODEL_DIRECTORY = os.path.join(root, 'modelFiles')
    MODEL_PATH = os.path.join(root, 'src', 'modelFiles', 'final_weights.h5')
    IMAGEJ_OUTPUT_PATH = os.path.join(root, 'output', 'imagej_files')
    QUANTIFICATION_OUTPUT_PATH = os.path.join(root, 'output', 'quantifications')
    VISUAL_OUTPUT_PATH = os.path.join(root, 'output', 'visual_output')
    OVERLAP = 80
    INCREASE_FACTOR = 2.5

    # Probably don't change this, unless you are g0d.
    def __init__(self):
        self.CHANNEL_NAMES = pd.read_csv(
            self.CHANNEL_PATH, sep='\t', header=None).values[:, 0]

        VALID_IMAGE_EXTENSIONS = ('tif', 'jpg', 'png')
        self.FILENAMES = [f for f in os.listdir(self.DIRECTORY_PATH) if f.endswith(
            VALID_IMAGE_EXTENSIONS) and not f.startswith('.')]
        if len(self.FILENAMES) < 1:
            raise NameError(
                'No image files found.  Make sure you are pointing to the right directory')

        self.N_DIMS, self.EXT, self.DTYPE, self.SHAPE, self.BOOST, self.READ_METHOD = cvutils.meta_from_image(os.path.join(
            self.DIRECTORY_PATH, self.FILENAMES[0]), SELF.BOOST)
