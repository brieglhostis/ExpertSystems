from scipy import exp


class Fuzzy_set:
    
    def __init__(self, name: str, description: str, function):
        self.name = name
        self.description = description
        self.function = function


# Suivent les fonctions les plus utilisées pour les fuzzy set
def trapeze(a, b, c, d):
    """
    Cette fonction renvoie la fonction d'un trapèze
    :param a: abscisse du début de la pente ascendante
    :param a: abscisse de la fin de la pente ascendante
    :param a: abscisse du début de la pente descendante
    :param a: abscisse du la fin de la pente descendante
    """
    
    def f(x):
        if x < a:
            return 0
        elif x < b:
            return (x - a) / (b - a)
        elif x < c:
            return 1
        elif x < d:
            return (x - d) / (c - d)
        else:
            return 0
    
    return f


def triangle(moyenne, ecart_type):
    """
    Cette fonction renvoie la fonction d'un triangle
    :param moyenne: moyenne du triangle
    :param ecart_type: écart-type du triangle
    """
    
    def f(x):
        if (moyenne - ecart_type / 2) < x and x <= moyenne:
            return (x - (moyenne - ecart_type / 2)) / (ecart_type / 2)
        elif (moyenne + ecart_type / 2) >= x and x > moyenne:
            return -(x - (moyenne + ecart_type / 2)) / (ecart_type / 2)
        else:
            return 0
    
    return f


def gaussienne(moyenne, ecart_type):
    """
    Cette fonction renvoie la fonction d'une gaussienne
    :param moyenne: moyenne de la gaussienne
    :param ecart_type: écart-type de la gaussienne
    """
    
    def f(x):
        return exp(-((x - moyenne) / ecart_type) ** 2)
    
    return f
