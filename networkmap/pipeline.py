"""
This tool parses various network 'dumps' such as traceroute, arp tables etc.
and produces a growing network graph of all reachable nodes.

"""
import logging
import json
import os
import shutil

import networkx as nx

from networkmap.errors import MyException
from networkmap.netgrapher import grow_graph
from networkmap.parsers import SUPPORTED_OS, SUPPORTED_DUMPFILES

logger = logging.getLogger('netgrapher')

DEFAULT_SAVEFILE = "networkmap"
DEFAULT_GRAPHIMG = "/tmp/out.png"

SUPPORTED_FILE_FORMATS = [
    'GEXF',
    'DOT',
    'JSON',
    'GRAPHML',
]
DEFAULT_FILE_FORMAT = 'JSON'


# see: http://stackoverflow.com/a/37578709/204634
# but also: https://networkx.readthedocs.io/en/stable/reference/drawing.html#module-networkx.drawing.nx_agraph
def load_graph(savefile, file_format, new_graph):
    """Does what it says on the tin(c)"""
    if savefile is None or new_graph:
        return nx.Graph()
    if os.path.exists(savefile):
        if file_format == 'GEXF':
            # importing here because if there's no xml.etree installed,
            # things should still work with other file formats.
            from xml.etree.cElementTree import ParseError as cParseError
            from xml.etree.ElementTree import ParseError as ParseError

            try:
                g = nx.read_gexf(savefile)
            # I hate catching 'Exception' but read_gexf raises
            # 'cElementTree.ParseError' (or ElementTree.ParseError, no 'c')
            # which is nowhere to be found
            # except Exception as e:
            # alternative solution, not sure it's better or not:
            except (cParseError, ParseError) as e:
                raise MyException("Cannot read file {} using format {}: {}".format(
                    savefile, file_format, e))
        elif file_format == 'DOT':
            import pygraphviz
            try:
                g = nx.nx_agraph.read_dot(savefile)
            except ImportError:
                raise MyException("Cannot find pygraphviz")
            except pygraphviz.agraph.DotError as e:
                logger.error("Cannot load file {}".format(savefile))
                raise MyException(e)
        elif file_format == 'JSON':
            from networkx.readwrite import json_graph
            with open(savefile) as f:
                json_data = json.load(f)
            g = json_graph.node_link_graph(json_data)
            logger.debug("Loaded JSON savefile. Nodes: {}".format(
                g.nodes(data=True)))
        elif file_format == 'GRAPHML':
            from networkx.readwrite import graphml
            g = graphml.read_graphml(savefile)
        else:
            raise MyException("Unknown file format {}".format(file_format))
    else:
        logger.info("Savefile not found - initialising new graph...")
        g = nx.Graph()
    return g


import matplotlib.pyplot as plt


def save_graph(graph, savefile, file_format):
    """Does what it says on the tin(c)"""
    if os.path.exists(savefile):
        shutil.copy(savefile, "{}.bak".format(savefile))
        logger.info("Network DOT file backup saved: {}.bak".format(savefile))

    if file_format == 'GEXF':
        nx.write_gexf(graph, savefile)
    elif file_format == 'DOT':
        nx.nx_agraph.write_dot(graph, savefile)
    elif file_format == 'JSON':
        from networkx.readwrite import json_graph
        json_data = json_graph.node_link_data(graph)
        # plt.figure(figsize=(8, 6))
        #
        # nx.draw(graph)
        # plt.title('Graph Representation of Sleeping Giant Trail Map', size=15)
        # plt.show()
        with open(savefile, 'w') as f:
            # f.write(json_data)
            json.dump(json_data, f, indent=4)
    elif file_format == 'GRAPHML':
        from networkx.readwrite import graphml
        graphml.write_graphml(graph, savefile)
    else:
        logger.error("Unknown file format requested")
    logger.info("Network file saved to {}".format(savefile))
    return graph


def handle_dot_format(savefile):
    try:
        import pygraphviz as pgv
        # convert to image
        f = pgv.AGraph(savefile)
        f.layout(prog='circo')
        f.draw(DEFAULT_GRAPHIMG)
        logger.info("Graph image saved in {}".format(DEFAULT_GRAPHIMG))
    except ImportError as e:
        logger.error("Cannot find pygraphviz.")
    except IOError as e:
        logger.error(
            "Something went wrong when drawing, but the dot file is "
            "still good. Try one of the graphviz programs manually "
            "(e.g. neato, circo)")


def pipeline(dumpfile, ip=None, dumpfile_type=None, dumpfile_os=None, new_graph=True):
    ip = ip if ip else None
    dumpfile_type = dumpfile_type
    dumpfile_os = dumpfile_os
    savefile = DEFAULT_SAVEFILE
    file_format = DEFAULT_FILE_FORMAT
    dumpfile = dumpfile
    if file_format == 'DOT':
        handle_dot_format(savefile)
    else:
        savefile = "{}{}{}".format(savefile, os.path.extsep, file_format.lower())
        loaded_graph = load_graph(savefile, file_format, new_graph)

        final_graph = grow_graph(
            loaded_graph, dumpfile,
            dumpfile_os=dumpfile_os,
            dumpfile_type=dumpfile_type,
            ip=ip
        )
        graph = save_graph(final_graph, savefile, file_format)
        return graph
