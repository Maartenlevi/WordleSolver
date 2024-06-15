# make script that will test the functions in Algorithm.py

import pytest
from Algorithm import compare_wordle, filter_possible_words, minimax_score, select_best_guess


def test_compare_wordle():
    assert compare_wordle('hello', 'hello') == [2, 2, 2, 2, 2]
    assert compare_wordle('hello', 'world') == [0, 0, 0, 0, 0]
    assert compare_wordle('hello', 'hills') == [2, 0, 0, 0, 1]
    assert compare_wordle('hello', 'hello') == [2, 2, 2, 2, 2]
    assert compare_wordle('hello', 'hello') == [2, 2, 2, 2, 2]

def test_filter_possible_words():
    assert filter_possible_words(['hello', 'world', 'hills'], 'hello', [2, 0, 0, 0, 1]) == ['hills']
    assert filter_possible_words(['hello', 'world', 'hills'], 'hello', [2, 2, 2, 2, 2]) == ['hello']
    assert filter_possible_words(['hello', 'world', 'hills'], 'hello', [0, 0, 0, 0, 0]) == ['world']
    assert filter_possible_words(['hello', 'world', 'hills'], 'hello', [2, 0, 0, 0, 1]) == ['hills']
    assert filter_possible_words(['hello', 'world', 'hills'], 'hello', [2, 0, 0, 0, 1]) == ['hills']

def test_minimax_score():
    assert minimax_score(['hello', 'world', 'hills'], 'hello') == 2
    assert minimax_score(['hello', 'world', 'hills'], 'world') == 1
    assert minimax_score(['hello', 'world', 'hills'], 'hills') == 1
    assert minimax_score(['hello', 'world', 'hills'], 'hello') == 2
    assert minimax_score(['hello', 'world', 'hills'], 'hello') == 2

def test_select_best_guess():
    assert select_best_guess(['hello', 'world', 'hills']) == 'world'
    assert select_best_guess(['hello', 'world', 'hills']) == 'world'
    assert select_best_guess(['hello', 'world', 'hills']) == 'world'
    assert select_best_guess(['hello', 'world', 'hills']) == 'world'
    assert select_best_guess(['hello', 'world', 'hills']) == 'world'

# Run the tests
if __name__ == '__main__':
    pytest.main()
