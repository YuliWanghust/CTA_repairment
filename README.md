# CTA_repairment

Submitted to [MICCAI'24] Car-Dcros: Enhancing Cardiovascular Artery Segmentation through Disconnected Repairment and Open Curve Snake: A dataset and benchmark

## Abstract

The segmentation of cardiovascular arteries in 3D medical images holds significant promise for assessing vascular health. Despite advancements in existing algorithms, persistent challenges persist, particularly in accurately segmenting smaller vascular structures and those affected by plaque, where the arteries can appear disconnected. To solve these challenges, we present a novel post-processing approach that harnesses a data-driven method to rectify disconnected cardiovascular artery structures. First, we generate synthetic dataset to mimic disconnected cardiovascular structure. Then, our approach redefines the problem as a keypoints detection task, wherein a neural network is trained to predict key points capable of bridging disconnected components. Additionally, we employ an open curve active contour model to seamlessly connect disconnected points while optimizing for smoothness and intensity fitness. Finally, our pipeline is deployed on a real institutional dataset to demonstrate generalization and clinical utility of our approach.

## Key contributions

- ****Introducing Car-Dcros****, a novel pipeline designed to reframe CTA segmentation by incorporating disconnected component repairment and smoothness optimization.
- ****Providing an open-source dataset**** of synthetic cardiovascular trees specifically tailored for key points detection.
- ****Demonstrating state-of-the-art performance**** on vessel segmentation through benchmarking against three coronary CTA datasets.

## Dataset

![Visualizations of the PTR dataset.](quali_res_1.png)

The Cardiovascular Disconnected dataset is available [here](https://livejohnshopkins-my.sharepoint.com/:f:/g/personal/ywang687_jh_edu/EgyMcSDR0KFLv5H7U8OxV7gBcduChUr2CmDA9iaeT9vUFg?e=3LGcr2). It consists of the following data splits:

### Data Structure

| Type (graphs based imgs) | Train  | Validation | Test  |
| -------------------------| ------ | ---------- | ----- |
| ASCOS                    | 28     | 4          | 8     |
| ImageCAS                 | 140    | 20         | 40    |
| JHH                      | 0      | 0          | 10    |
| Sythesized               | 2688   | 384        | 928   |

For each data type, the dataset includes the following files:

**Raw_data**: raw_data/train/:

```
- pulse_xxxxx_volume.nii.gz: Original binarized volume with 0 representing background and 1 representing airways or vessels. (xxxxx refers to pulse id)
- pulse_xxxxx_centerline.nii.gz: Extracted centerline of the original binarized volume.
- pulse_xxxxx_graph.json: Graph dictionary with edge information for each branch of the pulmonary tree, including location and features of each edge.
```

**Synthesized_data**: airway/synthesized_data/train/:

```
- pulse_xxxxx_idx_volume.nii.gz: Synthesized volume with a single disconnection.
- pulse_xxxxx_idx_kp1_part.nii.gz: Component kp1 of the synthesized volume.
- pulse_xxxxx_idx_kp2_part.nii.gz: Component kp2 of the synthesized volume.
- pulse_xxxxx_idx_data.npz: Meta data of the synthesized volume, including above volumes with corresponding keypoints coordinates and features of the disconnected edge. This is directly laoded into our training pipeline.
```

## Data Synthesis

### Requirements

To set up the required environments, install the following dependencies:

- Numpy:

```
pip install numpy
```

- SimpleITK

```
pip install SimpleITK
```

### Run

To generate synthesized data in bulk for training purposes, run the following command:

```
python data_synthesis.py -source_dir raw_data/ -target_dir synthesized_data/ -volume_num=30 -radius_min=1 -radius_max=15 -points_threshold=10
```

The command line parameters have the following meanings:

* source_dir: Directory of the raw data.
* target_dir: Directory to store the synthesized data.
* volume_num: The number of disconnected volumes to generate for each raw data (original volume).
* radius_min, radius_max: Only edges with a radius within this range will be selected as a disconnected branch.
* points_threshold: Only edges (centerlines) with a point number greater than this threshold will be selected as a disconnected branch.

## TODO

- [x] Our Pytorch implementation of keypoint detection will be released soon.
