### Installation instructions for Ubuntu 18.04
     
* Make sure <a href="https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html">CUDA</a>  and <a href="https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html">cuDNN</a> are installed. The code has been tested on TensorFlow 1.13.1, CUDA 10.0 and cuDNN 7.4+. 

* Follow <a href="https://github.com/QingyongHu/RandLA-Net">RandLA-Net</a> instruction to setup python environment
```
conda create -n randlanet python=3.5
source activate randlanet
pip install -r helper_requirements.txt
sh compile_op.sh
```
