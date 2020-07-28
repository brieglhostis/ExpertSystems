import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule


def deduction(current_facts: list, rules: list):
    """
    Update the current_facts list according to the rules we have
    """
    
    for rule in rules:
        ok = True
        for condition in rule.conditions:
            if condition not in current_facts:
                ok = False
                break
        if ok:
            for conclusion in rule.conclusions:
                current_facts.append(conclusion)
    return current_facts


def add_fact(current_facts: list, new_fact: Fact, rules: list):
    """
    Add a new fact to the current list of facts and update it
    """
    
    new_facts = current_facts + [new_fact]
    return deduction(new_facts, rules)


def remove_fact(current_facts: list, old_fact: Fact, rules: list):
    """
    Remove a fact from the current list of facts and update it
    """
    new_facts = current_facts.copy()
    new_facts.remove(old_fact)
    
    for rule in rules:
        if old_fact in rule.conditions:
            for conclusion in rule.conclusions:
                new_facts.remove(conclusion)
        elif old_fact in rule.conclusions:
            if len(rule.conditions) == 1:
                new_facts.remove(rule.conditions[0])
            else:
                for condition in rule.conditions:
                    if condition in new_facts:
                        print("Indécidable")
    
    return deduction(new_facts, rules)
