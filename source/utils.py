import numpy as np
import nibabel as nib
import os
from os.path import exists, dirname, join
from nipype.interfaces.image import Reorient

def get_orientation(nifti):
    """Reorient coronal nifties to RAS (->right, ->anterior, ->superior) orientation scheme"""
    coordinates = nib.aff2axcodes(nifti.affine)
    volume_shapes = nifti.header['dim'][1:4]
    minimal_index = np.argmin(volume_shapes)
    if coordinates[minimal_index] in ['S', 'I']:
        plane = 'ax'
    elif coordinates[minimal_index] in ['A', 'P']:
        plane = 'cor'
    else:
        print('Error, image in sagittal plane - no sagittal model')
        plane = ''
    return plane

def get_coord_system(nifti_path):
    nifti = nib.load(nifti_path)
    coordinates = nib.aff2axcodes(nifti.affine)
    coord_system = ''.join(coordinates)

    return coord_system

def get_task(plane):
    """returns name of task which was different for axial and coronal modes""" 
    if plane == 'ax':
        return 'Task002_Kidney'
    else:
        return 'Task003_coronal'

def flip_nifti(input_path, save_path, axis=1):
    nifti = nib.load(input_path)
    matrix = nifti.get_fdata()
    new_matrix = np.flip(matrix, axis=axis).astype(np.uint16)
    new_nifti = nib.Nifti1Image(new_matrix, header=nifti.header, affine=nifti.affine)
    nib.save(new_nifti, save_path)

def reorient(nifti_path, orientation='RAS', flip_axis=1):
    """The coronal model was trained on data from Groningen in RAS coordinate system, but standard nifties are always LPS"""
    reorient = Reorient(orientation=orientation)
    reorient.inputs.in_file = nifti_path
    res = reorient.run()
    reoriented_path = res.outputs.out_file
    flip_nifti(reoriented_path, nifti_path, axis=flip_axis)
    os.remove(reoriented_path)