import os

from cortex import dataset
from constant import OUTPUTS_DIR
from cortex.webgl.data import Package


# def make_static_light(out_path, data, types=("inflated",), recache=False, cmap="RdBu_r",
#                 template="static.html", layout=None, anonymize=False,
#                 disp_layers=['rois'], extra_disp=None, html_embed=True,
#                 copy_ctmfiles=True, **kwargs):

def make_static_light(data):

    data = dataset.normalize(data)
    if not isinstance(data, dataset.Dataset):
        data = dataset.Dataset(data=data)

    # Process the data
    package = Package(data)
    metadata = package.metadata(fmt="{name}_{frame}.png")
    images = package.images

    # Write out the PNGs
    for name, images in images.items():
        image_path = os.path.join(OUTPUTS_DIR, "{name}_{frame}.png")
        for i, img in enumerate(images):
            with open(image_path.format(name=name, frame=i), "wb") as binfile:
                binfile.write(img)

    return metadata
