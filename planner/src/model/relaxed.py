from typing import List, Tuple, Optional

# Big integer number to be used, instead of float infinity
BIG_INT: int = (1 << 32) - 1


class Status:
    """
    Class defining statuses of relaxed facts
    """
    UNREACHED: int = 0  # Not explored or unable to be reached
    REACHED: int = 1  # Explored during some search
    GOAL_ZONE: int = 2  # Connected to other fact, which is connected to GOAL fact trough 0 cost action
    BEFORE_GOAL_ZONE: int = 3  # Not connected to fact, that can reach goal


class RelaxedFact:
    """
    Class representing fact in STRIPS language for delete relaxation,
    contains helper variables for H_max & LM-cut heuristics
    """
    def __init__(self, fact_id: Tuple[int, int]):
        """
        :param fact_id: of fact (var, value)
        """
        self.id: Tuple[int, int] = fact_id
        self.pre_of: List['RelaxedAction'] = []  # Actions which have this fact as pre-condition
        self.add_of: List['RelaxedAction'] = []  # Actions which have this fact as add-effect
        self.status: int = Status.UNREACHED  # Status of the fact
        self.distance: int = BIG_INT  # Heuristic value
        self.default_dist: int = BIG_INT  # Starting heuristic value (for H_max heuristic)

    def __str__(self) -> str:
        """
        :return: String representation of relaxed fact
        """
        return (
            f"RelaxedFact: {self.id}, status: {self.status}, distance: {self.distance}, " +
            f"pre_size: {len(self.pre_of)}, add_size: {len(self.add_of)}"
        )


def _is_before(a: RelaxedFact, b: RelaxedFact) -> bool:
    """
    :param a: first fact
    :param b: second fact
    :return: True if first fact is lexicographically before the second fact
    """
    return (a.id[0] < b.id[0]) or (a.id[0] == b.id[0] and a.id[1] < b.id[1])


class RelaxedAction:
    """
    Class representing action in STRIPS language for delete relaxation,
    contains helper variables for H_max & LM-cut heuristics
    """
    def __init__(self, identifier: int, cost: int):
        """
        :param identifier: id of the action
        :param cost: cost of the action
        """
        self.id: int = identifier
        self.pre: List[RelaxedFact] = []  # Array of RelaxedFacts (pre-conditions)
        self.add: List[RelaxedFact] = []  # Array of RelaxedFacts (add-effects)
        self.cost: int = cost  # Current cost of action (modified by LM-cut)
        # Heuristic helper variables
        self.counter: int = 0  # How many pre-conditions are unfulfilled
        self.pre_size: int = 0  # Number of pre-conditions
        # LM-cut vars
        self.h_max_cost: int = BIG_INT  # Cost of reaching this in h_max
        self.h_max_supporter: Optional[RelaxedFact] = None  # Best supported
        self.default_cost: int = cost  # Default cost of action

    def update_h_max_supporter(self) -> None:
        """
        Updates supporter for action by taking the highest value precondition and
        comparing it to the current one (uses lexicographical ordering in case of equality)

        :return: None
        """
        assert(self.counter == 0)
        # Argmax over preconditions of this action
        for fact in self.pre:
            # Better supporter
            if fact.distance > self.h_max_supporter.distance:
                self.h_max_supporter = fact
            # Lexicographical ordering (to guarantee uniqueness)
            elif fact.distance == self.h_max_supporter.distance and _is_before(fact, self.h_max_supporter):
                self.h_max_supporter = fact
        self.h_max_cost = self.h_max_supporter.distance

    def __str__(self) -> str:
        """
        :return: String representation of relaxed action
        """
        return f"RelaxedAction: {self.id}, cost: {self.cost}, counter: {self.counter}, supp: {self.h_max_supporter}"
