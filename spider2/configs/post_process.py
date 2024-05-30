# import operator
import numpy as np
import re
from typing import List
from PIL import Image
import os, uuid, pickle
from dataclasses import dataclass
import sys
from pathlib import Path
here = Path(__file__).absolute().parent.parent
sys.path.append(str(here.parent))

def plot_process(mnt_dir,controller):
    '''
    This function is used to process the plot results
    save the plot information to the /mnt_dir/dabench/plot.pkl
    '''

    plot_path = os.path.join(mnt_dir, 'dabench')
    os.makedirs(plot_path, exist_ok=True)
    # TODO: process the plot results

    plot_path = os.path.join(plot_path, 'plot.pkl')
    return plot_path

