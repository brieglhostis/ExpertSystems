import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from Backward.Inference_engine import backward
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule
from Backward.Display import ask_about_fact
from User_interface.Main_menu import DisplayUI
from Knowledge_base_fuzzy.Facts_Fuzzy import Fact_Fuzzy
from Knowledge_base_fuzzy.Rules_Fuzzy import Rule_Fuzzy
from Knowledge_base_fuzzy.Fuzzy_set import Fuzzy_set, trapeze, triangle, gaussienne

## Démo


FSC1 = Fuzzy_set("Poor", "Gaussienne centrée en 0 d'écart-type 0.35", gaussienne(0, 0.35))
FSC2 = Fuzzy_set("Good", "Gaussienne centrée en 0.5 d'écart-type 0.25", gaussienne(0.5, 0.25))
FSC3 = Fuzzy_set("Excellent", "Gaussienne centrée en 1 d'écart-type 0.35", gaussienne(1, 0.35))
FSC4 = Fuzzy_set("Rancid", "Pente descendante de 0.25 à 0.5", trapeze(0, 0, 0.25, 0.5))
FSC5 = Fuzzy_set("Delicious", "Pente  montante de 0.5 à 0.75", trapeze(0.5, 0.75, 1, 1.1))

FSR1 = Fuzzy_set("Cheap", "Triangle centré en 0.25 d'aire 0.25", triangle(0.25, 0.5))
FSR2 = Fuzzy_set("Average", "Triangle centré en 0.5 d'aire 0.25", triangle(0.5, 0.5))
FSR3 = Fuzzy_set("Generous", "Triangle centré en 0.75 d'aire 0.25", triangle(0.75, 0.5))

FSTrue = Fuzzy_set("True", "Fonction identité", trapeze(0, 1, 1, 1.1))

"""
A = Fact("Service", 0.35, "Service's assessment")
B = Fact("Food", 0.65, "Food's assessment")
"""
RF1 = Rule_Fuzzy([(FSC1, "(no hedge)", "Service")], [(FSR1, "(no hedge)", "Tip")], "default description")
RF2 = Rule_Fuzzy([(FSC2, "(no hedge)", "Service")], [(FSR2, "(no hedge)", "Tip")], "default description")
RF3 = Rule_Fuzzy([(FSC3, "(no hedge)", "Service")], [(FSR3, "(no hedge)", "Tip")], "default description")

RF4 = Rule_Fuzzy([(FSC4, "(no hedge)", "Food")], [(FSR1, "(no hedge)", "Tip")], "default description")
RF5 = Rule_Fuzzy([(FSC5, "(no hedge)", "Food")], [(FSR3, "(no hedge)", "Tip")], "default description")

A = Fact("Man", "Socrate est un homme")
B = Fact("Mortal", "Socrate est mortel")
C = Fact("Head", "Socrate a une tête")
D = Fact("Hands", "Socrate a des mains")
E = Fact("Hair", "Socrate a des cheveux")
F = Fact("Face", "Socrate a un visage")

R1 = Rule([A], [B], "Tous les hommes sont mortels")
R2 = Rule([C, D], [A], "Ce qui a une tête et des mains est humain")
R3 = Rule([E, F], [C], "Ce qui a des cheveux et un visage a une tête")

# backward([E, D],[R1, R2, R3],B)

DisplayUI([A, B, C, D, E, F], [R1, R2, R3], [RF1, RF2, RF3, RF4, RF5],
          [FSTrue, FSC1, FSC2, FSC3, FSC4, FSC5, FSR1, FSR2, FSR3])
