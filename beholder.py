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
    methods_ = [
        method
        for method in dir(obj)
        if callable(getattr(obj, method)) and not method.startswith("_")
    ]
    # methods_ = [method_name for method_name in dir(obj) if method_name[0] != "_"]
    print(f"{len(methods_)} methods for {obj.__class__}: \n {methods_}")
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


from pathlib import Path
from typing import List, Dict


def search_files_for_strings(
    search_strings: List,
    search_pattern="*.ipynb",
    search_all_occurrences=False,
    case_sensitive_search=False,
    max_line_length=100,
) -> List[Dict]:
    """Search files for strings.
    Args:
        search_strings: List of strings to search for.
        search_pattern: File pattern to search for.
        search_all_occurrences: If True, include all occurrences of the search string in a line.
        case_sensitive_search: If True, perform case sensitive search.
        max_line_length: Maximum line length to print.
    Returns:
        List of dictionaries with search results.
    """
    # Get the current working directory as a Path object
    current_directory = Path.cwd()

    # Print search information
    print(f"Looking for: {search_strings} in {search_pattern} files")
    print(f"Include all occurrences: {search_all_occurrences}")
    print(f"Case sensitive search: {case_sensitive_search}")
    print(f"Maximum line length to print: {max_line_length} characters")
    print("File:", " " * 8, ": Search result:")
    print("." * 80)

    # Initialize a list to store search results
    search_results = []

    # Iterate through files matching the pattern recursively
    for file_path in Path(current_directory).rglob(search_pattern):
        with open(file_path, encoding="UTF-8") as file:
            file_content = file.readlines()

            for line_number, line in enumerate(file_content, start=1):
                # Iterate through search strings
                for search_string in search_strings:
                    if not case_sensitive_search:
                        line_lower = line.lower()
                        search_string = search_string.lower()
                    else:
                        line_lower = line

                    if search_string in line_lower:
                        # Truncate the line to the maximum length
                        if len(line) > max_line_length:
                            start_index = line_lower.index(search_string)
                            try:
                                end_index = line_lower.index("\n", start_index)
                            except ValueError:
                                end_index = len(
                                    line_lower
                                )  # If no newline, use end of line

                            if end_index - start_index > max_line_length:
                                truncated_line = line[
                                    start_index : start_index + max_line_length
                                ]
                            else:
                                # If the search string is near the end of the line,
                                # truncate the beginning of the line
                                truncated_line = line[
                                    max(0, end_index - max_line_length) : end_index
                                ]
                        else:
                            truncated_line = line.strip()

                        search_results.append(
                            {
                                "file_path": Path(current_directory) / file_path,
                                "line_number": line_number,
                                "line_text": truncated_line,
                            }
                        )

                        if not search_all_occurrences:
                            break

    return search_results


import pathlib
import urllib.request


def download_file_from_url(url: str, file_name: str, dest_folder="data"):
    """
    Download a file from a given URL and save it to a specified destination folder.

    Parameters:
    - url: The URL of the file to be downloaded.
    - dest_folder: The path of the destination folder where the file should be saved.
    - file_name: Name of the saved file.

    Returns:
    - file_path: Path where the file is saved.
    """
    local_data_dir = pathlib.Path(dest_folder)
    file_path = local_data_dir / file_name

    # Create the data directory if it does not exist
    if not os.path.exists(local_data_dir):
        os.makedirs(local_data_dir)

    # Download the file if it does not exist
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(url, file_path)
        print(f"File downloaded to {file_path}")
    else:
        print(f"File already exists at {file_path}")

    return file_path


def get_or_download_llm_model(
    llm_name: str, dest_folder: Path, tokenizer_cls: type, model_cls: type
):
    """
    Check if the LLM model exists in local storage, and if not, download it.

    Parameters:
    - llm_name: Name of the LLM model (e.g., "distilbert-base-uncased").
    - dest_folder: The root directory for storing models.
    - tokenizer_cls: Tokenizer class (e.g., DistilBertTokenizer).
    - model_cls: Model class (e.g., DistilBertModel).

    Returns:
    - tokenizer: The tokenizer for the LLM model.
    - model: The LLM model.
    """

    dest_folder.mkdir(exist_ok=True)
    model_dir = dest_folder / llm_name
    model_dir.mkdir(
        parents=True, exist_ok=True
    )  # if llm_name include subfolders, create them (parents=True)

    if llm_name in os.listdir(dest_folder):  # check if the model is already downloaded
        # Load the tokenizer and model from local storage
        os.system(f'say "{llm_name} is found on the local device"')
        tokenizer = tokenizer_cls.from_pretrained(model_dir)
        model = model_cls.from_pretrained(model_dir)
    else:
        # Download the model if it is not already downloaded
        tokenizer = tokenizer_cls.from_pretrained(llm_name)
        model = model_cls.from_pretrained(llm_name)
        # Save the tokenizer and model to local storage
        tokenizer.save_pretrained(model_dir)
        model.save_pretrained(model_dir)

    return tokenizer, model


if __name__ == "__main__":
    add_sys_path()
    for path in sys.path:
        print(path)
