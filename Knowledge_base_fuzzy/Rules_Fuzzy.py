import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from Knowledge_base_fuzzy.Fuzzy_set import Fuzzy_set

hedges = ["(no hedge)", "not", "a little", "slightly", "very", "extremely", "very very", "more or less", "somewhat",
          "indeed"]


class Rule_Fuzzy:
    
    def __init__(self, conditions: list, results: list, description: str):
        
        # Conditions
        self.conditions = []
        for condition in conditions:  # triplets Fuzzy_set - Hedge(str) - Fact.name
            fuzzy_set, hedge, fact_name = condition
            if hedge == "None" or hedge == "(no hedge)":
                f = fuzzy_set.function
            elif hedge == "not":
                def f(x):
                    return 1 - fuzzy_set.function(x)
            elif hedge == "a little":
                def f(x):
                    return fuzzy_set.function(x) ** 1.3
            elif hedge == "slightly":
                def f(x):
                    return fuzzy_set.function(x) ** 1.7
            elif hedge == "very":
                def f(x):
                    return fuzzy_set.function(x) ** 2
            elif hedge == "extremely":
                def f(x):
                    return fuzzy_set.function(x) ** 3
            elif hedge == "very very":
                def f(x):
                    return fuzzy_set.function(x) ** 4
            elif hedge == "more or less" or hedge == "somewhat":
                def f(x):
                    return fuzzy_set.function(x) ** 0.5
            elif hedge == "indeed":
                def f(x):
                    fx = fuzzy_set.function(x)
                    if fx <= 0.5 and fx >= 0:
                        return 2 * (fx ** 2)
                    elif fx > 0.5 and fx <= 1:
                        return 1 - 2 * ((1 - fx) ** 2)
            new_fuzzy_set = Fuzzy_set(fuzzy_set.name, fuzzy_set.description, f)
            self.conditions.append((new_fuzzy_set, hedge,
                                    fact_name))  # chaque condition est sous la forme d'un triplet fuzzy_set qui définit la courbe à tester; d'un hedge qui modifie la courbe précédente; du nom du fait à utiliser dans la règle
        
        # Results
        self.results = []
        for result in results:  # triplets Fuzzy_set - Hedge(str) - Fact.name
            fuzzy_set, hedge, fact_name = result
            if hedge == "None" or hedge == "(no hedge)":
                f = fuzzy_set.function
            elif hedge == "not":
                def f(x):
                    return 1 - fuzzy_set.function(x)
            elif hedge == "a little":
                def f(x):
                    return fuzzy_set.function(x) ** (1 / 1.3)
            elif hedge == "slightly":
                def f(x):
                    return fuzzy_set.function(x) ** (1 / 1.7)
            elif hedge == "very":
                def f(x):
                    return fuzzy_set.function(x) ** 0.5
            elif hedge == "extremely":
                def f(x):
                    return fuzzy_set.function(x) ** (1 / 3)
            elif hedge == "very very":
                def f(x):
                    return fuzzy_set.function(x) ** 0.25
            elif hedge == "more or less" or hedge == "somewhat":
                def f(x):
                    return fuzzy_set.function(x) ** 2
            elif hedge == "indeed":
                def f(x):
                    fx = fuzzy_set.function(x)
                    if fx <= 0.5 and fx >= 0:
                        return 2 * (fx ** 0.5)
                    elif fx > 0.5 and fx <= 1:
                        return 1 - 2 * ((1 - fx) ** 0.5)
            new_fuzzy_set = Fuzzy_set(fuzzy_set.name, fuzzy_set.description, f)
            self.results.append((new_fuzzy_set, hedge,
                                 fact_name))  # chaque conclusion est sous la forme d'un triplet fuzzy_set qui définit la courbe à tester; d'un hedge qui modifie la courbe précédente; du nom du fait affecté par la règle
        
        if description == "default description":
            self.description = "IF " + " AND ".join(
                [fact_name + " IS/ARE " + hedge + " " + fuzzy_set.name for fuzzy_set, hedge, fact_name in
                 conditions]) + " THEN " + " AND ".join(
                [fact_name + " IS/ARE " + hedge + " " + fuzzy_set.name for fuzzy_set, hedge, fact_name in results])
        else:
            self.description = description
