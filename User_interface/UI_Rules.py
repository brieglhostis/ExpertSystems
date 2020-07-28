import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from Knowledge_base.Rules import *
import User_interface


class RulesDisplay:
    
    def __init__(self, facts, rules, rules_fuzzy, fuzzy_sets, o_rules, root):
        """
        Displays the rules in the knowledge base, listing the conditions, in conclusions, and the description.
        There is also a button to add a new rule.
        Args:
            facts (list[Fact]): list of facts in the knowledge base
            rules (list[Rule]): list of rules in the knowledge base
            rules_fuzzy (list[Rule_Fuzzy]): list of rules in the knowledge base for the fuzzy algorithm
            fuzzy_sets (list[Fuzzy_Set]): list of fuzzy sets in the knowledge base for the fuzzy algorithm
            o_rules (ttk.frame): tab of the rules
            root (Tk): root window of the user interface
        """
        self.facts = facts
        self.rules = rules
        self.rules_fuzzy = rules_fuzzy
        self.fuzzy_sets = fuzzy_sets
        self.o_rules = o_rules
        self.root = root
        
        Label(o_rules, text="Conditions").grid(row=0, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        Label(o_rules, text="Conclusions").grid(row=0, column=1, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        Label(o_rules, text="Description").grid(row=0, column=2, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        
        # for each rule, we display the conditions, the conclusions and the description
        for i in range(len(rules)):
            RuleItem(self, i)
        
        # this button allows to create a new rule
        Button(o_rules, text="Créer une nouvelle règle", command=lambda: RuleCreation(self), padx="0.5c", pady="0.2c",
               overrelief="groove", cursor="hand2") \
            .grid(row=len(rules) + 2, columnspan=2, padx=("1c", 0), pady=("1c", "0.5c"), sticky=W)


class RuleCreation:
    
    def __init__(self, rulesDisplay):
        """
        Allows the user to create a new rule. The user has to select the condition and the conclusions among the facts,
        and to write a description before validating the creation of the rule.
        """
        
        self.rulesDisplay = rulesDisplay
        
        # The creation form will be in a new window
        self.new_rule_root = Toplevel()
        self.new_rule_root.title("Création d'une nouvelle règle")
        
        Label(self.new_rule_root, text="Conditions :").grid(row=0, padx="0.3c")
        Label(self.new_rule_root, text="Conclusions :").grid(row=0, column=2, padx="0.3c", sticky=E)
        
        # The user can select the conditions and the conclusions among the existing facts
        self.condition_vars = [IntVar() for _ in range(len(self.rulesDisplay.facts))]
        self.conclusion_vars = [IntVar() for _ in range(len(self.rulesDisplay.facts))]
        
        for i in range(len(self.rulesDisplay.facts)):
            Checkbutton(self.new_rule_root, text=self.rulesDisplay.facts[i].name, variable=self.condition_vars[i],
                        cursor="hand2") \
                .grid(row=i, column=1, sticky=W)
            Checkbutton(self.new_rule_root, text=self.rulesDisplay.facts[i].name, variable=self.conclusion_vars[i],
                        cursor="hand2") \
                .grid(row=i, column=3, sticky=W)
        
        # A field allows to write a description for the rule
        Label(self.new_rule_root, text="Description :").grid(row=len(self.rulesDisplay.facts) + 1, column=0, sticky=E,
                                                             pady="0.5c")
        self.description = Entry(self.new_rule_root, width=60)
        self.description.grid(row=len(self.rulesDisplay.facts) + 1, column=1, columnspan=3, pady="0.5c",
                              padx=(0, "0.5c"), sticky=W)
        
        Button(self.new_rule_root, text="   Créer   ", command=self.validate, overrelief="groove", cursor="hand2") \
            .grid(row=len(self.rulesDisplay.facts) + 2, columnspan=4, padx="0.5c", pady=("0.5c", "0.5c"))
    
    def validate(self):
        """
        This function is called when the button "creer" is pressed in the creation form. It saves the new rule in
        the knowledge base before calling the update function to display this new rule with the others
        """
        
        # We recover the choices made by the user in the form
        conditions = []
        conclusions = []
        for i in range(len(self.rulesDisplay.facts)):
            if self.condition_vars[i].get() == 1:
                conditions.append(self.rulesDisplay.facts[i])
            if self.conclusion_vars[i].get() == 1:
                conclusions.append(self.rulesDisplay.facts[i])
        
        # We save the new rule in the knowledge base
        self.rulesDisplay.rules.append(Rule(conditions, conclusions, self.description.get()))
        # The creation form is destroyed
        self.new_rule_root.destroy()
        # We call the update function to display the new rule
        User_interface.Main_menu.update(self.rulesDisplay.root, self.rulesDisplay.facts,
                                        self.rulesDisplay.rules, self.rulesDisplay.rules_fuzzy,
                                        self.rulesDisplay.fuzzy_sets)


class RuleItem:
    
    def __init__(self, rulesDisplay, position):
        """
        This function display a rule in the root window and provides a button to delete it
        Args:
            rulesDisplay (RulesDisplay): parent
            position (int): position of the rule to be displayed
        """
        self.rulesDisplay = rulesDisplay
        self.position = position
        rule = self.rulesDisplay.rules[position]
        
        conditions = ""
        for fact in rule.conditions:
            conditions += fact.name + ", "
        Label(self.rulesDisplay.o_rules, text=conditions[:-2], width=20, anchor="w") \
            .grid(row=position + 1, padx=("0.2c", 0), sticky=W)
        
        conclusions = ""
        for fact in rule.conclusions:
            conclusions += fact.name + ", "
        Label(self.rulesDisplay.o_rules, text=conclusions[:-2], width=20, anchor="w") \
            .grid(row=position + 1, column=1, sticky=W)
        
        Label(self.rulesDisplay.o_rules, text=rule.description, width=80, anchor="w") \
            .grid(row=position + 1, column=2, sticky=W)
        
        Button(self.rulesDisplay.o_rules, text="✘", borderwidth=0, command=self.delete_pressed, cursor="hand2",
               font=("Arial", 16)) \
            .grid(row=position + 1, column=3, sticky=W, padx=(0, "0.5c"))
    
    def delete_pressed(self):
        """
        Deletes the rule when the delete button is pressed
        """
        self.rulesDisplay.rules.pop(self.position)
        User_interface.Main_menu.update(self.rulesDisplay.root, self.rulesDisplay.facts,
                                        self.rulesDisplay.rules, self.rulesDisplay.rules_fuzzy,
                                        self.rulesDisplay.fuzzy_sets)
