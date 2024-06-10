from database_connection import connect, close

def get_word_by_index(index):
    # Connect to the database
    conn, cursor = connect()

    # get the word and letters from the database with the given index
    cursor.execute(
        "SELECT * FROM Words WHERE id = %s",
        (index,)
    )
    word = cursor.fetchone()


    # Close the cursor and connection
    close(conn)

    return word #output: (217, 'blend', 'b', 'l', 'e', 'n', 'd')

def compare_words(word, guess):
    """
    Check how many elements in the guess are in the correct position and how many are in the wrong position.

    Args:
        word (list): The word to compare to.
        guess (list): The guess to compare.

    Returns:
        tuple: The number of correct elements in the correct position and the number of correct elements in the wrong position.
    """
    correct_position = 0
    wrong_position = 0
    word_copy = list(word[1:])

    # Check for correct elements in the correct position
    for i in range(len(word[1:])):
        if word[1:][i] == guess[i]:
            correct_position += 1
            word_copy[i] = None

    # Check for correct elements in the wrong position
    for i in range(len(guess)):
        if guess[i] != word[1:][i] and guess[i] in word_copy:
            wrong_position += 1
            word_copy.remove(guess[i])

    return correct_position, wrong_position
def first_guess(starting_word):





