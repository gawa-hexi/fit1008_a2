from __future__ import annotations
from dataclasses import dataclass

from data_structures.linked_stack import *

from computer import Computer

from typing import TYPE_CHECKING, Union

from branch_decision import BranchDecision
# from virus import VirusType, TopVirus, BottomVirus, LazyVirus, RiskAverseVirus, FancyVirus

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType

# from virus import VirusType

@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """Removes the branch, should just leave the remaining following route."""

        return self.following.store



@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--

    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Removing the computer at the beginning of this series.
        """

        return self.following.store



    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """

        following: Route = Route(RouteSeries(computer=self.computer, following=self.following))
        return RouteSeries(computer=computer, following=following)


    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """

        following: Route = Route(RouteSeries(computer=computer, following=self.following))
        return RouteSeries(computer=self.computer, following=following)


    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.
        """

        following: Route = Route(self)
        return RouteSplit(top=Route(), bottom=Route(), following=following)


    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """

        following: Route = Route(RouteSplit(top=Route(), bottom=Route(), following=self.following))
        return RouteSeries(computer = self.computer, following = following)


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    store: RouteStore = None
    # computers: list[Computers] = []

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """

        return Route(RouteSeries(computer=computer, following=self))


    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        return Route(RouteSplit(top=Route(), bottom=Route(), following=self))



    def follow_path(self, virus_type: VirusType) -> None:
        """Follow a path and add computers according to a virus_type.

        E.G. select top

        For every RouteSplit, you should select either the top route or bottom route. After completing that Route, you need to visit the follow route (final in this case). Unfortunately, we can't tell you how to implement this.
        """

        to_search = LinkedStack()
        to_search.push(self)


        # i= 0
        while to_search.is_empty() == False:
            current = to_search.pop().store
            # i +=1


            if isinstance(current, RouteSeries):
                # print(f"\t@@@ RouteSeries found ...\n\tadding computer: {current.computer}")
                virus_type.add_computer(current.computer)
                next = current.following

            elif isinstance(current, RouteSplit):
                # print(f"\t@@@ RouteSplit found ...\n\t branch: {virus_type.select_branch(current.top, current.bottom)}")

                # input()
                next = virus_type.select_branch(current.top, current.bottom)
                to_search.push(current.following)


                if next == BranchDecision.TOP:
                    # input()
                    next = current.top

                elif next is BranchDecision.BOTTOM:
                    next = current.bottom
                elif next is BranchDecision.STOP:
                    break



            elif isinstance(current, type(None)) == False:
                next = current.store

            if isinstance(current, type(None)) == False:

                to_search.push(next)


    def add_all_computers(self, computers=None) -> list[Computer]:
        """Returns a list of all computers on the route.

        Complexity: O(n), where n is the combined total number of branches & computers
        """

        if computers is None:
            computers = []

        current = self.store


        if isinstance(current, RouteSplit):
            current.top.add_all_computers(computers)
            current.bottom.add_all_computers(computers)
            current.following.add_all_computers(computers)

        elif isinstance(current, RouteSeries):
            current.following.add_all_computers(computers)
            computers.append(current.computer)


        return computers
