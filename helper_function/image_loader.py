from secrets import token_hex
import os
from project import app
from PIL import Image


def image_loader(image_file):
    file_name = token_hex(8)
    _, f_ext = os.path.splitext(image_file.filename)
    n_filename = file_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', n_filename)
    i = Image.open(image_file)
    i.thumbnail((150, 150))
    i.save(picture_path)
    return n_filename
