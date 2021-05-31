"""
Author: Jingyu Gong
Date: May 2021
"""

import numpy as np
import plyfile
from plyfile import PlyData
import os
from os.path import exists, join, isfile, isdir
from os import makedirs, listdir
import glob
from utils.ply import write_ply

result_path = "results/Log_2020-07-19_11-22-39_s3dis_backbone/val_preds_499/"
split_room_path = "Data/S3DIS/Stanford3dDataset_v1.2/"
save_path = result_path + "visualization/"
method = "rfcr"

# color palette for nyu40 labels
def create_color_palette():
    return [
       (0x00, 0xff, 0xff),               # ceiling
       (0x4f, 0x95, 0xb3),		# floor
       (0xab, 0x66, 0x4b),      # wall
       (0xea, 0x82, 0x78),      # beam
       (0x42, 0xa3, 0x86),      # column
       (0x36, 0xaf, 0x50),      # window
       (0x5f, 0x7f, 0x46),      # door
       (0x43, 0x46, 0x44),      # table
       (0x1f, 0x2a, 0x55),      # chair
       (0x52, 0x0b, 0x52),      # sofa
       (0xcb, 0x27, 0x31),      # bookcase
       (0x45, 0x60, 0x64),      # board
       (0xd2, 0xd6, 0xd6)       # clutter
    ]

if not os.path.isdir(save_path):
    os.mkdir(save_path)

label_to_names = {0: 'ceiling',
                    1: 'floor',
                    2: 'wall',
                    3: 'beam',
                    4: 'column',
                    5: 'window',
                    6: 'door',
                    7: 'chair',
                    8: 'table',
                    9: 'bookcase',
                    10: 'sofa',
                    11: 'board',
                    12: 'clutter'}
name_to_label = {v: k for k, v in label_to_names.items()}
for pc in glob.glob(result_path + "*.ply"):
    print(pc)
    pc_data = PlyData.read(pc)
    pc_data = pc_data.elements[0].data
    points = np.array([pc_data['x'], pc_data['y'], pc_data['z']]).T
    preds = np.array(pc_data['preds'])
    labels = np.array(pc_data['class'])
    pred_colors = np.zeros(points.shape).astype(np.uint8)
    label_colors = np.zeros(points.shape).astype(np.uint8)
    color_palette = create_color_palette()
    for idx, color in enumerate(color_palette):
        pred_colors[preds==idx] = color
        label_colors[labels==idx] = color
    pc_data = PlyData.read(split_room_path + "original_ply/" +  pc.split("/")[-1][:-4] + ".ply")
    pc_data = pc_data.elements[0].data
    colors = np.array([pc_data['red'], pc_data['green'], pc_data['blue']]).T


    point_offset = 0
    area_name = pc.split("/")[-1][:-4]
    cloud_folder = join(split_room_path, area_name)
    cloud_name = area_name
    room_folders = [join(cloud_folder, room) for room in listdir(cloud_folder) if isdir(join(cloud_folder, room))]
    # Loop over rooms
    for i, room_folder in enumerate(room_folders):

        print('Cloud %s - Room %d/%d : %s' % (cloud_name, i+1, len(room_folders), room_folder.split('\\')[-1]))
        cloud_points = np.empty((0, 3), dtype=np.float32)
        cloud_colors = np.empty((0, 3), dtype=np.uint8)
        cloud_classes = np.empty((0, 1), dtype=np.int32)

        for object_name in listdir(join(room_folder, 'Annotations')):

            if object_name[-4:] == '.txt':

                # Text file containing point of the object
                object_file = join(room_folder, 'Annotations', object_name)

                # Object class and ID
                tmp = object_name[:-4].split('_')[0]
                if tmp in name_to_label:
                    object_class = name_to_label[tmp]
                elif tmp in ['stairs']:
                    object_class = name_to_label['clutter']
                else:
                    raise ValueError('Unknown object name: ' + str(tmp))

                # Read object points and colors
                with open(object_file, 'r') as f:
                    object_data = np.array([[float(x) for x in line.split()] for line in f])

                # Stack all data
                cloud_points = np.vstack((cloud_points, object_data[:, 0:3].astype(np.float32)))

        x_min, y_min, z_min = np.min(cloud_points, axis=0)
        x_max, y_max, z_max = np.max(cloud_points, axis=0)
        chosen_idx = (points[:,0] >= x_min) & (points[:,0] <= x_max) & (points[:,1] >= y_min) & (points[:,1] <= y_max)
        # Save as ply
        sub_points = points[chosen_idx]
        sub_pred_colors = pred_colors[chosen_idx]
        sub_preds = preds[chosen_idx]
        sub_label_colors = label_colors[chosen_idx]
        sub_labels = labels[chosen_idx]
        sub_colors = colors[chosen_idx]
        color_file = join(save_path, room_folder.split("/")[-1]+"_pc.ply")
        gt_output_file = join(save_path, room_folder.split("/")[-1]+"_gt.ply")
        pred_output_file = join(save_path, room_folder.split("/")[-1]+"_" + method + ".ply")

        write_ply(gt_output_file, (sub_points, sub_label_colors, sub_labels), ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])
        write_ply(pred_output_file, (sub_points, sub_pred_colors, sub_preds), ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])
        write_ply(color_file, (sub_points, sub_colors, sub_labels), ['x', 'y', 'z', 'red', 'green', 'blue', 'class'])
