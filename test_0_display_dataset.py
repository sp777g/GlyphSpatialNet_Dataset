import os
import json

from tqdm import tqdm
from src import get_ttf_paths, draw_image_from_ttf


def main(img_size):
    ttf_paths = get_ttf_paths('./_resources/collections')

    for idx, ttf_path in tqdm(enumerate(ttf_paths), total=len(ttf_paths)):
        prefix_path = 'tmp/display_dataset'
        ttf_name = os.path.basename(os.path.normpath(ttf_path)).split('.')[0]
        prefix_path = os.path.join(prefix_path, f'{idx:04d}_{ttf_name}')

        chars = json.load(open('./_resources/split_of_chars/seen_chars_for_test.json', encoding='utf-8'))
        chars = {char: os.path.join(prefix_path, f'{_idx:04d}' + '.png') for _idx, char in enumerate(chars)}

        if not os.path.isdir(prefix_path):
            os.makedirs(prefix_path, exist_ok=True)

        draw_image_from_ttf(
            ttf_path=ttf_path,
            img_size=img_size,
            chars=chars,
            draw_axis=False
        )


if __name__ == '__main__':
    main(img_size=128)
