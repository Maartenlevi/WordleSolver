from MiniMax import algorithm
from Brute_force import brute_force
from database_connection import close, connect


def run_algorithms(words):
    """
    Run algorithms on each word retrieved from the database.

    Args:
    - words: List of words fetched from the database.

    Returns:
    - None
    """
    # make sure the brute force statistics table is the same as the statistics table
    conn, cursor = connect()
    cursor.execute("SELECT starting_word FROM statistics")
    statistics_words = cursor.fetchall()

    amount_words = len(statistics_words)
    for word in statistics_words:
        print(f"\nProcessing starting word: {word[0]} ({statistics_words.index(word) + 1}/{amount_words})")
        brute_force(word[0])
    
    # Amount of words to test
    amount_words = len(words)

    for word in words:
        print(f"\nProcessing starting word: {word[0]} ({words.index(word) + 1}/{amount_words})")
        algorithm(word[0])
        brute_force(word[0])



def get_words(limit):
    """
    Retrieve words from the database grouped by starting letters.

    Returns:
    - List of words fetched from the database.
    """
    conn, cursor = connect()
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
               "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    words = []

    for letter in letters:
        cursor.execute("SELECT word FROM words WHERE letter1 = %s LIMIT = %s", (letter, limit))
        words += cursor.fetchall()

    close(conn)

    return words


words = get_words(15)
run_algorithms(words)
