import sys

sys.path.append("..\\Pole_IA_Systemes_Experts")
from Knowledge_base.Facts import Fact
from Knowledge_base.Rules import Rule
from Backward.Display import *
from tkinter import *
from Backward.Explanation_tree import *


def resolve_goal(facts: list, rules: list, goal: Fact, description: str, used_rules: list):
    """
    This function allows to know whether a fact (the goal) is verified or not
    Args:
        facts (list[Fact]): list of the known facts
        rules (list[Rule]): list of the rules that can be used
        goal (Fact): the fact understudy
        description (string): current state of the explanation about which facts and rules were used
        used_rules (list[Rule]): list of the rules that have been used
    Returns:
        bool: true if the goal is verified, false otherwise
    """
    
    # We immediately return True if the goal is already known
    if goal in facts:
        description += goal.description
        return True
    
    # Otherwise, we look for the rules where the goal is in the conclusions, and we study whether its conditions are
    # verified or not
    for rule in rules:
        if goal in rule.conclusions:
            if rule not in used_rules:
                used_rules.append(rule)
            verified = True
            temporary_description = ""
            for condition in rule.conditions:
                if condition not in facts and verified:
                    res, description = resolve_goal(facts, rules, condition, description, used_rules)
                    if not res:
                        verified = False
                temporary_description += condition.description + " et "
            if verified:
                description += temporary_description + rule.description + " donc " + goal.description + "\n"
                facts.append(goal)
                return True, description
    
    # Ask the user if the goal is true or false
    if ask_about_fact(goal):
        facts.append(goal)
        return True, description
    else:
        return False, description


def backward(facts: list, rules: list, goal: Fact):
    """
    This function calls the inference_engine on the data and displays it by calling the show_result function
    Args:
        facts (list[Fact]): list of the known facts
        rules (list[Rule]): list of the rules that can be used
        goal (Fact): the fact understudy
	"""
    used_rules = []
    res, description = resolve_goal(facts, rules, goal, "", used_rules)
    show_result(goal, description, res, facts, used_rules)
