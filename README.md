### Download docker image (private repo)
```
$ docker pull piotrekwoznicki/adpkd-net:v0.1
```
### Run
#### 1. Launch the container:
```
$ ./launch_container.sh [path_to_dataset - will be mounted at /workspace/data]
```

#### 2. Run inference:
```
$ cd /workspace/source
$ bash fit.sh  \
    --InputVol [abs_path_to_nifti_image]
    --OutputDir [where_to_save_segmentation_and_JSON]
    --small [whether to use single model (optional - requires longer calculation time)]
```

#### 3. Run inference for test:
```
$ cd /workspace/source
$ bash fit.sh  \
    --InputVol /workspace/test_data/nifti/T2_ax.nii.gz
    --OutputDir /workspace/test_data/results_ax

$ bash fit.sh  \
    --InputVol /workspace/test_data/nifti/T2_cor.nii.gz
    --OutputDir /workspace/test_data/results_cor
```
