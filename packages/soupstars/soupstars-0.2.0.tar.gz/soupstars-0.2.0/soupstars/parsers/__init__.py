# TODO: need these for building dynamic routes on the flask app and testing
# the parsers.

import os
import importlib


class InvalidParserDirectoryError(BaseException):
    pass


def _iter_parser_package_paths():
    """
    List the packages in the parsers directory
    """

    packages_directory = os.path.dirname(__file__)
    packages_directory_items = os.listdir(packages_directory)
    for item in packages_directory_items:
        if item == "__pycache__" or item == "__init__.py":
            continue
        item_path = os.path.join(packages_directory, item)
        if os.path.isdir(item_path):
            yield item_path
        else:
            raise InvalidParserDirectoryError("Found non-folder in parsers directory")


def _iter_parser_modules():
    for path in _iter_parser_package_paths():
        modules = os.listdir(path)
        for module in modules:
            if module not in ("__pycache__", "__init__.py"):
                yield os.path.join(path, module)


def _iter_parsers():
    """
    Iterate over all the parsers defined in packages in this directory
    """

    for filename in _iter_parser_modules():
        components = filename.split(os.path.sep)
        module = components.pop()
        module_name = module.split(".")[0]
        package_name = components.pop()
        parser_relative_directory = '.'.join(components[-2:])
        parser_import_path = ".".join([
            parser_relative_directory,
            package_name,
            module_name
        ])

        classname = "{pn}{mn}Parser".format(
            pn=package_name.capitalize(),
            mn=module_name.capitalize()
        )

        module = importlib.import_module(parser_import_path)
        parser = getattr(module, classname)
        yield parser


def _save_test_response(parser_name):
    """
    Call the default route of the host and save to a file next to the parser.
    Helpful for writing tests and updating them whenever the sources change.

    >>> _save_test_response('nytimes.article')
    >>> # writes to parsers/nytimes/article.response
    """

    pass
