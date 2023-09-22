"""Test the dtool_lookup_client_dependency_graph_plugin package."""


def test_version_is_string():
    import dtool_lookup_client_dependency_graph_plugin
    assert isinstance(dtool_lookup_client_dependency_graph_plugin.__version__, str)
