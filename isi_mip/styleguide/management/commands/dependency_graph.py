import glob
import os
import re

from django.core.management.base import BaseCommand

try:
    import networkx as nx
    from networkx.drawing import nx_agraph
except:
    raise Exception("To use this, you need to: pip install networkx pygraphviz")


class Command(BaseCommand):
    help = 'Create a tree-like structure showing which template includes which'

    def handle(self, *args, **options):
        re_include = re.compile("{%\s+?(include|extends)\s+?['|\"](.*?)['|\"]\s+?.*?%}", re.DOTALL)
        htmlfiles = glob.glob('**/*.html', recursive=True)

        G = nx.DiGraph()
        labels = {}
        for path in sorted(htmlfiles, key=lambda x: os.path.basename(x)):
            bpath = os.path.basename(path)
            with open(path, 'r') as datei:
                allet = datei.read()
                includes = re_include.findall(allet)
                for incl in includes:
                    if incl[0] == 'include':
                        x, y = bpath, os.path.basename(incl[1])
                        labels[(x, y)] = 'include'
                    else:
                        x, y = os.path.basename(incl[1]), bpath
                        labels[(x, y)] = 'extends'
                    G.add_edge(x, y)

        # pos = nx.spring_layout(G)
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        A = nx_agraph.to_agraph(G)
        A.graph_attr.update(rankdir='LR')
        A.draw('dependency_graph.png', prog='dot')
