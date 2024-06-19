import unittest
from Algorithm import algorithm, compare_wordle, filter_possible_words, minimax_score, select_best_guess

class Test_compare_wordle(unittest.TestCase):
    def test_compare_wordle(self):
        self.assertEqual(compare_wordle('hello', 'hello'), [2, 2, 2, 2, 2]) # all correct
        self.assertEqual(compare_wordle('hello', 'xxxxx'), [0, 0, 0, 0, 0]) # all wrong
        self.assertEqual(compare_wordle('hello', 'hxxxx'), [2, 0, 0, 0, 0]) # 1 correct
        self.assertEqual(compare_wordle('hello', 'hxxex'), [2, 1, 0, 0, 0]) # 1 correct and 1 in wrong position
        self.assertEqual(compare_wordle('hello', 'hexxl'), [2, 2, 1, 0, 0]) # 2 correct and 1 in wrong position
        self.assertEqual(compare_wordle('hello', 'xhxxx'), [1, 0, 0, 0, 0]) # 1 in wrong position
        self.assertEqual(compare_wordle('hello', 'ehxxx'), [1, 1, 0, 0, 0]) # 2 in wrong position
        self.assertEqual(compare_wordle('hello', 'ehlxx'), [1, 1, 2, 0, 0]) # 2 in wrong position and 1 in correct position

class Test_filter_possible_words(unittest.TestCase):
    def test_filter_possible_words(self):
        self.assertEqual(filter_possible_words(['hello', 'world', 'steak'], 'hello', [2, 2, 2, 2, 2]), ['hello'])
        self.assertEqual(filter_possible_words(['hello', 'world', 'steak'], 'hello', [2, 1, 0, 0, 0]), [])
        self.assertEqual(filter_possible_words(['hello', 'world', 'steak'], 'hello', [0, 1, 0, 0, 0]), ['steak'])
        self.assertEqual(filter_possible_words(['hello', 'world', 'steak'], 'hello', [0, 0, 0, 2, 1]), ['world'])
        self.assertEqual(filter_possible_words(['hello', 'world', 'steak'], 'hello', [1, 0, 0, 0, 0]), [] )


class Test_minimax_score(unittest.TestCase):
    def test_minimax_score(self):
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'hello'), 1)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'world'), 1)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'steak'), 1)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'xxxxx'), 3)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'hxxxx'), 2)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'hxxex'), 1)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'hexxl'), 1)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'xhxxx'), 2)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'ehxxx'), 1)
        self.assertEqual(minimax_score(['hello', 'world', 'steak'], 'ehlxx'), 1)

class Test_select_best_guess(unittest.TestCase):
    def test_select_best_guess(self):
        self.assertEqual(select_best_guess(['hello', 'world', 'steak']), 'hello')
        self.assertEqual(select_best_guess(['hello', 'world', 'steak', 'xxxxx']), 'xxxxx')
        self.assertEqual(select_best_guess(['hello', 'world', 'steak', 'hxxxx']), 'hxxxx')
        self.assertEqual(select_best_guess(['hello', 'world', 'steak', 'hxxex']), 'hxxex')
        self.assertEqual(select_best_guess(['hello', 'world', 'steak', 'hexxl']), 'hexxl')
        self.assertEqual(select_best_guess(['hello', 'world', 'steak', 'xhxxx']), 'xhxxx')
        self.assertEqual(select_best_guess(['hello', 'world', 'steak', 'ehxxx']), 'ehxxx')
        self.assertEqual(select_best_guess(['hello', 'world', 'steak', 'ehlxx']), 'ehlxx')



if __name__ == '__main__':
    unittest.main()
