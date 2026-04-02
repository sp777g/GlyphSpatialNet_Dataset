# GlyphSpatialNet_Dataset
This repository contains a collection of font files released under the SIL Open Font License.

## Declaration
The copyright of all fonts belongs to their original authors or copyright holders. This repository only serves as a collection and distribution of these OFL fonts and does not modify any font content. The distribution of this repository itself also follows the SIL Open Font License.

## Conda Environment
```
conda create -n FG_Dataset python=3.12 -y && conda activate FG_Dataset

pip --default-timeout=99999 install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu118
pip install potracer fonttools defcon ufo2ft
```

## Acknowledgments
Thank you to all the creators of OFL fonts for making it possible to share these excellent fonts.
