from database_connection import connect, close
from psycopg2 import Error


def insert_word(cursor, word):
    """
    Insert a word into the Words table.

    Args:
    - cursor: psycopg2 cursor object for database operations.
    - word: string, the word to insert into the database.

    Returns:
    - None
    """
    if len(word) == 5:
        try:
            cursor.execute(
                "INSERT INTO Words (word, letter1, letter2, letter3, letter4, letter5) VALUES (%s, %s, %s, %s, %s, %s)",
                (word, word[0], word[1], word[2], word[3], word[4])
            )
        except (Exception, Error) as error:
            print("Error while inserting data:", error)


def main(file_path):
    """
    Main function to read a file containing words and insert each word into the database.

    Args:
    - file_path: string, path to the text file containing words.

    Returns:
    - None
    """
    # Connect to the database
    conn, cursor = connect()

    # Read the file
    with open(file_path, 'r') as file:
        words = file.readlines()

    # Insert each word into the database
    for word in words:
        word = word.strip()  # Remove any surrounding whitespace
        insert_word(cursor, word)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    close(conn)


main('Data/words.txt')
