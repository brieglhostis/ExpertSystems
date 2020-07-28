import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from Knowledge_base.Facts import *
import User_interface


class FactDisplay:
    
    def __init__(self, facts, rules, rules_fuzzy, fuzzy_sets, o_facts, root):
        """
        Displays the facts in the knowledge base, with their names and descriptions. There is also a button to add a
        new fact.
        Args:
            facts (list[Fact]): list of facts in the knowledge base
            rules (list[Rule]): list of rules in the knowledge base
            rules_fuzzy (list[Rule_Fuzzy]): list of rules in the knowledge base for the fuzzy algorithm
            fuzzy_sets (list[Fuzzy_Set]): list of fuzzy sets in the knowledge base for the fuzzy algorithm
            o_facts (ttk.frame): tab of the facts
            root (Tk): root window of the user interface
        """
        self.facts = facts
        self.rules = rules
        self.rules_fuzzy = rules_fuzzy
        self.fuzzy_sets = fuzzy_sets
        self.o_facts = o_facts
        self.root = root
        
        Label(self.o_facts, text="Name").grid(row=0, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        Label(self.o_facts, text="Description").grid(row=0, column=1, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        
        # For each fact, we display its name and its description
        for i in range(len(self.facts)):
            FactItem(self, i)
        
        # This button allows the creation of a new fact in the knowledge base
        Button(self.o_facts, text="Créer un nouveau fait", command=lambda: FactCreation(self), padx="0.5c", pady="0.2c",
               overrelief="groove", cursor="hand2") \
            .grid(row=len(self.facts) + 2, columnspan=2, padx=("0.5c", 0), pady=("1c", "0.5c"), sticky=W)


class FactCreation:
    
    def __init__(self, factDisplay):
        """
        Allows the user to create a new fact in the knowledge base, giving it a name and a description
        """
        
        self.factDisplay = factDisplay
        
        # The creation form will be in a new window
        self.new_fact_root = Toplevel()
        self.new_fact_root.title("Création d'un nouveau fait")
        
        Label(self.new_fact_root, text="Name :").grid(row=0, pady=("0.5c", 0), padx=("0.5c", 0), sticky=E)
        self.name = Entry(self.new_fact_root)
        self.name.grid(row=0, column=1, pady=("0.5c", 0), sticky=W)
        Label(self.new_fact_root, text="Description :").grid(row=1, sticky=E)
        self.description = Entry(self.new_fact_root, width=60)
        self.description.grid(row=1, column=1, padx=(0, "0.5c"), sticky=W)
        
        Button(self.new_fact_root, text="Créer", command=self.validate, overrelief="groove", cursor="hand2") \
            .grid(row=2, columnspan=2, padx="0.5c", pady=("1c", "0.5c"))
    
    def validate(self):
        """
        This function is called when the button "creer" is pressed. It adds the new fact to the knowledge base and
        call the update function to display the new fact with the others
        """
        self.factDisplay.facts.append(Fact(self.name.get(), self.description.get()))
        self.new_fact_root.destroy()
        User_interface.Main_menu.update(self.factDisplay.root, self.factDisplay.facts,
                                        self.factDisplay.rules, self.factDisplay.rules_fuzzy,
                                        self.factDisplay.fuzzy_sets)


class FactItem:
    
    def __init__(self, factDisplay, position):
        """
        Displays a fact in the root window and provides a button to delete it
        Args:
            factDisplay (FactDisplay): parent
            position (int): position of the fact to display
        """
        self.factDisplay = factDisplay
        self.position = position
        
        Label(self.factDisplay.o_facts, text=self.factDisplay.facts[self.position].name, width=20, anchor="w") \
            .grid(row=self.position + 1, padx=("0.2c", 0), sticky=W)
        
        Label(self.factDisplay.o_facts, text=self.factDisplay.facts[self.position].description, width=70, anchor="w") \
            .grid(row=self.position + 1, column=1, sticky=W)
        
        Button(self.factDisplay.o_facts, text="✘", borderwidth=0, command=self.delete_pressed, cursor="hand2",
               font=("Arial", 16)) \
            .grid(row=self.position + 1, column=2, sticky=W, padx=(0, "0.5c"))
    
    def delete_pressed(self):
        """
        Deletes the fact when the delete button is pressed
        """
        self.factDisplay.facts.pop(self.position)
        User_interface.Main_menu.update(self.factDisplay.root, self.factDisplay.facts,
                                        self.factDisplay.rules, self.factDisplay.rules_fuzzy,
                                        self.factDisplay.fuzzy_sets)
