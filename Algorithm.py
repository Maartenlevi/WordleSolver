from database_connection import connect, close
import time
from collections import defaultdict


def get_all_words():
    conn, cursor = connect()
    cursor.execute("SELECT id, word FROM Words")
    words = cursor.fetchall()
    close(conn)
    return words


def compare_wordle(guess, target):
    result = [0] * len(guess)
    target_list = list(target)

    # First pass: identify correct positions
    for i in range(len(guess)):
        if guess[i] == target[i]:
            result[i] = 2
            target_list[i] = None  # Mark this letter as used

    # Second pass: identify letters in the wrong positions
    for i in range(len(guess)):
        if result[i] == 0 and guess[i] in target_list:
            result[i] = 1
            target_list[target_list.index(guess[i])] = None  # Mark this letter as used

    return result


def filter_possible_words(possible_words, guess, feedback):
    filtered_words = []

    # Loop through each word in the possible words list
    for word in possible_words:
        # Compare the word with the guess to get feedback
        word_feedback = compare_wordle(guess, word)

        # If the feedback matches the provided feedback, add the word to the filtered list
        if word_feedback == feedback:
            filtered_words.append(word)

    return filtered_words


def minimax_score(possible_words, guess):
    feedback_counts = defaultdict(int)

    for word in possible_words:
        feedback = tuple(compare_wordle(guess, word))
        feedback_counts[feedback] += 1

    return max(feedback_counts.values())


def select_best_guess(possible_words):
    best_guess = None
    best_score = float('inf')

    for guess in possible_words:
        score = minimax_score(possible_words, guess)
        if score < best_score:
            best_score = score
            best_guess = guess

    return best_guess


def main(starting_word):
    # check if the starting word is already in the database
    conn, cursor = connect()
    cursor.execute("SELECT starting_word FROM statistics WHERE starting_word = %s", (starting_word,))
    if cursor.fetchone() is None:
        # Start the timer
        start_time = time.time()

        # Load all words once
        all_words = [word[1] for word in get_all_words()]

        # Initialize variables
        total_games = 0
        wins = 0
        turns = 0
        median_turns = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        starting_word_eliminations = 0

        for word in all_words:
            total_games += 1
            target = word
            guess = starting_word.lower()
            possible_words = all_words

            for guess_count in range(6):  # Allow up to 6 guesses
                feedback = compare_wordle(guess, target)
                if guess == target:
                    wins += 1
                    turns += guess_count + 1
                    median_turns[guess_count + 1] += 1
                    break

                possible_words = filter_possible_words(possible_words, guess, feedback)
                if guess_count == 0:
                    starting_word_eliminations += len(possible_words)
                if not possible_words:
                    print(f"No possible words found for target '{target}'. There might be an error in the filtering logic.\n")
                    break

                guess = select_best_guess(possible_words)

        end_time = time.time()
        runtime = end_time - start_time
        win_rate = wins / total_games * 100
        # Calculate the median number of turns
        median_turn = sorted(median_turns.items(), key=lambda x: x[1], reverse=True)[0][0]
        starting_word_eliminations /= total_games

        # add the results to the database
        cursor.execute("INSERT INTO statistics (starting_word, total_games, wins, win_rate, average_turns, median_turns, execution_time, starting_word_eliminations) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (starting_word, total_games, wins, win_rate, turns / wins, median_turn, runtime, starting_word_eliminations))
        conn.commit()
        close(conn)

        print(f"Starting word: {starting_word}")
        print(f"Amount of games played: {total_games}")
        print(f"Number of wins: {wins}")
        print(f"Win rate: {win_rate:.2f}%")
        print(f"Average number of turns: {turns / wins:.2f}")
        print(f"Median number of turns: {median_turn}")

        print(f"Execution time: {runtime:.2f} seconds\n")

    else:
        print(f"The starting word '{starting_word}' is already in the database.\n")
        close(conn)


# Run the main function with the starting word 'salet'
starting_word = [
    "Crane", "Arise", "Roate", "Media", "Canoe", "Store",
    "Adieu", "Audio", "About", "Slate", "Crate", "Tales", "Slice",
    "Trace", "Roast", "Aisle", "Stare", "Salet", "Least", "Soare",
    "Sauce"
]

for word in starting_word:
    main(word)
