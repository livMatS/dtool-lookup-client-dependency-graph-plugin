"""dtool_lookup_client_dependency_graph_plugin package."""

from datetime import date, datetime

import click
import json
import logging

import pygments
import pygments.lexers
import pygments.formatters

import dtoolcore
import dtoolcore.utils
import dtool_config.cli
import dtool_lookup_api

from .utils import graph_to_dot, build_graph_from_dataset_list

logger = logging.getLogger(__name__)


# workaround for diverging python versions:
try:
    from importlib.metadata import version, PackageNotFoundError
    logger.debug("imported version, PackageNotFoundError from importlib.metadata")
except ModuleNotFoundError:
    from importlib_metadata import version, PackageNotFoundError
    logger.debug("imported version, PackageNotFoundError from importlib_metadata")

# first, try to determine dynamic version at runtime
try:
    __version__ = version(__name__)
    logger.debug("Determined version %s via importlib_metadata.version", __version__)
except PackageNotFoundError:
    # if that fails, check for static version file written by setuptools_scm
    try:
        from .version import version as __version__
        logger.debug("Determined version %s from autogenerated dtool_lookup_gui/version.py", __version__)
    except:
        logger.debug("All efforts to determine version failed.")
        __version__ = None


DTOOL_LOOKUP_SERVER_URL_KEY = "DTOOL_LOOKUP_SERVER_URL"
DTOOL_LOOKUP_SERVER_TOKEN_KEY = "DTOOL_LOOKUP_SERVER_TOKEN"


@click.command()
@click.argument("uuid")
@click.option("--dependency-keys", 'dependency_keys', default=None)
@click.option("-p", "--page-number", 'page_number', default=1, type=int)
@click.option("-s", "--page-size", 'page_size', default=10, type=int)
@click.option("--dot",  is_flag=True, show_default=True, default=False, help="Print graph in dot format.")
def graph(uuid, dependency_keys, page_number, page_size, dot):
    """Print the URIs associated with a UUID in the lookup server."""
    pagination = {}
    r = dtool_lookup_api.graph(uuid, dependency_keys=dependency_keys, page_number=page_number, page_size=page_size, pagination=pagination)
    logger.info(f"Pagination information: {pagination}")
    if dot:
        graph = build_graph_from_dataset_list(r)
        txt = graph_to_dot(graph)
        click.secho(txt, nl=False)
    else:
        formatted_json = json.dumps(r, indent=2)
        colorful_json = pygments.highlight(
            formatted_json,
            pygments.lexers.JsonLexer(),
            pygments.formatters.TerminalFormatter())
        click.secho(colorful_json, nl=False)
