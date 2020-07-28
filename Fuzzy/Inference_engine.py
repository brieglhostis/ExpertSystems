import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from Knowledge_base_fuzzy.Rules_Fuzzy import Rule_Fuzzy, hedges
import Fuzzy.Basic_functions as fbf
import matplotlib.pyplot as plt

defuzzification_methods = ["Centroid", "First maximum", "Mean maximum", "Last maximum", "Weighted centroid"]


def fuzzification_inference(bdf, bdr):
    """
	Cette fonction permet d'évaluer chaque règles en manipulant des graphes
	:param bdf: liste des faits qui sont connus (type list(Fact_Fuzzy))
	:param bdr: liste des règles à appliquer (type list(Rule_Fuzzy))
	:return: la liste des couples nom de fait / fonction résultante associée pour chaque fait résultant des règles
	"""
    result_functions = {}  # result_function est un dictionnaire qui à chaque nom de fait résultant des règles associe la fonction résultante de l'application des règles
    for rule in bdr:  # on applique chaque règle
        for fuzzy_set, hedge, fact_name in rule.conditions:  # chaque condition est sous la forme d'un triplet fuzzy_set qui définit la courbe à tester; d'un hedge qui modifie la courbe précédente; du nom du fait à utiliser dans la règle
            if fact_name in [f.name for f in
                             bdf]:  # on vérifie que le fait à utiliser est bien défini dans les faits initiaux
                fact = [f for f in bdf if f.name == fact_name][
                    0]  # on récupère le fait dans sont entièreté (nécessaire pour avoir son score associé)
                for result_fuzzy_set, hedge, result_fact_name in rule.results:  # chaque conclusion est sous la forme d'un triplet fuzzy_set qui définit la courbe à tester; d'un hedge qui modifie la courbe précédente; du nom du fait affecté par la règle
                    if result_fact_name not in result_functions:  # si le fait affecté par la règle n'a pas déjà été affecté auparavant, on l'introduit dans le dictionnaire result_functions
                        result_functions[result_fact_name] = []
                    result_functions[result_fact_name].append(fbf.min_function(
                        [fbf.constant_function(fuzzy_set.function(fact.value)),
                         result_fuzzy_set.function]))  # on ajoute la fonction résultante de la règle qui est la fonction du fuzzy set de la conclusion "coupée" à l'antécédant du score du fait initial pour la fonction du fuzzy set de la condition
    return [(name, result_functions[name]) for name in result_functions]


def defuzzification(result_functions, defuzzification_method):
    """
	Cette fonction permet de traduire la fonction d'évaluation des règles en un résultat.
	La méthode utilisée pour obtenir ce résultat, ainsi que la forme du résultat dépendent du cas d'application.
	:param result_function: la fonction résultante de l'inférence
	:param defuzzification_method: la méthode de defuzzification à utiliser
	:return: le résultat après défuzzification
	"""
    results = []
    if defuzzification_method == "Weighted centroid":  # le résultat est l'abscisse de la moyenne des centroid de chaque fonction résultante, dans ce cas, on a besoin de la liste entière des fonctions résultantes
        # the most commonly used because very efficient, BUT ONLY for symmetrical sets
        for fact_name, functions in result_functions:
            res = sum([fbf.centroid(fct) * fbf.val_max(fct) for fct in functions]) / sum(
                [fbf.val_max(fct) for fct in functions])
            results.append((fact_name, res))
    else:
        result_functions = [(name, fbf.max_function(functions)) for name, functions in
                            result_functions]  # dans les autres cas, on utilise la fonction maximun de toute les fonctions résultantes
        if defuzzification_method == "Centroid":  # le résultat est l'abscisse du centroid
            for fact_name, result_function in result_functions:
                results.append((fact_name, fbf.centroid(result_function)))
        elif defuzzification_method == "First maximum":  # le résultat est l'abscisse du premier maximum
            for fact_name, result_function in result_functions:
                results.append((fact_name, fbf.first_max(result_function)))
        elif defuzzification_method == "Mean maximum":  # le résultat est la moyenne des valeures en lesquelles le maximum est atteint
            for fact_name, result_function in result_functions:
                results.append((fact_name, fbf.mean_max(result_function)))
        elif defuzzification_method == "Last maximum":  # le résultat est l'abscisse du dernier maximum
            for fact_name, result_function in result_functions:
                results.append((fact_name, fbf.last_max(result_function)))
    
    return results


## Fuzzy

def fuzzy(bdf: list, bdr: list, defuzzification_method):
    """
	Cette fonction exécute l'algorithme entier mais cette version ne prend pas en entrée des règles en language naturel
	:param bdf: liste des faits qui sont connus (type list(Fact))
	:param bdr: liste des règles à appliquer(type list(Rule))
	:param defuzzification_method: la méthode de defuzzification à utiliser
	:return: le résultat après fuzzification
	"""
    f_res = fuzzification_inference(bdf, bdr)  # on applique les règles
    for name, result_functions in f_res:  # pour chaque fait résultant des règles ...
        function = fbf.max_function(
            result_functions)  # la fonction résultat est la fonction maximum des fonctions résultantes de l'application des règles
        x = [i / 100 for i in range(0, 101)]
        y = [function(xi) for xi in x]
        plt.plot(x, y)
        plt.suptitle(name)
        res = defuzzification([(name, result_functions)], defuzzification_method)[
            0]  # res est le résultat de la défuzzification
        plt.title(defuzzification_method + "'s abscissa : {}%".format(int(res[1] * 10000) / 100))
        plt.show()  # on affiche la focntion finale et le résultat
