import argparse
import nibabel as nib
import os
from os.path import exists, join
import shutil

from utils import reorient, get_coord_system


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Separate out kidneys and liver and calculate volumes')
    parser.add_argument('--image_path')
    parser.add_argument('--mask_path')
    parser.add_argument('--output_dir')
    parser.add_argument('--task')
    args = parser.parse_args()

    seg_path = args.mask_path
    image_path = args.image_path
    task = args.task
    output_dir = args.output_dir
    output_path = join(output_dir, 'seg.nii.gz')

    if exists(seg_path):
        os.makedirs(output_dir, exist_ok=True)
        shutil.copyfile(seg_path, output_path)
        if task == 'Task003_coronal':
            coord_system = get_coord_system(image_path)
            seg_path = reorient(output_path, orientation=coord_system, flip_axis=2)