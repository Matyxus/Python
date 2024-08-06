import unittest
from src.model import MyParser
from typing import List


class LoadTest(unittest.TestCase):
    """
    Class performing load test on basic problem included in project.
    """
    def test_loading(self) -> None:
        """
        Tests loading on 5 problems included in project.

        :return: None
        """
        problems: List[str] = ["blocks-4-0", "elevators01", "freecell01", "pegsol09", "sokoban03"]
        for problem in problems:
            self.assertTrue(MyParser.load_problem(problem) is not None)


if __name__ == '__main__':
    unittest.main()
