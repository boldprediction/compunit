# Computation Unit of Bold Predictions 
## This repository contains the latest code of Computation Unit of Bold Predictions developed by Team Incredible Minions under the guidance of Dr Leila Wehbe
### Steps to install Computation Unit on your device (Currently supported on Ubuntu and MacOS) 
1. Install git
2. git clone this repository
3. Run the following piece of code to install FSL. **This step requires python 2.7**
```
$ pip install python-pip
$ sudo apt install virtualenv
$ virtualenv venv2.7
$ source venv2.7/bin/activate
$ python fslinstaller.py
$ deactivate (Note: From here we dont need the venv2.7/python2.7)
```
4. Add the path for FSL <br />
**NOTE : Set the path for FSL by copying the following script into *[~/.bash_profile]* (MACOS) (or) *[~/etc/bash.bashrc]* (Ubuntu)** <br /><br />
       **For EC2 users - Please use the cloud Init script provided in the https://github.com/boldprediction/CloudInitScripts-**
       **and add it as directed in that repository. After that, please add the following script in *[~/etc/bash.bashrc]***

  - Add the following piece of code in the files mentioned above:
  
```
#FSL Setup 
FSLDIR=/usr/local/fsl
PATH = ${FSLDIR}/bin:${PATH}
export FSLDIR PATH
. ${FSLDIR}/etc/fslconf/fsl.sh
```
5. **Reboot the instance/system for FSL to work** <br />
6. Run the following code in the ***[/compunit]*** directory 
```
$ sudo apt-get install python3-venv
$ sudo apt-get install python3-dev
$ mkdir data
$ /bin/bash setup.sh ( This is a critical step, ensure that all packages are installed even if their wheels fail. Make sure pycortex is installed)
$ source venv/bin/activate
```
7. In this step, you must download the **data** folder from google drive link below and place the contents in the ***[~/compunit/data]*** as instructed below -
    - Link to the google drive 'https://drive.google.com/drive/folders/16YJCsN9qgTeULR4OwyAnl_afrqK9TxYg?usp=sharing'
    - From the folder downloaded from Google Drive, place the entire content of this folder into ***[~/compunit/data]***
    - Note that your ***[~/compunit/data]*** folder should have the following files 
      * /filestore  (Folder)
      * /subjects   (Folder)
      * /semanticmodels (Folder)
      * /MNI_nan_mask.npy (File)
8. **To start the computation unit, run the following script when the venv(Not venv2.7) is activated from *[~/compunit]***
```
$ cd src
$ python3 main.py 
```

### FAQ's 
1. Computation Unit creates and logs activities in the logfile named 'compunit.log' which is in *[~/compunit/logs]* folder 
2. We noticed that sometimes few of the packages are not installed when we run the setup.sh script. Althought, we couldn't replicate this issue, 
we advice people to install these packages using `pip3 install <package_name>` in the virtual environment ***venv*** (Not venv2.7) 
