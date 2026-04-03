import json
import random

if __name__ == "__main__":
    random.seed(42)

    ref_chars_for_test_all = json.load(open('tmp/ref_chars_for_test_all.json', encoding='utf-8'))
    random.shuffle(ref_chars_for_test_all)

    n_ref = 8
    ref_chars_for_test = ref_chars_for_test_all[:n_ref]
    print(f'ref_chars_for_test={ref_chars_for_test}')
    print(len(ref_chars_for_test))

    with open(f'./_resources/split_of_chars/ref_chars_for_test_{n_ref}.json', 'w', encoding='utf-8') as f:
        json.dump(ref_chars_for_test, f, ensure_ascii=False, indent=2)
