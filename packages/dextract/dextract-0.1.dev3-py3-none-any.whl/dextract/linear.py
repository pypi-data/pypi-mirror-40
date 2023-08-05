#!/usr/bin/env python
# coding: utf-8

# Developer: Carlos Hernandez (cseHdz)
# Date: October 2018

"""
Optional Parameters
-----------

XL Extraction:
------------------------- Extracting XL Files --------------------------------
- parallel_xl (int):
    Outline the number of parallel processes to run

- process (dict): data process to follow (includes all sections below)
    requires extraction, pre_clean and post_clean keys

- as_named_list (Bool):
    Transform the result from extraction into a named list

- names_from_list (list):
    list of names to use for name_list

- names_from_dict {df['ID']: name}:
    dictionary of names to assigned depending on the ID column
    generated through conversion to list
---------------------- Extracting Individual Shets Files ----------------------

- unmerge (bool):
    Unmergecells identified as merged in xlrd


Data Process:
------------------------- General Data Process---------------------------------
- process {key: {extraction}, {pre_clean}, {post_clean}}: data process to follow (includes all sections below)
    requires extraction, pre_clean and post_clean keys

- ignore_process (Bool):
    designed for recursive extraction process - avoid all process


Extraction:
--------------------------- Extraction Process --------------------------------
- data_loss (0-1):
    % of cells that must be empty to consider a cell empty

- thresholds {0: (0-1), 1: (0-1), 2:(0-1)}
    override statistic threshold generation

- method (str):
    slicing method

- s_output (str):
    Type of output to retrieve from slicing ([slice list], search, 'all')

- search_dict {name: search_str}:
    Values to find and name for resulting df

- concat_search_axis (int):
    Concatenate dfs if result from extraction is list


Pre_Clean:
----------------------------- Pre-Cleaning Process ----------------------------
- transpose_data (Bool):
    Transpose rows to cols

- ignore_empty_rows (Bool):
    Delete fully empty rows

- ignore_empty_cols (Bool):
    Delete fully empty cols

- ignore_empty_cells (Bool):
    Ignore non-complete rows

- delete_by_threshold (float 0-1)
    Filter rows that are empty to a certain threshold


Post_Clean:
----------------------------- Post-Cleaning Process ---------------------------

- treat_axis_as_data (axis):
    Treat entire axis as data type

- header_row (int):
    Arbitrary header row

- header_column (int):
    Arbitrary header column

- fill_headings (Bool):
    Fill columns and rows identified as HEADING (ffill)

- index_as_col (Bool):
    Add index as a column

- compress_header (Bool):
    Unique value for columns based on index HEADINGS

- add_header (df):
    Custom header to append to the result df(s)

- ensure_no_rep (list or str)
    Ensure values are not repeated in a series

- transpose_output (Bool):
    Transpose final df

- drop_partial_records (Bool):
    Remove records that are incomplete

- drop_empty_records (Bool):
    Remove records that are fully empty

- drop_empty_cols (Bool):
    Remove columns that are fully empty

- add_columns {name: default_value}:
    Add columns with a specified name and a default value

- columns_as_row (Bool):
    Add columns as Header

- rename_columns {cur_name: new_name}:
    Rename columns in a dataframe

- rename_index {cur_name: new_name}:
    Rename rows in a dataframe

- delete_columns ([name_list])
    Delete a list of columns if found

"""

""" ----------------------------- IMPORTING --------------------------------"""
# In[]:
import os
import copy
import xlrd
import pandas as pd
import numpy as np
import pyexcel as pe
import pyexcel_xls
import pyexcel_xlsx
import statistics
from collections import Counter
from multiprocessing import Pool
import gc
import csv


""" ------------------------------- SLICING --------------------------------"""
# In[]:
def __map_value(value, file_type = None):

    """ Determine the type of a given value """
    if file_type == 'xlrd':
        return list(0, 1, 2, 2, 2, 0, 0)[value]
    else:
        if type(value) is str and bool(value): return 1 # HEADING
        elif type(value) is int or type(value) is float: return 2 # DATA
        else: return 0 # EMPTY


# In[]:
def __calc_density(data):

    """ Determine the types and counts of rows and column within a
        list of lists """
    rdensity = [[__map_value(x) for x in row] for row in data]
    cdensity = __transpose_data(rdensity)

    """ Type of all cells within data """
    fdensity = [__map_value(x) for row in data for x in row]

    return {"rows": [dict(Counter(x)) for x in rdensity],
            "cols": [dict(Counter(x)) for x in cdensity],
            "full": dict(Counter(fdensity))}


