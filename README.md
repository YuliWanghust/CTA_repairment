# CTA_repairment

Submitted to [MICCAI'24] Car-Dcros: A Dataset and Benchmark for Enhancing Cardiovascular Artery Segmentation through Disconnected Components Repair and Open Curve Snake

## Key contributions

- ****Introducing Car-Dcros****, a novel pipeline designed to reframe CTA segmentation by incorporating disconnected component repairment and smoothness optimization.
- ****Providing an open-source dataset**** of synthetic cardiovascular trees specifically tailored for key points detection.
- ****Demonstrating state-of-the-art performance**** on vessel segmentation through benchmarking against three coronary CTA datasets.

## Dataset

![Visualizations of the PTR dataset.](quali_res_1.png)

The Cardiovascular Disconnected dataset is available [here](). It consists of the following data splits:

### Data Structure

| Type (graphs based imgs) | Train  | Validation | Test  |
| -------------------------| ------ | ---------- | ----- |
| ASCOS                    | 28     | 4          | 8     |
| ImageCAS                 | 140    | 20         | 40    |
| Ours                     | 0      | 0          | 10    |
| Sythesized               | 2688   | 384        | 928   |

For each data type, the dataset includes the following files:

**Raw_data**:

1. pulse_xxxxx_volume.nii.gz  % original volume
2. pulse_xxxxx_centerline.nii.gz  % extracted centerline
3. pulse_xxxxx_graph.graphml  % graph with edge information


**CTA Synthesized_data**:

1. xxx_idx_volume.nii.gz: Synthesized volume with a singular disconnection.
2. xxx_idx_kp1_part.nii.gz: Component kp1 extracted from the synthesized volume.
3. xxx_idx_kp2_part.nii.gz: Component kp2 extracted from the synthesized volume


## Data Synthesis

### Run

To generate synthesized data in bulk for training purposes, run the following command:
```
python CTA_syn.py
```

### Run Open Curve Snake

The code provided is a Python implementation of the revised Open Curve Snakes methods. It does not aim to be a fast or efficient implementation.

### Requirements

To set up the required environments, install the following dependencies:
```
pip install requriement.txt
python setup.py
```

### Test

The code is documented and in tests.py under the folder of test
```
python ./test.py
```

## Acknowledegment
Part of the code and user instructions are modified or revised from morph snakes [here](https://github.com/pmneila/morphsnakes) and Pulmonary-Tree-Repairing [here](https://github.com/M3DV/pulmonary-tree-repairing)



