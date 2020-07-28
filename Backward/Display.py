import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule
from Backward.Explanation_tree import *


def ask_about_fact(fact: Fact):
    """
    Asks the user about whether a fact is true or false threw an interface provided by tkinter
    Args:
        fact (Fact): the fact we want to know about

    Returns:
        bool: true if the fact is true, false otherwise
    """
    
    window = Tk()
    window.title("Question !")
    
    Label(window, text=fact.description, font=("Arial", 18)).grid(padx="1c", pady=("0.5c", "1c"), columnspan=3)
    
    def fact_is_true():
        global boolean
        boolean = True
        window.quit()
        window.destroy()
    
    def fact_not_true():
        global boolean
        boolean = False
        window.quit()
        window.destroy()
    
    Button(window, text="Vrai", fg="green", command=fact_is_true, width="15") \
        .grid(column=0, row=1, padx="0.5c", pady="0.5c")
    
    Button(window, text="Ne sais pas", fg="black", command=fact_not_true, width="15") \
        .grid(column=1, row=1, padx="0.5c", pady="0.5c")
    
    Button(window, text="Faux", fg="red", command=fact_not_true, width="15") \
        .grid(column=2, row=1, padx="0.5c", pady="0.5c")
    
    window.mainloop()
    
    try:
        return boolean
    except NameError:
        return False


def show_result(goal: Fact, description: str, true_fact: bool, facts: list, used_rules: list):
    """
    Displays the result of the inference engine and the explanation of the facts and rules used to reach this conclusion
    Args:
        goal (Fact): the fact understudy
        description (String): the explanation of the rules and facts used
        true_fact (bool): is True if the goal is verified, False otherwise
        facts (list[fact]): list of the known facts
        used_rules (list[Rule]): list of the rules that have been used
    """
    root = Tk()
    root.title("Résultat !")
    
    if true_fact:
        Label(root, text=goal.description, font=("Arial", 18)) \
            .grid(padx="1c", pady="1c")
        
        Label(root, text="car {}".format(description), font=("Arial", 10)) \
            .grid(row=1, padx="1c", pady="1c")
    
    else:
        Label(root, text="Impossible à dire", font=("Arial", 18)) \
            .grid(padx="1c", pady="1c")
    
    display_explanation_tree(facts, used_rules, root)
    
    root.mainloop()
