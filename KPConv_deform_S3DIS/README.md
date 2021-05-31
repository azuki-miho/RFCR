A step-by-step installation guide for Ubuntu 18.04 is provided in [INSTALL.md](./INSTALL.md). 

## Data Preparation
S3DIS dataset can be found <a href="https://goo.gl/forms/4SoGp4KtH1jfRqEj2">here (4.8GB)</a>. Download the file named `Stanford3dDataset_v1.2.zip`, uncompress the folder and move it to `Data/S3DIS/Stanford3dDataset_v1.2`.

## Experiments
If you want to train the model, use the following instruction

```
CUDA_VISIBLE_DEVICES=0 python3 training_S3DIS.py
```

If you want to test the trained model, change the 'chosen_log' parameter and use the following instruction

```
CUDA_VISIBLE_DEVICES=0 python3 test_any_model.py
```

If you want to visualize the results on S3DIS Area-5, change the 'result_path' and 'split_room_path' parameters and use the following instruction

```
python3 visuliaze_s3dis.py
```
