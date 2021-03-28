import sys
import nibabel as nib
from os.path import exists
from utils import get_orientation, get_task, reorient

if __name__ == '__main__':
    input_path = sys.argv[1]
    if exists(input_path):
        nifti = nib.load(input_path)
        plane = get_orientation(nifti)
        task = get_task(plane)
        print(task)
        if plane == 'cor':
            reorient(input_path)
        