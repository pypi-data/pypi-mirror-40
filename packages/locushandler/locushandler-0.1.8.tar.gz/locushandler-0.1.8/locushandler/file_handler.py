"""
Module for processing files with Locus codes
"""
import os
import re
import pandas as pd
import numpy as np
from locushandler.params import BARCODE_FIELDS
import locushandler.file_helper as fh
import locushandler.string_parser as sp
from locushandler.validation import LocusValidationError


def find_errors(df, column_of_interest):
    """
    Take in a dataframe that has a column containing loci.
    Iterate through the column to find the specific errors
    associated with each line if they exist.

    :param df: (DataFrame)
    :param column_of_interest: (string) column to check for errors

    :return: (dict) line numbers in the dataframe that have errors,
            with respective error messages
    """
    errors = {}
    args = {'output_type': 'dict',
            'granularity': 'full',
            'dr': True, 'io': True}
    for idx, row in df.iterrows():
        try:
            sp.string_parser(row[column_of_interest], **args)
        except LocusValidationError as error:
            errors[idx] = str(error)
            continue
    return errors


def parse_file(file_path_or_df, column_of_interest, output_type, granularity, dr, io,
               merge=True, encoding='latin-1', header=0):
    """
    Take in a file that has or multiple columns with barcode field in them.
    Parse the column specified and break them down into multiple columns,
    each of them containing a very granular element of a field.
    The output path is standardized.

    :param file_path: (string) full path of the file with barcode field to
     parse
    :param column_of_interest: (string) column to parse from the locus
                                        Barcode, from BARCODE_FIELDS

    :param granularity: (string) in GRANULARITY
    :return: parsed_file: (string or dataframe) path of the parsed file
                        or dataframe with the file with added columns
    """
    try:
        if isinstance(file_path_or_df, pd.DataFrame):
            df_data = file_path_or_df
        else:
            df_data = pd.read_csv(file_path_or_df, encoding=encoding, header=header)

        df_data.dropna(subset=[column_of_interest], axis=0, inplace=True)

        # Parse column_of_interest into list
        args_parser = ('list', granularity, column_of_interest.lower(), dr, io,)
        df_data[column_of_interest] = df_data[column_of_interest].astype(str).apply(
            sp.string_parser,
            args=args_parser)

        # Expand list into dataframe columns
        type_column = BARCODE_FIELDS[column_of_interest.lower()]
        list_elements = fh.gran_to_fields(granularity, type_column, dr, io)
        df_data[list_elements] = pd.DataFrame(df_data[column_of_interest].values.tolist(),
                                              index=df_data.index)
        df_data.drop(column_of_interest, 1, inplace=True)
        if merge:
            df_data = merge_locus(df_data, merge_all=True)

    except KeyError:
        print('Make sure column_of_interest appears in your file and is a valid barcode field.')
        raise
    except FileNotFoundError:
        print('The file you want to open doesn\'t exist.')
        raise
    except LocusValidationError:
        errors = find_errors(df_data, column_of_interest)
        print('The following errors were found in the file you want to parse:')
        for error in errors:
            print('line {}: {}'.format(error, errors[error]))

    if output_type == 'path':
        if os.path.isfile(file_path_or_df):
            # Create standardized output path
            # 'data/intermediary/inpath_parsed_granularity_column.csv'
            if '/' in file_path_or_df:
                # If file is in another folder .../.../.../file.csv
                reg = re.compile(r'(?P<file>(\w|\W)*(\w*/)*\w*).csv')
            else:
                # If file is in current folder file.csv
                reg = re.compile(r'(?P<file>(\w|\W)*).csv')
            search = reg.search(file_path_or_df)
            file_name = search.group('file')
        else:
            file_name = 'dataframe'
        # Add suffix at end of file
        output = '_'.join([file_name, 'parsed',
                           granularity, column_of_interest]) + '.csv'
        df_data.to_csv(output, index=False)
        return output
    return df_data


def map_to_locus(file_path_or_df, code_column, classification_system, crosswalk_path,
                 column_of_interest,
                 granularity, dr, io, merge=True,
                 encoding_data='latin-1', encoding_cw='latin-1', header=0):
    """
    Takes in a file that uses a classification system, and uses the parsed
    crosswalk
    to translate codes into Locus function with the specified granularity.
    Either adds multiple columns to the table (one for each element of the
    barcode fields)or just add one column with the desired granularity.
    The output path is standardized.

    :param file_path: (string) full path of the input file
    :param code_column: (string) name of the column of the classification system in the file to map
    :param classification_system: (string) name of the column of the classification
            system in the crosswalk file
    :param crosswalk_path: (string) full path of the crosswalk csv
    :param output_type: (string) from TABLE_OUTPUT_TYPE
    :param granularity: (string) from GRANULARITY
    :param column_of_interest: (string) column to retrieve from the locus
                                        Barcode, from BARCODE_FIELDS
    :return:(string or dataframe) path of the mapped file
                        or dataframe with Locus fields

    """

    try:
        if isinstance(file_path_or_df, pd.DataFrame):
            df_data = file_path_or_df
        else:
            df_data = pd.read_csv(file_path_or_df, encoding=encoding_data, header=header)
        df_map = get_mapping(crosswalk_path=crosswalk_path,
                             classification_system=classification_system,
                             column_of_interest=column_of_interest,
                             granularity=granularity, dr=dr, io=io,
                             encoding=encoding_cw)
        df_data[code_column] = df_data[code_column].astype(str)
        df_map[classification_system] = df_map[classification_system].astype(str)
        df_data = df_data.merge(df_map, left_on=code_column,
                                right_on=classification_system).drop(classification_system, 1)
        if merge:
            df_data = merge_locus(df_data, merge_all=True)
        return df_data
    except KeyError:
        print('Make sure you input the right name of column for the classification system '
              'in the file you want to map to Locus.')
        raise


