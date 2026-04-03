import json
import os
import shutil

from glob import glob
from typing import List


def get_ttf_paths(path: str) -> List[str]:
    ttf_paths = list()
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        assert os.path.isdir(full_path)
        ttf_path = glob(f'{full_path}/*.ttf') + glob(f'{full_path}/*.otf') + glob(f'{full_path}/*.ttc')
        assert len(ttf_path) == 1
        ttf_paths.append(ttf_path[0])

    return ttf_paths


def copy_for_train():
    seen_fonts_for_train = json.load(open('./_resources/split_of_fonts/seen_fonts_for_train.json', encoding='utf-8'))

    for font_path in seen_fonts_for_train:
        src_path = os.path.join('./_resources/collections', font_path)
        _, font_name = os.path.split(src_path)
        tgt_path = os.path.join('./_results/dataset_train/seen_fonts_for_train', font_name)

        print(src_path)
        print(tgt_path)

        shutil.copyfile(src_path, tgt_path)


def copy_for_test():
    unseen_fonts_for_test = json.load(open('./_resources/split_of_fonts/unseen_fonts_for_test.json', encoding='utf-8'))

    for font_path in unseen_fonts_for_test:
        src_path = os.path.join('./_resources/collections', font_path)
        _, font_name = os.path.split(src_path)
        tgt_path_1 = os.path.join('./_results/dataset_test_UFSC/unseen_fonts_for_test', font_name)
        tgt_path_2 = os.path.join('./_results/dataset_test_UFUC/unseen_fonts_for_test', font_name)

        print(src_path)
        print(tgt_path_1)
        print(tgt_path_2)

        shutil.copyfile(src_path, tgt_path_1)
        shutil.copyfile(src_path, tgt_path_2)


if __name__ == "__main__":
    copy_for_train()
    copy_for_test()
