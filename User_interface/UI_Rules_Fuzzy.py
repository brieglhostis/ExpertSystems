import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from Knowledge_base_fuzzy.Rules_Fuzzy import *
import User_interface


class RulesFuzzyDisplay:
    
    def __init__(self, facts, rules, rules_fuzzy, fuzzy_sets, o_rules_fuzzy, root):
        """
        Displays the rules in the knowledge base for the fuzzy algorithm, listing the conditions, in conclusions, and the description.
        There is also a button to add a new rule.
        Args:
            facts (list[Fact]): list of facts in the knowledge base
            rules (list[Rule]): list of rules in the knowledge base
            rules_fuzzy (list[Rule_Fuzzy]): list of rules in the knowledge base for the fuzzy algorithm
            fuzzy_sets (list[Fuzzy_Set]): list of fuzzy sets in the knowledge base for the fuzzy algorithm
            o_rules_fuzzy (ttk.frame): tab of the rules for the fuzzy algorithm
            root (Tk): root window of the user interface
        """
        self.facts = facts
        self.rules = rules
        self.rules_fuzzy = rules_fuzzy
        self.o_rules_fuzzy = o_rules_fuzzy
        self.fuzzy_sets = fuzzy_sets
        self.root = root
        
        Label(o_rules_fuzzy, text="Conditions").grid(row=0, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        Label(o_rules_fuzzy, text="Conclusions").grid(row=0, column=1, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        Label(o_rules_fuzzy, text="Description").grid(row=0, column=2, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        
        # for each rule, we display the conditions, the conclusions and the description
        for i in range(len(rules_fuzzy)):
            RuleFuzzyItem(self, i)
        
        # this button allows to create a new rule
        Button(o_rules_fuzzy, text="Créer une nouvelle règle", command=lambda: RuleCreation(self), padx="0.5c",
               pady="0.2c",
               overrelief="groove", cursor="hand2") \
            .grid(row=len(rules_fuzzy) + 2, columnspan=2, padx=("1c", 0), pady=("1c", "0.5c"), sticky=W)


class RuleCreation:
    
    def __init__(self, rulesFuzzyDisplay):
        """
        Allows the user to create a new rule.
        a description is automatically generated
        """
        
        self.rulesFuzzyDisplay = rulesFuzzyDisplay
        self.fuzzy_sets = rulesFuzzyDisplay.fuzzy_sets
        
        # The creation form will be in a new window
        self.new_rule_root = Toplevel()
        self.new_rule_root.title("Création d'une nouvelle règle")
        
        Label(self.new_rule_root, text="Conditions :").grid(row=0, padx="0.3c")
        
        Label(self.new_rule_root, text="Nom du fait").grid(row=1, padx="0.3c")
        Label(self.new_rule_root, text="Hedge").grid(row=1, column=2, padx="0.3c")
        Label(self.new_rule_root, text="Fuzzy set").grid(row=1, column=3, padx="0.3c")
        
        Label(self.new_rule_root, text="Conclusions :").grid(row=0, column=4, padx="0.3c")
        
        Label(self.new_rule_root, text="Nom du fait").grid(row=1, column=4, padx="0.3c")
        Label(self.new_rule_root, text="Hedge").grid(row=1, column=6, padx="0.3c")
        Label(self.new_rule_root, text="Fuzzy set").grid(row=1, column=7, padx="0.3c")
        
        self.condition_vars = [(StringVar(), StringVar(value="(no hedge)"), StringVar()) for i in range(5)]
        self.conclusion_vars = [(StringVar(), StringVar(value="(no hedge)"), StringVar()) for i in range(5)]
        
        for i in range(5):
            # The form for conditions
            
            Entry(self.new_rule_root, textvariable=self.condition_vars[i][2]).grid(row=i + 2, padx="0.3c")
            Label(self.new_rule_root, text="IS/ARE").grid(row=i + 2, column=1, padx="0.3c")
            OptionMenu(self.new_rule_root, self.condition_vars[i][1], *hedges).grid(row=i + 2, column=2, padx="0.3c")
            OptionMenu(self.new_rule_root, self.condition_vars[i][0],
                       *[fuzzy_set.name for fuzzy_set in rulesFuzzyDisplay.fuzzy_sets]).grid(row=i + 2, column=3,
                                                                                             padx="0.3c")
            
            # The form for conclusions
            
            Entry(self.new_rule_root, textvariable=self.conclusion_vars[i][2]).grid(row=i + 2, column=4, padx="0.3c")
            Label(self.new_rule_root, text="IS/ARE").grid(row=i + 2, column=5, padx="0.3c")
            OptionMenu(self.new_rule_root, self.conclusion_vars[i][1], *hedges).grid(row=i + 2, column=6, padx="0.3c")
            OptionMenu(self.new_rule_root, self.conclusion_vars[i][0],
                       *[fuzzy_set.name for fuzzy_set in rulesFuzzyDisplay.fuzzy_sets]).grid(row=i + 2, column=7,
                                                                                             padx="0.3c")
        
        Button(self.new_rule_root, text="   Créer   ", command=self.validate, overrelief="groove", cursor="hand2") \
            .grid(row=max(len(self.condition_vars), len(self.conclusion_vars)) + 2, column=1, columnspan=4, padx="0.5c",
                  pady=("0.5c", "0.5c"))
    
    def validate(self):
        """
        This function is called when the button "creer" is pressed in the creation form. It saves the new rule in
        the knowledge base before calling the update function to display this new rule with the others
        """
        # We recover the choices made by the user in the form
        conditions = []
        conclusions = []
        
        for i in range(5):
            if self.condition_vars[i][0].get() != "" and self.condition_vars[i][1].get() != "":
                fuzzy_set = [fs for fs in self.fuzzy_sets if fs.name == self.condition_vars[i][0].get()][0]
                conditions.append((fuzzy_set, self.condition_vars[i][1].get(), self.condition_vars[i][2].get()))
            if self.conclusion_vars[i][0].get() != "" and self.conclusion_vars[i][1].get() != "":
                fuzzy_set = [fs for fs in self.fuzzy_sets if fs.name == self.conclusion_vars[i][0].get()][0]
                conclusions.append((fuzzy_set, self.conclusion_vars[i][1].get(), self.conclusion_vars[i][2].get()))
        
        # We save the new rule in the knowledge base
        self.rulesFuzzyDisplay.rules_fuzzy.append(Rule_Fuzzy(conditions, conclusions, "default description"))
        
        # The creation form is destroyed
        self.new_rule_root.destroy()
        # We call the update function to display the new rule
        User_interface.Main_menu.update(self.rulesFuzzyDisplay.root, self.rulesFuzzyDisplay.facts,
                                        self.rulesFuzzyDisplay.rules, self.rulesFuzzyDisplay.rules_fuzzy,
                                        self.rulesFuzzyDisplay.fuzzy_sets)


class RuleFuzzyItem:
    
    def __init__(self, rulesFuzzyDisplay, position):
        """
        This function display a rule in the root window and provides a button to delete it
        Args:
            rulesDisplay (RulesDisplay): parent
            position (int): position of the rule to be displayed
        """
        self.rulesFuzzyDisplay = rulesFuzzyDisplay
        self.position = position
        rule = self.rulesFuzzyDisplay.rules_fuzzy[position]
        
        conditions = ""
        for fuzzy_set, hedge, fact_name in rule.conditions:
            conditions += fact_name + " IS/ARE " + hedge + " " + fuzzy_set.name + ", "
        Label(self.rulesFuzzyDisplay.o_rules_fuzzy, text=conditions[:-2], width=40, anchor="w") \
            .grid(row=position + 1, padx=("0.2c", 0), sticky=W)
        
        conclusions = ""
        for fuzzy_set, hedge, fact_name in rule.results:
            conclusions += fact_name + " IS/ARE " + hedge + " " + fuzzy_set.name + ", "
        Label(self.rulesFuzzyDisplay.o_rules_fuzzy, text=conclusions[:-2], width=40, anchor="w") \
            .grid(row=position + 1, column=1, sticky=W)
        
        Label(self.rulesFuzzyDisplay.o_rules_fuzzy, text=rule.description, width=60, anchor="w") \
            .grid(row=position + 1, column=2, sticky=W)
        
        Button(self.rulesFuzzyDisplay.o_rules_fuzzy, text="✘", borderwidth=0, command=self.delete_pressed,
               cursor="hand2",
               font=("Arial", 16)) \
            .grid(row=position + 1, column=3, sticky=W, padx=(0, "0.5c"))
    
    def delete_pressed(self):
        """
        Deletes the rule when the delete button is pressed
        """
        self.rulesFuzzyDisplay.rules_fuzzy.pop(self.position)
        User_interface.Main_menu.update(self.rulesFuzzyDisplay.root, self.rulesFuzzyDisplay.facts,
                                        self.rulesFuzzyDisplay.rules, self.rulesFuzzyDisplay.rules_fuzzy,
                                        self.rulesFuzzyDisplay.fuzzy_sets)
