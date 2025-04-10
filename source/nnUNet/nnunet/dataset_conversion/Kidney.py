#    Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from collections import OrderedDict
import SimpleITK as sitk
from batchgenerators.utilities.file_and_folder_operations import *


if __name__ == "__main__":
    
    folder = "/home/woznicki/kidney/axial_nnUNet/base/nnUNet_raw_data/Task002_Kidney"

    # train
    img_train = subfiles(join(folder, 'imagesTr'))
    labels_train = subfiles(join(folder, 'labelsTr'))

    # test
    img_test = subfiles(join(folder, 'imagesTs'))


    json_dict = OrderedDict()
    json_dict['name'] = "Kidney"
    json_dict['description'] = "ADPKD kidney segmentation - axial"
    json_dict['tensorImageSize'] = "4D"
    json_dict['reference'] = "see challenge website"
    json_dict['licence'] = "see challenge website"
    json_dict['release'] = "0.0"
    json_dict['modality'] = {
        "0": "MRI",
    }
    json_dict['labels'] = {
        "0": "background",
        "1": "kidney"
    }
    json_dict['numTraining'] = len(img_train)
    json_dict['numTest'] = len(img_test)
    json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i.split("/")[-1][:-7], "label": "./labelsTr/%s.nii.gz" % i.split("/")[-1][:-7]} for i in
                             labels_train]
    json_dict['test'] = ["./imagesTs/%s.nii.gz" % i.split("/")[-1][:-12] for i in img_test]

    save_json(json_dict, os.path.join(folder, "dataset.json"))

