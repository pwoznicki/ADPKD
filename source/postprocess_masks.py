import argparse
import nibabel as nib
import numpy as np
from scipy import ndimage
from scipy.ndimage.measurements import center_of_mass
import os
from os.path import join, exists, dirname
import json


def get_voxel_volume(mask_nifti):
    '''return volume of single volume, in ml'''
    voxel_vol = mask_nifti.header['pixdim'][1] * mask_nifti.header['pixdim'][2] * mask_nifti.header['pixdim'][3]
    return voxel_vol / 1000

def calculate_volume(nifti_path):
    '''returns volume of a given .nii.gz segmentation, in ml'''
    mask_nifti = nib.load(nifti_path)
    pixelnum = np.sum(mask_nifti.get_fdata())
    volume = pixelnum * get_voxel_volume(mask_nifti)
    return np.round(volume, 2)

def is_right_kidney(nifti_mask, center):
	LR_direction = nib.aff2axcodes(nifti_mask.affine)[0]
	matrix = nifti_mask.get_fdata()
	midline = matrix.shape[0] / 2
	assert(LR_direction in ['L', 'R'])
	if center[0] < midline:
		if LR_direction == 'R':
			right = False
		else:
			right = True
	else:
		if LR_direction == 'R':
			right = True
		else:
			right = False
	
	return right       

def separate_kidneys_and_liver(mask_path):
	if exists(mask_path):
		out_dir = dirname(mask_path)
		os.makedirs(out_dir, exist_ok=True)
		mask = nib.load(mask_path)
		matrix = mask.get_fdata()
		print(matrix.shape)
		separate_matrix = {}
		#kidneys are always labeled with label=1 (liver, if present, with label=2)
		separate_matrix['both_kidneys'] = (matrix == 1)
		separate_matrix['left_kidney'] = np.zeros(matrix.shape)
		separate_matrix['right_kidney'] = np.zeros(matrix.shape)
		separate_matrix['liver'] = (matrix == 2)
		labels, num_labels = ndimage.label(separate_matrix['both_kidneys']) 
		lkv, rkv = 0, 0
		for i in range(1, num_labels+1):
			if is_right_kidney(mask, center_of_mass(labels == i)):
				separate_matrix['right_kidney'][labels == i] = 1    
			else:
				separate_matrix['left_kidney'][labels == i] = 1    
		for organ in separate_matrix.keys():
			print(organ, str(np.sum(separate_matrix[organ])))
			if not np.sum(separate_matrix[organ]) == 0:
				new_mask = nib.Nifti1Image(separate_matrix[organ], affine=mask.affine, header=mask.header)
				nib.save(new_mask, join(out_dir, organ+'.nii.gz'))

def create_json(dirpath):
	organs = ['both_kidneys', 'left_kidney', 'right_kidney', 'liver']
	results = {}
	for organ in organs:
		mask_path = join(dirpath, organ + '.nii.gz')
		if exists(mask_path):
			volume = calculate_volume(mask_path)
			results[organ] = {}
			results[organ]['volume'] = str(volume) + ' ml'
		else:
			results[organ] = 'not measured'

	json_savepath = join(dirpath, 'results.json')
	with open(json_savepath, 'w') as f:
		json.dump(results, f, indent=4)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Separate out kidneys and liver and calculate volumes')
	parser.add_argument('--prediction_dir')
	args = parser.parse_args()

	prediction_dir = args.prediction_dir
	mask_path = join(prediction_dir, 'seg.nii.gz')
	separate_kidneys_and_liver(mask_path)
	create_json(prediction_dir)