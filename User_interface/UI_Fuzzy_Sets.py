import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from Knowledge_base_fuzzy.Fuzzy_set import *
import User_interface

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FuzzySetsDisplay:
    
    def __init__(self, facts, rules, rules_fuzzy, fuzzy_sets, o_fuzzy_sets, root):
        """
        Displays the fuzzy sets in the knowledge base listing the name, a graph of the function and a description
        Args:
            facts (list[Fact]): list of facts in the knowledge base
            rules (list[Rule]): list of rules in the knowledge base
            rules_fuzzy (list[Rule_Fuzzy]): list of rules in the knowledge base for the fuzzy algorithm
            fuzzy_sets (list[Fuzzy_Set]): list of fuzzy sets in the knowledge base for the fuzzy algorithm
            o_fuzzy_sets (ttk.frame): tab of the rules
            root (Tk): root window of the user interface
        """
        self.facts = facts
        self.rules = rules
        self.rules_fuzzy = rules_fuzzy
        self.o_fuzzy_sets = o_fuzzy_sets
        self.fuzzy_sets = fuzzy_sets
        self.root = root
        
        Label(self.o_fuzzy_sets, text="Name").grid(row=0, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        Label(self.o_fuzzy_sets, text="Fonction").grid(row=0, column=1, padx=("1c", 0), pady=("0.2c", "0.5c"), sticky=W)
        Label(self.o_fuzzy_sets, text="Description").grid(row=0, column=2, padx=("1c", 0), pady=("0.2c", "0.5c"),
                                                          sticky=W)
        
        # For each fuzzy set, we display its name, its function and its description
        for i in range(len(self.fuzzy_sets)):
            FuzzySetItem(self, i)
        
        # This button allows the creation of a new fuzzy set in the knowledge base
        Button(self.o_fuzzy_sets, text="Créer un nouveau fuzzy set", command=lambda: FuzzySetCreation(self),
               padx="0.5c", pady="0.2c",
               overrelief="groove", cursor="hand2") \
            .grid(row=len(self.fuzzy_sets) + 2, columnspan=2, padx=("0.5c", 0), pady=("1c", "0.5c"), sticky=W)


class FuzzySetCreation:
    
    def __init__(self, fuzzySetDisplay):
        """
        Allows the user to create a new fuzzy set in the knowledge base, giving it a name and a description
        """
        
        self.fuzzySetDisplay = fuzzySetDisplay
        
        # The creation form will be in a new window
        self.new_fuzzy_set_root = Toplevel()
        self.new_fuzzy_set_root.title("Création d'un nouveau fait")
        
        Label(self.new_fuzzy_set_root, text="Name :").grid(row=0, pady=("0.5c", 0), padx=("0.5c", 0), sticky="E")
        self.name = Entry(self.new_fuzzy_set_root)
        self.name.grid(row=0, column=1, pady=("0.5c", 0), sticky=W)
        
        # The user can chose among the existing functions one (and only one) function for the new fuzzy set
        Label(self.new_fuzzy_set_root, text="Fonction :").grid(row=0, column=2, pady=("0.5c", 0), padx=("0.5c", 0),
                                                               sticky=E)
        
        self.var_function_type = IntVar(value=1)
        self.var_function_caracteristics = [
            [StringVar(value="0"), StringVar(value="0"), StringVar(value="0"), StringVar(value="0")],
            [StringVar(value="0"), StringVar(value="0")]]
        
        # Form for a trapeze
        Radiobutton(self.new_fuzzy_set_root, text="trapèze", variable=self.var_function_type, value=1,
                    cursor="hand2") \
            .grid(row=0, column=3, pady=("0.5c", 0), sticky=W)
        Label(self.new_fuzzy_set_root, text="Début de montée :").grid(row=0, column=5, pady=("0.5c", 0), sticky="E")
        Entry(self.new_fuzzy_set_root, textvariable=self.var_function_caracteristics[0][0]).grid(row=0, column=6,
                                                                                                 pady=("0.5c", 0),
                                                                                                 sticky="W")
        Label(self.new_fuzzy_set_root, text="Fin de montée:").grid(row=0, column=7, pady=("0.5c", 0), sticky="E")
        Entry(self.new_fuzzy_set_root, textvariable=self.var_function_caracteristics[0][1]).grid(row=0, column=8,
                                                                                                 pady=("0.5c", 0),
                                                                                                 sticky="W")
        Label(self.new_fuzzy_set_root, text="Début de descente :").grid(row=1, column=5, pady=("0.5c", 0), sticky="E")
        Entry(self.new_fuzzy_set_root, textvariable=self.var_function_caracteristics[0][2]).grid(row=1, column=6,
                                                                                                 pady=("0.5c", 0),
                                                                                                 sticky="W")
        Label(self.new_fuzzy_set_root, text="Fin de descente :").grid(row=1, column=7, pady=("0.5c", 0), sticky="E")
        Entry(self.new_fuzzy_set_root, textvariable=self.var_function_caracteristics[0][3]).grid(row=1, column=8,
                                                                                                 pady=("0.5c", 0),
                                                                                                 sticky="W")
        
        # Form for a gaussian function
        Radiobutton(self.new_fuzzy_set_root, text="gaussienne", variable=self.var_function_type, value=2,
                    cursor="hand2") \
            .grid(row=2, column=3, pady=("0.5c", 0), sticky=W)
        Label(self.new_fuzzy_set_root, text="Moyenne :").grid(row=2, column=5, pady=("0.5c", 0), sticky="E")
        Entry(self.new_fuzzy_set_root, textvariable=self.var_function_caracteristics[1][0]).grid(row=2, column=6,
                                                                                                 pady=("0.5c", 0),
                                                                                                 sticky="W")
        Label(self.new_fuzzy_set_root, text="Ecart Type :").grid(row=2, column=7, pady=("0.5c", 0), sticky="E")
        Entry(self.new_fuzzy_set_root, textvariable=self.var_function_caracteristics[1][1]).grid(row=2, column=8,
                                                                                                 pady=("0.5c", 0),
                                                                                                 sticky="W")
        
        # A field allows to write a description for the fuzzy set
        Label(self.new_fuzzy_set_root, text="Description :").grid(row=3, column=0, sticky=E, pady=("0.5c", 0),
                                                                  padx=("0.5c", 0))
        self.description = Entry(self.new_fuzzy_set_root, width=60)
        self.description.grid(row=3, column=1, columnspan=3, pady="0.5c",
                              padx=(0, "0.5c"), sticky=W)
        
        Button(self.new_fuzzy_set_root, text="Créer", command=self.validate, overrelief="groove", cursor="hand2") \
            .grid(row=4, columnspan=2, padx="0.5c", pady=("1c", "0.5c"))
    
    def validate(self):
        """
        This function is called when the button "creer" is pressed. It adds the new fuzzy set to the knowledge base and
        calls the update function to display the new fuzzy set with the others
        """
        
        # Now we must transform the caracteristic values of the functions into floats
        for i in range(len(self.var_function_caracteristics)):
            for j in range(len(self.var_function_caracteristics[i])):
                self.var_function_caracteristics[i][j] = float(self.var_function_caracteristics[i][j].get())
        
        if self.var_function_type.get() == 1:
            [a, b, c, d] = self.var_function_caracteristics[0]
            function = trapeze(a, b, c, d)
        else:
            [mu, sigma] = self.var_function_caracteristics[1]
            function = gaussienne(mu, sigma)
        self.fuzzySetDisplay.fuzzy_sets.append(Fuzzy_set(self.name.get(), self.description.get(), function))
        self.new_fuzzy_set_root.destroy()
        User_interface.Main_menu.update(self.fuzzySetDisplay.root, self.fuzzySetDisplay.facts,
                                        self.fuzzySetDisplay.rules, self.fuzzySetDisplay.rules_fuzzy,
                                        self.fuzzySetDisplay.fuzzy_sets)


class FuzzySetItem:
    
    def __init__(self, fuzzySetDisplay, position):
        """
        Displays a fuzzy set in the root window
        Args:
            fuzzySetDisplay (FuzzySetsDisplay): parent
            position (int): position of the fuzzy set to display
        """
        self.fuzzySetDisplay = fuzzySetDisplay
        self.position = position
        
        Label(self.fuzzySetDisplay.o_fuzzy_sets, text=self.fuzzySetDisplay.fuzzy_sets[self.position].name, width=20,
              anchor="w") \
            .grid(row=self.position + 1, padx=("0.5c", 0), sticky=W)
        
        f = Figure(figsize=(0.5, 0.5), dpi=100)
        a = f.add_subplot(111)
        x = [t / 30 for t in range(0, 31)]
        a.plot(x, [self.fuzzySetDisplay.fuzzy_sets[self.position].function(t) for t in x])
        a.axis('off')
        
        canvas = FigureCanvasTkAgg(f, self.fuzzySetDisplay.o_fuzzy_sets)
        canvas.get_tk_widget().grid(row=self.position + 1, column=1)
        
        Label(self.fuzzySetDisplay.o_fuzzy_sets, text=self.fuzzySetDisplay.fuzzy_sets[self.position].description,
              width=70, anchor="w") \
            .grid(row=self.position + 1, column=2, padx=("0.2c", 0), sticky=W)
        
        Button(self.fuzzySetDisplay.o_fuzzy_sets, text="✘", borderwidth=0, command=self.delete_pressed, cursor="hand2",
               font=("Arial", 16)) \
            .grid(row=self.position + 1, column=3, sticky=W, padx=(0, "0.5c"))
    
    def delete_pressed(self):
        """
        Deletes the fuzzy set when the delete button is pressed
        """
        self.fuzzySetDisplay.fuzzy_sets.pop(self.position)
        User_interface.Main_menu.update(self.fuzzySetDisplay.root, self.fuzzySetDisplay.facts,
                                        self.fuzzySetDisplay.rules, self.fuzzySetDisplay.rules_fuzzy,
                                        self.fuzzySetDisplay.fuzzy_sets)
