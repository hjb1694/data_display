import os
import getpass
import sys

MyUserName = getpass.getuser()
Here = os.getcwd()

dirname = input("directory name of environmnet: ")

env = os.path.join(Here,dirname)

version = str(sys.version_info.major) + "." + str(sys.version_info.minor)

os.system("mkdir " + env)

command = "python" + version +" -m venv " + env
print(command)
os.system(command)

print("environment created, run 'source activate' from bin folder to start")