# In[]:
def __calc_threshold(density):

    """ Find the thresholds required to assess if a record is
    a header, data or empty """
    ratios = {0:[], 1:[],  2:[]}
    threshold = {0: 0.6, 1: 0.5, 2: 0.3} # Minimum threshold

    """Iterate thro every row's density only passing through exising types
       Calculate cells ratios from total and add it if it exceeds minimum """
    for row in density:
        for i in row.keys():
            ratio = row[i]/sum(row.values())
            if ratio > threshold[i]: ratios[i].append(ratio)

    """ Perform Quick statistics to identify dispersion
        A minimum of two observations is required to replace minimum  """
    for key, x in ratios.items():
        if len(x) > 1:
            threshold[key] = statistics.mean(x)
            threshold[key]-= 0.2 * statistics.stdev(x)

        """ Ensure the threshold is smaller than the first one, otherwise
            it will not capture the type given conditions are elif """
        if key > 0: threshold[key] = min(threshold[key], threshold[key - 1])

    return threshold


# In[]:
def __slice_data (density, thresholds):

    """ Slice a list of list based on the content of its records using
        thredhold parameters to assign record types
    """

    START, SLICE = -1, 3 # Control Data Types
    ERROR, HEADING, DATA = 0, 1, 2 # Basic Data Types

    """
        Decisions Matrix to create slices (prev_type, cur_type) as key
        1. start_head (SH) - Begin couting records for a new HEADING section
        2. end_head (EH) - Finish counting records for current HEADING section
        3. start_data (SD) - Begin couting records for a new DATA section
        4. end_data (ED) - Finish counting records for current DATA section
        5. start_slice (SS) - Begin couting records for a new SLICE
        6. end_slice (ES) - Finish counting records for current SLICE
    """
    SH, EH, SD, ED, SS, ES = 0, 1, 2, 3, 4, 5

    DECISIONS = {(-1,0): [0,0,0,0,0,0],
                 (-1,1): [1,0,0,0,1,0],
                 (-1,2): [0,0,1,0,1,0],
                 (0,0) : [0,0,0,0,0,0],
                 (0,1) : [1,0,0,0,1,0],
                 (0,2) : [0,0,1,0,1,0],
                 (1,0) : [0,1,0,0,0,1],
                 (1,1) : [0,0,0,0,0,0],
                 (1,2) : [0,1,1,0,0,0],
                 (2,0) : [0,0,0,1,0,1],
                 (2,1) : [1,0,0,1,1,1],
                 (2,2) : [0,0,0,0,0,0]}

    slices = []

    """ index - type of rows
        items - sum of cell types in the slice """
    default_stypes = {'index':{t:{'count' :0,
                                  'ranges':[]} for t in range(ERROR, DATA +1)},
                      'items':{t:{'count':0} for t in range(ERROR, DATA + 1)}}

    """ ranges for each section"""
    default_ranges = {t:{'start':0,'end':0} for t in range(HEADING, SLICE + 1)}

    """ Initialize falg values and slice tracking dictionaries """
    cur_type, prev_type = START, START
    stypes = copy.deepcopy(default_stypes)
    ranges = copy.deepcopy(default_ranges)
    size = sum(list(density[0].values()))

    for index, x in enumerate(density):

        """ Determine type of each row according to thredhold
            If thresholds are met, then Data Type is found
            If HEADING and ERROR thredholds are 10, treat as DATA (ignore)
            If there are no ERRORS, then majority rules
            If there is no DATA and ERROR did not meet threshold, then HEADING
        """
        n = [int(x.get(i) or 0) for i in range(ERROR,SLICE)]

        if n[ERROR] >= size * thresholds[ERROR]: cur_type = ERROR
        elif n[HEADING] >= size * thresholds[HEADING]: cur_type = HEADING
        elif n[DATA] >= size * thresholds[DATA]: cur_type = DATA
        elif thresholds[HEADING] == thresholds[ERROR] == 10: cur_type = DATA
        elif n[ERROR] == 0: cur_type = max(x, key=x.get)
        elif n[DATA] == 0: cur_type = HEADING
        else: cur_type = DATA

        """ Get decision matrix for current case """
        decision = DECISIONS[(prev_type, cur_type)]

        # print(x, cur_type, prev_type, index, n)

        if index == len(density) - 1: # Last record

            """ Add the last record if it is a HEADING or DATA """
            if cur_type > ERROR:

                if decision[SH]: ranges[HEADING]['start'] = index
                if decision[SD]: ranges[DATA]['start'] = index

                for key, value in x.items():
                    stypes['items'][key]['count'] += value

                if prev_type == ERROR: # Ensure the slice has a start
                    ranges[SLICE]['start'] = index

                ranges[cur_type]['end'] = index + 1 # Ranges are non-inclusive

                s = np.array((ranges[cur_type]['start'],
                              ranges[cur_type]['end']))
                stypes['index'][cur_type]['ranges'].append(s)
                stypes['index'][cur_type]['count'] += 1
                s = None

                decision[ES] = 1

        """ Finish a specific Data Type Section """
        if (decision[EH] or decision[ED]):
            ranges[prev_type]['end'] = index
            s = np.array((ranges[prev_type]['start'],
                          ranges[prev_type]['end']))
            stypes['index'][prev_type]['ranges'].append(s)
            stypes['index'][prev_type]['count'] += 1

            s = None

        """ Finish a Slice """
        if decision[ES]:
            ranges[SLICE]['end'] = index

            if index == len(density) - 1 and cur_type > ERROR:
                ranges[SLICE]['end'] += 1

            s = np.array((ranges[SLICE]['start'], ranges[SLICE]['end']))
            ssize = ranges[SLICE]['end'] - ranges[SLICE]['start']
            slices.append({"slice": s,
                           "types": stypes,
                           "size": ssize})
            s = None

        """ Begin a new slice """
        if decision[SS] or decision[ES]:
            stypes = copy.deepcopy(default_stypes)
            ranges = copy.deepcopy(default_ranges)
            ranges[SLICE]['start'] = index

        """ Restart sections as required """
        if decision[SH]: ranges[HEADING]['start'] = index
        if decision[SD]: ranges[DATA]['start'] = index

        """ Add current record to current slice if not error """
        if cur_type > ERROR:
            for key, value in x.items(): # Ranges are non-inclusive
                stypes['items'][key]['count'] += value

            ranges[cur_type]['end'] = index
            ranges[SLICE]['end'] = index

        prev_type = cur_type

    return slices


