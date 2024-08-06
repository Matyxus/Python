from src.model import State, Problem, BIG_INT, Status, RelaxedFact, RelaxedAction
import heapq
from typing import List, Dict, Tuple


class Heuristic:
    """ Class serving as parent to all heuristics, provides utility methods """
    def __init__(self, task: Problem):
        """
        :param task: defined in STRIPS language
        """
        assert(task is not None and task.is_loaded())
        print(f"Initializing {self.__class__.__name__} heuristic")
        self.facts: Dict[Tuple[int, int], RelaxedFact] = {}
        self.actions: List[RelaxedAction] = []
        self.queue: List[Tuple[int, int, RelaxedFact]] = []
        self.tie_breaker: int = 0
        # Statistics
        self.calls: int = 0
        self.total_time: float = 0
        self.init_time: float = 0

    def evaluate(self, state: State) -> int:
        """
        :param state: current state
        :return: value of the given state, BIG_INT if no solution exists
        """
        raise NotImplementedError("Error, method 'evaluate' must be implemented by children of Heuristic class!")

    def init_vars(self, task: Problem) -> None:
        """
        :param task: defined in STRIPS language
        :return: None
        """
        raise NotImplementedError("Error, method 'init_vars' must be implemented by children of Heuristic class!")

    # ------------------------ Utils ------------------------

    def enqueue(self, fact: RelaxedFact, cost: int) -> None:
        """
        :param fact: to be added to min-queue
        :param cost: cost by which this fact was reached
        :return: None
        """
        assert(cost >= 0)
        # Enqueue only unexplored facts or those with better value
        if fact.status == Status.UNREACHED or fact.distance > cost:
            fact.status = Status.REACHED
            fact.distance = cost
            heapq.heappush(self.queue, (cost, self.tie_breaker, fact))
            self.tie_breaker += 1
        return

    def __call__(self, state: State) -> int:
        """
        :param state: current state
        :return: value of the given state
        """
        return self.evaluate(state)

