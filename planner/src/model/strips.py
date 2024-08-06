from typing import Optional, List, FrozenSet, Tuple


class Fact:
    """
    Class representing fact in STRIPS language
    """
    _counter: int = 0  # Counts number of instances of Fact class

    def __init__(self, name: str, n_states: int, atoms: List[Tuple[str, str]]):
        """
        :param name: name of fact
        :param n_states: total number of states fact can be in (0, n_states-1)
        :param atoms: atoms representing all states [(Atom/NegatedAtom, name), ....]
        """
        self.name: str = name
        self.id: int = Fact._counter
        self.n_values: int = n_states
        self.atoms: Optional[List[Tuple[str, str]]] = atoms
        assert(len(atoms) == n_states)
        Fact._counter += 1

    # ---------------------------- Utils ----------------------------

    def get_range(self) -> List[Tuple[int, int]]:
        """
        :return: List of all possible pairing of fact
        """
        return [(self.id, i) for i in range(self.n_values)]

    def get_atom(self, value: int) -> str:
        """
        :param value: value of atom (i.e. index)
        :return: string representation of atom (prefix '!' if it is negated)
        """
        assert(value < self.n_values)
        return ("!" if self.atoms[value][0] == "NegatedAtom" else "") + self.atoms[value][1]

    def __str__(self) -> str:
        """
        :return: String representation of fact
        """
        return f"(fact: {self.name}, id: {self.id}, n_states: {self.n_values}, atoms: {self.atoms})"


class State:
    """
    Class representing state of justification graph in STRIPS language
    """
    _counter: int = 0  # Counts number of instances of State class

    def __init__(self, facts: FrozenSet[Tuple[int, int]], actions: List[int]):
        """
        :param facts: representing current state
        :param actions: used to get to this state (ordered dictionary)
        """
        self.id: int = State._counter
        self.facts: FrozenSet[Tuple[int, int]] = facts  # Set of (Fact_id : value)
        self.actions: List[int] = actions
        State._counter += 1

    def get_facts(self) -> List[int]:
        """
        :return: Id's of fact in given state
        """
        return [f for (f, _) in self.facts]

    # ------------------------------------- Queue and Dictionary operators -------------------------------------

    def __lt__(self, other: 'State') -> bool:
        """
        :param other: state
        :return: True if the current state id is lower than other
        """
        return self.id < other.id

    def __eq__(self, other: 'State') -> bool:
        """
        :param other: state
        :return: True if states are equal (set of facts are equal)
        """
        return self.facts == other.facts

    def __hash__(self) -> int:
        """
        :return: Hash of state (set of facts)
        """
        return hash(self.facts)

    def __str__(self) -> str:
        """
        :return: String representation of state
        """
        return f"(state: {self.facts})"


class Action:
    """
    Class representing action in STRIPS language
    """
    _counter: int = 0  # Counts number of instances of Fact class

    def __init__(
            self, name: str, cost,
            pre: FrozenSet[Tuple[int, int]],
            add: FrozenSet[Tuple[int, int]],
            rem: FrozenSet[Tuple[int, int]]
        ):
        """
        :param name: name of action
        :param cost: cost of action (non negative number)
        :param pre: pre-conditions of action
        :param add: add-effects of action
        :param rem: del-effects of action
        """
        self.name: str = name
        self.id: int = Action._counter
        self.pre: FrozenSet[Tuple[int, int]] = pre  # Set of (Fact_id : value)
        self.add: FrozenSet[Tuple[int, int]] = add  # Set of (Fact_id : value)
        self.rem: FrozenSet[Tuple[int, int]] = rem  # Set of (Fact_id : value)
        self.cost: int = max(cost, 0)
        Action._counter += 1

    def is_pre_fact(self, fact: Tuple[int, int]) -> bool:
        """
        :param fact: fact tuple of (fact_id, value)
        :return: True if fact is in pre-conditions of this action, False otherwise
        """
        return fact in self.pre

    def is_applicable(self, state: State) -> bool:
        """
        :param state: current state
        :return: True if action can be used in the given state, False otherwise
        """
        # Only if sate contains all pre-conditions we can apply action, do not apply if action has no effect
        return state.facts.issuperset(self.pre) and not self.add.issubset(state.facts)

    def apply(self, state: State) -> Optional[State]:
        """
        :param state: current state
        :return: New state after action was applied, None if action cannot be applied
        """
        return State((state.facts - self.rem) | self.add, state.actions + [self.id])

    def has_pre(self) -> bool:
        """
        :return: True if action has pre-conditions, false otherwise
        """
        return len(self.pre) != 0

    def __str__(self) -> str:
        """
        :return: String representation of action
        """
        return f"(action: {self.name}, cost: {self.cost}, pre: {self.pre}, add: {self.add}, del: {self.rem})"


