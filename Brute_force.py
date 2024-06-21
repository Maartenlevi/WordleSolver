from Algorithm import compare_wordle, filter_possible_words, get_all_words
from database_connection import connect, close
import time
import random


def get_guess(possible_words):
    return random.choice(possible_words)


def brute_force(starting_words):

    # check if the word is 5 characters long
    if len(starting_words) != 5:
        print("The starting word should be 5 characters long.")
        return

    # make sure the first letter is uppercase
    starting_word = starting_words.capitalize()

    # check if the starting word is already in the database
    conn, cursor = connect()
    cursor.execute("SELECT starting_word FROM brute_force_statistics WHERE starting_word = %s", (starting_word,))
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

                guess = get_guess(possible_words)

        end_time = time.time()
        runtime = end_time - start_time
        win_rate = wins / total_games * 100
        # Calculate the median number of turns
        median_turn = sorted(median_turns.items(), key=lambda x: x[1], reverse=True)[0][0]
        starting_word_eliminations /= total_games

        # Prepare the values for wins on each turn
        wins_turn_1 = median_turns[1]
        wins_turn_2 = median_turns[2]
        wins_turn_3 = median_turns[3]
        wins_turn_4 = median_turns[4]
        wins_turn_5 = median_turns[5]
        wins_turn_6 = median_turns[6]

        # Add the results to the database
        cursor.execute("""
            INSERT INTO brute_force_statistics (
                starting_word, total_games, wins, win_rate, average_turns, median_turns, execution_time, starting_word_eliminations,
                wins_turn_1, wins_turn_2, wins_turn_3, wins_turn_4, wins_turn_5, wins_turn_6
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            starting_word, total_games, wins, win_rate, turns / wins, median_turn, runtime, starting_word_eliminations,
            wins_turn_1, wins_turn_2, wins_turn_3, wins_turn_4, wins_turn_5, wins_turn_6
        ))
        conn.commit()
        close(conn)

    else:
        close(conn)
