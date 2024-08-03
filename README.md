# fastapi
fastapideployment

# Setting up Server in VPS hostinger..
1. Open CLI in VPS hostinger
2. copy this command 'sudo apt update'
3. 'sudo apt install -y software-properties-common'
3. 'sudo apt install -y build-essential libssl-dev libffi-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libgdbm-dev libdb-dev libpcap-dev'
4. 'sudo add-apt-repository ppa:deadsnakes/ppa'
5. 'sudo apt update'
6. 'sudo apt install python3.9' (Need to install python 3.9.7 cause packages are supported in this version of python.)
7. 'sudo apt install python3.9-distutils'
8. 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
9. 'sudo python3.9 get-pip.py'
10. 'python3.9 --version' (results should be Python 3.9.something..)

# Setting python 3.9.something as a Primary python interpreter..
1. sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
2. sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2
3. sudo update-alternatives --config python3

4. If you encounter issues with broken packages, try running:
5.  'sudo apt --fix-broken install'

# Clone the repository to the VPS Hostinger
1. run 'git clone "https://github.com/lightdarkmaster/fastapi" ' to clone repository.
2. and then 'cd fastapi'
3. run 'pip3 install -r requirements.txt'
## if it doesn't work 
install requirements one by one.
e.g 
1. pip3 install tensorflow
2. pip3 install tensorflow
3. pip3 install fastapi
4. pip3 install uvicorn
5. pip3 install python-multipart
6. pip3 install pillow
7. pip3 install tensorflow-serving-api
8. pip3 install matplotlib
9. pip3 install numpy

after all intallations run this command
1. cd app
2. uvicorn main-tf-serving:app --reload --host 0.0.0.0
3. and the server will run if no errors occurs during the process and all packages are installed properly..

uvicorn main-tf-serving:app --reload --host 0.0.0.0

<<<<<<< HEAD
# need SSL certificate for the  VPS server2
# need to fix the unprocessable entity error.
# Need to fix ASAP.. redirect domain to the IP address.
# I Change to Almalinux
# GCF Google cloud platform and Google Cloud Function..
=======
1. need SSL certificate for the  VPS server2
2. need to fix the unprocessable entity error.
>>>>>>> origin/main
