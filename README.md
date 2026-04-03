# GlyphSpatialNet_Dataset
This repository contains: (1) a collection of font files released under the SIL Open Font License; (2) how to build datasets for deep learning; (3) rendering and vectorization.

## Declaration
The copyright of all fonts belongs to their original authors or copyright holders. This repository only serves as a collection and distribution of these OFL fonts and does not modify any font content. The distribution of this repository itself also follows the SIL Open Font License. The fonts and licenses can be downloaded [here](https://drive.google.com/file/d/1paUDHTp7PtPpfLcHZAb6tzcheSAPsZqn/view?usp=sharing).

## Conda Environment
```
conda create -n FG_Dataset python=3.12 -y && conda activate FG_Dataset

pip --default-timeout=99999 install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu118
pip install potracer fonttools defcon ufo2ft

pip install numpy<2  # If an error occurs
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
Create the following directory:
```
_results/dataset_train/seen_fonts_for_train
_results/dataset_test_UFSC/unseen_fonts_for_test
_results/dataset_test_UFUC/unseen_fonts_for_test
```
Copy the corresponding files according to the division results to build a dataset:
```
python copy_files.py
```
Manually copy the following files:
```
(1) Copy source font:
0000\SourceHanSerifSC-Regular.otf ->
    dataset_train\
    dataset_test_UFUC\
    dataset_test_UFSC\

(2) Copy ref_chars:
ref_chars_for_test_8.json ->
    dataset_test_UFSC\
    dataset_test_UFUC\

(3) Copy split of characters:
seen_chars_for_train.json ->
    dataset_train\
seen_chars_for_test.json ->
    dataset_test_UFSC\
unseen_chars_for_test.json ->
    dataset_test_UFUC\
```
**Attention**: Different operating systems handle file suffixes differently. We strongly recommend that you print the results [here](https://github.com/sp777g/GlyphSpatialNet_Dataset/blob/main/src/utils.py#L43) to determine which font files have been effectively read. The same reading code **also exists** in the data loader of our model.

You can collect other font files on your own and obtain your own dataset through the above process.

If you use the data collected by this repository, the resulting dataset should be consistent with:
 - [[dataset_train.zip]]()
 - [[dataset_test_UFSC.zip]]()
 - [[dataset_test_UFUC.zip]]()

## Rendering and Vectorization
This code shows the rendering method we use:
```
python test_0_display_dataset.py
```
This code shows the process of render-vectorize-rerender:
```
python test_1_img_to_vec_to_img.py
```

## Acknowledgments
Thank you to all the creators of OFL fonts for making it possible to share these excellent fonts.
