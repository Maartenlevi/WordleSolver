from database_connection import connect, close
import matplotlib.pyplot as plt
import os
from Algorithm import algorithm


# Define Wordle colors
wordle_green = '#6aaa64'
wordle_yellow = '#c9b458'
wordle_gray = '#D9D9D9'

def create_general_statistics(starting_word):
    # make sure the first letter is uppercase
    starting_word = starting_word.capitalize()

    # get the information from the database
    conn, cursor = connect()
    cursor.execute("SELECT win_rate, average_turns, median_turns, starting_word_eliminations, execution_time, total_games "
                   "FROM statistics WHERE starting_word = %s", (starting_word,))

    # get the data and put it into a list
    data = cursor.fetchone()
    if data is None:
        algorithm(starting_word)
        cursor.execute("SELECT win_rate, average_turns, median_turns, starting_word_eliminations, execution_time, total_games "
                       "FROM statistics WHERE starting_word = %s", (starting_word,))
        data = cursor.fetchone()

    close(conn)
    # put the data into a list
    general_statistics = []
    for i in range(len(data)):
        general_statistics.append(data[i])
    average_execution_time = data[4] / data[5]
    general_statistics.append(average_execution_time)

    return general_statistics
def create_ranking(starting_word):
    conn, cursor = connect()

    # Get the ranking of all starting words
    cursor.execute("""
           SELECT starting_word, win_rate, average_turns, starting_word_eliminations,
                  ROW_NUMBER() OVER (ORDER BY win_rate DESC, average_turns, starting_word_eliminations) AS rank
           FROM statistics
       """)

    rows = cursor.fetchall()
    close(conn)

    amount_words = len(rows)

    # Find the rank of the specified starting word
    rank = None
    for idx, row in enumerate(rows):
        if row[0] == starting_word:
            rank = row[4]
            break

    if rank is None:
        raise ValueError(
            f"The starting word '{starting_word}' is not in the database or there are not enough words for comparison.")

    # Get the two words above and two words below the specified starting word
    total_words = len(rows)
    if rank <= 2:
        start_idx = 0
        end_idx = 5
    elif rank >= total_words - 1:
        start_idx = total_words - 5
        end_idx = total_words
    else:
        start_idx = rank - 3
        end_idx = rank + 2

    ranking_list = rows[start_idx:end_idx]

    # Format the ranking list to only include rank and starting words
    formatted_ranking_list = [(row[4], row[0]) for row in ranking_list]
    return formatted_ranking_list, amount_words



def create_wins_on_turns_graph(data, starting_word):
    # Get the number of wins for each turn
    wins = {1: data[8], 2: data[9], 3: data[10], 4: data[11], 5: data[12], 6: data[13]}
    turns = list(wins.keys())
    num_wins = list(wins.values())
    average = data[2]


    # Create the figure and axis with a size of 540x590 pixels
    fig, ax = plt.subplots(figsize=(500 / 100, 500 / 100), dpi=100)
    fig.patch.set_facecolor(wordle_gray)
    ax.set_facecolor('white')

    # Create the bar chart
    bars = ax.bar(turns, num_wins, color=wordle_green)

    # Add a vertical line for the average number of turns and display the value
    plt.axvline(x=average, color=wordle_yellow, linestyle='--', linewidth=2)
    plt.text(float(average) + 0.1, max(num_wins) / 2, f'{average:.2f}', color='black', fontsize=10)

    # Add labels and title
    plt.xlabel('Number of turns', color='black')
    plt.ylabel('Number of wins', color='black')
    plt.title('Number of wins for turns', color='black')

    # Customize ticks
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')

    # Add horizontal grid lines
    plt.grid(True, which='major', linestyle='--', linewidth=0.5, color='black', alpha=0.7, axis='y')

    # Add values inside the bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height + 20),
                    ha='center', va='center', color='black', fontsize=10)

    # add a legend
    plt.legend(['Average number of turns', 'Number of wins'], loc='upper left', fontsize='small', facecolor=wordle_gray)

    # Adjust layout to make it fit better
    plt.tight_layout()

    # Save the plot in the Graphs folder in the data folder
    fig.savefig(f'Data/Graphs/{starting_word}_wins_on_turns.png')

def create_graphs(starting_word):
    # make sure the first letter is uppercase
    starting_word = starting_word.capitalize()

    # get the information from the database
    conn, cursor = connect()
    cursor.execute("SELECT * FROM statistics WHERE starting_word = %s", (starting_word,))


    # get the data and put it into a list
    data = cursor.fetchone()
    if data is None:
        close(conn)
        algorithm(starting_word)
        conn, cursor = connect()
        cursor.execute("SELECT * FROM statistics WHERE starting_word = %s", (starting_word,))
        data = cursor.fetchone()

    close(conn)

    # check if the graphs are already in the Graphs folder and if it does return the graphs
    if os.path.exists(f'Data/Graphs/{starting_word}_wins_on_turns.png'):
        file_path = f'Data/Graphs/{starting_word}_wins_on_turns.png'
    else:
        create_wins_on_turns_graph(data, starting_word)
