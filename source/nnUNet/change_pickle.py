import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
from batchgenerators.utilities.file_and_folder_operations import load_pickle, save_pickle 
import pandas as pd
import random
import collections


if __name__ == '__main__':
    path = '/home/woznicki/kidney/axial_nnUNet/base/nnUNet_preprocessed/Task002_Kidney/splits_final.pkl'
    df = pd.read_csv('./lookup_df.csv')
    l = []
    for i in range(5):
        val_indices = df[df.train_fold == i][df.test == False].nnunet_id
        train_indices = df[df.train_fold != i][df.test == False].nnunet_id
        
        print(len(val_indices), len(train_indices))

        val_list = [str(id_) for id_ in val_indices]
        train_list = [str(id_) for id_ in train_indices]
        
        ordict = collections.OrderedDict([('train', train_list), ('val', val_list)])
        
        l.append(ordict)
    print(l)
    save_pickle(l, path)
