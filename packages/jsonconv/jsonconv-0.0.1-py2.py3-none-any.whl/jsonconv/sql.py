from . import common


def read(connection, query=None):
    """Returns query results as JSON object

    Args:
        connection (DB-API 2.0 compliant connection object)
        query (str): query to be run (if None, a connection object will be returned, allowing to get any query as JSON)
    Returns:
        json_data (JSON object) : query results
    """
    conn = connection

    def _dict_factory(cursor, row):
        """Factory method for returning SQL data as JSON object"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = _dict_factory
    if query is None:
        c = conn.cursor()
        json_data = c.execute(query).fetchall()
        conn.commit()  # in case query requires it
        return json_data
    else:
        return conn


def write(json_data, table, connection, cursor=None, is_tmp=False, ignore_on_conflict=None):
    """Writes json_data to table
    This will create the table if it does not exist and insert the remaining data into the table

    Args:
        json_data (JSON object): JSON data to be written
        table (str) : name of table to write to
        connection (DB-API 2.0 compliant connection object)
        cursor: (connection.cursor): cursor for executing statements (if None, will be created)
        ignore_on_conflict (bool): if True, any conflicts will be resolved by not inserting a row. if False, rows in json_data will overwrite conflicting rows in the table (default: if any conflict, raise an exception)

    Returns:
        rowcount (int): number of records affected
    """
    if isinstance(json_data, dict):  # if only contains one row
        json_data = [json_data]  # put in a list for compatiblity with rest of function

    if len(json_data) > 0:  # if not empty
        columns, types = common._get_columns(json_data, get_types=True)
        _create_table_if_not_exists(json_data, table, connection)
        return _insert_into_table(json_data, columns, table, connection, cursor, ignore_on_conflict)


def _create_table_if_not_exists(columns, types, connection, table, is_tmp):
    columns_string = ",".join(columns)
    c = read(connection).cursor()
    try:
        c.execute("SELECT NULL FROM {}".format(table)).fetchone()

    except Exception as e:
        if "table" in repr(e).lower():  # no such table
            # create table
            # concatenate data type and column name. used for next statement
            types_to_sql = {"int": "int", "bool": "int", "float": "real"}
            sql_types = [types_to_sql.get(t, "text") for t in types]

            tmp = "TEMPORARY" if is_tmp else ""

            columns_string = ",".join(" ".join(col_and_type) for col_and_type in zip(columns, sql_types))

            c.execute("CREATE {} TABLE {} ({})".format(tmp, table, columns_string))

            connection.commit()
        else:
            raise e


def _insert_into_table(json_data, columns, table, connection, cursor, ignore_on_conflict):
    cursor = connection.cursor() if cursor is None else cursor
    question_marks = ",".join(["?"] * len(columns))  # one "?" per column

    rows = [
        # stringify each column then put into tuple
        tuple(str(r) for r in row.values())
        for row in json_data
    ]  # combine tuples (i.e. rows) into one list

    cursor.executemany("INSERT INTO {} ({}) VALUES ({})".format(table, ",".join(columns), question_marks), rows)
    connection.commit()
    return cursor.rowcount
