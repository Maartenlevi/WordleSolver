import tkinter as tk
import os
from create_graphs import create_graphs, create_ranking, create_general_statistics, create_letter_heatmap
from Algorithm import algorithm


def on_focus_in(event):
    if starting_word_entry.get() == "Input a starting word...":
        starting_word_entry.delete(0, tk.END)
        starting_word_entry.config(fg='black')


def on_focus_out(event):
    if starting_word_entry.get() == "" or starting_word_entry.get() == "Input a starting word...":
        starting_word_entry.delete(0, tk.END)
        starting_word_entry.insert(0, "Input a starting word...")
        starting_word_entry.config(fg='#4d4d4d')


def load_graph(starting_word):
    starting_word = starting_word.capitalize()
    # Check if the graph image exists
    if os.path.exists(f'Data/Graphs/{starting_word}_wins_on_turns.png'):
        # Load the graph image
        graph_image = tk.PhotoImage(file=f'Data/Graphs/{starting_word}_wins_on_turns.png')
        return graph_image
    else:
        # Create the graph image if it does not exist
        try:
            create_graphs(starting_word)
            graph_image = tk.PhotoImage(file=f'Data/Graphs/{starting_word}_wins_on_turns.png')
            return graph_image
        except ValueError as e:
            print(e)
    return None


def load_ranking_list(starting_word):
    try:
        ranking_list, amount_of_words = create_ranking(starting_word)
        return ranking_list, amount_of_words
    except ValueError as e:
        print(e)
        return None


def load_general_statistics(starting_word):
    try:
        general_statistics = create_general_statistics(starting_word)
        return general_statistics
    except ValueError as e:
        print(e)
        return None


def load_letter_heatmap():
    # Check if the graph image exists
    if os.path.exists(f'Data/Graphs/letter_heatmap.png'):
        # Load the graph image
        graph_image = tk.PhotoImage(file=f'Data/Graphs/letter_heatmap.png')
        return graph_image
    else:
        # Create the graph image if it does not exist
        try:
            create_letter_heatmap()
            graph_image = tk.PhotoImage(file=f'Data/Graphs/letter_heatmap.png')
            return graph_image
        except ValueError as e:
            print(e)
    return None


def display_graph(graph_image, frame):
    # Clear previous contents of the frame (if any)
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a label to display the graph image
    graph_label = tk.Label(frame, image=graph_image)
    graph_label.image = graph_image  # Keep reference to prevent garbage collection
    graph_label.pack(fill="both", expand=True)  # Adjust packing based on your layout


def display_ranking_list(ranking_list, amount_of_words, frame):
    # Clear previous contents of the frame (if any)
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a label for the ranking title
    title_label = tk.Label(frame, text="Ranking:", bg='#D9D9D9', font=('Inter', 30, "bold"),
                           anchor='center', justify='left')
    title_label.pack(fill="x", pady=10)

    # Create a label for each ranking entry with the actual rank
    for starting_word in ranking_list:
        rank_label = tk.Label(frame, text=f"{starting_word[0]}. {starting_word[1]}", bg='#D9D9D9',
                              font=('Inter', 20, "italic"), anchor='center', justify='left')
        rank_label.pack(fill="x", pady=10)

    # create a label on the bottom right saying how many words are in the ranking
    amount_label = tk.Label(frame, text=f"Amount of words in the ranking: {amount_of_words}", bg='#D9D9D9', font=('Inter', 10, 'italic'),
                            anchor='w', justify='left')
    amount_label.pack(fill="x", pady=10, padx=10)

    # create a label on the bottom left saying what the ranking is based on
    description_label = tk.Label(frame, text="Based on: \nAverage amount of guesses needed to win,\n"
                                             "the win rate and how many words are "
                                             "\nstill possible after the first turn.",
                                 bg='#D9D9D9', font=('Inter', 10, 'italic'), anchor='w', justify='left')
    description_label.pack(fill="x", pady=10, padx=10)


def display_general_statistics(general_statistics):
    # Clear previous contents of the frame (if any)
    for widget in top_rectangle1.winfo_children():
        widget.destroy()

    for widget in top_rectangle2.winfo_children():
        widget.destroy()

    for widget in top_rectangle3.winfo_children():
        widget.destroy()

    for widget in title_rectangle.winfo_children():
        widget.destroy()

    general_statistics = general_statistics
    percentage_of_words_eliminated = round((general_statistics[5] - general_statistics[3]) / general_statistics[5] * 100, 2)
    # Create a label for the statistics title
    title_label = tk.Label(title_rectangle, text="General statistics:", bg='#D9D9D9', font=('Inter', 20, "bold"),
                           anchor='center', justify='left')
    title_label.pack(fill="x", pady=10)

    # Create a label for each statistic entry
    statistic1_label = tk.Label(top_rectangle1, text=f"Win rate: {general_statistics[0]}%\n"
                                f"Average amount of turns: {general_statistics[1]}",
                                bg='#D9D9D9', font=('Inter', 13, "italic"), anchor='w', justify='left')
    statistic1_label.pack(fill="x", pady=5, padx=10)

    statistic2_label = tk.Label(top_rectangle2, text=f"Starting word eliminations: {percentage_of_words_eliminated}%\n"
                                f"Median number of turns: {general_statistics[2]}",
                                bg='#D9D9D9', font=('Inter', 13, "italic"), anchor='w', justify='left')
    statistic2_label.pack(fill="x", pady=5, padx=10)

    statistic3_label = tk.Label(top_rectangle3, text=f"Execution time per game: {round(general_statistics[6], 3)} seconds\n"
                                f"Total execution time: {round(general_statistics[4])} seconds",
                                bg='#D9D9D9', font=('Inter', 13, "italic"), anchor='w', justify='left')
    statistic3_label.pack(fill="x", pady=5, padx=10)