# In[]:
def __concat_slices (sliceA, sliceB, data):

    """ Concat ROW and COLUMN slices - Get rectangular slices """
    slices = []
    for sA in sliceA:
        for sB in sliceB:
            """ Concatenate indices """
            r = np.concatenate((sA['slice'], sB['slice']), axis = 0)
            s_data = [[data[i][j] for j in range(r[2],r[3])]\
                       for i in range(r[0],r[1])]

            """ Recalculate new density """
            density = __calc_density(s_data)
            slices.append({'slice': r,
                           'shape': {'size': sA['size']*sB['size'],
                                     'rows': sA['size'],
                                     'cols': sB['size']},
                           'density': density,
                           'index': {'rows': sA['types']['index'],
                                     'cols': sB['types']['index']}})
    return(slices)


# In[]:
def __get_slices(data, data_loss = 1, thresholds = {}, method = "full"):

    """ Calculate the type density of the data provided """
    density = __calc_density(data)

    """ Default thresholds """
    if len(thresholds) == 0:
        thresholds = {"rows": __calc_threshold(density["rows"]),
                      "cols": __calc_threshold(density["cols"])}

    if data_loss < 1: # Overrides EMPTY threshold
        thresholds["rows"][0] = max(1 - data_loss, 0.6)
        thresholds["cols"][0] = max(1 - data_loss, 0.6)

    if method == "rows": # Ensures cols are treated as data
        thresholds["cols"][0] = 10
        thresholds["cols"][1] = 10

    elif method == "cols": # Ensures rows are treated as data
        thresholds["rows"][0] = 10
        thresholds["rows"][1] = 10

    """ Calculate ROW SLICES, COLUMN SLICES, then concatenate """
    rslices = __slice_data(density["rows"], thresholds["rows"])
    cslices = __slice_data(density["cols"], thresholds["cols"])
    slices = __concat_slices(rslices, cslices, data)

    """ Sort them by size - Assumption is largest slice is data """
    return sorted(slices, key=lambda slices: slices["shape"]["size"],
                  reverse = True)


# In[]:
def __build_slice_index(slice_index):
    index = []

    """ Index a slice based on the types - Assist in Cleaning """
    for key, value in slice_index.items():
        if value['count'] > 0:
            index.extend([str(x) + ['E','H','D'][key] \
                          for i in value['ranges']\
                          for x in range(i[0],i[1])])

    """ Sort by column and row number """
    return sorted(index, key=lambda index: int(index[:-1]))


# In[]:
def __create_df_slices(data, **kwargs):

    """ Slice data according to method specified
        full - Rows + Columns
        rows - Treat all columns as data
        columns - Treat all rows as data
    """

    method = kwargs.get("method", "full")
    data_loss = kwargs.get("data_loss", 0)

    if method in ['full', 'rows','cols']:
        df_slices = []
        slices = __get_slices(data, data_loss, method = method)

        for s in slices:
            r = s['slice']
            s_data = [[data[i][j] for j in range(r[2],r[3])] \
                       for i in range(r[0],r[1])] # Extract slice from ranges

            df = pd.DataFrame(s_data)

            """ Index and columns should reflect data types identified """
            df.index = __build_slice_index(s['index']['rows'])
            df.columns = __build_slice_index(s['index']['cols'])

            df_slices.append(df)

        return df_slices
    else: return pd.DataFrame(data)

