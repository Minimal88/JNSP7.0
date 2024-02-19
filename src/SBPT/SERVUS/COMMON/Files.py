import sys
from pandas import read_csv
from COMMON.Dates import convertYearMonthDay2JulianDay
from collections import OrderedDict

def readDataFile(dataFilePath, columnNameList, skipRows = 1):
    """
    Read specific columns from a statistics file and return a DataFrame.

    Parameters:
    - statisticsFilePath: Path to the statistics file.
    - columnNameList: List of column names to be read.
    - skipRows: Number of rows to skip. 1 by default.

    Returns:
    - FetchedData containing the specified columns.
    """
    # Read the specified columns from the file
    FetchedData = read_csv(
        dataFilePath, delim_whitespace=True, skiprows=skipRows, header=None, usecols=columnNameList)    

    # Set column names based on the provided columnList    
    #FetchedData.columns = columnNameList

    return FetchedData

# Function to read the configuration file
def readConf(CfgFile):
    Conf = OrderedDict({})
    with open(CfgFile, 'r') as f:
        # Read file
        Lines = f.readlines()

        # Read each configuration parameter which is compound of a key and a value
        for Line in Lines:
            if "#" in Line: continue
            if not Line.strip(): continue
            LineSplit = Line.split('=')
            try:
                LineSplit = list(filter(None, LineSplit))
                Conf[LineSplit[0].strip()] = LineSplit[1].strip()

            except:
                sys.stderr.write("ERROR: Bad line in conf: %s\n" % Line)

    return Conf

def processConf(Conf):
    ConfCopy = Conf.copy()
    for Key in ConfCopy:
        Value = ConfCopy[Key]
        if Key == "INI_DATE" or Key == "END_DATE":
            ParamSplit = Value.split('/')

            # Compute Julian Day
            Conf[Key + "_JD"] = \
                int(round(
                    convertYearMonthDay2JulianDay(
                        int(ParamSplit[2]),
                        int(ParamSplit[1]),
                        int(ParamSplit[0]))
                    )
                )

    return Conf