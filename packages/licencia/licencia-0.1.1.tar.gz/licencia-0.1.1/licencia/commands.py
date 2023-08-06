import sys

from cleo import Command

from .core import create_table
from .core import get_package_names
from .core import get_packages_metadata
from .core import load_toml


class ListCommand(Command):
    """
    List the licenses for external packages used in your repository.

    list
        {--o|order=name : Control display order by "name" or "license".}
        {--f|format=compact : Select the output format among: "compact", "markdown", or "rst"}

    """

    def handle(self):
        try:
            pyproject = load_toml("poetry.lock")
        except FileNotFoundError:
            self.line_error("ERROR: The lock file not found.", style="error")
            sys.exit(1)

        package_names = get_package_names(pyproject)
        if not package_names:
            self.line("No data")
            sys.exit(1)

        results = get_packages_metadata(package_names)

        rows = [(p["name"], p["license"]) for p in results]

        order = self.option("order")
        style = self.option("format")
        table = create_table(rows, order=order, style=style)

        print(table)
