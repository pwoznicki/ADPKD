### Download docker image (private repo)
```
$ docker pull piotrekwoznicki/adpkd-net:v0.1
```
### Run
#### 1. Launch the container:
```
$ bash launch_container.sh [path_to_dataset - will be mounted at /workspace/data]
```

#### 2. Run inference:
```
$ cd /workspace/source
$ bash fit.sh  \
    -i / --InputVol [abs_path_to_nifti_image]
    -o / --OutputDir [where_to_save_segmentation_and_JSON]
    --small [whether to use single model - OPTIONAL (requires shorter calculation time)]
```

#### 3. Run inference for test:
```
$ cd /workspace/source
$ bash fit.sh  \
    -i /workspace/test_data/T2_ax.nii.gz
    -o /workspace/data/test_results_ax

$ bash fit.sh  \
    -i /workspace/test_data/T2_cor.nii.gz
    -o /workspace/data/test_results_cor
```