""" -----------------------------EXCEL HELPERS------------------------------"""
# In[]:
def __unmerge_xl(full_path, sheet_name):

    """ Unmerge cells in a workbook """
    xl = xlrd.open_workbook(full_path, on_demand = True)
    sheet = xl.sheet_by_name(sheet_name)

    """ Intialize data as a list of lists """
    data = [sheet.row_values(i) for i in range(0, sheet.nrows)]

    """ Copy files from merged cells """
    for rs, re, cs, ce in sheet.merged_cells:
        for row in range(rs, re):
            for col in range(cs, ce):
                data[row][col] = data [rs][cs]
    return data


# In[]:
def __wrapper_extract_sheet(arg):

    """ Unwrap arguments to enable concurreny
        (only one argument can be received)

        Return a dictionary with the name of the sheet
    """
    full_path, s, kwargs = arg
    return {s: extract_sheet(full_path, s, **kwargs)}

""" ---------------------- EXTRACTION PROCESS HELPERS-----------------------"""

# In[]:
def __map_slice(df, regex):

    """ Find whether the current slice contains a given string """
    mask = np.column_stack([df[col].astype(str).str.contains(regex, na=False) \
                            for col in df])

    if len(df.loc[mask.any(axis=1)]): return True # Return if occurrene is 1
    else: return False


# In[]:
def __process_data(data, **kwargs):

    #print('Full Process - ', kwargs)
    """ Run the entire data process including recurssion if required """

    result = __single_process(data, **kwargs) # First Data process
    if isinstance(result, str): return result

    """ If an additional process is found feed it - Return dictionary"""
    if kwargs.get("process") is not None:

        if isinstance(result, list): result = dict(enumerate(result))
        elif isinstance(result, pd.DataFrame): result = {'0': result}

        process = kwargs.get("process")
        for key, p_dict in process.items():
            if result.get(key) is not None:
                if isinstance(result[key], pd.DataFrame): df = result[key]
                elif isinstance(result[key], list) and len(result[key]) == 0:
                    p_dict = None
                else: df = result[key][0]

                """ If tag is found with a None entry, just return df """
                if p_dict is None: result[key]  = df
                else: result[key] = extract_df(df, **p_dict) # Recursion

    return result


# In[]:
def __single_process(data, **kwargs):

    #print('Single Process - ', kwargs)
    """ Run a single data process """
    data = __trim_strings(data)
    pre_clean_dict = kwargs.get("pre_clean", {})
    data = __pre_clean(data, **pre_clean_dict)

    """ Extract the data """
    extraction_dict = kwargs.get("extraction", {})
    dfs = __data_extraction(data, **extraction_dict)

    post_clean_dict = kwargs.get("post_clean", {})

    """ Clean all the data frames - Iterate through list/dict if needed"""
    if isinstance(dfs, pd.DataFrame):
        return __post_clean(dfs, **post_clean_dict)
    elif isinstance(dfs, str): return dfs
    elif isinstance(dfs, list):
        return [__post_clean(df, **post_clean_dict) for df in dfs]
    elif isinstance(dfs, dict):
        result = {}
        for key, df in dfs.items():
            if isinstance(df, str): result['key'] = df
            elif isinstance(df, list):
                result[key] = [__post_clean(d,**post_clean_dict) for d in df]
            else: result [key] =  __post_clean(df, **post_clean_dict)
        return result
    else: return None


# In[]:
def __data_extraction(data, s_output = [0], **kwargs):

    # print('Extraction - ', kwargs)

    """ Extract data from a list of lists using a slicing method """
    if s_output not in ['all', 'search'] and not(isinstance(s_output, list)):
        return pd.DataFrame(data)

    df_slices = __create_df_slices(data, **kwargs)

    if s_output == 'all':
        result = df_slices # Return everything - No Names
    elif s_output == 'search':
        result = map_slices(df_slices, **kwargs) # Return a named dictionary
    elif isinstance(s_output, list):
        result = [df_slices[i] for i in s_output if isinstance(i, int)]
    else: result = pd.DataFrame(data)

    """ Ensure return type is can be df, dict or list """
    return result


