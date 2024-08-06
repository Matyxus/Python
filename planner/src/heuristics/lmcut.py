from src.heuristics.heuristic import Heuristic, State, Problem, Status, RelaxedFact, RelaxedAction, BIG_INT
import time
import heapq
from typing import List, Optional

"""
*********************************************************************************************************
*            This code is heavily inspired by: https://github.com/YannickZutter/fast-downward           *
*********************************************************************************************************
"""


class LmCut(Heuristic):
    """
    Class for LM-cut heuristic, defines helper variables to speed up execution.
    """
    def __init__(self, task: Problem):
        """
        :param task: defined in STRIPS language
        """
        super(LmCut, self).__init__(task)
        self.artificial_start: Optional[RelaxedFact] = None
        self.artificial_goal: Optional[RelaxedFact] = None
        self.init_vars(task)

    def evaluate(self, state: State) -> int:
        self.calls += 1
        now: float = time.time()
        cost: int = 0
        cut: List[RelaxedAction] = []
        second_queue: List[RelaxedFact] = []
        # Do the first pass of h_max
        self.first_exploration(state)
        self.init_time += (time.time() - now)
        # The artificial goal was not reach, return BIG_INT
        if self.artificial_goal.status == Status.UNREACHED:
            return BIG_INT
        i: int = 0
        # Iterate h_max till the artificial goal heuristic value is 0
        while self.artificial_goal.distance != 0:
            i += 1
            # Identify facts that can reach goal fact with 0 cost actions
            self.mark_goal_plateau(self.artificial_goal)
            assert(not cut)
            # Find cut
            self.second_exploration(state, second_queue, cut)
            assert(len(cut) != 0)
            # Update costs of actions and LM-cut heuristic value
            min_cost: int = BIG_INT
            for action in cut:
                min_cost = min(min_cost, action.cost)
            for action in cut:
                action.cost -= min_cost
            cost += min_cost
            # Do h_max gain, this time from the found cut
            self.first_exploration_incremental(cut)
            cut.clear()
            # Reset statuses of all facts which were related to the goal fact
            for fact in self.facts.values():
                if fact.status == Status.GOAL_ZONE or fact.status == Status.BEFORE_GOAL_ZONE:
                    fact.status = Status.REACHED
            self.artificial_start.status = Status.REACHED
            self.artificial_goal.status = Status.REACHED
        self.total_time += (time.time() - now)
        # print(f"Iterations: {i}")
        return cost

    # ---------------------------------- Search ----------------------------------

    def first_exploration(self, state: State) -> None:
        """
        Performs one h_max iteration from given state facts.
        Computes best supporter fact of actions and their heuristic (h_max) cost.

        :param state: given state to be evaluated
        :return: None
        """
        # Prepare exploration by setting all values to their defaults
        assert(not self.queue)
        self.reset_vars()
        # Enqueue initial facts and artificial starting fact
        for fact_pair in state.facts:
            self.enqueue(self.facts[fact_pair], 0)
        self.enqueue(self.artificial_start, 0)
        # Continue as in H_max (till queue is empty or goal is reached and processed)
        while self.queue:
            v, _, fact = heapq.heappop(self.queue)
            assert(fact.distance <= v)
            if fact.distance < v:
                continue
            for action in fact.pre_of:
                action.counter -= 1
                # This fact is the highest cost fact of current action -> means it is best supporter
                if action.counter == 0:
                    action.h_max_supporter = fact
                    action.h_max_cost = fact.distance
                    # Enqueue neighbours
                    cost = fact.distance + action.cost
                    for add_fact in action.add:
                        self.enqueue(add_fact, cost)
        return

    def first_exploration_incremental(self, cut: List[RelaxedAction]) -> None:
        """
        Takes advantage of cut, instead of recomputing the entire
        procedure of h_max, enqueues facts with cost equal to the
        h_max cost of actions and action cost

        :param cut: found LM-cut
        :return: None
        """
        assert(not self.queue)
        # Add only facts from the add-effects of actions in cut
        for action in cut:
            cost: int = action.h_max_cost + action.cost
            for fact in action.add:
                self.enqueue(fact, cost)
        # Continue till done
        while self.queue:
            v, _, fact = heapq.heappop(self.queue)
            assert(fact.distance <= v)
            if fact.distance < v:
                continue
            # Find action where this fact is the best supporter
            for action in fact.pre_of:
                if action.h_max_supporter != fact:
                    continue
                # Check if we can update
                old_cost: int = action.h_max_cost
                if old_cost > fact.distance:
                    action.update_h_max_supporter()
                    new_cost: int = action.h_max_cost
                    # This operator has become cheaper
                    if new_cost != old_cost:
                        assert(new_cost < old_cost)
                        cost: int = new_cost + action.cost
                        # Enqueue neighbours
                        for neigh in action.add:
                            self.enqueue(neigh, cost)
        return

    def second_exploration(self, state: State, queue: List[RelaxedFact], cut: List[RelaxedAction]) -> None:
        """
        :param state: given state to be evaluated
        :param queue: list working as queue (in lifo order)
        :param cut: empty list to which operators forming cut are added
        :return: None
        """
        assert(not queue)
        assert(not cut)
        # Initialize queue
        self.artificial_start.status = Status.BEFORE_GOAL_ZONE
        queue.append(self.artificial_start)
        for fact in state.facts:
            relaxed_fact: RelaxedFact = self.facts[fact]
            relaxed_fact.status = Status.BEFORE_GOAL_ZONE
            queue.append(relaxed_fact)
        # Start exploring
        while queue:
            relaxed_fact = queue.pop()
            # Find action, which this fact is best supporter of (among the action this fact is precondition)
            for action in relaxed_fact.pre_of:
                if action.h_max_supporter != relaxed_fact:
                    continue
                # Find out if we are able to reach to another neighbour fact which reached GOAL
                reached_goal: bool = False
                for neigh in action.add:
                    if neigh.status == Status.GOAL_ZONE:
                        assert(action.cost > 0)
                        reached_goal = True
                        cut.append(action)
                        break
                # Unable to reach goal fact, mark neighbour facts as being "before-goal"
                if not reached_goal:
                    for neigh in action.add:
                        if neigh.status != Status.BEFORE_GOAL_ZONE:
                            assert(neigh.status == Status.REACHED)
                            neigh.status = Status.BEFORE_GOAL_ZONE
                            queue.append(neigh)
        return

    def mark_goal_plateau(self, sub_goal: Optional[RelaxedFact]) -> None:
        """
        Starts recursively going over facts (from artificial goal fact),
        which are valid (not None) and not marked as being able to reach GOAL fact.
        Given such a fact (mark is as being in "goal-zone"), we start looking
        trough actions where this fact is in the "add-effects", and subsequently trough
        other facts action has in "add-effects", if the action cost is zero.
        If such action exist, the action best h_max supporter is recursively added to exploration.

        :param sub_goal: fact, which can reach GOAL state with zero cost action
        :return: None
        """
        # Only explore non-goal facts, which are valid
        if sub_goal is not None and sub_goal.status != Status.GOAL_ZONE:
            sub_goal.status = Status.GOAL_ZONE
            for action in sub_goal.add_of:
                if action.cost == 0:
                    self.mark_goal_plateau(action.h_max_supporter)
        return

    # ---------------------------------- Utils ----------------------------------

    def init_vars(self, task: Problem) -> None:
        # print(f"Initializing LM-cut relaxed facts & actions")
        # Initialize relaxed facts + new artificial start & end facts
        for fact in task.facts:
            for pair in fact.get_range():
                self.facts[pair] = RelaxedFact(pair)
        # Give them such values, so they cannot be referenced
        self.artificial_start = RelaxedFact((-1, -1))
        self.artificial_goal = RelaxedFact((BIG_INT, BIG_INT))
        # Process actions, create relaxed action for each, reference them in their facts
        for action in task.actions:
            relaxed_action: RelaxedAction = RelaxedAction(action.id, action.cost)
            for fact in action.pre:
                relaxed_action.pre.append(self.facts[fact])
            for fact in action.add:
                relaxed_action.add.append(self.facts[fact])
            if not action.pre:
                relaxed_action.pre.append(self.artificial_start)
            relaxed_action.pre_size = len(relaxed_action.pre)
            relaxed_action.counter = relaxed_action.pre_size
            self.actions.append(relaxed_action)
        # Build artificial goal action (invalid ID so we cannot index it)
        artificial_action: RelaxedAction = RelaxedAction(BIG_INT, 0)
        for fact in task.goal_state.facts:
            artificial_action.pre.append(self.facts[fact])
        artificial_action.add.append(self.artificial_goal)
        artificial_action.pre_size = len(artificial_action.pre)
        artificial_action.counter = artificial_action.pre_size
        self.actions.append(artificial_action)
        # Cross-reference relaxed actions with their facts
        for relaxed_action in self.actions:
            for fact in relaxed_action.pre:
                fact.pre_of.append(relaxed_action)
            for fact in relaxed_action.add:
                fact.add_of.append(relaxed_action)
        return

    def reset_vars(self) -> None:
        """
        Resets fact and actions to their defaults, called every time new state is evaluated.

        :return: None
        """
        self.tie_breaker = 0
        # Reset facts
        for fact in self.facts.values():
            fact.status = Status.UNREACHED
        self.artificial_goal.status = Status.UNREACHED
        self.artificial_goal.distance = BIG_INT
        self.artificial_start.status = Status.UNREACHED
        # Reset actions
        for action in self.actions:
            action.counter = action.pre_size
            action.cost = action.default_cost
            action.h_max_cost = BIG_INT
            action.h_max_supporter = None
        return


if __name__ == '__main__':
    from src.model import MyParser
    from sys import argv

    if len(argv) > 0:
        problem: Problem = MyParser.load_problem("elevators01")
        heuristic: LmCut = LmCut(problem)
        print(f"Cost: {heuristic.evaluate(problem.initial_state)}")
        print(f"Time taken: {round(heuristic.total_time, 10)}sec. for problem: {problem.name}")
        print(f"Time spent on init: {round(heuristic.init_time, 10)} sec.")
    else:
        print(f"Expected name or path of problem file as command line argument!")



