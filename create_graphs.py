from database_connection import connect, close
import matplotlib.pyplot as plt
import os


# Define Wordle colors
wordle_green = '#6aaa64'
wordle_yellow = '#c9b458'
wordle_gray = '#D9D9D9'

def create_wins_on_turns_graph(data, starting_word):
    # Get the number of wins for each turn
    wins = {1: data[8], 2: data[9], 3: data[10], 4: data[11], 5: data[12], 6: data[13]}
    turns = list(wins.keys())
    num_wins = list(wins.values())
    average = data[2]


    # Create the figure and axis with a size of 540x590 pixels
    fig, ax = plt.subplots(figsize=(490 / 100, 490 / 100), dpi=100)
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

    # Display the plot
    plt.show()

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
    close(conn)

    # check if the graphs are already in the Graphs folder and if it does return the graphs
    if os.path.exists(f'Data/Graphs/{starting_word}_wins_on_turns.png'):
        file_path = f'Data/Graphs/{starting_word}_wins_on_turns.png'
    else:
        create_wins_on_turns_graph(data, starting_word)


    return data


print(create_graphs('crane'))
