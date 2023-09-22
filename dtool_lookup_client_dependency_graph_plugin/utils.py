import logging
import textwrap
import uuid

from collections import defaultdict

logger = logging.getLogger(__name__)


def is_uuid(value):
    '''Check whether the data is a UUID.'''
    value = str(value)
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def graph_to_dot(
        graph,
        node2rule=lambda node: node,
        node2style=lambda node: "rounded",
        node2label=lambda node: node,
):
    """Print dot format, adapted from https://github.com/snakemake/snakemake/blob/a4ff3280db0beb4f1a077ee880433f767c4ad142/snakemake/dag.py#L2015C5-L2064C1"""

    # color rules
    n = len(graph)
    logger.debug("Graph has %d nodes", n)
    huefactor = 2 / (3 * n)
    rulecolor = {
        vertex: "{:.2f} 0.6 0.85".format(i * huefactor)
        for i, vertex in enumerate(graph)
    }

    # markup
    node_markup = '\t{}[label = "{}", color = "{}", style="{}"];'.format
    edge_markup = "\t{} -> {}".format

    # node ids
    ids = {node: i for i, node in enumerate(graph)}

    logger.debug(f"Node ids: {ids}")

    # calculate nodes
    nodes = [
        node_markup(
            ids[node],
            node2label(node),
            rulecolor[node2rule(node)],
            node2style(node),
        )
        for node in graph
    ]
    # calculate edges
    edge_tuples = [(node, dep) for node, deps in graph.items() for dep in deps]
    for i, edge in enumerate(edge_tuples):
        logger.debug("Edge %d: %s -> %s", i, *edge)
    edges = [
        edge_markup(ids[dep], ids[node])
        for node, deps in graph.items()
        for dep in deps
    ]

    return textwrap.dedent(
        """\
        digraph snakemake_dag {{
            graph[bgcolor=white, margin=0];
            node[shape=box, style=rounded, fontname=sans, \
            fontsize=10, penwidth=2];
            edge[penwidth=2, color=grey];
        {items}
        }}\
        """
    ).format(items="\n".join(nodes + edges))


def build_graph_from_dataset_list(datasets, dependency_key=None, root_uuid=None):
    """Build graph from list of datasets."""

    logger.debug("Server response on querying dependency graph for UUID = {}.".format(root_uuid))

    graph = defaultdict(set)
    uuid_vertex_dict = dict()
    missing_uuids = list()

    for dataset in datasets:
        # This check should be redundant, as all documents have field 'uuid'
        # and this field is unique:
        uuid = dataset['uuid']
        if 'uuid' in dataset and uuid not in uuid_vertex_dict:
            logger.debug(f"Add dependency graph vertex '{uuid}'.")
            v = dict(
                uuid=uuid,
                name=dataset['name'],
                kind='root' if uuid == root_uuid else 'dependent')
            uuid_vertex_dict[uuid] = v
            graph[dataset['uuid']].update(set())

    for dataset in datasets:
        if 'uuid' in dataset and 'derived_from' in dataset:
            for parent_uuid in dataset['derived_from']:
                if is_uuid(parent_uuid):
                    if parent_uuid not in uuid_vertex_dict:
                        # This UUID is present in the graph but not in the database
                        logger.debug(f"Add dependency graph vertex of missing dataset '{parent_uuid}'.")
                        v = dict(
                            uuid=parent_uuid,
                            name='Dataset does not exist in database.',
                            kind='does-not-exist')

                        uuid_vertex_dict[parent_uuid] = v
                        missing_uuids += [parent_uuid]

                    logger.debug(f"Add dependency graph edge between child '{dataset['uuid']}' and parent {parent_uuid}.")
                    graph[dataset['uuid']].update([parent_uuid])
                else:
                    logger.warning(
                        "Parent dataset '{}' of child '{}': '{}' is no "
                        "valid UUID, ignored.".format(parent_uuid,
                                                      dataset['uuid'],
                                                      dataset['name']))

    logger.debug(f"Done building dependency graph.")
    if len(missing_uuids):
        logger.warning(f"Datasets {missing_uuids} missing in graph.")

    return graph
