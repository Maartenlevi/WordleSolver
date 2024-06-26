from database_connection import connect, close


def get_letter_frequency(letter):
    """
    Get the frequency of a letter in each position of a word.

    Args:
    - letter: The letter to get the frequency of.

    Returns:
    - letter_frequency: A list of the frequency of the letter in each position of a word.
    """

    # make sure the letter is lowercase
    letter = letter.lower()
    # do a query to get the frequency of the letter in 1st position then 2nd position etc.
    conn, cursor = connect()
    cursor.execute("SELECT COUNT(*) AS count_of_letter_in_position1 FROM words WHERE letter1 = %s", (letter,))
    count_of_letter_in_position1 = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) AS count_of_letter_in_position2 FROM words WHERE letter2 = %s", (letter,))

    count_of_letter_in_position2 = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) AS count_of_letter_in_position3 FROM words WHERE letter3 = %s", (letter,))

    count_of_letter_in_position3 = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) AS count_of_letter_in_position4 FROM words WHERE letter4 = %s", (letter,))

    count_of_letter_in_position4 = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) AS count_of_letter_in_position5 FROM words WHERE letter5 = %s", (letter,))

    count_of_letter_in_position5 = cursor.fetchone()[0]

    # close the connection
    close(conn)

    letter_frequency = [count_of_letter_in_position1, count_of_letter_in_position2, count_of_letter_in_position3, count_of_letter_in_position4, count_of_letter_in_position5]

    return letter_frequency


def insert_data(letter, letter_frequency):
    """
    Insert the frequency of a letter in each position of a word into the database.

    Args:
    - letter: The letter to insert the frequency of.
    - letter_frequency: A list of the frequency of the letter in each position of a word.

    Returns:
    - None
    """

    # do a query to insert the data into the database
    conn, cursor = connect()
    cursor.execute("""
                UPDATE statistics2
                SET position1 = %s, position2 = %s, position3 = %s, position4 = %s, position5 = %s
                WHERE letter = %s
            """, (letter_frequency[0], letter_frequency[1], letter_frequency[2], letter_frequency[3], letter_frequency[4], letter))

    # Commit the transaction
    conn.commit()

    # close the connection

    close(conn)


def create_letter_frequency():
    """
    Create the letter frequency table.

    Args:
    - None

    Returns:
    - None
    """
    # get all the letters
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # loop through all the letters
    for letter in letters:
        # check if the letter is in the database
        conn, cursor = connect()
        cursor.execute("SELECT letter FROM statistics2 WHERE letter = %s", (letter,))
        if cursor.fetchone() is None:
            # get the frequency of the letter
            letter_frequency = get_letter_frequency(letter)
            # insert the data into the database
            insert_data(letter, letter_frequency)
        else:
            print(f"The letter '{letter}' is already in the database.")
        close(conn)


# Run the function to create the letter frequency table
create_letter_frequency()
