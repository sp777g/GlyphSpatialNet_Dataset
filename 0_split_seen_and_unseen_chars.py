import json
import random

from tqdm.auto import tqdm
from src import get_ttf_paths, draw_image_from_ttf, get_defined_chars


def get_avail_chars():
    ttf_paths = get_ttf_paths('./_resources/collections')
    base_char = json.load(open('GB_T_2312.json', encoding='utf-8'))
    base_char_set = set(base_char)
    gb_t_2313_chars = set(base_char)

    for _, ttf_path in tqdm(enumerate(ttf_paths), total=len(ttf_paths)):
        chars = get_defined_chars(ttf_path, gb_t_2313_chars)
        avail_chars = set([key for key, value in draw_image_from_ttf(
            ttf_path=ttf_path,
            img_size=64,
            chars={key: None for key in chars},
            draw_axis=False
        ).items() if value is not None])
        base_char_set = base_char_set.intersection(avail_chars)

    all_avail_chars = sorted(list(base_char_set))
    print(f'all_avail_chars={all_avail_chars}')
    print(len(all_avail_chars))
    print("============================")

    with open('tmp/all_avail_chars.json', 'w', encoding='utf-8') as f:
        json.dump(all_avail_chars, f, ensure_ascii=False, indent=2)


def split_seen_and_unseen_chars():
    n_seen = 5000
    n_unseen = 1000
    n_ref = 700

    all_avail_chars = json.load(open('tmp/all_avail_chars.json', encoding='utf-8'))
    random.shuffle(all_avail_chars)

    assert len(all_avail_chars) >= n_seen + n_unseen + n_ref

    seen_chars_for_train = all_avail_chars[:n_seen]
    unseen_chars_for_test = all_avail_chars[n_seen:n_seen + n_unseen]
    ref_chars_for_test_all = all_avail_chars[n_seen + n_unseen:n_seen + n_unseen + n_ref]

    print(f'seen_chars_for_train={seen_chars_for_train}')
    print(len(seen_chars_for_train))
    print(f'unseen_chars_for_test={unseen_chars_for_test}')
    print(len(unseen_chars_for_test))

    with open('./_resources/split_of_chars/seen_chars_for_train.json', 'w', encoding='utf-8') as f:
        json.dump(seen_chars_for_train, f, ensure_ascii=False, indent=2)

    with open('./_resources/split_of_chars/unseen_chars_for_test.json', 'w', encoding='utf-8') as f:
        json.dump(unseen_chars_for_test, f, ensure_ascii=False, indent=2)

    _seen_chars_for_train = json.load(open('./_resources/split_of_chars/seen_chars_for_train.json', encoding='utf-8'))
    random.shuffle(_seen_chars_for_train)
    seen_chars_for_test = _seen_chars_for_train[:n_unseen]

    print(f'seen_chars_for_test={seen_chars_for_test}')
    print(len(seen_chars_for_test))

    with open('./_resources/split_of_chars/seen_chars_for_test.json', 'w', encoding='utf-8') as f:
        json.dump(seen_chars_for_test, f, ensure_ascii=False, indent=2)

    print(f'ref_chars_for_test_all={ref_chars_for_test_all}')
    print(len(ref_chars_for_test_all))

    with open('tmp/ref_chars_for_test_all.json', 'w', encoding='utf-8') as f:
        json.dump(ref_chars_for_test_all, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    random.seed(42)

    get_avail_chars()
    split_seen_and_unseen_chars()
