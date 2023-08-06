# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:46:21 2018

@author: a002028
"""
import os
import numpy as np
from fnmatch import fnmatch
from datetime import datetime
import shutil
from trollsift.parser import globify, parse
import inspect


def check_path(path):
    """
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def copyfile(src, dst):
    """
    :param src: Source path
    :param dst: Destination path
    :return: File copied
    """
    shutil.copy2(src, dst)


def copytree(src, dst, symlinks=False, ignore=None):
    """
    Source: https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
    :param src:
    :param dst:
    :param symlinks:
    :param ignore:
    :return:
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def create_directory_structure(dictionary, base_path):
    """
    Creates directory based on nested dictionary
    :param dictionary: nested dictionary
    :param base_path: Base folder
    :return: Folders from keys in dictionary
    """
    if len(dictionary) and not isinstance(dictionary, str):
        for direc in dictionary:
            if isinstance(direc, str):
                if '.' not in direc:
                    create_directory_structure(dictionary[direc], os.path.join(base_path, direc))
            elif isinstance(direc, dict):
                create_directory_structure(dictionary[direc], os.path.join(base_path, direc))
    else:
        os.makedirs(base_path)


def decdeg_to_decmin(pos, string_type=True, decimals=2):
    """
    :param pos: Position in format DD.dddd (Decimal degrees)
    :param string_type: As str?
    :param decimals: Number of decimals
    :return: Position in format DDMM.mm(Degrees + decimal minutes)
    """
    pos = float(pos)
    deg = np.floor(pos)
    minute = pos % deg * 60.0
    if string_type:
        if decimals:
            # FIXME Does not work properly
            output = ('%%2.%sf'.zfill(8) % decimals % (float(deg) * 100.0 + minute))
        else:
            output = (str(deg * 100.0 + minute))
    else:
        output = (deg * 100.0 + minute)
    return output


def decmin_to_decdeg(pos, string_type=True, decimals=4):
    """
    :param pos: str, Position in format DDMM.mm (Degrees + decimal minutes)
    :param string_type: As str?
    :param decimals: Number of decimals
    :return: Position in format DD.dddd (Decimal degrees)
    """
    # pos = pos.replace(' ','')
    # if len(pos.split('.')[0]) > 2:
    #     return pos
    pos = float(pos)
    output = np.floor(pos/100.) + (pos % 100)/60.
    output = "%.5f" % output
    if string_type:
        return output
    else:
        return float(output)


def generate_strings_based_on_suffix(dictionary, suffix):
    """
    :param dictionary: Nested dictionary
    :param suffix: str, e.g. '.txt'
    :return: generator to produce a stringlist
    """
    for item in dictionary.values():
        if isinstance(item, dict):
            yield from generate_strings_based_on_suffix(item, suffix)
        elif not is_sequence(item):
            continue
        else:
            for value in item:
                if value.endswith(suffix):
                    yield value


def get_datetime(date_string, time_string):
    """
    :param date_string: YYYY-MM-DD
    :param time_string: HH:MM:SS  /  HH:MM
    :return:
    """
    if len(time_string) == 8:
        return datetime.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M:%S')
    elif len(time_string) == 5:
        return datetime.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M')
    else:
        return None


def get_datetime_now(fmt='%Y-%m-%d %H:%M:%S'):
    """
    :param fmt:
    :return:
    """
    return datetime.now().strftime(fmt)


def get_file_list_based_on_suffix(file_list, suffix):
    """
    Get filenames endinge with "suffix"
    :param file_list:
    :param suffix:
    :return:
    """
    match_list = []

    for fid in file_list:
        if fid.endswith(suffix):
            match_list.append(fid)

    return match_list


def get_file_list_match(file_list, match_string): 
    """
    Get filenames containing "match_string"
    :param file_list:
    :param match_string:
    :return:
    """
    match_list = []
    
    for fid in file_list:
        if fnmatch(fid, match_string):
            match_list.append(fid)
            
    return match_list


def get_filebase(path, pattern):
    """
    Get the end of *path* of same length as *pattern*
    :param path: str
    :param pattern: str
    :return:
    """
    # A pattern can include directories
    tail_len = len(pattern.split(os.path.sep))
    return os.path.join(*path.split(os.path.sep)[-tail_len:])


def get_filename(file_path):
    """
    :param file_path:
    :return:
    """
    return os.path.basename(file_path)


def get_format_from_datetime_obj(x, fmt):
    """
    :param x: datetime object
    :param fmt: format of output
    :return: str (can be any kind of date/time related string format)
    """
    return x.strftime(fmt)


def get_index_where_df_equals_x(df, x):
    """
    :param df: pd.DataFrame
    :param x: any kind of value
    :return: Boolean
    """
    return np.where(df == x)


def get_kwargs(func, info):
    """
    Creates a key word dictionary to use as input to "func"
    :param func: Function
    :param info: Dictionary with info to include in kwargs
    :return: kwargs
    """
    funcargs = inspect.getfullargspec(func)
    kwargs = {key: info.get(key) for key in funcargs.args}
    return kwargs


def get_method_dictionary(obj):
    """
    :param obj: Object
    :return: Dictionary of all methods from object including those from parent classes
    """
    return {func: True for func in dir(obj) if not func.startswith("__")}


def get_object_path(obj):
    """
    :param obj:
    :return:
    """
    return obj.__module__ + "." + obj.__name__


def match_filenames(filenames, pattern):
    """
    Get the filenames matching *pattern*
    :param filenames: list
    :param pattern: str
    :return:
    """
    matching = []
    for filename in filenames:
        if type(pattern) == list:
            for p in pattern:
                if fnmatch(get_filebase(filename, p), globify(p)):
                    matching.append(filename)
        else:
            if fnmatch(get_filebase(filename, pattern), globify(pattern)):
                matching.append(filename)
    return matching


def is_sequence(arg):
    """
    Checks if an object is iterable (you can loop over it) and not a string
    ** Taken from SHARKToolbox
    :param arg:
    :return:
    """
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__iter__"))


def set_export_path(export_dir=None):
    """
    :param export_dir:
    :return:
    """
    if not export_dir:
        export_dir = os.getcwd() + '/exports'

    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)

