import numpy as np
import pandas as pd
import nibabel as nib
from os.path import join, exists
import os
import random

BASE_PATH = '/home/woznicki/prostate/smart_data'

ids = {}
ids['train'] = {}
#leave out: 64, 4, 42465432, 117
#has no PZ: 422
ids['train']['munich'] = ['82', '424', '15', '80', '78', '136', '133', '21', 
    '186', '105', '205', '104', '375', '318', '449', '450', '399', '236', 
    '112', '343', '44', '264', '106', '74', '396', '433', '387', '354', '24', 
    '251', '296', '3', '47', '313', '235', '120', '358', '331', '67', 
    '467', '69', '278', '116', '140', '8', '29', '276', '45', '154', '12', 
    '280', '123', '127', '427', '100', '6', '404', '98', '48', '397', '148', 
    '19', '139', '271', '234', '66', '22', '323', '409', '413', '270', '430', 
    '312', '348', '290', '20', '213', '269', '458', '184', '327', '57', '322',
    '146', '345', '394', '77', '315', '389', '196', '243', '232', '33', '339', 
    '107', '308', '113', '256', '326', '25', '275', '96', '93', '26', '374', 
    '258', '37', '435', '51', '223', '324', '328', '83', '71', '85', '395', 
    '329', '16', '425', '11', '210', '301', '282', '62', '373', '198', '362']

ids['test'] = {}
ids['test']['munich'] = ['52', '346', '353', '268', '9']

ids['train']['mannheim'] = ['42206381', '42275272', '42270074', '42421025', 
    '42416638', '40469708', '42192440', '42268841', '38807089', '41428382', 
    '42414865', '41043434', '42246932', '42474664', '42231307', '42301949', 
    '42084176', '41084646', '42024831', '37991413', '42287018', '42300752',  
    '42384333', '42476204', '41469681', '42472675', '40427341', '41144828', 
    '42413567', '40100707', '42303722', '42364837', '40415152', '42100725', 
    '42130844', '42465432', '42219315', '42010918', '42318634', '40461243', 
    '42288876', '42463744', '42085543', '42273180', '42288871', '42260750', 
    '42400045', '41490758', '42370136', '42300643', '42143677', '41013789', 
    '41334801', '42169994', '42264870', '42412192', '42426031', '41450801', 
    '41433200', '41376001', '42283594', '42425116', '42028505', '41209508', 
    '42413485', '41432699', '42272264', '41193976', '40465462', '42369521', 
    '42354460', '40367447', '42322037', '42375739', '42376962', '38055872', 
    '42453585', '42464262', '40204522', '40297414', '41118252', '42384439', 
    '42368410', '41236408', '40496514', '42426384', '42205663', '42394641', 
    '42225042', '42474983', '42328769', '42325086', '41256772', '42290296', 
    '40547820', '42414376', '41270877', '42365354', '42386446', '42297004', 
    '41124387', '42221848', '42328782', '42318972', '42206923', '42413874', 
    '42332044', '42441159', '36736754', '41180145', '42108497', '41425968', 
    '41481111', '42464703', '41494166', '42100443', '42110004', '42351987',
    '42370644', '42283106', '41152973', '42458064', '42376871', '34456968', 
    '42354727', '42430170', '42348123', '40509650', '41448844', '41378217', 
    '37363568', '42284149', '42285270', '42163976', '40230416', '42427239', 
    '40062268', '40411913', '42223583', '41202519', '42384697', '42263670', 
    '42311637', '41439597', '40460522', '42274384', '42151890', '42310554', 
    '41080090', '42278259', '42084108', '42459741', '42287920', '42167373', 
    '42047927', '42252424', '42271887', '42283356', '40484527', '42278486', 
    '42447956', '42329957', '42380708', '42266524', '42016622', '41219752', 
    '42329143', '41446635', '42487633', '40413900', '41186776', '42354577', 
    '42376504', '42364523', '42351733', '41092362', '41162398', '42324910', 
    '42423532', '42278601', '41381655', '40017594', '40078272', '42100694', 
    '42411096', '42364732', '42398570', '41257607', '42284403']

ids['test']['mannheim'] = ['42411096', '42364732', '42398570', '41257607', '42284403']

seqs = [('ADC_reslice', 0), ('T2', 1)]

def get_suffix(seq):
    if seq == 'T2':
        return '_0001.nii.gz'
    elif seq == 'ADC_reslice':
        return '_0000.nii.gz'
    else:
        raise NameError()

if __name__ == '__main__':
    
    out_dir = '/home/woznicki/kidney/axial_nnUNet/base/nnUNet_raw_data/Task001_Prostate/'
    os.makedirs(join(out_dir, 'imagesTr'), exist_ok=True)
    os.makedirs(join(out_dir, 'labelsTr'), exist_ok=True)
    os.makedirs(join(out_dir, 'imagesTs'), exist_ok=True)
    os.makedirs(join(out_dir, 'labelsTs'), exist_ok=True)
    
    cnt = 0
    df = pd.DataFrame(columns=['patient_id', 'seq', 'test', 'nnunet_id', 'train_fold'])
    
    for cohort in [('train', 'Tr'), ('test', 'Ts')]:
        for source in ['munich', 'mannheim']:
            folds = [x % 5 for x in range(len(ids[cohort[0]][source]))]
            random.shuffle(folds)
            patient_cnt = 0

            for id_ in ids[cohort[0]][source]:
                print(id_)
                for seq in seqs:
                    seq_path = join(BASE_PATH, source, seq[0], id_)
                    
                    path = join(seq_path, 'img.nii')
                    assert(exists(path))
                    data = nib.load(path)
                    img = data.get_fdata()
                    matrix = img
                    new_data = nib.Nifti1Image(matrix, data.affine, data.header)
                    suffix = get_suffix(seq[0])
                    save_name = join(out_dir, 'images' + cohort[1], str(cnt) + suffix)
                    nib.save(new_data, save_name)

                wp_path =  join(seq_path, 'whole_prostate.nii')
                pz_path =  join(seq_path, 'peripheral_zone.nii')
                lesion_path =  join(seq_path, 'lesion.nii')

                assert(exists(wp_path))
                assert(exists(pz_path))
                assert(exists(lesion_path))

                wp_nifti = nib.load(wp_path)
                pz_nifti = nib.load(pz_path)
                lesion_nifti = nib.load(lesion_path)

                wp_matrix = wp_nifti.get_fdata()
                pz_matrix = pz_nifti.get_fdata()
                lesion_matrix = lesion_nifti.get_fdata()
                lesion_matrix = (lesion_matrix > 0).astype('uint8')
                
                matrix = wp_matrix.astype('uint8')
                matrix[pz_matrix == 1] = 2
                matrix[lesion_matrix == 1] = 3
                print(np.unique(matrix))

                new_seg = nib.Nifti1Image(matrix, wp_nifti.affine, wp_nifti.header)
                save_name = join(out_dir, 'labels' + cohort[1], str(cnt) + '.nii.gz')
                nib.save(new_seg, save_name)

                if cohort[0] == 'test':
                    test = 1
                    fold = -1
                else:
                    test = 0
                    fold = folds[patient_cnt]
                df = df.append({'patient_id': id_, 'source': source, 'test': test, 'nnunet_id': cnt, 'train_fold': fold}, ignore_index=True)
                cnt += 1
                patient_cnt += 1

    df.to_csv('../lookup_df_prostate.csv')
                
