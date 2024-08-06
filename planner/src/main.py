from src.model import MyParser, State, Problem, BIG_INT
from src.heuristics import Heuristic, H_max, LmCut
import time
import heapq
from sys import argv
from typing import Optional, Union, List, Dict, Tuple, Type


class Planner:
    """
    Classical implementation of A* to solver planning task
    in STRIPS language with h-max or lm-cut heuristics.
    """
    def __init__(self, problem: Union[str, Problem], heuristic: Type[Heuristic], output_file: str = ""):
        """
        :param problem: name of problem file to be loaded or full path
        :param heuristic: the given heuristic to be used in A* algorithm
        :param output_file: file which will contain the plan of the problem
        """
        self.task: Problem = problem if isinstance(problem, Problem) else MyParser.load_problem(problem)
        assert (self.task is not None and self.task.is_loaded())
        self.heuristic: Heuristic = heuristic(self.task)
        self.output_file: str = output_file

    def a_star(self, start: State) -> Optional[Tuple[State, int]]:
        """
        :param start: starting state
        :return: Goal state if found, None otherwise
        """
        # print(f"Running A* from {start}")
        # print(f"Goal: {self.task.goal_state}")
        # ---------- Init ----------
        queue: List[Tuple[int, State]] = [(0, start)]  # [(f + g, State), ...]
        heapq.heapify(queue)
        score: Dict[State, Tuple[int, int]] = {start: (0, 0)}  # {State: (f, g), ...}
        i, v, g = 0, 0, 0
        v_, g_ = 0, 0
        # ---------- Search ----------
        while queue:
            prio, state = heapq.heappop(queue)
            print(f"\riter: {i}", end="")
            i += 1
            # Extract the score for the state
            g, v = score[state]
            # Check for goal
            if self.task.is_goal(state):
                print(f"\nFound goal, iterations: {i}, hash size: {len(score)}")
                print(self.task.plan_info(state.actions, g, self.output_file))
                return state, g
            # Avoid exploring state with higher cost
            elif g + v < prio:
                continue
            # Find all neighbours, over all applicable actions
            for action in self.task.actions:
                if not action.is_applicable(state):
                    continue
                v = g + action.cost
                new_state: State = action.apply(state)
                # Extract values to vars to avoid further dict entries
                v_, g_ = score.get(new_state, (BIG_INT, -1))
                if v < v_:
                    # Avoid recomputing the heuristic value (-1 is given as invalid value -> has to be >= 0)
                    g_ = (g_ if g_ != -1 else self.heuristic.evaluate(new_state))
                    score[new_state] = (v, g_)
                    heapq.heappush(queue, (v + g_, new_state))
        # print("Result was not found!")
        return None

    def print_stats(self, goal: State, start: float) -> None:
        """
        :return: None
        """
        print(f"************* Statistics *************")
        print(f"Goal state: {planner.task.state_info(goal)}")
        print(f"Time spent on {self.heuristic.__class__.__name__}: {round(self.heuristic.total_time, 3)} sec.")
        print(f"Average: {round(self.heuristic.total_time / max(self.heuristic.calls, 1), 3)}s/call({self.heuristic.calls}).")
        print(f"Total init time: {round(self.heuristic.init_time, 3)} sec.")
        print(f"Time taken: {round(time.time() - start, 3)} sec.")


if __name__ == '__main__':
    if len(argv) > 2:
        start: float = time.time()
        planner: Planner = Planner(argv[1], (H_max if argv[2] == "hmax" else LmCut), "" if len(argv) == 3 else argv[3])
        goal: Optional[Tuple[State, int]] = planner.a_star(planner.task.initial_state)
        if goal is not None:
            planner.print_stats(goal[0], start)
    else:
        print(f"Expected at least 2 arguments: [problem name, heuristic, output file (optional)]")


