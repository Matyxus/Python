from src.heuristics.heuristic import Heuristic, State, Problem, Status, RelaxedFact, RelaxedAction
import time
import heapq
from typing import Tuple, FrozenSet


class H_max(Heuristic):
    """
    Class for H_max heuristic, defines helper variables to speed up execution
    """
    def __init__(self, task: Problem):
        """
        :param task: defined in STRIPS language
        """
        super(H_max, self).__init__(task)
        # Problem related vars
        self.goals: FrozenSet[Tuple[int, int]] = task.goal_state.facts
        self.tie_breaker = 0
        self.goal_counter: int = len(self.goals)
        self.init_vars(task)

    def evaluate(self, state: State) -> int:
        self.calls += 1
        now: float = time.time()
        # print(f"Running Hmax heuristic on state: {state}")
        # ---------------- Init ----------------
        self.queue.clear()
        for fact in self.facts.values():
            fact.status = Status.UNREACHED
            fact.distance = fact.default_dist
        for action in self.actions:
            action.counter = action.pre_size
        # Push facts of starting state
        self.tie_breaker = 0
        for fact in state.facts:
            self.enqueue(self.facts[fact], 0)
        self.init_time += (time.time() - now)
        # Search trough facts till goal is reach (or all facts are used)
        self.search()
        self.total_time += (time.time() - now)
        return max([self.facts[fact].distance for fact in self.goals])

    def search(self) -> None:
        """
        Performs the h_max heuristic search on initial facts

        :return: None
        """
        achieved_goals: int = 0
        while achieved_goals != self.goal_counter and self.queue:
            v, _, fact = heapq.heappop(self.queue)
            # Check whether we already visited this fact
            if fact.distance < v:
                continue
            elif fact.id in self.goals:
                achieved_goals += 1
            # Iterate over all operators this fact is a precondition of
            for action in fact.pre_of:
                action.counter -= 1
                # Action can be used to update values, all pre-condition fulfilled
                if action.counter == 0:
                    value = action.cost + v
                    for neighbor in action.add:
                        self.enqueue(neighbor, value)
        return

    # ---------------------------------- Utils ----------------------------------

    def init_vars(self, task: Problem) -> None:
        # Create relaxed facts for all facts in the task description.
        for fact in task.facts:
            for pair in fact.get_range():
                self.facts[pair] = RelaxedFact(pair)
        # print(f"Facts: {self.facts}")
        for action in task.actions:
            relaxed_action: RelaxedAction = RelaxedAction(action.id, action.cost)
            # Initialize precondition_of-list for each fact
            if action.pre:
                relaxed_action.pre_size = len(action.pre)
                for var in action.pre:
                    self.facts[var].pre_of.append(relaxed_action)
                for var in action.add:
                    relaxed_action.add.append(self.facts[var])
                self.actions.append(relaxed_action)
            # Handle operators that have no preconditions
            else:
                for pair in action.add:
                    self.facts[pair].default_dist = min(self.facts[pair].default_dist, action.cost)


if __name__ == '__main__':
    from src.model import MyParser
    from sys import argv

    if len(argv) > 1:
        problem: Problem = MyParser.load_problem(argv[1])
        heuristic: H_max = H_max(problem)
        print(f"Cost: {heuristic.evaluate(problem.initial_state)}")
        print(f"Time taken: {round(heuristic.total_time, 10)}sec. for problem: {problem.name}")
        print(f"Time spent on init: {round(heuristic.init_time, 10)} sec.")
    else:
        print(f"Expected name or path of problem file as command line argument!")
