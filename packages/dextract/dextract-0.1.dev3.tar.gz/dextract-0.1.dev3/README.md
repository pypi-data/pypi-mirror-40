# dExtract - A Layered Extractor of Data

## Package Overview

dExtract is based on an Object-Oriented Framework to perform transformations
on data on a sequential basis.


The minimal structure requires:
1. An object of the Sequential Class
2. Objects inheriting from the Base Layer Class


Data flows between layers by sending the transform output to the subsequent
layer. The model can be run completely or from a specific index.

### Sequential Class
The sequential class describes a pipeline of transformations.
- Layers are saved in a dictionary keyed by Layer Types and count by type.
- The method summary returns the components of the model for visualization.


### Types of Layers
There are 4 main types of layers inheriting from the BaseLayer.

#### 1.Slicer (DataLayer)
The slicer layer requires a data input that will be split into a series of
'slices' based on data sparsity/density. Row and column slices are calculated
and then concatenated to fined 'boxed areas'.

The output can be defined as a list or as search dictionary to find specific
values in the resulting slices for quick identification.

The type of each row and column are defined by simple statistical thresholds.
These can be customized according to user parameters.

There are 3 main data types: DATA (2), HEADING (1), EMPTY (0)

The data is then divided according to the DECISIONS matrix on `slicing.py`.

Decisions Matrix to create slices (prev_type, cur_type) as key
1. start_head (SH) - Begin counting records for a new HEADING section
2. end_head (EH) - Finish counting records for current HEADING section
3. start_data (SD) - Begin counting records for a new DATA section
4. end_data (ED) - Finish counting records for current DATA section
5. start_slice (SS) - Begin counting records for a new SLICE
6. end_slice (ES) - Finish counting records for current SLICE

```
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
```

#### 2.Cleaner (DataLayer)
The Cleaner layer will apply predefined transformations based on kwargs.
Each transformation is applied on an individual basis.

The `clean.py` helper includes all transformations and it is easily extendible.
Open the helper for a complete definition of each transformation

#### 3.Extractor (BaseLayer)
The Extractor layer provides an interface to retrieve external data.

On **v0.9dev1**: csv, xl (Excel) and single Excel sheet are supported

Future development includes:
- SAS files through the SAS7BDAT Package
- Asynchronous feed-forward extraction (allow the model to run in chunks)
- Web Scrapping (Both files and websites)

#### 4.Flattener (BaseLayer)
The Flattener layer transforms a nested dictionary of data into a single level
dictionary.

It transforms all inputs into dataframes and identifies the result names by
adding dictionary keys as 'levels' and concatenates them into a DataFrame ID.

Based on the input names dictionary or list, each dataframe is then assigned
a new name matching the resulting ID.
