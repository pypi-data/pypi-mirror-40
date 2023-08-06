def _get_columns(json_data, get_types=False):
    """Gets column names of json_data by looking at longest dictionary
    Args:
        json_data (JSON object): JSON data
        get_types (bool): if True, column types will also be returned

    Returns:
        out (list or tuple of lists): if get_types is False, returns only column names list, else also returns column types
    """
    fullest_row = max(json_data, key=lambda x: len(x))
    columns = fullest_row.keys()  # get row w/ most columns to find data types
    if get_types:
        types = [type(fullest_row[c]).__name__ for c in columns]
        return columns, types
    else:
        return columns