def display_letter_heatmap(letter_heatmap):
    # Clear previous contents of the frame (if any)
    for widget in rectangle3.winfo_children():
        widget.destroy()

    # Create a label to display the graph image
    graph_label = tk.Label(rectangle3, image=letter_heatmap)
    graph_label.image = letter_heatmap  # Keep reference to prevent garbage collection
    graph_label.pack(fill="both", expand=True)  # Adjust packing based on your layout


def on_enter(event):
    starting_word = starting_word_entry.get()
    starting_word = starting_word.capitalize()

    # check if the starting word is 5 characters long
    if len(starting_word) != 5:
        return

    if starting_word and starting_word != "Input a starting word...":
        graph_image = load_graph(starting_word)
        ranking_list, amount_of_words = load_ranking_list(starting_word)
        general_statistics = load_general_statistics(starting_word)
        letter_heatmap = load_letter_heatmap()

        if graph_image:
            # Display the graph image in one of the rectangles (example: rectangle1)
            display_graph(graph_image, rectangle1)  # Modify to display in other rectangles as needed

        if ranking_list:
            # Display the ranking list in another rectangle (example: rectangle2)
            display_ranking_list(ranking_list, amount_of_words, rectangle2)

        if general_statistics:
            # Display the general statistics in another rectangle (example: rectangle3)
            display_general_statistics(general_statistics)

        if letter_heatmap:
            # Display the letter heatmap in another rectangle (example: rectangle3)
            display_graph(letter_heatmap, rectangle3)

        else:
            # Run the algorithm if data is not available
            algorithm(starting_word)
            graph_image = load_graph(starting_word)
            display_ranking_list(ranking_list, amount_of_words, rectangle2)
            display_general_statistics(general_statistics)
            display_letter_heatmap(letter_heatmap, rectangle3)

            if graph_image:
                # Display the graph image in one of the rectangles
                display_graph(graph_image, rectangle1)  # Modify to display in other rectangles as needed

            if ranking_list:
                # Display the ranking list in another rectangle (example: rectangle2)
                display_ranking_list(ranking_list, amount_of_words, rectangle2)

            if general_statistics:
                # Display the general statistics in another rectangle (example: rectangle3)
                display_general_statistics(general_statistics)

            if letter_heatmap:
                # Display the letter heatmap in another rectangle (example: rectangle3)
                display_graph(letter_heatmap, rectangle3)

    # Reset the entry field to placeholder text and color
    starting_word_entry.delete(0, tk.END)
    starting_word_entry.insert(0, "")
    starting_word_entry.config(fg='#4d4d4d')


# Create the main window
root = tk.Tk()
root.title("WordleSolver")
root.geometry("1800x900")
root.configure(bg='white')

# Title label
title_label = tk.Label(root, text="WordleSolver", font=("Inter", 50, "bold"), bg='white', anchor='center')
title_label.place(x=450, y=9, width=900, height=115)

# Starting word section with label and entry
starting_word_label = tk.Label(root, text="Starting word", font=('Inter', 30, "bold"), anchor='center', bg='#FFFFFF')
starting_word_label.place(x=64, y=104, width=295, height=45)

# Entry for the starting word and add a placeholder
starting_word_entry = tk.Entry(root, font=('Inter', 15, "italic"), bg='#D9D9D9', fg='#4d4d4d')
starting_word_entry.place(x=64, y=156, width=295, height=45)
starting_word_entry.insert(0, "Input a starting word...")

# Event bindings
starting_word_entry.bind("<FocusIn>", on_focus_in)
starting_word_entry.bind("<FocusOut>", on_focus_out)
starting_word_entry.bind("<Return>", on_enter)

# Rectangles for displaying graphs
rectangle1 = tk.Frame(root, bg='#D9D9D9')
rectangle1.place(x=64, y=336, width=500, height=500)

rectangle2 = tk.Frame(root, bg='#D9D9D9')
rectangle2.place(x=650, y=336, width=500, height=500)

rectangle3 = tk.Frame(root, bg='#D9D9D9')
rectangle3.place(x=1236, y=336, width=500, height=500)

# 3 small rectangles on top
top_rectangle1 = tk.Frame(root, bg='#D9D9D9')
top_rectangle1.place(x=650, y=216, width=362, height=77)

top_rectangle2 = tk.Frame(root, bg='#D9D9D9')
top_rectangle2.place(x=1012, y=216, width=362, height=77)

top_rectangle3 = tk.Frame(root, bg='#D9D9D9')
top_rectangle3.place(x=1374, y=216, width=362, height=77)

# title rectangle for general statistics
title_rectangle = tk.Frame(root, bg='#D9D9D9')
title_rectangle.place(x=650, y=156, width=1086, height=60)

# Start the main loop
root.mainloop()
