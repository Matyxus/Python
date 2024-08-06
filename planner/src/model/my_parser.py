from src.model.strips import Fact, Action, State, Problem
from os.path import isfile
from pathlib import Path
from typing import List, Tuple, Optional, TextIO


def _initialize_cwd() -> str:
    """
    :raise ValueError: in case directory 'planner' cannot be found in path
    :return: absolute path to project root
    """
    cwd: Path = Path(__file__)
    if "planner" not in str(cwd):
        raise ValueError(
            "Location of 'my_parser.py' file is incorrect,"
            f" unable to find 'planner' in '{str(cwd)}' !"
        )
    while not str(cwd).endswith("planner"):
        cwd = cwd.parent
    return str(cwd)


class MyParser:
    """
    Class containing static methods for converting '.sas' files into STRIPS problems.
    """
    DATA_DIR: str = _initialize_cwd() + "/data"
    INSTANCE: str = DATA_DIR + "/{0}.sas"

    @staticmethod
    def load_problem(problem_name: str) -> Optional[Problem]:
        """
        :param problem_name: name of problem file or absolute path
        :return: Problem class representing problem in STRIPS language, None if an error occurred
        """
        print(f"Loading problem file: '{problem_name}'")
        problem_path: str = problem_name if isfile(problem_name) else MyParser.INSTANCE.format(problem_name)
        if not isfile(problem_path):
            print(f"Unable to find file: {problem_path}")
            return None
        # Reset class counters to 0
        Fact._counter = 0
        Action._counter = 0
        State._counter = 0
        # Load file ...
        print(f"Starting to prepare STRIPS Task ...")
        problem: Problem = Problem(problem_name)
        with open(problem_path, "r") as file:
            if not (MyParser._skip_until(file, "end_metric")):
                return None  # Skip to vars definition
            # Load number of vars (facts)
            line = file.readline().rstrip()
            if not line or not line.isdigit() or (num_facts := int(line)) == 0:
                print(f"Expected positive number as number of variables, got: '{line}'")
                return None
            # print(f"Loading: {num_facts} facts")
            # Load all variables -> facts
            for i in range(num_facts):
                fact: Optional[Fact] = MyParser._load_fact(file)
                if fact is None:
                    return None
                problem.facts.append(fact)
            if not (MyParser._skip_until(file, "begin_state")):
                return None  # Skip to initial state
            # Load initial & goal states
            state_values: List[Tuple[int, int]] = []
            for i in range(num_facts):
                line = file.readline().rstrip()
                if not line or not line.isdigit():
                    print(f"Expected positive digit as number of variables, got: '{line}'")
                    return None
                state_values.append((i, int(line)))
            problem.initial_state = State(frozenset(state_values), [])
            if not (MyParser._skip_until(file, "begin_goal")):
                return  # Skip to goal state
            line = file.readline().rstrip()
            if not line or not line.isdigit() or (num_goals := int(line)) == 0:
                print(f"Expected positive number as number of goal states, got: '{line}'")
                return None
            state_values.clear()
            for i in range(num_goals):
                line = file.readline().rstrip()
                goal = line.split()
                if len(goal) != 2 or not (goal[0].isdigit() and goal[1].isdigit()):
                    print(f"Expected goal state to be 2 numbers, got: '{goal}'")
                    return None
                state_values.append((int(goal[0]), int(goal[1])))
            problem.goal_state = State(frozenset(state_values), [])
            line = file.readline().rstrip()
            if line != "end_goal":
                print(f"Expected last line of goal states to be 'end_goal', got: '{line}'")
                return None
            # Skip to operators
            line = file.readline().rstrip()
            if not line or not line.isdigit() or (num_operators := int(line)) == 0:
                print(f"Expected positive number as number of operators, got: '{line}'")
                return None
            # Load all operators -> actions
            # print(f"Loading: {num_operators} operators")
            for i in range(num_operators):
                action: Optional[Action] = MyParser._load_action(file, problem)
                if action is None:
                    return None
                problem.actions.append(action)
            problem.n_actions = num_operators
            problem.n_facts = num_facts
            # End
        print("Successfully loaded problem file")
        return problem

    @staticmethod
    def _load_fact(file: TextIO) -> Optional[Fact]:
        """
        :param file:
        :return:
        """
        if file.closed:
            print("Cannot load fact, file is closed!")
            return None
        line: str = file.readline().rstrip()
        if line != "begin_variable":
            print(f"Expected first line of variable to be 'begin_variable', got: '{line}'")
            return None
        # Load var name
        var_name: str = file.readline().rstrip()
        file.readline().rstrip()  # Ignore axiom layer
        line = file.readline().rstrip()
        if not line or not line.isdigit():
            print(f"Expected number of atoms to be positive digit, got: '{line}'")
            return None
        # Load atoms
        num_atoms: int = int(line)
        atoms: List[Tuple[str, str]] = []
        for i in range(num_atoms):
            line = file.readline().rstrip()
            atom: List[str] = line.split()
            if len(atom) < 2 or atom[0] not in {"Atom", "NegatedAtom", "<none"}:
                print(
                    f"Expected each atom to be of type: "
                    f"(Atom, NegatedAtom or <None of those>) and have name, got: '{atom}'"
                )
                return None
            atoms.append((atom[0], "".join(atom[1:])))
        if file.readline().rstrip() != "end_variable":
            print(f"Expected last line of variable to be 'end_variable', got: '{line}'")
            return None
        return Fact(var_name, num_atoms, atoms)

    @staticmethod
    def _load_action(file: TextIO, problem: Problem) -> Optional[Action]:
        """
        :param file: pointer to opened file
        :param problem: current problem instance
        :return: Action in STRIPS, None if an error occurred
        """
        if file.closed:
            print("Cannot load fact, file is closed!")
            return None
        line: str = file.readline().rstrip()
        if line != "begin_operator":
            print(f"Expected first line of operator to be 'begin_operator', got: '{line}'")
            return None
        # Load action name
        action_name: str = file.readline().rstrip()
        if not action_name:
            print("Name of action is empty string!")
            return None
        # Skip to pre-vail conditions
        line = file.readline().rstrip()
        if not line or not line.isdigit():
            print(f"Expected digit as number of pre-conditions, got: '{line}'")
            return None
        pre: List[Tuple[int, int]] = []
        add: List[Tuple[int, int]] = []
        rem: List[Tuple[int, int]] = []
        # Load pre-veil conditions (pre-conditions which do not affect the variables)
        for i in range(int(line)):
            line = file.readline().rstrip()
            prevail_condition: List[str] = line.split()
            if len(prevail_condition) != 2 or not (prevail_condition[0].isdigit() and prevail_condition[1].isdigit()):
                print(f"Expected variable number and value in prevail condition, got: '{prevail_condition}'")
                return None
            pre.append((int(prevail_condition[0]), int(prevail_condition[1])))
        # Load pre-conditions & add & del conditions of actions
        line = file.readline().rstrip()
        if not line or not line.isdigit() or (pre_conditions := int(line)) == 0:
            print(f"Expected positive number as count of pre-conditions & effects, got: '{line}'")
            return None
        for i in range(pre_conditions):
            line = file.readline().rstrip()
            pre_condition: List[str] = line.split()
            if len(pre_condition) != 4 or not all(map(MyParser._is_integer, pre_condition)):
                print(f"Expected pre-condition and effect to be 4 numbers, got: '{pre_condition}'")
                return None
            add.append((int(pre_condition[1]), int(pre_condition[3])))
            # Ignore first value (i.e. the associated effects)
            if int(pre_condition[2]) != -1:  # Ignore "any" value pre-conditions
                pre.append((int(pre_condition[1]), int(pre_condition[2])))
                rem.append(pre[-1])
            else:  # Use any value pre-conditions to remove all possible values of this fact (apart from the added one)
                for (fact, value) in problem.facts[int(pre_condition[1])].get_range():
                    if value != add[-1][1]:
                        rem.append((fact, value))
        # Load action cost
        line = file.readline().rstrip()
        if not line or not line.isdigit():
            print(f"Expected cost as number of action, got: '{line}'")
            return None
        # Skip last line
        if file.readline().rstrip() != "end_operator":
            print(f"Expected last line of operator to be 'end_operator', got: '{line}'")
            return None
        return Action(action_name, int(line), frozenset(pre), frozenset(add), frozenset(rem))

    # --------------------------------------- Utils ---------------------------------------

    @staticmethod
    def _skip_until(file: TextIO, target_line: str) -> bool:
        """
        :param file:
        :param target_line:
        :return:
        """
        # print(f"Skipping file until line: '{target_line}'")
        if file.closed:
            print(f"Cannot skip in file till: '{target_line}', file is closed!")
            return False
        while (line := file.readline().rstrip()) and line and line != target_line:
            pass
        return line == target_line

    @staticmethod
    def _is_integer(string: str) -> bool:
        """
        :param string: text
        :return: True if text is integer, false otherwise
        """
        try:
            int(string)
        except ValueError:
            return False
        return True
