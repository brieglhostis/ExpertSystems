import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from tkinter import ttk
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule
from User_interface.UI_Rules import *
from User_interface.UI_Facts import *
from User_interface.UI_Rules_Fuzzy import *
from User_interface.UI_Fuzzy_Sets import *
from User_interface.UI_Run import *


class DisplayUI:
    
    def __init__(self, facts, rules, rules_fuzzy, fuzzy_sets):
        """
        This function generates the entire user interface with the help of the classes UI_Run, UI_Rules and UI_Facts. It
        uses the python library tkinter, and creates tabs with the Notebook
        Args:
            facts (list[Fact]): list of facts in the knowledge base
            rules (list[Rule]): list of rules in the knowledge base
        """
        self.root = Tk()
        self.root.title("Base de connaissances")
        
        n = ttk.Notebook(self.root)
        n.pack()
        o_rules = ttk.Frame(n)
        o_rules.pack()
        o_facts = ttk.Frame(n)
        o_facts.pack()
        o_rules_fuzzy = ttk.Frame(n)
        o_rules_fuzzy.pack()
        o_fuzzy_sets = ttk.Frame(n)
        o_fuzzy_sets.pack()
        o_run = ttk.Frame(n)
        o_run.pack()
        n.add(o_rules, text="  Rules  ")
        n.add(o_facts, text="  Facts  ")
        n.add(o_rules_fuzzy, text="  Fuzzy Rules  ")
        n.add(o_fuzzy_sets, text="  Fuzzy Sets  ")
        n.add(o_run, text="  Run  ")
        
        # We create the display of the rules tab...
        RulesDisplay(facts, rules, rules_fuzzy, fuzzy_sets, o_rules, self.root)
        # ... of the facts tab...
        FactDisplay(facts, rules, rules_fuzzy, fuzzy_sets, o_facts, self.root)
        # ... of the fuzzy rules tab...
        RulesFuzzyDisplay(facts, rules, rules_fuzzy, fuzzy_sets, o_rules_fuzzy, self.root)
        # ... of the fuzzy sets tab...
        FuzzySetsDisplay(facts, rules, rules_fuzzy, fuzzy_sets, o_fuzzy_sets, self.root)
        # ... and of the run tab.
        RunDisplay(facts, rules, rules_fuzzy, fuzzy_sets, o_run, self.root)
        
        self.root.mainloop()


def update(root, facts, rules, rules_fuzzy, fuzzy_sets):
    """
    This function update the entire display when the knowledge base is changed
    Args:
        root (Tk): root window of the current display
        facts (list[Fact]): list of facts in the knowledge base
        rules (list[Rule]): list of rules in the knowledge base
    """
    root.destroy()
    DisplayUI(facts, rules, rules_fuzzy, fuzzy_sets)
