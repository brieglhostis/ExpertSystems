import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from tkinter import *
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule


def show_result_forward(description: str, true_fact: bool):
    """
    Displays the result of the inference engine and the explanation of the facts and rules used to reach this conclusion
    Args:
        description (String): the explanation of the rules and facts used
        true_fact (bool): is True if we can get the new conclusions with our know facts and rules, False otherwise
    """
    root = Tk()
    root.title("Résultat !")
    
    if true_fact:
        Label(root, text="car {}".format(description), font=("Arial", 10)) \
            .grid(row=1, padx="1c", pady="1c")
    
    else:
        Label(root, text="Impossible à dire", font=("Arial", 18)) \
            .grid(padx="1c", pady="1c")
    
    root.mainloop()
