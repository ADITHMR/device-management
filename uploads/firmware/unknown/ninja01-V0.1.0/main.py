# Author: Adith Pillai
# Language: MicroPython
# Project Name: RoboNinjaz

import machine
import time
from drivers.display import *
from drivers.ir_decode import *
from process.run_activity import run
from utils import get_jsonvalue_from_file


proj=get_jsonvalue_from_file("schema.dat","PROJECT")
print(f"project_name-->{proj}")

try:
    run(proj)


except KeyboardInterrupt:
    pass
