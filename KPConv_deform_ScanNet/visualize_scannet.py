"""
Author: Jingyu Gong
Date: May 2021
"""

import numpy as np
import plyfile
from plyfile import PlyData
import os
import glob
from utils.ply import write_ply

#result_path = "results/Log_2020-08-26_08-38-15_add_weight_697/val_preds_449/"
result_path = "test/Log_2020-10-05_09-36-55_regionce_701/val_predictions/"
mesh_path = "Data/Scannet/training_meshes/"
save_path = result_path + "visualization/"
method = "rfcr"

# color palette for nyu40 labels
def create_color_palette():
    return [
       (0, 0, 0),
       (174, 199, 232),		# wall
       (152, 223, 138),		# floor
       (31, 119, 180), 		# cabinet
       (255, 187, 120),		# bed
       (188, 189, 34), 		# chair
       (140, 86, 75),  		# sofa
       (255, 152, 150),		# table
       (214, 39, 40),  		# door
       (197, 176, 213),		# window
       (148, 103, 189),		# bookshelf
       (196, 156, 148),		# picture
       (23, 190, 207), 		# counter
       (178, 76, 76),  
       (247, 182, 210),		# desk
       (66, 188, 102), 
       (219, 219, 141),		# curtain
       (140, 57, 197), 
       (202, 185, 52), 
       (51, 176, 203), 
       (200, 54, 131), 
       (92, 193, 61),  
       (78, 71, 183),  
       (172, 114, 82), 
       (255, 127, 14), 		# refrigerator
       (91, 163, 138), 
       (153, 98, 156), 
       (140, 153, 101),
       (158, 218, 229),		# shower curtain
       (100, 125, 154),
       (178, 127, 135),
       (120, 185, 128),
       (146, 111, 194),
       (44, 160, 44),  		# toilet
       (112, 128, 144),		# sink
       (96, 207, 209), 
       (227, 119, 194),		# bathtub
       (213, 92, 176), 
       (94, 106, 211), 
       (82, 84, 163),  		# otherfurn
       (100, 85, 144)
    ]

if not os.path.isdir(save_path):
    os.mkdir(save_path)

for pc in glob.glob(result_path + "*.ply"):
    print(pc)
    pc_data = PlyData.read(pc)
    pc_data = pc_data.elements[0].data
    points = np.array([pc_data['x'], pc_data['y'], pc_data['z']]).T
    preds = np.array(pc_data['preds'])
    if result_path[-2] == 's':
        labels = np.array(pc_data['gt'])
    else:
        labels = np.array(pc_data['class'])
    pred_colors = np.zeros(points.shape).astype(np.uint8)
    label_colors = np.zeros(points.shape).astype(np.uint8)
    color_palette = create_color_palette()
    for idx, color in enumerate(color_palette):
        pred_colors[preds==idx] = color
        label_colors[labels==idx] = color
    pred_colors[labels==0] = color_palette[0]
    pred_output_file = save_path + pc.split("/")[-1][:-4] + "_" + method + ".ply"
    gt_output_file = save_path + pc.split("/")[-1][:-4] + "_" + "gt" + ".ply"
    color_file = save_path + pc.split("/")[-1][:-4] + "_" + "pc" + ".ply"
    write_ply(pred_output_file, [points, pred_colors, preds], ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])
    write_ply(gt_output_file, [points, label_colors, labels], ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])
    #original pc
    pc_data = PlyData.read(mesh_path + pc.split("/")[-1][:-4] + "_mesh.ply")
    pc_data = pc_data.elements[0].data
    points = np.array([pc_data['x'], pc_data['y'], pc_data['z']]).T
    colors = np.array([pc_data['red'], pc_data['green'], pc_data['blue']]).T
    labels = np.array(pc_data['class'])
    write_ply(color_file, [points, colors, labels], ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])