# In[]
def __pop_level(lv_obj, lv_value, depth, lv_names = {}):

    """ Add dictionary keys as columns in dataframes
        Recursively explore keys in a dictionary

        lv_obj refers to the object at the current depth
        lv_names is a dictionary of names given (lv_value, depth) combinations

        If a string or None is found, return error String

        For single Dataframes - add columns
        For lists - iterate numerically
        For dictionary - pop lv_obj by lv_obj
    """

    """ Get the name for the current column """
    if isinstance(lv_names, dict) and len(lv_names) > 0:
        lv_name = lv_names.get((lv_value, depth), str(depth) + 'L')
    else: lv_name = str(depth) + 'L'

    # print(lv_value, depth, type(lv_obj), lv_name)

    if lv_obj is None: return str(lv_name) + ' - Not Found'
    elif isinstance(lv_obj, str): return  lv_name + " - " + lv_obj

    elif isinstance(lv_obj, pd.DataFrame): # Single Dataframe

        result = lv_obj
        """ Add a table ID to identify source """
        if 'ID' in result.columns:
            result['ID'] = str(lv_value) + '-' + result['ID']
        else: result['ID'] = str(lv_value)

        result = __add_columns_to_df(lv_obj, {lv_name: lv_value})

        return result

    elif isinstance(lv_obj, list):

        """ Add this level to all the members of the list
            List is a passthrough for all objects at the current level
        """
        result = []
        for obj in lv_obj:
            temp = __pop_level(obj, lv_value, depth, lv_names = lv_names)

            """ Extend a list, Pop a dictionary, or append Dataframe """
            if isinstance(temp, list): result.extend(temp)
            else: result.append(temp)

        return result

    elif isinstance(lv_obj, dict):

        """ Pop the current level of a dictionary
            Dive a level deeper
        """
        result = []
        for key, obj in lv_obj.items():
            temp = __pop_level(obj, key, depth + 1, lv_names)
            if isinstance(temp, list):
                result.extend(__pop_level(temp, lv_value, depth, lv_names))
            else: result.append(temp)
        return result

"""-------------------------------- CLEANING -------------------------------"""
# In[]:
def __pre_clean(data, **kwargs):

    # print('Pre Clean - ', kwargs)
    """ Transpose data prior to slicing """
    if kwargs.get("transpose_data", False):
        data = __transpose_data(data)

    """ Ignore all rows that are completely empty """
    if kwargs.get("ignore_empty_rows", False):
        data = __delete_empty_rows(data)

    """ Ignore all rows that are completely empty """
    if kwargs.get("ignore_empty_cols", False):
        data = __delete_empty_cols(data)

    """ Ignore any row with at least one empty column """
    if kwargs.get("ignore_empty_cells", False):
        data = __delete_empty_cells(data)

    """ Ignore any row with empty columns as per threshold """
    if kwargs.get("delete_by_threshold") is not None:
        data = __delete_by_threshold(data, kwargs.get("delete_by_threshold"))

    return data


# In[]:
def __post_clean(df, **kwargs):

    #print('Post Clean - ', kwargs)
    if not isinstance(df, pd.DataFrame):
        return df

    """ Treat all entries in axis as data"""
    if kwargs.get("treat_axis_as_data") is not None:
        axis = kwargs.get("treat_axis_as_data")
        df = __treat_axis_as_data(df, axis)

    """ Add the current Index as a Row - Sensitive to positioning """
    if kwargs.get("index_as_col", False):
        df = __add_index_as_col(df)

    """ Identify an arbitrary header row """
    if kwargs.get("header_row") is not None:
        header_row = kwargs.get("header_row", False)
        if header_row >= 0 and header_row <= df.shape[0] -1:
            df = __rename_df(df, {df.iloc[header_row].name:'fH'}, axis = 0)

    """ Identify an arbitrary header column """
    if kwargs.get("header_column") is not None:
        header_column = kwargs.get("header_column", False)
        if header_column >= 0 and header_column <= df.shape[1] -1:
            df = __rename_df(df, {list(df.columns)[header_column]:'fH'},
                                  axis = 1)

    """ Fill records and columns qualified as Headings """
    if kwargs.get("fill_headings", False):
        df = __fill_headings(df)

    """ Compress Headings to values from rows """
    if kwargs.get("compress_header", False):
        df = __compress_header(df)

        """ Add the current Index as a Row - Sensitive to positioning """
    if kwargs.get("columns_as_row", False):
        df = __add_columns_as_row(df)

    """ Compress Headings to values from rows """
    if kwargs.get("add_header") is not None:
        df = __add_header_to_df(df, kwargs.get("add_header"))

    """ Ensure there are no repetitions in a pandas series """
    if kwargs.get("ensure_no_rep") is not None:
        rows_to_check = kwargs.get("ensure_no_rep")
        if isinstance(rows_to_check, list):
            for r in rows_to_check:
                if r in df.index: df.loc[r] = __ensure_no_rep(df.loc[r])
        elif isinstance(rows_to_check, str) and rows_to_check in df.index:
            df.loc[rows_to_check] = __ensure_no_rep(df.loc[rows_to_check])

    """ If partial records should be deleted """;
    if kwargs.get("drop_partial_records", False):
        df = __drop_empty_records(df, 'any')

    """ If full empty records should be deleted """
    if kwargs.get("drop_empty_records", False):
        df = __drop_empty_records(df, 'all')

    """ If full empty columns should be deleted """
    if kwargs.get("drop_empty_columns", False):
        df = __drop_empty_columns(df)

    """ Transpose the df """
    if kwargs.get("transpose_output", False):
        df = __transpose_df(df)

    """ Add columns to the dataset """
    if kwargs.get("add_columns") is not None:
        cols_dict = kwargs.get("add_columns")
        if isinstance(cols_dict, dict):
            df = __add_columns_to_df(df, cols_dict)

    """ Rename with Headers """
    if kwargs.get("rename_columns") is not None:
        new_names = kwargs.get("rename_columns")
        if isinstance(new_names, dict):
            df = __rename_df(df, new_names, axis = 1)

    """ Rename Indices """
    if kwargs.get("rename_index") is not None:
        new_names = kwargs.get("rename_index")
        if isinstance(new_names, dict):
            df = __rename_df(df, new_names, axis = 0)

    if kwargs.get("delete_columns") is not None:
        col_list = kwargs.get("delete_columns")
        if isinstance(col_list, list):
            df = __del_from_df(df, col_list, axis = 1)

    return df

