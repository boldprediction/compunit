#!/bin/bash
python3 -m venv venv/
source venv/bin/activate
pip3 install decorator==4.4.0       
pip3 install future==0.17.1 
pip3 install html5lib==1.0.1 
pip3 install networkx==2.1
pip3 install scipy==1.2.0
pip3 install setuptools==41.0.1
pip3 install Shapely==1.6.4.post2
pip3 install six==1.12.0
pip3 install webencodings==0.5.1
pip3 install wheel==0.33.4

pip3 install tables==3.5.1
pip3 install nibabel==2.4.0
pip3 install Cython==0.29.6
pip3 install nipy==0.4.2
pip3 install h5py==2.9.0
pip3 install Pillow==6.0.0
pip3 install seaborn==0.9.0
pip3 install tornado==4.3
pip3 install lxml==4.3.3

pip install boto3
cd venv
pip3 install -e git+git@github.com:boldprediction/pycortex.git#egg=pycortex
deactivate
