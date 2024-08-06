import unittest
from src.model import MyParser, Problem
from src.heuristics import H_max
from typing import List, Tuple


class HmaxTest(unittest.TestCase):
    """
    Class performing test on H_max heuristic first iteration and its value on
    5 simple problems.
    """
    def test_hmax(self) -> None:
        """
        Tests H_max on 5 problems included in project.

        :return: None
        """
        problems: List[Tuple[str, int]] = [
            ("blocks-4-0", 2), ("elevators01", 9), ("freecell01", 4),
            ("pegsol09", 2), ("sokoban03", 3),
        ]
        for (problem_name, value) in problems:
            task: Problem = MyParser.load_problem(problem_name)
            self.assertEqual(H_max(task).evaluate(task.initial_state), value)


if __name__ == '__main__':
    unittest.main()
