from Algorithm import algorithm, get_all_words
from Brute_force import brute_force
from database_connection import close, connect

# List of starting words to test
#words = get_all_words()

# get all words from the database that start with s
conn, cursor = connect()
cursor.execute("SELECT * FROM words WHERE word LIKE 's%'")
words = cursor.fetchall()
close(conn)

# Amount of words to test
amount_words = len(words)


for word in words:
    print(f"\nProcessing starting word: {word[1]} ({words.index(word) + 1}/{amount_words})")
    algorithm(word[1])
    brute_force(word[1])
