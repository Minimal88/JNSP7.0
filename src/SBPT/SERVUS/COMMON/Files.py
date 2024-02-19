from pandas import read_csv

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