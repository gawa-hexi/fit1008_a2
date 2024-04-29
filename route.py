from __future__ import annotations
from dataclasses import dataclass

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
        # print("self: ", self)
        # x = Route().add_computer_before(computer)
        # print("new: ", x)
        #
        # return x
        # return RouteSeries()

        following: Route = Route(RouteSeries(computer=self.computer, following=self.following))
        return RouteSeries(computer=computer, following=following)
        # raise NotImplementedError()




        # add_computer_before
        # raise NotImplementedError()

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """

        following: Route = Route(RouteSeries(computer=computer, following=self.following))
        return RouteSeries(computer=self.computer, following=following)



        raise NotImplementedError()

    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.
        """

        following: Route = Route(self)
        return RouteSplit(top=Route(), bottom=Route(), following=following)
        # raise NotImplementedError()

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """

        # new_branch = RouteSplit(top=Route(None), bottom=Route(None), following=Route(self))
        # # new_format = RouteSeries(computer=self.computer, following=new_branch)
        # new_format = RouteSeries(computer=self.computer, following=Route(new_branch))
        #
        # return new_format

        following: Route = Route(RouteSplit(top=Route(), bottom=Route(), following=self.following))
        return RouteSeries(computer = self.computer, following = following)
        # raise NotImplementedError()


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """

        return Route(RouteSeries(computer=computer, following=self))
        # return Route
        # raise NotImplementedError()

    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        return Route(RouteSplit(top=Route(), bottom=Route(), following=self))
        # raise NotImplementedError()

    def follow_path(self, virus_type: VirusType) -> None:
        """Follow a path and add computers according to a virus_type."""
        raise NotImplementedError()

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route."""
        raise NotImplementedError()