"""--------------------------- List of Lists Helpers -----------------------"""
# In[]:

def __trim_strings(data):

    """ Trim all strings within each row """
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if isinstance(data[r][c], str): data[r][c] = data[r][c].strip()

    return data

# In[]:
def __transpose_data(data):

    """ Transpose a list of lists """
    return list(zip(*data))


# In[]:
def __filter_row(row, f_string, partial = False):

    """ Filter rows that contain f_string, either all or partial(any) flags """
    n = sum([1 if x != f_string else 0 for x in row])
    if partial: return n
    return n == 0


# In []:
def __delete_empty_rows(data):

    """ Filter rows that are empty """
    return [r for r in data if not(__filter_row(r, ''))]


# In[]:
def __delete_empty_cols(data):

    """ Filter columns that are empty (transpose and process as columns) """
    temp = __delete_empty_rows(__transpose_data(data))
    return __transpose_data(temp)


# In []:
def __delete_empty_cells(data):

    """ Filter rows that are empty """
    return [r for r in data if __filter_row(r, '', partial = True) == len(r)]


# In []:
def __delete_by_threshold(data, threshold):

    """ Filter rows that are empty to a certain threshold """
    return [r for r in data if __filter_row(r, '', partial = True) >= \
            (1-threshold) * len(r)]

"""--------------------------- Data Frame Helpers --------------------------"""

def __treat_axis_as_data(df, axis):

    """ Determe axis to use for headings """
    headings = df.columns if axis == 1 or axis == 'columns' else df.index

    """ If not currently labelled as DATA, add D subscript """
    new_names = {h: str(h) + 'D' for h in headings if h[-1] != 'D'}
    df = __rename_df(df, new_names = new_names, axis = axis)

    return df


# In[]:
def __drop_empty_records(df, how = 'all'):

    """ Replace spaces and empty characters with np.nan """
    result = df.replace(r"^(?![\s\S])|^(\s)|^(0\b)", np.nan,
                   regex = True).dropna(how = how)
    result = result.replace(np.nan, '')
    return result


def __drop_empty_columns(df):

    """ Get a list of unique values and delete if all empty """
    cols = [col for col in df.columns if list(set(df[col])) == ['']]

    df = df.drop(columns= cols)
    return df


# In[]:
def __add_header_to_df(df, add_header):

    """ Extract the current record types """
    h_index = [x for x in df.index if str(x)[-1] != 'D']
    d_index = [x for x in df.index if str(x)[-1] == 'D']

    """ Add a header on top of rows """
    add_header.index = [str(i) + 'aH' for i in range(add_header.shape[0])]

    if len(h_index) > 0:
        header = pd.concat([df.loc[h_index], add_header], sort = False)
    else: header = add_header

    return pd.concat([header, df.loc[d_index]], sort = False)


# In[]:
def __add_columns_to_df(df, cols_dict):

    """ Add columns from a dictionary in the format
        cols_dict = {col_name : default_value} """
    result = copy.deepcopy(df)

    for name, value in cols_dict.items():
        result[name] = value

    return result


def __del_from_df(df, name_list, axis = 1):

    """ Drop columns from a list """
    result = copy.deepcopy(df)

    for name in name_list:
        if name in result.columns:
            result.drop(name, axis  = 1, inplace = True)

    return result

