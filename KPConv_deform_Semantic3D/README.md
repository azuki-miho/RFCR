A step-by-step installation guide for Ubuntu 18.04 is provided in [INSTALL.md](./INSTALL.md). 

## Data Preparation
Semantic3D dataset can be found <a href="https://www.semantic3d.net">here</a>. Download and unzip them and place them in `Data/Semantic3D/original_data`. It's noteworthy, there might be a mismatch between the `txt` and `labels` files for `neugasse_station1_xyz_intensity_rgb`, please fix it.

## Experiments
If you want to train the model, use the following instruction

```
CUDA_VISIBLE_DEVICES=0 python3 training_Semantic3D.py
```

If you want to test the trained model, change the 'chosen_log' parameter and use the following instruction

```
CUDA_VISIBLE_DEVICES=0 python3 test_any_model.py
```

If you want to visualize the results on Semantic3D, change the 'result_path' parameters and use the following instruction

```
python3 visuliaze_semantic3d.py
```

## Acknowledgments
This repo is modified from the the recent work <a href="https://github.com/HuguesTHOMAS/KPConv">KPConv</a>.
