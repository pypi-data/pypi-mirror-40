import importlib_metadata
import tomlkit
from beautifultable import BeautifulTable


def load_toml(filename):
    """
    Load toml file.

    :param filename: filename
    :return: toml body
    :rtype: dict

    """
    with open(filename) as f:
        return tomlkit.parse(f.read())


def get_package_names(pyproject):
    """
    Get package names

    :param dict pyproject: pyproject.toml body.
    :return: Package names
    :rtype: list

    """
    package_names = []
    for pkg in pyproject["package"]:
        if pkg["category"] == "main":
            package_names.append(pkg["name"])
    return package_names


def get_packages_metadata(package_names):
    """
    Get list of installed package's metadata

    :param list package_names: Install package names.
    :return: list of dict. Dict contains package name and license.
    :rtype: list

    """
    results = []
    for name in package_names:
        d = {"name": name}
        try:
            metadata = importlib_metadata.metadata(name)
        except importlib_metadata.api.PackageNotFoundError:
            continue
        else:
            d["version"] = metadata["Version"]
            d["license"] = metadata["License"]
            results.append(d)
    return results


def create_table(rows, order, style):
    """
    Create table for display

    :param list rows: table rows
    :param str order: table sorted order
    :param str style: table style
    :return: table for display
    :rtype: BeautifulTable

    """
    table = BeautifulTable()
    table.column_headers = ["name", "license"]
    table.column_alignments["name"] = BeautifulTable.ALIGN_LEFT
    table.column_alignments["license"] = BeautifulTable.ALIGN_LEFT

    if style == "markdown":
        table.set_style(BeautifulTable.STYLE_MARKDOWN)
    elif style == "rst":
        table.set_style(BeautifulTable.STYLE_RESTRUCTURED_TEXT)
    else:
        table.set_style(BeautifulTable.STYLE_COMPACT)

    for row in rows:
        table.append_row(row)

    if order == "license":
        table.sort("license")

    return table
