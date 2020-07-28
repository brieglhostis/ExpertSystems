import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule


def display_explanation_tree(facts, rules, root):
    """
    This function displays an explanation tree in order to explain more clearly the reasoning of the inference engine
    Args:
        facts (list[fact]): list of the facts explored (true or false)
        rules (list[rule]): list of the rules that have been used
        root (tk.Tk): root window of the result display
    """
    G = nx.DiGraph()
    
    fact_names = []
    node_colors = []
    
    # We add the facts to the graph
    for fact in facts:
        G.add_node(fact.name)
        fact_names.append(fact.name)
    
    # We add the edges according to the rules, with the color depending on the usability of the rule
    for i in range(len(rules)):
        
        if len(rules[i].conditions) > 1:
            usable = True
            for fact in rules[i].conditions:
                if fact not in facts:
                    usable = False
            
            G.add_node("AND ({})".format(i))
            
            if usable:
                for condition in rules[i].conditions:
                    G.add_edge(condition.name, "AND ({})".format(i), color='green')
                for conclusion in rules[i].conclusions:
                    G.add_edge("AND ({})".format(i), conclusion.name, color='green')
            else:
                for condition in rules[i].conditions:
                    G.add_edge(condition.name, "AND ({})".format(i), color='red')
                for conclusion in rules[i].conclusions:
                    G.add_edge("AND ({})".format(i), conclusion.name, color='red')
        
        else:
            if rules[i].conditions[0] in facts:
                for conclusion in rules[i].conclusions:
                    G.add_edge(rules[i].conditions[0].name, conclusion.name, color='green')
            else:
                for conclusion in rules[i].conclusions:
                    G.add_edge(rules[i].conditions[0].name, conclusion.name, color='red')
    
    # The nodes are colorized depending on the veracity of the fact
    for node in G.nodes():
        if node in fact_names:
            node_colors.append('#03fc10')
        elif node[:3] == "AND":
            node_colors.append('white')
        else:
            node_colors.append('red')
    
    edges = G.edges()
    edge_colors = [G[u][v]['color'] for u, v in edges]
    
    # The graph is displayed in the tkinter window
    f = plt.figure()
    a = f.add_subplot(111)
    plt.axis('off')
    
    nx.draw_networkx(G, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=1000, font_size=8)
    
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, pady=(0, "0.5c"))
