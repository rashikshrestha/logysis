import re
import numpy as np

def logysis(filename: str):
    """Read Logfile
    
    Parameters
    ----------
    filename: str
        Path to logfile

    Returns
    -------
    out: list
        List of dictionary items of data
    """
    idx, data = read_logfile(filename)
    header = read_header(data)
    out = read_data(data, idx, header)
    return out

def read_logfile(filename: str):
    """Read log file

    Reads a text file and returns each line in list.
    Removes traning \n of each line.

    Parameters
    ----------
    filename: str
        Log file path 

    Returns
    -------
    idx: list
        List of idex of each data point
    data: list
        List of lines in logfile
    """
    # Read Log file
    with open(filename, 'r') as f:
        data = f.readlines()

    # Get LineNumbers of beginning of keypoint data
    idx = []
    for i in range(len(data)):

        # Remove new line character at the end (if exists)
        if data[i][-1] == '\n':
            data[i] = data[i][:-1]

        if data[i] == "---":
            idx.append(i)

    return idx[:-1], data


def read_header(data: list):
    """Reader the header of logfile

    Parameters
    ----------
    data: list
        List of lines in logfile

    Returns
    -------
    header: list
        Headers
    """
    start_reading = 0
    header = []
    for line in data:
        if line == '###':
            if not start_reading:
                start_reading = 1
                continue
            else:
                break
        if start_reading:
            l = re.split(';|,', line)
            header.append(l)

    return header


def parse_csv(csv_data: str, dtype: str) -> np.ndarray:
    """
    Parse csv string to numpy array

    Parameters
    ----------
    kpts_string: str
        Keypoints String

    Returns
    -------
    k_np: np.ndarray
        Keypoints (N,2) [np.float32]
    """
    csv_data = csv_data.replace(" ", "")  # Remove spaces if exists
    k = re.split(';|,', csv_data)  # Split on the basis of , and ;
    if k[-1] == '':  # Remove last element if empty
        k = k[:-1]
    dim_values = re.split('x', k[0])
    dim = []
    for d in dim_values:
        dim.append(int(d))
    dim = tuple(dim)
    k = k[1:]
    k_float = [float(x) for x in k]
    k_np = np.array(k_float)
    k_np = k_np.reshape(dim)

    if dtype == 'np.float32':
        return k_np.astype(np.float32)
    if dtype == 'np.uint8':
        return k_np.astype(np.uint8)
    else:
        print("UNKNOWN DATATYPE")


def read_val(value: str, dtype: str) -> np.ndarray:
    """
    Read value string to desired value

    Parameters
    ----------
    value: str
        Value in string

    Returns
    -------
    v: int/float/bool
        Desired Value
    """
    if dtype == 'int':
        return int(value)

    elif dtype == 'float':
        return float(value)

    elif dtype == 'str':
        return str(value)

    elif dtype == 'bool':
        if value == '0':
            return False
        elif value == '1':
            return True
        else:
            print("UNKNOWN BOOL VALUE")
    else:
        print("UNKNOWN DATATYPE")


def read_data(data: list, idx: list, header: list) -> list:
    """Read the logfile data

    Parameters
    ----------
    data: list
        List of lines in logfile
    idx: list
        List of idex of each data point
    header: list
        List of headers

    Returns
    -------
    data_out: list
        List of dictionary items of data
    """
    data_out = []

    for i in idx:
        data_item = {}

        for j in range(len(header)):

            if header[j][1] == 'csv':
                value = parse_csv(data[i+j+1], header[j][2])

            elif header[j][1] == 'val':
                value = read_val(data[i+j+1], header[j][2])

            data_item[header[j][0]] = value

        data_out.append(data_item)

    return data_out