class Problem:
    """
    Class representing planning problem in STRIPS language
    """
    def __init__(self, name: str):
        """
        :param name: name of problem
        """
        self.name = name
        self.facts: List[Fact] = []
        self.actions: List[Action] = []
        self.n_facts: int = 0
        self.n_actions: int = 0
        self.initial_state: Optional[State] = None
        self.goal_state: Optional[State] = None

    def is_valid(self, state: State) -> bool:
        """
        :param state: current state
        :return: True if state is valid, false otherwise
        """
        # Check that all facts and their values are valid
        return all([(0 <= f < self.n_facts) and (0 <= v < self.facts[f].n_values) for (f, v) in state.facts])

    def is_goal(self, state: State) -> bool:
        """
        :param state: current state
        :return: True if given state is goal state, False otherwise
        """
        return state.facts.issuperset(self.goal_state.facts)

    # --------------------------- Utils ---------------------------

    def is_loaded(self) -> bool:
        """
        :return: True if problem is loaded
        :raises ValueError if problem is missing some parts
        """
        if not self.name:
            raise ValueError("Error, problem is missing name!")
        elif not self.facts or not self.actions:
            raise ValueError("Error, problem is missing facts and/or actions!")
        elif self.n_facts != len(self.facts) or self.n_actions != len(self.actions):
            raise ValueError("Error, number of facts and/or action is not equal to the true amount!")
        elif self.initial_state is None or not self.is_valid(self.initial_state):
            raise ValueError("Error, initial state is invalid!")
        elif self.goal_state is None or not self.is_valid(self.goal_state):
            raise ValueError("Error, goal state is invalid!")
        return True

    def plan_info(self, plan: List[int], cost: int, output_file: str = "") -> str:
        """
        :param plan: sequence of actions
        :param cost: cost of plan
        :param output_file: file to which the plan gets written, optional (default None)
        :return: string representation of plan
        """
        info: str = "\n".join([self.actions[action_id].name for action_id in plan]) + f"\nPlan cost: {cost}"
        if output_file:
            with open(output_file, "w") as file:
                file.writelines(info)
        return info

    def state_info(self, state: State) -> str:
        """
        :param state: current state
        :return: string representation of state
        """
        if state is None:
            return "<None>"
        return "[" + " ".join([self.facts[fact_id].get_atom(value) for (fact_id, value) in state.facts]) + "]"

    def action_info(self, action: Action) -> str:
        """
        :param action: current action
        :return: string representation of action
        """
        ret_val: str = f"(Action: {action.name}, cost: {action.cost}, "
        ret_val += "\npre: [" + " ".join([self.facts[fact_id].get_atom(value) for (fact_id, value) in action.pre]) + "]"
        ret_val += "\nadd: [" + " ".join([self.facts[fact_id].get_atom(value) for (fact_id, value) in action.add]) + "]"
        ret_val += "\ndel: [" + " ".join([self.facts[fact_id].get_atom(value) for (fact_id, value) in action.rem]) + "]"
        return ret_val + ")"

    def __str__(self) -> str:
        """
        :return: string representation of problem
        """
        ret_val: str = f"Problem: {self.name}\n"
        ret_val += f"Facts: {self.n_facts}\n"
        for fact in self.facts:
            ret_val += f"\t{fact}\n"
        ret_val += f"Actions: {self.n_actions}\n"
        for action in self.actions:
            ret_val += f"\t{self.action_info(action)}\n"
        ret_val += f"Initial state:\n{self.state_info(self.initial_state)}\n"
        ret_val += f"Goal state:\n{self.state_info(self.goal_state)}\n"
        return ret_val
