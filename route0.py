from __future__ import annotations
from dataclasses import dataclass
from data_structures import referential_array

from computer import Computer

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType


@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/

series_b = RouteSeries(b, Route(RouteSeries(d, Route(None))))

series_b.remove_branch =
RouteSeries(
computer=c,
following=Route(store=None)
)

"""

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """Removes the branch, should just leave the remaining following route."""
        # raise NotImplementedError()
        # .store removes route wrapper(?); returns following item
        return self.following

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
        # raise NotImplementedError()
        # return follow object, or empty computer?
        return Route(self.following)


    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """
        # # Can make RouteSeries just return self, rather than typing all out again? Actually probs not
        # # new = RouteSeries(computer=computer, following=Route(self))
        #
        # # input(self.following)
        #
        old = RouteSeries(computer=self.computer, following=self.following)
        new = RouteSeries(computer=computer, following=Route(old))
        return new

        # return self.add_computer_before(computer)



    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """

        # input(self.following)
        print('\n\n\t@@@  RouteSeries.add_computer_after()  @@@')
        print("\tnew computer: ", computer)
        print("\tself.following: ", self.following)
        print("\tself.computer: ", self.computer)
        print("\tself: ", self)


        # adds new computer
        new = RouteSeries(computer=computer, following=Route(self.following))
        # adds to old computer
        new_format = RouteSeries(computer=self.computer, following=Route(new))

        print("\tnew RouteSeries: ", new_format)
        # input()
        return new_format


        # new = RouteSeries(computer=computer, following=RouteSeries(computer=None, following=Route(self)))
        # new_format = RouteSeries(computer=computer, following=self.following)
        # # adds the old computer
        # new_format = RouteSeries(computer=computer, following=Route(store=new_format))

        # raise NotImplementedError()





    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.
        """
        print('\n@@@ ADD EMPTY BRANCH BEFORE @@@\n')
        print("following.store: ", self.following)
        # creates new branch, with top & bottom as standard route object
        new_branch = RouteSplit(top=Route(None), bottom=Route(None), following=(self))

        # return Route(new_branch)
        return new_branch

        # return self.add_empty_branch_before()

        # raise NotImplementedError()

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """
        print('\n@@@ ADD EMPTY BRANCH BEFORE @@@\n')
        print("following.store: ", self.following)
        new_branch = RouteSplit(top=Route(None), bottom=Route(None), following=Route(self))
        # new_format = RouteSeries(computer=self.computer, following=new_branch)
        new_format = RouteSeries(computer=self.computer, following=Route(new_branch))

        return new_format








RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    # this variable is either a RouteSeries, RouteSplit or None
    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """

        print("\n\n\t@@@ ROUTE.add_computer_before @@@")
        print("\nself: ", self)
        print("\nself.store:", self.store)
        # return Route(store=RouteSeries(computer=computer, following=self.store))
        return Route(store=RouteSeries(computer=computer, following=self))

        # raise NotImplementedError()


    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        # print('\n\t@@@  Route.add_empty_branch_before()  @@@')
        # print("\tstore: ", self.store)
        # print("\tself: ", self)
        # input()
        # raise NotImplementedError()
        # top & bottom not None, as code expects Route object. Using empty Route objects keeps it consistent :))
        return Route(store=RouteSplit(top=Route(None), bottom=Route(), following=self))

    def follow_path(self, virus_type: VirusType) -> None:
        """Follow a path and add computers according to a virus_type."""
        raise NotImplementedError()

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route."""
        raise NotImplementedError()








if __name__=="__main__":

    from computer import Computer
    a, b, c, d = (Computer(letter, 5, 5, 1.0) for letter in "abcd")
    print(b)

    empty = Route(None)

    series_b = RouteSeries(b, Route(RouteSeries(d, Route(None))))

    split = RouteSplit(
        Route(series_b),
        empty,
        Route(RouteSeries(c, Route(None)))
    )

    t = Route(RouteSeries(
        a,
        Route(split)
        ))




    # res1 = series_b.add_empty_branch_after()
    # assertIsInstance(res1, RouteSeries)
    # assertEqual(res1.computer, b)
    # assertIsInstance(res1.following.store, RouteSplit)
    # assertEqual(res1.following.store.bottom.store, None)
    # assertEqual(res1.following.store.top.store, None)
    # assertIsInstance(res1.following.store.following.store, RouteSeries)
    # assertEqual(res1.following.store.following.store.computer, d)
    # assertEqual(res1.following.store.following.store.following.store, None)

    # res2 = split.remove_branch()
    # self.assertIsInstance(res2, RouteSeries)
    # self.assertEqual(res2.computer, c)
    # self.assertEqual(res2.following.store, None)
    #
    # res3 = empty.add_empty_branch_before()
    # self.assertIsInstance(res3, Route)
    # self.assertIsInstance(res3.store, RouteSplit)
    # self.assertEqual(res3.store.bottom.store, None)
    # self.assertEqual(res3.store.top.store, None)
    # self.assertEqual(res3.store.following.store, None)
