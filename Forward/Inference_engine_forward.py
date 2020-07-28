import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule
from Forward.display import *
from tkinter import *


def resolve_proposition(facts: list, rules: list, proposition: Fact):
    """
    This function allows to know whether a proposition is verified or not
    Args:
        facts (list[Fact]): list of the known facts
        rules (list[Rule]): list of the rules that can be used
        proposition (Fact): the fact we want to verify
    Returns:
        bool: true if the proposition is verified, false otherwise
    """
    
    # We immediately return True if the proposition is already known
    if proposition in facts:
        return True
    
    # Otherwise, we search for all the conclusions we can get with our facts and rules
    copy = facts.copy()
    for rule in rules:
        interet = False
        for conclusion in rule.conclusions:
            if conclusion not in facts:
                interet = True
                break
        if interet:
            ok = True
            for condition in rule.conditions:
                if condition not in facts:
                    ok = False
                    break
            if ok:
                for conclusion in rule.conclusions:
                    facts.append(conclusion)
    
    # Return False if the proposition is no verified
    if copy == facts:
        return False  # 此时不能得到任何新的结论，这时输出 on ne sait rien d'autre.
    
    # Return True if the proposition is verified, false otherwise
    return resolve_proposition(facts, rules, proposition)


def forward(facts: list, rules: list, Facts: list, explication: str):
    """
    This function calls the proposition_description on the data and display all the new conclusions we can get with our known facts and rules
    Args:
        facts (list[Fact]): list of the known facts
        rules (list[Rule]): list of the rules that can be used
        Facts (list[Fact]): list of all the facts
    Returns:
        list: all the new conclusions we can get with our known facts and rules
    """
    
    # Get the list of the new propositions that are not in the facts
    new_propositions = []
    for proposition in Facts:
        if proposition not in facts:
            new_propositions.append(proposition)
    
    # Get the list of the verified new proposition
    new_propositions_verified = []
    for new_proposition in new_propositions:
        if resolve_proposition(facts, rules, new_proposition):
            new_propositions_verified.append(new_proposition)
    
    # Display the new descriptions and the used rules if we have, False otherwise
    if new_propositions_verified != []:
        new_discription = []
        rules_used = []
        temporary_description = ""
        for proposition in new_propositions_verified:
            new_discription.append(proposition.description)
            for rule in rules:
                for conclusion in rule.conclusions:
                    if conclusion == proposition:
                        rule_condition = []
                        for condition in rule.conditions:
                            rule_condition.append(condition.description)
                        rules.remove(rule)
                        rules_used += [rule_condition]
                        explication += temporary_description + proposition.name + " : " + rule.description + ", donc " + proposition.description + "." + "\n"
        # print(new_description)
        # print(rules_used)
        return True, explication
    else:
        return False, "We can't get any new conclusion with our known facts and rules."


def forward_display(facts: list, rules: list, Facts: list):
    """
    This function calls the inference_engine_forward on the data and displays it by calling the show function
    Args:
        facts (list[Fact]): list of the known facts
        rules (list[Rule]): list of the rules that can be used
    """
    res, explication = forward(facts, rules, Facts, "")
    show_result_forward(explication, res)
