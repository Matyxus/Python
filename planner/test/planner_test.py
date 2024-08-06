import unittest
from src.main import Planner, MyParser, Problem
from src.heuristics import H_max, LmCut


class PlannerTest(unittest.TestCase):
    """ Class testing planner with Hmax and LmCut heuristics on 5 problems included in project"""

    def test_blocks(self):
        """
        Tests planner on blocks problem

        :return: None
        """
        task: Problem = MyParser.load_problem("blocks-4-0")
        self.assertEqual(Planner(task, H_max).a_star(task.initial_state)[1], 6)
        self.assertEqual(Planner(task, LmCut).a_star(task.initial_state)[1], 6)

    def test_elevators(self):
        """
        Tests planner on elevators problem

        :return: None
        """
        task: Problem = MyParser.load_problem("elevators01")
        self.assertEqual(Planner(task, H_max).a_star(task.initial_state)[1], 42)
        self.assertEqual(Planner(task, LmCut).a_star(task.initial_state)[1], 42)

    def test_freecell(self):
        """
        Tests planner on freecell problem

        :return: None
        """
        task: Problem = MyParser.load_problem("freecell01")
        self.assertEqual(Planner(task, H_max).a_star(task.initial_state)[1], 9)
        self.assertEqual(Planner(task, LmCut).a_star(task.initial_state)[1], 9)

    def test_pegsol(self):
        """
        Tests planner on pegsol problem

        :return: None
        """
        task: Problem = MyParser.load_problem("pegsol09")
        self.assertEqual(Planner(task, H_max).a_star(task.initial_state)[1], 8)
        self.assertEqual(Planner(task, LmCut).a_star(task.initial_state)[1], 8)

    def test_sokoban(self):
        """
        Tests planner on sokoban problem

        :return: None
        """
        task: Problem = MyParser.load_problem("sokoban03")
        self.assertEqual(Planner(task, H_max).a_star(task.initial_state)[1], 10)
        self.assertEqual(Planner(task, LmCut).a_star(task.initial_state)[1], 10)


if __name__ == '__main__':
    unittest.main()
