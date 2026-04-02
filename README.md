# GlyphSpatialNet_Dataset
This repository contains: (1) a collection of font files released under the SIL Open Font License; (2) how to build datasets for deep learning; (3) rendering and vectorization.

## Declaration
The copyright of all fonts belongs to their original authors or copyright holders. This repository only serves as a collection and distribution of these OFL fonts and does not modify any font content. The distribution of this repository itself also follows the SIL Open Font License. The fonts and licenses can be downloaded [here](https://drive.google.com/file/d/1paUDHTp7PtPpfLcHZAb6tzcheSAPsZqn/view?usp=sharing).

## Conda Environment
```
conda create -n FG_Dataset python=3.12 -y && conda activate FG_Dataset

pip --default-timeout=99999 install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu118
pip install potracer fonttools defcon ufo2ft
```

## Preprocessing
Create the following directory:
```
tmp
_resources/split_of_chars
_resources/split_of_fonts
```
Run these .py files sequentially to split the dataset:
```
python 0_split_seen_and_unseen_chars.py
python 1_prepare_ref_chars.py
python 2_split_seen_and_unseen_fonts.py
```
## Build Dataset
Copy the corresponding files according to the division results to build a dataset:
```
```
**Attention**: Different operating systems handle file suffixes differently. We strongly recommend that you print the results here to determine which font files have been effectively read. The same reading code **also exists** in the data loader of our model.

## Rendering and Vectorization

## Acknowledgments
Thank you to all the creators of OFL fonts for making it possible to share these excellent fonts.
