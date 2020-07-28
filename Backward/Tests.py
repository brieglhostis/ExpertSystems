import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from Backward.Inference_engine import backward
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule
from Backward.Display import ask_about_fact
from User_interface.Main_menu import DisplayUI

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

# DisplayUI([A, B, C, D, E, F], [R1, R2, R3], [], [])
