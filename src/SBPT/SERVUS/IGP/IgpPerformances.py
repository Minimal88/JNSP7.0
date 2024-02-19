#!/usr/bin/env python

########################################################################
# SBPT/SRC/IgpPerformances.py:
# This function is the Main Function of IGP PERF Module
#
#  Project:        SBPT/SERVUS
#  File:           IgpPerforamnces.py
#  Date(YY/MM/DD): 24/02/19
#
#   Author: Esteban Martinez Valvere
#   Copyright 2021 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
# Usage:
# i.e: IgpPerformances $SCEN_PATH

# Internal dependencies:
#   COMMON
########################################################################

# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, projectDir)
from COMMON.Dates import convertYearMonthDay2JulianDay
from COMMON.Dates import convertJulianDay2YearMonthDay
from COMMON.Dates import convertYearMonthDay2Doy


#####################################################################
#END OF IGP PERFORMANCES MODULE
#######################################################
