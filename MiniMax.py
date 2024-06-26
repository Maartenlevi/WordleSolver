from database_connection import connect, close
import time


def get_all_words():
    conn, cursor = connect()
    cursor.execute("SELECT id, word FROM words")
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
    feedback_counts = {}

    for word in possible_words:
        feedback = tuple(compare_wordle(guess, word))
        if feedback in feedback_counts:
            feedback_counts[feedback] += 1
        else:
            feedback_counts[feedback] = 1
    # example: feedback_counts = {(2, 2, 2, 2, 2): 1, (2, 1, 0, 0, 0): 2, (0, 0, 0, 0, 0): 1}

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


def algorithm(starting_words):
    # check if the word is 5 characters long
    if len(starting_words) != 5:
        print("The starting word should be 5 characters long.")
        return
    # make sure the first letter is uppercase
    starting_word = starting_words.capitalize()
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
        amount_words = len(all_words)

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
            # make a progress bar in percentages but only print it every 5%
            if total_games % (amount_words // 5) == 0:
                print(f"{total_games / amount_words * 100:.0f}% of the words have been processed.")

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
            INSERT INTO statistics (
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
