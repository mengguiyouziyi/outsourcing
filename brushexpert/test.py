import os

bpath = os.path.join(os.getcwd(), 'file')
item_base_path = 'United Kingdom1'
png_path = os.path.join(bpath, item_base_path)
png_file = f'{png_path}.png'
with open(png_file, 'w') as out:
    out.write('nihao')