# In[]:
def __add_index_as_col(df):

    """ Extract the Index from df """
    temp = pd.DataFrame(df.index)
    temp.index = df.index
    temp.columns = ['iH']

    return pd.concat([temp, df], axis = 1)


# In[]:
def __add_columns_as_row(df):

    """ Extract Columns from df """
    temp = pd.DataFrame(df.columns).T
    temp.columns = df.columns
    temp.index = ['iH']

    return pd.concat([temp, df], axis = 0)


# In[]:
def __fill_headings(df):

    """ Fill Columns & Rows identified as Headings """
    result = df
    for x in df.columns:
        if str(x)[-1] == 'H': result[x] = result[x].replace('', None)
    for x in df.index:
        if str(x)[-1] == 'H': result.loc[x] = result.loc[x].replace('', None)

    return result


# In[]:
def __rename_df(df, new_names = {}, axis = 1):


    """ Rename a DataFrame axis ensuring no repeated entries are found """
    names = {}

    """ Determe axis to use for headings """
    headings = df.columns if axis == 1 or axis == 'columns' else df.index

    for col in list(headings):
        """ If new_names is not specified, just ensure there is no
            repetition """
        key = new_names[col] if col in new_names.keys() else col
        if key == '': key = 'U' # Replace empty values with 'U' for Unknown

        key = str(key)
        """ Find the number of ocurrences and establish the new key """
        count = int(sum([1 if key == n else 0 \
                                 for n in names.values()]) or 0)

        new_key = key if count == 0 and len(key) > 1 else str(count + 1) + key

        """ Populate the dictionary of entries to be renamed"""
        names[col] = new_key

    result = df.rename(names, axis = axis)

    return result


# In[]:
def __compress_header(df):

    """ Identify Heading and Data Rows """
    h_index = [x for x in list(df.index) if str(x)[-1] == 'H']
    d_index = [x for x in list(df.index) if str(x)[-1] == 'D']

    """ If there is at least one heading - joing values of H rows """
    if len(h_index) > 0:
        header = df.loc[h_index]

        names = {}
        for k in df.columns:
            unique_vals = list(set(header[k]))
            if all(isinstance(h, str) for h in unique_vals):
                names[k] = '_'.join(unique_vals)

        result = __rename_df(df.loc[d_index], names, axis = "columns")
    else: result = df

    return result


# In[]:
def __transpose_df(df):

    """ Identify Heading and Data Rows """
    h_index = [x for x in list(df.index) if str(x)[-1] != 'D']
    d_index = [x for x in list(df.index) if str(x)[-1] == 'D']

    """ Identify Pivot Columns """
    v_index = [x for x in list(df.columns) if str(x)[-1] != 'D']

    """ Tranpose the data & the header """
    result = pd.melt(df.loc[d_index], id_vars = v_index)
    header = df.loc[h_index].T

    header = __del_escape_chars_df(header)

    """ Merge the header as columns, if repeated add '_y' to header columns """
    result = pd.merge(result, header, how = 'left', left_on ='variable',
                    right_index= True , suffixes = ('','_y'))

    """ Delete variable created by melt """
    result = result.drop(['variable'], axis = "columns")

    """ Attempt to find the proper headings - if exisiting
        (i.e. Pivot Columns) """
    if header.shape[0] > 0:

        names = {}
        for k in v_index:
            if k in header.index:
                unique_vals = list(set(header.loc[k]))
                if all(isinstance(h, str) for h in unique_vals):
                    names[k] = '_'.join(unique_vals)

    if not(names is None):
        result = __rename_df(result, names, axis = "columns")

    return result

# In[]:
def __del_escape_chars_df(df):

    """ Replace escape characters with a space (' ') """
    escapes = ['\t', '\n', '\a', '\b', '\f', '\r', '\v']
    for e in escapes: df = df.replace(e, ' ', regex = True)

    return df


# In[]:
def __ensure_no_rep(series):

    """ Ensure there is no repetition in pandas Series """
    new_vals = []
    for index, value in series.iteritems():
        value = str(value)
        """ Find the number of ocurrences and establish the new value """
        count = int(sum([1 if value == v else 0 for v in new_vals]) or 0)
        new_val = value if count == 0 else value + str(count + 1)

        """ Add the new identified value """
        new_vals.append(new_val)
        series[index] = new_val

    return series


# In[]:
""" ---------------------------EXTERNAL FUNCTIONS---------------------------"""

""" ---------------------------------CLEANING-------------------------------"""
def clean_df(df,**kwargs):
    """ External caller for df cleaning
        Receives only Post_Clean arguments
    """
    return __post_clean(df, **kwargs)


""" -------------------------------EXTRACTION-------------------------------"""


