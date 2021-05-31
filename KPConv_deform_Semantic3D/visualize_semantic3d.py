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

#result_path = "test/Log_2020-10-14_13-02-17_758/val_predictions/"
result_path = "results/Log_2020-10-28_13-36-31/val_preds_499/"
mesh_path = "Data/Semantic3D/ply_subsampled/train/"
save_path = result_path + "visualization/"
method = "kpconv"

# color palette for nyu40 labels
def create_color_palette():
    return [
       (0, 0, 0),
       (0xc0, 0xc0, 0xc0),		# road
       (0x00, 0x41, 0x0e),      # grass
       (0x00, 0xfc, 0x34),      # tree
       (0xfc, 0xfd, 0x39),      # bush
       (0xea, 0x02, 0x19),      # building
       (0x83, 0x0f, 0xa9),      # hardscape
       (0x00, 0xfa, 0xf6),      # hardscape
       (0xf1, 0x05, 0x6e)       # cars
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
    #
    points = points[labels!=0]
    pred_colors = pred_colors[labels!=0]
    label_colors = label_colors[labels!=0]
    preds = preds[labels!=0]
    labels = labels[labels!=0]
    pred_output_file = save_path + pc.split("/")[-1][:-4] + "_" + method + ".ply"
    gt_output_file = save_path + pc.split("/")[-1][:-4] + "_" + "gt" + ".ply"
    color_file = save_path + pc.split("/")[-1][:-4] + "_" + "pc" + ".ply"
    write_ply(pred_output_file, [points, pred_colors, preds], ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])
    write_ply(gt_output_file, [points, label_colors, labels], ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])
    #original pc
    pc_data = PlyData.read(mesh_path + pc.split("/")[-1][:-4] + ".ply")
    pc_data = pc_data.elements[0].data
    points = np.array([pc_data['x'], pc_data['y'], pc_data['z']]).T
    colors = np.array([pc_data['red'], pc_data['green'], pc_data['blue']]).T
    colors = colors.astype(np.uint8)
    labels = np.array(pc_data['class'])
    points = points[labels!=0]
    colors = colors[labels!=0]
    labels = labels[labels!=0]
    write_ply(color_file, [points, colors, labels], ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])


