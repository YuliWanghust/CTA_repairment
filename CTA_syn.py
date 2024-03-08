import numpy as np
import os
import SimpleITK as sitk
import random
import json
import argparse
import sys


class DataSynthesizer:
    def __init__(
            self,
            source_directory,
            target_directory,
    ):
        """
        source_directory: The directory of the raw data.
        target_directory: The directory of the data to be synthesized.

        Input: source_directory/
                - xxx_volume.nii.gz  % original volume
                - xxx_graph.graphml  % graph with edge information

        Output: target_directory/
                - xxx_idx_volume.nii.gz  % synthesized volume with single disconnection
                - xxx_idx_kp1.nii.gz  % kp1 part of the synthesized volume
                - xxx_idx_kp2.nii.gz  % kp2 part of the synthesized volume
                ...

        Note: centerline information will not be used in this process.
        """
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.pulse_ids = [i[:11] for i in os.listdir(source_directory) if '.json' in i]

    def process_data(self, pulse_id, volume, edge, index):
        point_coordinates = np.array(edge['point_coord'])
        point_number = edge['point_number']
        tolerance = 0
        flag = 0
        while True:
            # Choose the location of KP1 and KP2
            kp1_range = [0.05, 0.4]
            kp2_range = [0.6, 0.95]
            kp1_location = np.random.random() * (kp1_range[1] - kp1_range[0]) + kp1_range[0]
            kp2_location = np.random.random() * (kp2_range[1] - kp2_range[0]) + kp2_range[0]
            kp1 = point_coordinates[round(kp1_location * point_number)]
            kp2 = point_coordinates[round(kp2_location * point_number)]
            kp_mid = point_coordinates[round(0.5 * point_number)]
            coordinates = np.argwhere(volume != 0)

            edge_points_diff = point_coordinates[1:] - point_coordinates[:-1]  # point_x - point_(x+1)
            edge_points_distance = np.sqrt(np.sum(edge_points_diff ** 2, axis=1))
            edge_points_to_end_distance = []
            for i in range(point_number):
                if i == 0:
                    edge_points_to_end_distance.append(0.0)
                elif i == point_number - 1:
                    edge_points_to_end_distance.append(0.0)
                else:
                    edge_points_to_end_distance.append(min(np.sum(edge_points_distance[:i]), np.sum(edge_points_distance[i:])))
            edge_points_to_end_distance = np.array(edge_points_to_end_distance)

            vector_1 = kp_mid - kp1
            vector_2 = kp_mid - kp2
            radius_cutoff = np.random.random() * (2 - 1.3) + 1.3
            noise_level = np.random.random() * (4 - 1) + 1

            for p in coordinates:
                if (p - kp1).dot(vector_1) > 0 and (p - kp2).dot(vector_2) > 0:
                    distance = np.sum((p - point_coordinates) ** 2, axis=1)
                    closest_index = np.argmin(distance)

                    if distance[closest_index] < (edge['radius_max'] * radius_cutoff) ** 2:
                        volume[p[0], p[1], p[2]] = 0
                        ratio = 1 - (edge_points_to_end_distance[closest_index] / np.max(edge_points_to_end_distance))

                        if random.random() < ratio ** noise_level * 0.5:
                            volume[p[0], p[1], p[2]] = 1

            volume_img = sitk.GetImageFromArray(volume)
            component_image = sitk.ConnectedComponent(volume_img)
            sorted_component_image = sitk.RelabelComponent(component_image, minimumObjectSize=15, sortByObjectSize=True)
            sorted_component = sitk.GetArrayFromImage(sorted_component_image)

            # label_0: the label of the kp1 component; label_1: the label of the kp2 component
            label_0 = sorted_component[kp1[0], kp1[1], kp1[2]]
            label_1 = sorted_component[kp2[0], kp2[1], kp2[2]]

            # label=0: background
            if label_0 * label_1 > 0 and label_0 != label_1:
                seg_0 = sorted_component == label_0
                seg_1 = sorted_component == label_1
                disconnected_volume = np.logical_or(seg_0, seg_1) + 0
                seg_0_size = np.sum(seg_0)
                seg_1_size = np.sum(seg_1)

                # Make sure kp1 locate at the main part of the pulmonary tree
                if seg_0_size > seg_1_size:
                    kp1_seg = seg_0 + 0
                    kp2_seg = seg_1 + 0
                    kp1_coord = kp1
                    kp2_coord = kp2
                else:
                    kp1_seg = seg_1 + 0
                    kp2_seg = seg_0 + 0
                    kp1_coord = kp2
                    kp2_coord = kp1

                disconnected_volume_nii = sitk.GetImageFromArray(np.uint8(disconnected_volume))
                sitk.WriteImage(disconnected_volume_nii, os.path.join(self.target_directory, pulse_id) +
                                '_'+str(index)+'_volume.nii.gz')

                kp1_volume_nii = sitk.GetImageFromArray(np.uint8(kp1_seg))
                sitk.WriteImage(kp1_volume_nii, os.path.join(self.target_directory, pulse_id) +
                                '_' + str(index) + '_kp1_part.nii.gz')

                kp2_volume_nii = sitk.GetImageFromArray(np.uint8(kp2_seg))
                sitk.WriteImage(kp2_volume_nii, os.path.join(self.target_directory, pulse_id) +
                                '_' + str(index) + '_kp2_part.nii.gz')

                npz_name = os.path.join(self.target_directory, pulse_id + '_' + str(index) + '_data.npz')
                if not os.path.exists(npz_name):
                    np.savez_compressed(npz_name,
                                        volume=disconnected_volume,
                                        kp1_part=kp1_seg,
                                        kp2_part=kp2_seg,
                                        kp1_coord=kp1_coord,
                                        kp2_coord=kp2_coord,
                                        edge_points=point_coordinates,  # (n,3)
                                        edge_radius_avg=edge['radius_avg'],
                                        edge_radius_min=edge['radius_min'],
                                        edge_radius_max=edge['radius_max'],
                                        edge_volume=edge['volume'],
                                        edge_surface_area=edge['surface_area'],
                                        edge_length=edge['length'],
                                        edge_tortuosity=edge['tortuosity']
                                        )