def get_mapping(crosswalk_path, classification_system, column_of_interest,
                granularity, dr, io,
                encoding='latin-1'):
    """
       Takes in a classification system, and builds the locus mapping at the right granularity

       :param classification_system: (string) name of the column in the crosswalk file
       :param crosswalk_path: (string) full path of the crosswalk csv
       :param granularity: (string) from GRANULARITY
       :param column_of_interest: (string) column to retrieve from the locus
                                        Barcode, from BARCODE_FIELDS
       :param dr, io (bool) : include or not dr and io in the final df
       :return:(dataframe) dataframe with two columns, classification code and
                            associated Locus code
    """
    try:
        df_map = parse_file(file_path_or_df=crosswalk_path,
                            column_of_interest=column_of_interest,
                            output_type='df',
                            granularity=granularity, dr=dr, io=io,
                            encoding=encoding)
        type_column = BARCODE_FIELDS[column_of_interest.lower()]
        cols = fh.gran_to_fields(granularity, type_column, dr=dr, io=io)
        df_map = df_map[[classification_system] + cols]
        return df_map
    except KeyError:
        print('Make sure you input the right name of column for the classification system.')
        raise


def merge_locus(df, merge_all=False, merge_act=False, merge_res=False,
                merge_dr=False, merge_io=False, merge_sub=False):
    """
    Merge columns with elements of a loci into single columns

    :param df: input dataframe
    :param merge_all: (bool) True if want only one column 'Locus' with full loci
    :param merge_act: (bool) True if want to merge all act
    :param merge_res: (bool) True if want to merge all res
    :param merge_dr: (bool) True if want to merge all dr
    :param merge_io: (bool) True if want to merge all io
    :param merge_sub: (bool) True if want to merge all sub
    :return: dataframe with merged columns
    """
    columns = df.columns
    dr = [x for x in columns if x.startswith('dr') and x[2:].isdigit()]
    act = [x for x in columns if x.startswith('a') and x[1:].isdigit()]
    res = [x for x in columns if x.startswith('r') and x[1:].isdigit()]
    io = [x for x in columns if x.startswith('io') and x[2:].isdigit()]
    sub = [x for x in columns if x.startswith('sub') and x[3:].isdigit()]
    all_col = []
    df = df.replace(np.nan, '').replace('V', 'Div')
    trans_int = lambda x: int(x) if x != '' and x != 'Div' else x
    join_nopoint = lambda x: ''.join(x)
    join_point = lambda x: '.'.join(x)

    if merge_all:
        merge_act = True
        merge_res = True
        merge_dr = True
        merge_io = True
        merge_sub = True
    if merge_dr and dr:
        # Handles dr2 float
        if 'dr2' in dr:
            df['dr2'] = df['dr2'].apply(trans_int)
        df['dr'] = df[dr].astype(str).apply(join_nopoint, axis=1)
        df.drop(dr, 1, inplace=True)
        all_col.append('dr')
    if merge_sub and sub:
        df['sub'] = df[sub].astype(str).apply(join_nopoint, axis=1)
        df.drop(sub, 1, inplace=True)
        all_col.append('sub')
    if merge_act and act:
        df['act'] = df[act].astype(str).apply(join_point, axis=1)
        df.drop(act, 1, inplace=True)
        all_col.append('act')
    if merge_res and res:
        df['res'] = df[res].astype(str).apply(join_nopoint, axis=1)
        df.drop(res, 1, inplace=True)
        all_col.append('res')
    if merge_io and io:
        if 'io2' in io:
            df['io2'] = df['io2'].apply(trans_int)
        df['io'] = df[io].astype(str).apply(join_nopoint, axis=1)
        df.drop(io, 1, inplace=True)
        all_col.append('io')

    if merge_all:
        df['Locus'] = df[all_col].astype(str).apply(lambda x: ' '.join(x), axis=1).apply(
            lambda x: x.strip())
        df.drop(all_col, 1, inplace=True)

    df = df.replace('FDivDiv', 'F', regex=True) \
        .replace('FDiv', 'F', regex=True)

    return df
