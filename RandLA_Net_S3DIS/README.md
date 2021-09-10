A step-by-step installation guide for Ubuntu 18.04 is provided in [INSTALL.md](./INSTALL.md). 

## Data Preparation
S3DIS dataset can be found 
<a href="https://docs.google.com/forms/d/e/1FAIpQLScDimvNMCGhy_rmBA2gHfDu3naktRm6A8BPwAWWDv-Uhm6Shw/viewform?c=0&w=1">here</a>. 
Download the files named "Stanford3dDataset_v1.2_Aligned_Version.zip". Uncompress the folder and move it to 
`./data/S3DIS`.

If you want to prepare the dataset
```
python utils/data_prepare_s3dis.py
```
## Experiments
If you want to start 6-fold cross validation
```
sh jobs_6_fold_cv_s3dis.sh
```

If you want to evaluate the performance on Area-5 
```
sh jobs_area5_s3dis.sh
```

## Acknowledgments
This repo is modified from the recent work <a href="https://github.com/QingyongHu/RandLA-Net">RandLA-Net</a>.

## License
Licensed under the CC BY-NC-SA 4.0 license, see [LICENSE](./LICENSE).
