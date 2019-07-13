<h1> How to install Compunit on amazon ec2 ( Ubuntu ) </h1>
1. Install git <br>
2. git clone this repository <br>
3. remove the protodata folder inside the compunit<br>
4. <strong>Note: the follow step is to install FSL and set path which requires python 2.7</strong> <br>
4.1. $ pip install python-pip <br>
4.2. $ sudo apt install virtualenv <br>
4.3. $ virtualenv venv2.7 <br>
4.4. $ source venv2.7/bin/activate <br>
4.5. $ python fslinstaller.py <br>
4.6. NOTE : Set the path of FSL in /.bash_profile and .bashrc and /etc/bash.bashrc<br>
Add the following piece of code in the files below : 
<p>
# FSL Setup
FSLDIR=/usr/local/fsl <br>
PATH=${FSLDIR}/bin:${PATH} <br>
export FSLDIR PATH <br>
. ${FSLDIR}/etc/fslconf/fsl.sh <br>
</p> 
<p> 
  in these files by running the following commands : <br>
            $ vi /etc/bash.bashrc <br>
            $ vi ~/.bash_profile <br>
            $ vi /home/.bashrc <br> </p>
4.8. $ deactivate ( This command deactivates the virtual env and from here we dont need the venv2.7) <br> 
4.7. reboot the instance for FSL to work<br>
5. $ sudo apt-get install python3-venv<br>
6. $ sudo apt-get install python3-dev<br>
7. $ /bin/bash setup.sh  ( This is a critical step, ensure that all packages are installed even if their wheels fail. Make sure pycortex is installed) <br>
8. $ source venv/bin/activate<br>
9. In this step, you must download the following folder from google drive link below and place the contents in that folders as instructed below. <br>
9.1. Link to the google drive 'https://drive.google.com/drive/folders/14r5DwNgAAn2LdGHVLpxY660VOFE0XsWu?usp=sharing' <br> 
9.2. From this downloaded folder, place the subfolder named 'protodata' in the compunit folder in your instance. The folder must be in the same path as your 'core' subfolder<br>
9.3 From this downloaded folder, place the subfolder named 'AFS','BFS,'CFS','MNI' and 'colormaps' in the compunit folder in your instance. The folder must be in this path '/home/ubuntu/compunit/venv/src/pycortex/filestore/db' in the 'db' folder <br>
10. $ cd core <br>
11. $ python replicate.py <br>
<h3> From the next time, all you need to do to run this unit is to run the commands 8, 10 and 11. </h3> 
