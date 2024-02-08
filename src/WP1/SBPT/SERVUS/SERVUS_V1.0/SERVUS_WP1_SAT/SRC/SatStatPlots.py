#!/usr/bin/env python

########################################################################
# SatStatPlots.py:
# This script defines all internal functions of SatPerformance Module
#
#  Project:        SBPT
#  File:           SatStatPlots.py
#  Date(YY/MM/DD): 24/02/08
#
#   Author: GNSS Academy
#   Copyright 2020 GNSS Academy
# 
# Internal dependencies:
#   COMMON
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)
from collections import OrderedDict
#from COMMON.Plots import generatePlot
from COMMON import GnssConstants
from math import sqrt
import numpy as np
