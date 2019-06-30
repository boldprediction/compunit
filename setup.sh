#!/bin/bash
python3 -m venv venv/
source venv/bin/activate
pip3 install tables==3.5.1
pip3 install nibabel==2.4.0
pip3 install Cython==0.29.6
pip3 install nipy==0.4.2
pip3 install h5py==2.9.0
pip3 install Pillow==6.0.0
pip3 install seaborn==0.9.0
pip3 install tornado==4.3
pip3 install lxml==4.3.3
pip3 install -e git+https://github.com/gallantlab/pycortex.git#egg=pycortex
deactivate
