"""Sets the path to the TOP folder so that the modules can be imported"""
import sys
import os
import pandas as pd


# from the src folder
# Windows: set PYTHONPATH=%PYTHONPATH%;C:.....\src
# Linux: export PYTHONPATH=$PYTHONPATH:/home/.../src
# Docker: ENV PYTHONPATH="./src"


# src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_folder = os.path.abspath(os.path.dirname(__file__))
# project_path = os.path.abspath(os.path.join(os.path.dirname(src_folder)))
other_folders = os.path.join(src_folder, "NLP")
pathlist = [src_folder, other_folders]


def add_sys_path(pathlist=pathlist):
    """Add path to sys.path if it is not there"""
    for path_name in pathlist:
        if path_name not in sys.path:
            sys.path.append(path_name)


def remove_sys_path(pathlist=pathlist):
    """Remove path from sys.path if it is there"""
    for path_name in pathlist:
        if path_name in sys.path:
            sys.path.remove(path_name)


add_sys_path(pathlist)
# remove_sys_path(path_list)


def get_variable_name(obj: object) -> str:
    """Returns the name of the variable"""
    for name, value in globals().items():
        if id(value) == id(obj):
            return name
    return None


def print_methods(obj: object) -> list:
    """Returns all methods of an object"""
    methods_ = [method_name for method_name in dir(obj) if method_name[0] != "_"]
    print(
        f"{len(methods_)} methods for {get_variable_name(obj)} ({obj.__class__}): \n {methods_}"
    )
    return methods_


def call_methods(obj: object):
    methods_ = print_methods(obj)
    for method_name in methods_:
        try:
            method = getattr(obj, method_name)
            if callable(method):
                print(f"Calling method: {method_name}")
                try:
                    result = method()
                    print(f"Result: {result}\n")
                except Exception as e:
                    print(f"Error: {e}\n")
            else:
                print(f"{method_name} is not callable.\n")
        except Exception as e:
            # print(f"Error: {e}\n")
            pass


def check_na(df: pd.DataFrame, dtype_sort=True) -> pd.DataFrame:
    """
    Check for missing values in a dataframe
    df - dataframe
    sort - sort by column name or by dtype or by nans% (if `category` dtype is present)
    """

    import pandas as pd

    sort = ["dtype", "nans%"] if dtype_sort else ["nans%"]
    dict_ = {}
    for col in df.columns:
        dict_[col] = {
            "dtype": df[col].dtype,
            "nans": df[col].isna().sum(),
            "nans%": df[col].isna().sum() / df.shape[0] * 100,
        }
    return (
        pd.DataFrame(dict_)
        .T.sort_values(by=sort, ascending=False)
        .style.bar(subset=["nans%"], color="#faebd7")
        .format(precision=1, thousands=",")
    )


if __name__ == "__main__":
    add_sys_path()
    for path in sys.path:
        print(path)
