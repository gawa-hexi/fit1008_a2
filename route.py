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
        # raise NotImplementedError()
        # return follow object, or empty computer?
        return self.following.store


    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """
        # Can make RouteSeries just return self, rather than typing all out again? Actually probs not
        new = RouteSeries(computer=computer, following=Route(store=self))
        # new = RouteSeries(computer=computer, following=RouteSeries(computer=self.computer), following=self.following.store)
        return new_route_series




    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """
        # adds new computer
        new = RouteSeries(computer=computer, following=self.following)
        # adds to old computer
        new_format = RouteSeries(computer=self.computer, following=Route(store=new))

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
        # creates new branch, with top & bottom as standard route object
        new_branch = RouteSplit(top=Route(None), bottom=Route(None), following=self)

        return new_branch

        # raise NotImplementedError()

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """
        new_branch = RouteSplit(top=Route(None), bottom=Route(None), following=self.following)
        # new_format = RouteSeries(computer=self.computer, following=new_branch)
        new_format = RouteSeries(computer=self.computer, following=Route(store=new_branch))

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
        return Route(store=RouteSeries(computer=computer, following=self.store))
        # raise NotImplementedError()

    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        # raise NotImplementedError()
        # top & bottom not None, as code expects Route object. Using empty Route objects keeps it consistent :))
        returns Route(store=RouteSplit(top=Route(store=None), bottom=Route(store=None), following=self.store))

    def follow_path(self, virus_type: VirusType) -> None:
        """Follow a path and add computers according to a virus_type."""
        raise NotImplementedError()

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route."""
        raise NotImplementedError()
