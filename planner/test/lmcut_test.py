import unittest
from src.model import MyParser, Problem
from src.heuristics import LmCut
from typing import List, Tuple


class LmCutTest(unittest.TestCase):
    """
    Class performing test on LmCut heuristic first iteration and its value on
    5 simple problems.
    """
    def test_lmcut(self) -> None:
        """
        Tests LmCut on 5 problems included in project.

        :return: None
        """
        problems: List[Tuple[str, int]] = [
            ("blocks-4-0", 6), ("elevators01", 31), ("freecell01", 7),
            ("pegsol09", 2), ("sokoban03", 3),
        ]
        for (problem_name, value) in problems:
            task: Problem = MyParser.load_problem(problem_name)
            self.assertEqual(LmCut(task).evaluate(task.initial_state), value)


if __name__ == '__main__':
    unittest.main()
