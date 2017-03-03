#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os.path


paths = glob.glob('Source/*.jpg')


if os.path.exists('Result'):
    pass
else:
    os.mkdir('Result')

for p in paths:
    folder, image = os.path.split(p)
    new_path = 'Result/{0}'.format(image)
    img_conv = 'convert {0} -resize 200 {1}'.format(p, new_path)
    os.system(img_conv)
    print(new_path)
