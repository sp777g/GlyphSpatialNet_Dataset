import json
import random
import os

from src.utils import get_ttf_paths


def cut_file_path(file_path: str) -> str:
    path_1, path_2 = os.path.split(file_path)
    _, path_1 = os.path.split(path_1)
    file_path = os.path.join(path_1, path_2)

    return file_path


if __name__ == "__main__":
    random.seed(42)

    ttf_paths = [os.path.normpath(ttf_path) for ttf_path in sorted(get_ttf_paths('./_resources/collections'))]
    ttf_paths = [cut_file_path(ttf_path) for ttf_path in ttf_paths]
    source_font = [ttf_paths[0]]

    ttf_paths = ttf_paths[1:]
    random.shuffle(ttf_paths)

    n_seen = 200
    n_unseen = 21
    seen_fonts_for_train = sorted(ttf_paths[:n_seen])
    unseen_fonts_for_test = sorted(ttf_paths[n_seen:n_seen + n_unseen])

    print(source_font)
    print(seen_fonts_for_train)
    print(len(seen_fonts_for_train))
    print(unseen_fonts_for_test)
    print(len(unseen_fonts_for_test))

    with open('./_resources/split_of_fonts/source_font.json', 'w', encoding='utf-8') as f:
        json.dump(source_font, f, ensure_ascii=False, indent=2)

    with open('./_resources/split_of_fonts/seen_fonts_for_train.json', 'w', encoding='utf-8') as f:
        json.dump(seen_fonts_for_train, f, ensure_ascii=False, indent=2)

    with open('./_resources/split_of_fonts/unseen_fonts_for_test.json', 'w', encoding='utf-8') as f:
        json.dump(unseen_fonts_for_test, f, ensure_ascii=False, indent=2)
