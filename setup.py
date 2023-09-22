import os
from setuptools import setup

url = "https://github.com/IMTEK-Simulation/dtool-lookup-client-dependency-graph-plugin"
readme = open('README.rst').read()


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="dtool_lookup_client_dependency_graph_plugin",
    packages=["dtool_lookup_client_dependency_graph_plugin"],
    description="Dtool plugin for retrieving dependency graph from dtool lookup server",
    long_description=readme,
    include_package_data=True,
    author="Johannes Laurin Hörmann",
    author_email="johannes.laurin@gmail.com",
    use_scm_version={
        "root": '.',
        "relative_to": __file__,
        "write_to": os.path.join("dtool_lookup_client_dependency_graph_plugin", "version.py"),
        "local_scheme": local_scheme},
    setup_requires=[
        'setuptools_scm'
    ],
    url=url,
    install_requires=[
        "asgiref",
        "click",
        "requests",
        "dtoolcore>=3.9.0",
        "dtool-cli>=0.7.1",
        "dtool_config>=0.1.1",
        "dtool-lookup-api>=0.7.0",
        "pygments",
    ],
    entry_points={
        "dtool.cli": [
            "graph=dtool_lookup_client_dependency_graph_plugin:graph"
        ],
    },
    license="MIT"
)
