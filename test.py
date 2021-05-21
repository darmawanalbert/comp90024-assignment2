import subprocess as sp
import os

os.environ["INSTANCE1"] = "1"
sp.call("echo $INSTANCE1", shell=True)