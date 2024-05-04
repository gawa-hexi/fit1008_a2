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
        # adds initial route
        to_search.push(self)
        # print("\n\n")
        # print('==='*30)

        # print(self)
        # print(type(to_search.is_empty()))
        # next_node=

        i= 0
        while to_search.is_empty() == False:
            current = to_search.pop().store

            # print('- - '*10)
            # print(f'i :  {i} \n')
            i +=1
            # print(f"\nProcessing: {type(current).__name__}")

            # print("Class RouteSeries:", id(RouteSplit))
            # print("Class current:", id(type(current)))


            # print("\nROUTE: ", current, "\n")

            # print(to_search)

            # print(type(current))


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
                # print(next)
                # print(f"\t traversing: {next}")

                # print(2)


            elif isinstance(current, type(None)) == False:
                next = current.store
            #
            # if isinstance(current, RouteStore):
            #     print(3)
            #     input()
            # print("RouteSplit defined:", 'RouteSplit' in globals())


            # virus_type.select_branch(self.store.top, self.store.bottom)


            # print("\nI!!!")
            # if type(current) == Route
#
            # next = current.store
            # print(isinstance(current, type(None)))
            if isinstance(current, type(None)) == False:
                # input(8)
                # return None
                # break
                to_search.push(next)
            # input()


        # Route.
        # if VirusType == BranchDecision.TOP:

         # class BranchDecision(Enum):
            # TOP = auto()
            # BOTTOM = auto()
            # STOP = auto()




        # raise NotImplementedError()

    def add_all_computers(self, computers=None) -> list[Computer]:
        """Returns a list of all computers on the route.

        Complexity: O(n), where n is the combined total number of branches & computers
        """

        if computers is None:
            computers = []

        current = self.store

        if isinstance(current, RouteSplit):
            print(f"\t@@@ RouteSplit found ...") #"\n\t branch: {virus_type.select_branch(current.top, current.bottom)}")
            current.top.add_all_computers(computers)
            current.bottom.add_all_computers(computers)
            current.following.add_all_computers(computers)

        elif isinstance(current, RouteSeries):
            print(f"\t@@@ RouteSeries found ...\n\tadding computer: {current.computer}")
            current.following.add_all_computers(computers)
            computers.append(current.computer)

        return computers

            # if next == BranchDecision.TOP:
            #     # input()
            #     next = current.top
            #
            # elif next is BranchDecision.BOTTOM:
            #     next = current.bottom
            # # print(next)
            # print(f"\t traversing: {next}")

            # print(2)

        #
        # elif isinstance(current, type(None)) == False:
        #     next = current.store



if __name__ == "__main__":

    from virus import *

    tw = TopVirus()
    bw = BottomVirus()
    top_top = Computer("top-top", 5, 3, 0.1)
    top_bot = Computer("top-bot", 3, 5, 0.2)
    top_mid = Computer("top-mid", 4, 7, 0.3)
    bot_one = Computer("bot-one", 2, 5, 0.4)
    bot_two = Computer("bot-two", 0, 0, 0.5)
    final   = Computer("final", 4, 4, 0.6)
    route = Route(RouteSplit(
        Route(RouteSplit(
            Route(RouteSeries(top_top, Route(None))),
            Route(RouteSeries(top_bot, Route(None))),
            Route(RouteSeries(top_mid, Route(None))),
        )),
        Route(RouteSeries(bot_one, Route(RouteSplit(
            Route(RouteSeries(bot_two, Route(None))),
            Route(None),
            Route(None),
        )))),
        Route(RouteSeries(final, Route(None)))
    ))


    route.follow_path(tw)
    route.follow_path(bw)


# if __name__ == "__main__":
#     # x = Route()
#     a, b, c, d = (Computer(letter, 5, 5, 1.0) for letter in "abcd")
#
#     empty = Route(None)
#
#     series_b = RouteSeries(b, Route(RouteSeries(d, Route(None))))
#
#     split = RouteSplit(
#         Route(series_b),
#         empty,
#         Route(RouteSeries(c, Route(None)))
#     )
#
#     t = Route(RouteSeries(
#         a,
#         Route(split)
#     ))
#
#
#     tw = TopVirus()
#     bw = BottomVirus()
#     lw = LazyVirus()
#
#     series_b = Route(series_b)
#
#     series_b.follow_path(tw)
#     print(tw.computers)
