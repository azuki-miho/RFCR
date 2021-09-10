A step-by-step installation guide for Ubuntu 18.04 is provided in [INSTALL.md](./INSTALL.md). 

## Data Preparation
Scannet v2 dataset can be found <a href="http://www.scan-net.org/">here</a> and move it to `Data/Scannet`.

## Experiments
If you want to train the model, use the following instruction

```
CUDA_VISIBLE_DEVICES=0 python3 training_Scannet.py
```

If you want to test the trained model, change the 'chosen_log' parameter and use the following instruction

```
CUDA_VISIBLE_DEVICES=0 python3 test_any_model.py
```

If you want to visualize the results on the validation set of Scannet v2, change the 'result_path' and 'mesh_path' parameters and use the following instruction

```
python3 visuliaze_scannet.py
```

## Acknowledgment
This repo is modified from the the recent work <a href="https://github.com/HuguesTHOMAS/KPConv">KPConv</a>.
