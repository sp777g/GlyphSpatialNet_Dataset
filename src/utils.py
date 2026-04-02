import defcon
import ufo2ft
import numpy as np
import os

from PIL import Image, ImageDraw, ImageFont
from potrace import Bitmap
from fontTools.ttLib import TTFont, TTCollection
from io import BytesIO
from glob import glob


def get_coordinate(img_size: int) -> dict[str, int]:
    #################################################
    factor = 0.8
    baseline_offset = 0.1
    char_size = int(factor * img_size + 0.5)
    start_x = int(img_size / 2 - char_size / 2 + 0.5)
    start_y = int(img_size / 2 + char_size / 2 - baseline_offset * img_size + 0.5)
    #################################################

    return {'char_size': char_size, 'start_x': start_x, 'start_y': start_y}


def get_defined_chars(ttf_path: str, gb_t_2313_chars: set[str]) -> set[str]:
    ex = os.path.basename(os.path.normpath(ttf_path)).split('.')[-1].lower()
    if ex == 'ttc':
        font = TTCollection(ttf_path)[0]
    else:
        font = TTFont(ttf_path)

    all_defined_chars = set([chr(y) for y in font["cmap"].tables[0].cmap.keys()])
    defined_chars = gb_t_2313_chars.intersection(all_defined_chars)

    return defined_chars


def get_ttf_paths(path: str) -> list[str]:
    ttf_paths = list()
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        assert os.path.isdir(full_path)
        ttf_path = glob(f'{full_path}/*.ttf') + glob(f'{full_path}/*.otf') + glob(f'{full_path}/*.ttc')
        assert len(ttf_path) == 1
        ttf_paths.append(ttf_path[0])

    return ttf_paths


def render_single_char(font: ImageFont, char: str, img_size: int, xy: tuple[int, int],
                       draw_axis: bool) -> Image or None:
    image = Image.new(mode="L", size=(img_size, img_size), color=255)
    draw = ImageDraw.Draw(im=image)
    draw.text(xy=xy, text=char, font=font, anchor='ls')

    is_avail = True
    if (255 - np.array(image)).sum() == 0:
        print(f'检测到空白图像，请检查字体{font.getname()}是否支持字符\'{char}\'')
        is_avail = False
        image = None

    if is_avail and draw_axis:
        start_x, start_y = xy
        draw.line(xy=((0, start_y), (img_size, start_y)), fill=0)
        draw.line(xy=((start_x, 0), (start_x, img_size)), fill=0)

    return image


def draw_image_from_ttf(ttf_path: str | BytesIO, img_size: int, chars: dict[str, str | None],
                        draw_axis: bool = False) -> dict[str, Image]:
    """
    :param ttf_path:
    :param img_size:
    :param chars: {char: saved_file_name}
    :param draw_axis:
    :return:
    """
    #################################################
    coord = get_coordinate(img_size=img_size)
    char_size = coord['char_size']
    start_x = coord['start_x']
    start_y = coord['start_y']
    #################################################

    font = ImageFont.truetype(font=ttf_path, size=char_size)

    result = dict()
    for char, saved_file_name in chars.items():
        img = render_single_char(font=font, char=char, img_size=img_size, xy=(start_x, start_y), draw_axis=draw_axis)
        if saved_file_name is not None:
            assert img is not None, f'检测到空白图像，拒绝保存'
            img.save(saved_file_name)

        result[char] = img

    return result


def create_ufo(font_name: str, em: int) -> defcon.Font:
    font = defcon.Font()
    font.info.familyName = font_name
    font.info.unitsPerEm = em
    return font


def transform(x: int, y: int, img_size: int, em: int) -> tuple[int, int]:
    #################################################
    coord = get_coordinate(img_size=img_size)
    char_size = coord['char_size']
    start_x = coord['start_x']
    start_y = coord['start_y']
    #################################################

    scale = em / char_size

    z = np.array([x, y])
    a = np.array([[scale, 0], [0, -scale]])
    b = np.array([-scale * start_x, scale * start_y])

    z = a @ z + b

    return z.tolist()


