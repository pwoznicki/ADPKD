#!/bin/bash

#parse the arguments
usage() { echo "Usage: $0 [--InputVol <string>] [--OutputDir <string>] [--small (optional)]" 1>&2; exit 1; }

Model="large"

while [ "$#" -gt 0 ]; do
    case "$1" in
        -i|--InputVol)
            InputVol="$2"; shift 2
            ;;
        -o|--OutputDir)
            OutputDir="$2"; shift 2
            ;;
        --small)
            Model="small"; shift
            ;;
        *)
			echo "unknown option $1" >&2;
            usage; exit 1
            ;;
    esac
done

if [ ! -f "${InputVol}" ]; then
    echo "Input nifti volume does NOT exist"
fi

WorkDir="/workspace/temp"
SourceDir="/workspace/source"

export nnUNet_raw_data_base=${WorkDir}
export nnUNet_preprocessed=${SourceDir}/trained_models/preprocessing
export RESULTS_FOLDER=${SourceDir}/trained_models
export PYTHONIOENCODING=utf-8

rm -rf ${WorkDir} || true
mkdir -p ${WorkDir}/input
mkdir -p ${WorkDir}/output
rm -rf ${OutputDir} || true
mkdir -p ${OutputDir}

#appropriate naming for the network (X_0000.nii.gz)
cp ${InputVol} ${WorkDir}/input/1_0000.nii.gz

Task=`python3 fix_orientation.py ${WorkDir}/input/1_0000.nii.gz`
echo ${Task}

#infer segmentation model
cd ${SourceDir}/nnUNet

if [[ "${Model}" == "large" ]]
then
    nnUNet_predict -i ${WorkDir}/input -o ${WorkDir}/output/3d_fullres -m 3d_fullres -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -p nnUNetPlansv2.1 -t ${Task} --save_npz
    nnUNet_predict -i ${WorkDir}/input -o ${WorkDir}/output/2d -m 2d -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -p nnUNetPlansv2.1 -t ${Task} --save_npz
    nnUNet_ensemble -f ${WorkDir}/output/3d_fullres ${WorkDir}/output/2d -o ${WorkDir}/output/ensemble \
        -pp ${RESULTS_FOLDER}/nnUNet/ensembles/${Task}/ensemble_2d__nnUNetTrainerV2__nnUNetPlansv2.1--3d_fullres__nnUNetTrainerV2__nnUNetPlansv2.1/postprocessing.json
else
    nnUNet_predict -i ${WorkDir}/input -o ${WorkDir}/output/ensemble -m 2d -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -p nnUNetPlansv2.1 -t ${Task}
fi
python3 ${SourceDir}/move_result_maybe_reorient.py --image_path ${InputVol} --mask_path ${WorkDir}/output/ensemble/1.nii.gz --output_dir ${OutputDir} --task ${Task}

#generate JSON with statistics
python3 ${SourceDir}/postprocess_masks.py --prediction_dir ${OutputDir}
