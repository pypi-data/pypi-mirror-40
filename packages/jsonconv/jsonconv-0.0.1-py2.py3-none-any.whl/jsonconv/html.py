from . import common


def write(json_data, page_title="", h2="", h3="", url_key="", url_for_key=""):
    """
    Args:
        json_data (JSON) : list of dicts
        page_title (str) : What should appear as the page title
        h2 (str): What should appear in the <h2> tag
        h3 (str): What should appear in the <h3> tag
        url_key (str) : dict key containing a URL (if any)
        url_for_key (str) : dict key for which the values will be in an <a> tag (e.g. if set to name: every value in the column "name" will contain the link)

    Returns:
        html (str): HTML page with JSON data in a table
    """
    if url_key != "" and url_for_key == "":
        raise ValueError("url_key with no url_for_key")
    elif url_key == "" and url_for_key != "":
        raise ValueError("url_for_key with no url_key")
    columns = common._get_columns(json_data)
    if url_key != "":
        columns.remove(url_key)

    thead = "\t\t\t\t<th>"
    # keep all columns except the url column
    thead = "\n\t\t\t\t<th>".join(columns)
    tbody = ""
    for row in json_data:
        tbody += "\t\t\t<tr>\n"
        # keep all columns except the url column
        for col in (col for col in row if col != url_key):
            if col == url_for_key:
                # put text in an <a> element, with url in the href attribute.
                value = "<a href={}>{}</a>".format(row[url_key], row[col])
            else:
                value = row[col]
            tbody += "\t\t\t\t<td>{}\n".format(value)
        tbody += "\t\t\t</tr>\n"
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" name="viewport"
content="width=device-width, initial-scale=1">
<title>{}</title>
</head>
<body>
<h2>{}</h2>
<h3>{}</h3>
<table>
    <thead>
        <tr>
{}
        </tr>
    </thead>
    <tbody>
{}
    </tbody>
</table>
</body>
</html>
""".format(page_title, h2, h3, thead, tbody)
    return html