def add_char_to_ufo(font: defcon.Font, chars: dict[str, Image]) -> None:
    assert len(chars) > 0
    em = font.info.unitsPerEm

    for char, image in chars.items():
        img_size = image.size[0]

        bm = Bitmap(image)
        plist = bm.trace(opticurve=False)

        assert len(char) == 1
        unicode_val = ord(char)
        hex_code = f"{unicode_val:04X}"  # 自动处理4位以上
        glyph_name = f"uni{hex_code}"

        glyph = font.newGlyph(glyph_name)
        glyph.width = em
        font[glyph_name].unicodes = [unicode_val]

        pen = glyph.getPen()
        for curve in plist:
            x = curve.start_point.x
            y = curve.start_point.y
            x, y = transform(x, y, img_size, em)
            pen.moveTo((x, y))

            for segment in curve.segments:
                if segment.is_corner:
                    x = segment.c.x
                    y = segment.c.y
                    x, y = transform(x, y, img_size, em)
                    pen.lineTo((x, y))

                    x = segment.end_point.x
                    y = segment.end_point.y
                    x, y = transform(x, y, img_size, em)
                    pen.lineTo((x, y))
                else:
                    c1_x = segment.c1.x
                    c1_y = segment.c1.y
                    c2_x = segment.c2.x
                    c2_y = segment.c2.y
                    x = segment.end_point.x
                    y = segment.end_point.y
                    c1_x, c1_y = transform(c1_x, c1_y, img_size, em)
                    c2_x, c2_y = transform(c2_x, c2_y, img_size, em)
                    x, y = transform(x, y, img_size, em)
                    pen.curveTo((c1_x, c1_y), (c2_x, c2_y), (x, y))

            pen.closePath()


def save_ttf(font: defcon.Font, output_path: str) -> TTFont:
    ttf_font = ufo2ft.compileTTF(
        font,
        useProductionNames=False,
        removeOverlaps=True,
        convertCubics=True,
    )

    post_table = ttf_font["post"]
    post_table.formatType = 3.0
    post_table.extraNames = []

    if output_path is not None:
        ttf_font.save(output_path)

    return ttf_font


def save_ttf_from_image(font_name: str, em: int, chars: dict[str, Image], output_path: str = None) -> TTFont:
    """
    :param font_name:
    :param em:
    :param chars: {char: PIL.Image}
    :param output_path:
    :return:
    """
    ufo_font = create_ufo(font_name=font_name, em=em)
    add_char_to_ufo(font=ufo_font, chars=chars)
    return save_ttf(font=ufo_font, output_path=output_path)


def display_and_check(ttf_path: str) -> None:
    file_name = os.path.basename(os.path.normpath(ttf_path))
    print(f'file_name={file_name}')

    font = TTFont(ttf_path)
    assert 'h' + 'hea' in font, '字体不支持水平布局'

    em_units = font['head'].unitsPerEm
    print(f'em={em_units}')

    name_table = font['name']
    family_name = name_table.getName(1, 3, 1) or name_table.getName(1, 1, 0)
    full_name = name_table.getName(4, 3, 1) or name_table.getName(4, 1, 0)
    print(f'family_name={family_name.toUnicode()}')
    print(f'full_name={full_name.toUnicode()}')

    hhea_table = font['hhea']
    ascender = hhea_table.ascent
    descender = hhea_table.descent
    print(f'ascender={ascender} ({ascender / em_units:.4f})')
    print(f'descender={descender} ({descender / em_units:.4f})')


def identity_check(image_size: int, images: dict[str, Image], tolerance: float = 1e-2,
                   output_path: str = None) -> float:
    font = save_ttf_from_image(
        font_name='Font_temp',
        em=1000,
        chars=images,
        output_path=output_path
    )

    buffer = BytesIO()
    font.save(buffer)
    buffer.seek(0)

    reconstructed_images = draw_image_from_ttf(
        ttf_path=buffer,
        img_size=image_size,
        chars={key: None for key in images.keys()}
    )

    # max_pixel_loss = 0.
    # for char in images.keys():
    #     img = np.array(images[char])
    #     re_img = np.array(reconstructed_images[char])
    #     assert img.size == re_img.size
    #
    #     diff = np.abs(img - re_img)
    #     extreme_diff_count = np.sum(diff == 255)
    #     total_pixels = img.size
    #
    #     pixel_loss = extreme_diff_count / total_pixels
    #     max_pixel_loss = max(max_pixel_loss, pixel_loss)
    #     assert pixel_loss < tolerance, f'字符\'{char}\'的重建损失大于{tolerance}'

    max_l1_loss = 0.
    for char in images.keys():
        img = np.array(images[char])
        re_img = np.array(reconstructed_images[char])
        assert img.size == re_img.size

        l1_loss = np.mean(np.abs(img / 255.0 - re_img / 255.0))

        max_l1_loss = max(max_l1_loss, l1_loss)


    buffer.close()
    return max_l1_loss
