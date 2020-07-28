import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from Forward.Inference_engine_forward import *
from Backward.Inference_engine import *
from Fuzzy.Inference_engine import *
from Knowledge_base_fuzzy.Fuzzy_set import Fuzzy_set
from Knowledge_base_fuzzy.Facts_Fuzzy import Fact_Fuzzy
from Knowledge_base_fuzzy.Rules_Fuzzy import Rule_Fuzzy


class RunDisplay:
    
    def __init__(self, facts, rules, rules_fuzzy, fuzzy_sets, o_run, root):
        """
        This function display a menu constituted of different buttons in order to execute a certain kind of expert systems
        Args:
            facts (list[Fact]): list of facts in the knowledge base
            rules (list[Rule]): list of rules in the knowledge base
            rules_fuzzy (list[Rule_Fuzzy]): list of rules in the knowledge base for the fuzzy algorithm
            fuzzy_sets (list[Fuzzy_Set]): list of fuzzy sets in the knowledge base for the fuzzy algorithm
            o_run (ttk.frame): tab of the runs
            root (Tk): root window of the user interface
        """
        self.facts = facts
        self.rules = rules
        self.rules_fuzzy = rules_fuzzy
        self.fuzzy_sets = fuzzy_sets
        self.o_run = o_run
        self.root = root
        
        Button(self.o_run, text=" Run Forward Chaining ", command=lambda: RunForward(self), fg="green", padx="0.5c",
               pady="0.2c",
               overrelief="groove", cursor="hand2") \
            .grid(padx="1c", pady=("1c", "0.5c"))
        Button(self.o_run, text=" Run Backward Chaining ", command=lambda: RunBackward(self), fg="green", padx="0.5c",
               pady="0.2c", overrelief="groove", cursor="hand2") \
            .grid(padx="1c", pady="0.5c", row=1)
        Button(self.o_run, text=" Run Fuzzy System Expert ", command=lambda: RunFuzzy(self), fg="green", padx="0.5c",
               pady="0.2c", overrelief="groove", cursor="hand2") \
            .grid(padx="1c", pady="0.5c", row=2)


class RunForward:
    
    def __init__(self, runDisplay):
        """
        Allows to run an expert system in forward chaining. The user can choose the known fact to get all the results
        """
        
        self.runDisplay = runDisplay
        
        self.forward_root = Toplevel()
        
        # The user can choose among the already known facts
        Label(self.forward_root, text="Faits connus :").grid(row=0, column=2, sticky=E)
        
        self.var_goal = IntVar()
        self.var_goal.set(1)
        self.var_known = [IntVar() for _ in range(len(self.runDisplay.facts))]
        for i in range(len(self.runDisplay.facts)):
            Radiobutton(self.forward_root, text=self.runDisplay.facts[i].name, variable=self.var_goal, value=i + 1,
                        cursor="hand2") \
                .grid(row=i, column=1, sticky=W)
            Checkbutton(self.forward_root, text=self.runDisplay.facts[i].name, variable=self.var_known[i],
                        cursor="hand2") \
                .grid(row=i, column=3, sticky=W)
        
        # The user can also choose which rules should be used (all are selected by default)
        Label(self.forward_root, text="Règles à utiliser :").grid(row=0, column=4, sticky=E)
        
        self.var_rules = [IntVar(value=1) for _ in range(len(self.runDisplay.rules))]
        for j in range(len(self.runDisplay.rules)):
            Checkbutton(self.forward_root, text=self.runDisplay.rules[j].description, variable=self.var_rules[j],
                        cursor="hand2") \
                .grid(row=j, column=5, sticky=W)
        
        Button(self.forward_root, text="  Execute  ", command=self.forward_execution, overrelief="groove",
               cursor="hand2") \
            .grid(row=len(self.runDisplay.rules) + len(self.runDisplay.facts), pady="0.5c", columnspan=6)
        
        def forward_execution(self):
            """
            This function is called when the button "execute" is pressed. It calls the forward function to run the
            inference engine
            """
            # We recover the known facts chose by the user...
            known = []
            for i in range(len(self.runDisplay.facts)):
                if self.var_known[i].get() == 1:
                    known.append(self.runDisplay.facts[i])
            
            # ... and the rules that the inference engine can use
            rules = []
            for j in range(len(self.runDisplay.rules)):
                if self.var_rules[j].get() == 1:
                    rules.append(self.runDisplay.rules[j])
            
            # We get all the facts
            Facts = []
            for k in range(len(self.runDisplay.facts)):
                Facts.append(self.runDisplay.facts[k])
            
            # We destroy the launch window and call the inference engine
            self.forward_root.destroy()
            forward_display(known, rules, Facts)
        
        pass