# In[]:
def extract_xl(path, file_name, sheets, **kwargs):

    # print('Xl - ', kwargs)

    """ Process an excel from list of sheets provided.
        Concurrency is enabled to extract multiple sheets.
    """
    full_path = os.path.join(path, file_name)
    process = kwargs.get("process", False)

    """ Attempt to find a dedicated process for all sheets """
    if process: p_dict = {s: process.get(s, process.get('default',{})) \
                          for s in sheets}
    else: p_dict = {s: {} for s in sheets}

    """ Allow for concurrent processing of sheets """
    n_process = kwargs.get("parallel_xl", 1)
    if not (isinstance(n_process, int)): n_process = 1

    if n_process > 1 and len(sheets) > 1:

        """ Start a pool of n parallel_process """
        pool = Pool(n_process)
        arg = [(full_path, s, p_dict.get(s)) for s in sheets]

        """ Iterate through all the sheets """
        result = pool.map(__wrapper_extract_sheet, arg)

        """ Garbage Collection and closing unecessary python instances """
        pool.terminate()
        gc.collect()

    else: # Run instance by instance
        result = {s: extract_sheet(full_path, s, **p_dict.get(s)) \
                  for s in sheets}

    if kwargs.get("as_named_list", False):

        """ Create default column names """
        lv_names = kwargs.get("lv_names", {})
        lv_names[(file_name, 0)] = "File_Name"
        for s in sheets: lv_names[(s, 1)] = "Sheet_Name"

        kwargs["lv_names"] = (lv_names) # Repack dictionary

        result = pop_keys_df_dict(result, file_name, **kwargs)

    return result

# In[]:
def extract_sheet(full_path, sheet_name,  **kwargs):

    """ Extract an Excel Sheet using available parameters
        - xlrd is used for unmerging
        - pyexcel is used otherwise
    """
    try:
        unmerge = kwargs.get("unmerge", True)
        data = __unmerge_xl(full_path, sheet_name) if unmerge \
        else pe.get_sheet(file_name = full_path, sheet_name = sheet_name)
    except:
        return sheet_name + ' - Not Found'

    return __process_data(data, **kwargs)


# In[]:
def map_slices(df_slices, search_dict, concat_search_axis = None, **kwargs):

    """ Map a set of slices according to the search dictionary.
        Search if performed in order.
        If multiple entries are found for the same key, option to concatenate.
    """

    smap = {}
    assigned = [False] * len(df_slices) # All slices are unassigned

    for key, elem in search_dict.items():
        smap[key] = []

        """ Loop through unssigned slices and find string """
        for i in range(0, len(df_slices)):
            if (not assigned[i] and __map_slice(df_slices[i], elem)):
                smap[key].append(df_slices[i])
                assigned[i] = True

        """ Concat dataframes is required """
        if concat_search_axis is not None and len(smap[key]) > 1:
            smap[key] = [pd.concat(smap[key], axis = concat_search_axis)]
    return smap


# In[]:
def extract_df (df, **kwargs):

    # print(" Extract df -" , kwargs)
    if kwargs.get("ignore_process", False): return df

    """ Extract a DataFrame using available parameters """
    return __process_data(df.values.tolist(), **kwargs)


# In[]:
def extract_csv (path, file_name, **kwargs):
    data_list = pe.get_array(file_name = os.path.join(path, file_name),
                             encoding = 'utf8')
    return __process_data(data_list, **kwargs)


# In[]
def pop_keys_df_dict(df_dict, dict_name, **kwargs):

    # print('Pop Keys - ', kwargs)
    """ Trigger recurve process to convert dict kets to cdf columns """
    lv_names = kwargs.get("lv_names", {})
    result = __pop_level(df_dict, dict_name, 0, lv_names)

    """ Transform list into dictionary
        - get name from a specific column
        - get name from explicit dictionary matching joined levels
        - get name from ordered list
    """

    if kwargs.get("name_from_list") is not None:
        name_list = kwargs.get("name_from_list")

        if len(name_list) == len(result):
            return {name: r for r in result for name in name_list}

    elif kwargs.get("name_from_dictionary") is not None:

        name_dict = kwargs.get("name_from_dictionary")
        new_dict ={'errors':[], } # Restart the dictionary

        for item in result:
            if isinstance(item, pd.DataFrame) and 'ID' in item.columns\
            and len(item['ID'])> 0:

                """ Find name in dictionary or label as unkown, ensure names
                    are unique """
                name = name_dict.get(item['ID'][0], "Unknown")

                count = int(sum([1 if name == n else 0 \
                                 for n in new_dict.keys()]) or 0)
                name = name if count == 0 else name + '_' + str(count + 1)
                new_dict[name] = item

            else: new_dict['errors'].append(item)

        return new_dict

    else: return result
