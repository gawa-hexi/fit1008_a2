from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from branch_decision import BranchDecision
from route import Route, RouteSeries, RouteSplit

from data_structures.linked_stack import LinkedStack



class VirusType(ABC):

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        self.computers.append(computer)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        raise NotImplementedError()


class TopVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the top branch
        return BranchDecision.TOP


class BottomVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the bottom branch
        return BranchDecision.BOTTOM


class LazyVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Try looking into the first computer on each branch,
        take the path of the least difficulty.
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                return BranchDecision.TOP
            elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP
        # If one of them has a computer, don't take it.
        # If neither do, then take the top branch.
        if top_route:
            return BranchDecision.BOTTOM
        return BranchDecision.TOP


class RiskAverseVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus is risk averse and likes to choose the path with the lowest risk factor.

        """
        top = top_branch.store
        bot = bottom_branch.store


        if isinstance(top, RouteSeries) and isinstance(bot, RouteSeries):
            top_com = top.computer
            bot_com = bot.computer

            """ [1.1] If 1 computer with risk factor of 0.0, take path. """
            if top_com.risk_factor == 0.0:
                if bot_com.risk_factor != 0.0:
                    return BranchDecision.TOP

                """ [1.1.1] multiple computers with risk_factor of 0.0?
                    take path with lowest hacking difficulty. """
                if top_com.hacking_difficulty > bot_com.hacking_difficulty:
                    return BranchDecision.BOTTOM
                elif bot_com.hacking_difficulty > top_com.hacking_difficulty:
                    return BranchDecision.TOP

                    """ If there is still a tie, continue to the next comparisons (-> 1.2)"""

            elif bot_com.risk_factor == 0.0:
                return BranchDecision.BOTTOM


            """ [1.2] Take highest value between the hacking_difficulty and 1/2 their hacked_value. """

            highest_top = top_com.hacking_difficulty
            if (top_com.hacked_value // 2) > highest_top:
                highest_top = top_com.hacked_value // 2
            highest_top = highest_top // top_com.risk_factor

            highest_bot = bot_com.hacking_difficulty
            if (bot_com.hacked_value // 2) > highest_bot:
                highest_bot = bot_com.hacked_value // 2
            highest_bot = highest_bot // bot_com.risk_factor

            """ [1.2]... Divide by risk factor. If the risk factor is zero, skip this step. """
            if (highest_bot != 0) and (highest_top != 0):
                if highest_bot > highest_top:
                    return BranchDecision.BOTTOM
                elif highest_bot < highest_top:
                    return BranchDecision.TOP


            """ [1.3] Take the path with the higher value."""
            if bot_com.hacked_value > top_com.hacked_value:
                return BranchDecision.BOTTOM
            elif bot_com.hacked_value < top_com.hacked_value:
                return BranchDecision.TOP

            else:
                """ [1.3.1] If there is a tie, take the path with the lower risk factor."""
                if bot_com.risk_factor < top_com.risk_factor:
                    return BranchDecision.BOTTOM
                elif bot_com.risk_factor > top_com.risk_factor:
                    return BranchDecision.TOP
                else:
                    """If there is still a tie, then STOP."""
                    return BranchDecision.STOP


            """ [2.1] If only one has a RouteSeries and the other a RouteSplit, pick the RouteSplit."""
        elif isinstance(top, RouteSeries):
            return BranchDecision.BOTTOM
        elif isinstance(bot, RouteSeries):
            return BranchDecision.TOP


            """ In all other cases default to the Top path. """
        return BranchDecision.TOP



class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus has a fancy-pants and likes to overcomplicate its approach.
        """

        top = top_branch.store
        bot = bottom_branch.store

        " [1.0] Evaluate the Polish Notation "

        terms = self.CALC_STR.split()
        stack = LinkedStack()

        for term in terms:
            if term in "+-*/":
                b = stack.pop()
                a = stack.pop()
                if term == '+':
                    stack.push(a + b)
                elif term == '-':
                    stack.push(a - b)
                elif term == '*':
                    stack.push(a * b)
                elif term == '/':
                    stack.push(a / b)
            else:
                stack.push(float(term))

        # print
        threshold = stack.pop()
        print(threshold)

        """ [2.0] If only one has a RouteSeries and the other a RouteSplit, pick the RouteSplit. """
        if isinstance(top, RouteSeries) and isinstance(bot, RouteSplit):
            return BranchDecision.BOTTOM
        elif isinstance(top, RouteSplit) and isinstance(bot, RouteSeries):
            return BranchDecision.TOP


        """ [3.0] If both top and bot are RouteSeries """

        """ [3.1] If top hacked_value < threshold, take top.
                   If bot hacked_value  > threshold, take bottom."""
        if isinstance(top, RouteSeries) and isinstance(bot, RouteSeries):
            if top.computer.hacked_value < threshold:
                return BranchDecision.TOP
            elif bot.computer.hacked_value > threshold:
                return BranchDecision.BOTTOM
            else:
                """ [3.2] If neither, then STOP. """
                return BranchDecision.STOP

        """ [4.0] In all other cases default to the Top path."""
        return BranchDecision.TOP
