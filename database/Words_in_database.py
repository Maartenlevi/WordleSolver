from database_connection import connect, close
from psycopg2 import Error


# Function to insert a word into the Words table
def insert_word(cursor, word):
    if len(word) == 5:
        try:
            cursor.execute(
                "INSERT INTO Words (word, letter1, letter2, letter3, letter4, letter5) VALUES (%s, %s, %s, %s, %s, %s)",
                (word, word[0], word[1], word[2], word[3], word[4])
            )
        except (Exception, Error) as error:
            print("Error while inserting data", error)


def main(file_path):
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

main('/database/words.txt')