class RunBackward:
    
    def __init__(self, runDisplay):
        """
        Allows to run an expert system in backward chaining. The user can choose the fact to test and the already known facts.
        """
        
        self.runDisplay = runDisplay
        
        self.backward_root = Toplevel()
        
        # The user can chose among the existing facts one (and only one) fact to test, and the already known facts
        Label(self.backward_root, text="Fait à tester :").grid(padx=("0.2c", 0), sticky="E")
        Label(self.backward_root, text="Faits connus :").grid(row=0, column=2, sticky="E")
        
        self.var_goal = IntVar()
        self.var_goal.set(1)
        self.var_known = [IntVar() for _ in range(len(self.runDisplay.facts))]
        for i in range(len(self.runDisplay.facts)):
            Radiobutton(self.backward_root, text=self.runDisplay.facts[i].name, variable=self.var_goal, value=i + 1,
                        cursor="hand2") \
                .grid(row=i, column=1, sticky=W)
            Checkbutton(self.backward_root, text=self.runDisplay.facts[i].name, variable=self.var_known[i],
                        cursor="hand2") \
                .grid(row=i, column=3, sticky=W)
        
        # The user can also choose which rules should be used (all are selected by default)
        Label(self.backward_root, text="Règles à utiliser :").grid(row=0, column=4, sticky="E")
        
        self.var_rules = [IntVar(value=1) for _ in range(len(self.runDisplay.rules))]
        for j in range(len(self.runDisplay.rules)):
            Checkbutton(self.backward_root, text=self.runDisplay.rules[j].description, variable=self.var_rules[j],
                        cursor="hand2") \
                .grid(row=j, column=5, sticky="W")
        
        Button(self.backward_root, text="  Execute  ", command=self.backward_execution, overrelief="groove",
               cursor="hand2") \
            .grid(row=len(self.runDisplay.rules) + len(self.runDisplay.facts), pady="0.5c", columnspan=6)
    
    def backward_execution(self):
        """
        This function is called when the button "execute" is pressed. It calls the backward function to run the
        inference engine
        """
        
        # We recover the known facts chose by the user...
        known = []
        for i in range(len(self.runDisplay.facts)):
            if self.var_known[i].get() == 1:
                known.append(self.runDisplay.facts[i])
        
        # ... and the rules that the inference engine can use
        rules = []
        for j in range(len(self.runDisplay.rules)):
            if self.var_rules[j].get() == 1:
                rules.append(self.runDisplay.rules[j])
        
        # We destroy the launch window and call the inference engine
        self.backward_root.destroy()
        backward(known, rules, self.runDisplay.facts[self.var_goal.get() - 1])


class RunFuzzy:
    
    def __init__(self, runDisplay):
        """
        Allows to run an expert system in Fuzzy logic. The user can choose to set facts and their grades.
        """
        
        self.runDisplay = runDisplay
        
        self.fuzzy_root = Toplevel()
        
        fact_names = []
        for rule in self.runDisplay.rules_fuzzy:
            for fuzzy_set, hedge, fact_name in rule.conditions:
                if not fact_name in fact_names:
                    fact_names.append(fact_name)
        
        self.fact_names = fact_names
        
        # The user can chose the initial facts and their grades
        Label(self.fuzzy_root, text="Fait :").grid(padx=("0.2c", 0), sticky="e")
        
        self.fact_grade = [DoubleVar(value=0) for _ in range(len(fact_names))]
        for i in range(len(fact_names)):
            Label(self.fuzzy_root, text=fact_names[i]).grid(row=i, column=1, sticky=W)
            Entry(self.fuzzy_root, textvariable=self.fact_grade[i]).grid(row=i, column=2, sticky=W)
        
        # The user can also choose which rules should be used (all are selected by default)
        Label(self.fuzzy_root, text="Règles à utiliser :").grid(row=0, column=3, sticky="e")
        
        self.var_rules = [IntVar(value=1) for _ in range(len(self.runDisplay.rules_fuzzy))]
        for j in range(len(self.runDisplay.rules_fuzzy)):
            Checkbutton(self.fuzzy_root, text=self.runDisplay.rules_fuzzy[j].description, variable=self.var_rules[j],
                        cursor="hand2") \
                .grid(row=j, column=4, sticky=W)
        
        # The user can choose the defuzzification method
        Label(self.fuzzy_root, text="Méthode de défuzzification :").grid(row=0, column=5, sticky="e")
        
        self.defuzzification_method = StringVar(value="Centroid")
        OptionMenu(self.fuzzy_root, self.defuzzification_method, *defuzzification_methods).grid(row=0, column=6,
                                                                                                padx="0.3c")
        
        Button(self.fuzzy_root, text="  Execute  ", command=self.fuzzy_execution, overrelief="groove",
               cursor="hand2") \
            .grid(row=len(self.runDisplay.rules_fuzzy) + len(fact_names), pady="0.5c", columnspan=6)
    
    def fuzzy_execution(self):
        """
        This function is called when the button "execute" is pressed. It calls the fuzzy function to run the
        inference engine
        """
        
        # We recover the known facts chose by the user...
        facts = []
        for i in range(len(self.fact_names)):
            fact_name = self.fact_names[i]
            translated_fact = Fact_Fuzzy(fact_name, self.fact_grade[i].get(), "")
            facts.append(translated_fact)
        
        # ... and the rules that the inference engine can use
        rules = []
        for j in range(len(self.runDisplay.rules_fuzzy)):
            if self.var_rules[j].get() == 1:
                rules.append(self.runDisplay.rules_fuzzy[j])
        
        # We destroy the launch window and call the inference engine
        self.fuzzy_root.destroy()
        fuzzy(facts, rules, self.defuzzification_method.get())
