import psycopg2


# Function to insert a word into the Words table
def insert_word(cursor, word):
    if len(word) == 5:
        cursor.execute(
            "INSERT INTO Words (word, letter1, letter2, letter3, letter4, letter5) VALUES (%s, %s, %s, %s, %s, %s)",
            (word, word[0], word[1], word[2], word[3], word[4])
        )

def main():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="WordleSolver",
        user="postgres",
        password="@Hilversum02@"
    )
    cursor = conn.cursor()

    # Read the file
    with open('C:/Users/meijg/PycharmProjects/WordleSolver/Data/words.txt', 'r') as file:
        words = file.readlines()

    # Insert each word into the database
    for word in words:
        word = word.strip()  # Remove any surrounding whitespace
        insert_word(cursor, word)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

main()
