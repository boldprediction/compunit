# import six
import os
# import glob
# import copy
import json
# if six.PY2:  # python 2
#     from Queue import Queue
#     from ConfigParser import NoOptionError
# else:  # python 3
#     from queue import Queue
#     from configparser import NoOptionError
import shutil
# import random
# import functools
# import binascii
# import mimetypes
# import threading
# import warnings
# import webbrowser
# import numpy as np
# from tornado import web

# from .FallbackLoader import FallbackLoader
from cortex import utils, dataset #options, volume,
from cortex.database import db
# from . import serve
from cortex.webgl.data import Package



def make_static_light(outpath, data, types=("inflated",), recache=False, cmap="RdBu_r",
                template="static.html", layout=None, anonymize=False,
                disp_layers=['rois'], extra_disp=None, html_embed=True,
                copy_ctmfiles=True, **kwargs):
    outpath = os.path.abspath(os.path.expanduser(outpath)) # To handle ~ expansion
    if not os.path.exists(outpath):
        os.makedirs(outpath)
        os.makedirs(os.path.join(outpath, "data"))

    data = dataset.normalize(data)
    if not isinstance(data, dataset.Dataset):
        data = dataset.Dataset(data=data)

    # db.auxfile = data

    package = Package(data)
    # subjects = list(package.subjects)

    # ctmargs = dict(method='mg2', level=9, recache=recache, decimate=True)
    # ctms = dict((subj, utils.get_ctmpack(subj,
    #                                      types,
    #                                      disp_layers=disp_layers,
    #                                      extra_disp=extra_disp,
    #                                      **ctmargs))
    #             for subj in subjects)

    # db.auxfile = None
    # if layout is None:
    #     layout = [None, (1,1), (2,1), (3,1), (2,2), (3,2), (3,2), (3,3), (3,3), (3,3)][len(subjects)]

    # ## Rename files to anonymize?
    # submap = dict()
    # for i, (subj, ctmfile) in enumerate(ctms.items()):
    #     oldpath, fname = os.path.split(ctmfile)
    #     fname, ext = os.path.splitext(fname)
    #     if anonymize:
    #         newfname = "S%d"%i
    #         submap[subj] = newfname
    #     else:
    #         newfname = fname
    #     ctms[subj] = newfname+".json"

    #     for ext in ['json','ctm', 'svg']:
    #         srcfile = os.path.join(oldpath, "%s.%s"%(fname, ext))
    #         newfile = os.path.join(outpath, "%s.%s"%(newfname, ext))
    #         if os.path.exists(newfile):
    #             os.unlink(newfile)

    #         if os.path.exists(srcfile) and copy_ctmfiles:
    #             shutil.copy2(srcfile, newfile)

    #         if ext == "json" and anonymize:
    #             ## change filenames in json
    #             nfh = open(newfile)
    #             jsoncontents = nfh.read()
    #             nfh.close()

    #             ofh = open(newfile, "w")
    #             ofh.write(jsoncontents.replace(fname, newfname))
    #             ofh.close()

    # if len(submap) == 0:
    #     submap = None

    #Process the data
    metadata = package.metadata(fmt="/static/simulate/data/{name}_{frame}.png")
    images = package.images
    #Write out the PNGs
    for name, imgs in images.items():
        impath = os.path.join(outpath, "data", "{name}_{frame}.png")
        for i, img in enumerate(imgs):
            with open(impath.format(name=name, frame=i), "wb") as binfile:
                binfile.write(img)

    return json.dumps(metadata)