import torch
import torchvision

import torchvision.transforms as transforms
import torch.nn.functional as F

from PIL import Image
from src import draw_image_from_ttf, save_ttf_from_image, display_and_check


def tensor_to_pil(img, padding, n_row, func=None, img_type='L'):
    img = img * 0.5 + 0.5
    img = torchvision.utils.make_grid(tensor=img, padding=padding, nrow=n_row)
    ndarr = img.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
    img = Image.fromarray(ndarr).convert(img_type)

    if func is not None and n_row == 1:
        img = func(img)

    return img


def calc_RMSE(fake, real):
    fake = Image.open(fake).convert('RGB')
    real = Image.open(real).convert('RGB')

    ms_transforms = transforms.Compose([transforms.Resize([64, 64]),
                                        transforms.ToTensor()])

    fake = ms_transforms(fake).unsqueeze(0)
    real = ms_transforms(real).unsqueeze(0)

    rmse = torch.sqrt(F.mse_loss(fake, real)).item()
    print(f'RMSE: {rmse:.4}')


def save_diff(fake, real, file_name):
    fake = Image.open(fake).convert('L')
    real = Image.open(real).convert('L')

    d_transforms = transforms.Compose([transforms.ToTensor()])

    fake = d_transforms(fake).unsqueeze(0)
    real = d_transforms(real).unsqueeze(0)

    res_p = torch.nn.functional.relu(real - fake)
    res_m = torch.nn.functional.relu(fake - real)

    res_p = torch.cat([torch.zeros_like(res_p), res_p, res_p], dim=1)
    res_m = torch.cat([res_m, torch.zeros_like(res_m), res_m], dim=1)

    res = 1. - (res_p + res_m)

    fake = fake.repeat(1, 3, 1, 1)
    real = real.repeat(1, 3, 1, 1)

    img = torch.cat([fake, real, res], dim=0) * 2 - 1
    img = tensor_to_pil(img, padding=1, n_row=3, img_type='RGB')

    img.save(file_name)


def main():
    ttf_path = r'_resources\collections\0042\ChillRoundGothic_Heavy.otf'
    display_and_check(ttf_path)

    chars_ = {'智': 'tmp/智.png', '慧': 'tmp/慧.png'}
    image_size = 128

    images_ = draw_image_from_ttf(
        ttf_path=ttf_path,
        img_size=image_size,
        chars=chars_,
        draw_axis=False
    )

    font = save_ttf_from_image(
        font_name='font_tmp',
        em=1000,
        chars=images_,
        output_path='tmp/font_tmp.otf'
    )

    images_ = draw_image_from_ttf(
        ttf_path='tmp/font_tmp.otf',
        img_size=128,
        chars={'智': 'tmp/re_智.png'},
        draw_axis=False
    )

    calc_RMSE(
        fake='tmp/re_智.png',
        real='tmp/智.png'
    )
    save_diff(
        fake='tmp/re_智.png',
        real='tmp/智.png',
        file_name='tmp/diff_智.png'
    )


if __name__ == "__main__":
    main()
