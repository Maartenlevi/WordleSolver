import tkinter as tk
import os
from Data.create_graphs import create_graphs, create_ranking, create_general_statistics, create_letter_heatmap, create_brute_force_statistics
from MiniMax import algorithm


def clear_frame(frame):
    """Clears all widgets (children) from a tkinter frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def on_focus_in(event):
    """Clear the entry field when focused and change the text color."""
    if starting_word_entry.get() == "Input a starting word...":
        starting_word_entry.delete(0, tk.END)
        starting_word_entry.config(fg='black')


def on_focus_out(event):
    """Reset the entry field to placeholder text and color."""
    if starting_word_entry.get() == "" or starting_word_entry.get() == "Input a starting word...":
        starting_word_entry.delete(0, tk.END)
        starting_word_entry.insert(0, "Input a starting word...")
        starting_word_entry.config(fg='#4d4d4d')


def load_graph(starting_word):
    """Loads or creates a graph image based on the starting word."""
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
    """Loads or creates a ranking list based on the starting word."""
    try:
        ranking_list, amount_of_words = create_ranking(starting_word)
        return ranking_list, amount_of_words
    except ValueError as e:
        print(e)
        return None


def load_general_statistics(starting_word):
    """Loads or creates general statistics based on the starting word."""
    try:
        general_statistics = create_general_statistics(starting_word)
        return general_statistics
    except ValueError as e:
        print(e)
        return None


def load_brute_force_statistics(starting_word):
    """Loads or creates brute force statistics based on the starting word."""
    try:
        brute_force_statistics = create_brute_force_statistics(starting_word)
        return brute_force_statistics
    except ValueError as e:
        print(e)
        return None


def load_letter_heatmap():
    """Loads or creates a letter heatmap."""
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
    """Display the graph image in the specified frame."""
    # Clear previous contents of the frame (if any)
    clear_frame(frame)
    # Create a label to display the graph image
    graph_label = tk.Label(frame, image=graph_image)
    graph_label.image = graph_image  # Keep reference to prevent garbage collection
    graph_label.pack(fill="both", expand=True)  # Adjust packing based on your layout


def display_ranking_list(ranking_list, amount_of_words, frame):
    """Display the ranking list in the specified frame."""
    # Clear previous contents of the frame (if any)
    clear_frame(frame)

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


def display_general_statistics(general_statistics, brute_force_statistics):
    """Display the general statistics in the specified frame."""
    # Clear previous contents of the frame (if any)
    clear_frame(top_rectangle1)
    clear_frame(top_rectangle2)
    clear_frame(top_rectangle3)
    clear_frame(title_rectangle)

    general_statistics = general_statistics
    brute_force_statistics = brute_force_statistics
    percentage_of_words_eliminated = round((general_statistics[5] - general_statistics[3]) / general_statistics[5] * 100, 2)

    # Create a label for the statistics title
    title_label = tk.Label(title_rectangle, text="General statistics(Minimax vs Brute Force):", bg='#D9D9D9', font=('Inter', 20, "bold"),
                           anchor='center', justify='left')
    title_label.pack(fill="x", pady=10)

    # Create a label for each statistic entry
    statistic1_label = tk.Label(top_rectangle1, text=f"Win rate: {general_statistics[0]}%, {brute_force_statistics[0]}%, Δ is {brute_force_statistics[0] - general_statistics[0]}%\n"
                                f"Average amount of turns: {general_statistics[1]}, {brute_force_statistics[1]}, Δ is {brute_force_statistics[1] - general_statistics[1]} turns",
                                bg='#D9D9D9', font=('Inter', 10, "italic"), anchor='w', justify='left')
    statistic1_label.pack(fill="x", pady=5, padx=10)

    statistic2_label = tk.Label(top_rectangle2, text=f"Starting word eliminations: {percentage_of_words_eliminated}% or {general_statistics[3]} words left\n"
                                f"Median number of turns: {general_statistics[2]}, {brute_force_statistics[2]}, Δ is {brute_force_statistics[2] - general_statistics[2]} turns",
                                bg='#D9D9D9', font=('Inter', 10, "italic"), anchor='w', justify='left')
    statistic2_label.pack(fill="x", pady=5, padx=10)

    statistic3_label = tk.Label(top_rectangle3, text=f"Execution time per game: {round(general_statistics[6], 3)}s, {round(brute_force_statistics[6], 3)}s, Δ is {round(general_statistics[6], 3) - round(brute_force_statistics[6], 3)}s\n"
                                f"Total execution time: {round(general_statistics[4])}s, {round(brute_force_statistics[4])}s, Δ is {round(general_statistics[4]) - round(brute_force_statistics[4])}s\n",
                                bg='#D9D9D9', font=('Inter', 10, "italic"), anchor='w', justify='left')
    statistic3_label.pack(fill="x", pady=5, padx=10)


def display_letter_heatmap(letter_heatmap):
    """Display the letter heatmap in the specified frame."""
    # Clear previous contents of the frame (if any)
    clear_frame(rectangle3)

    # Create a label to display the graph image
    graph_label = tk.Label(rectangle3, image=letter_heatmap)
    graph_label.image = letter_heatmap  # Keep reference to prevent garbage collection
    graph_label.pack(fill="both", expand=True)  # Adjust packing based on your layout


def on_enter(event):
    """Run the algorithm when the Enter key is pressed."""
    starting_word = starting_word_entry.get()
    starting_word = starting_word.capitalize()

    # check if the starting word is 5 characters long and if it isn't stop the function
    if len(starting_word) != 5:
        return

    if starting_word and starting_word != "Input a starting word...":
        graph_image = load_graph(starting_word)
        ranking_list, amount_of_words = load_ranking_list(starting_word)
        general_statistics = load_general_statistics(starting_word)
        brute_force_statistics = load_brute_force_statistics(starting_word)
        letter_heatmap = load_letter_heatmap()

        if graph_image:
            # Display the graph image in one of the rectangles (example: rectangle1)
            display_graph(graph_image, rectangle1)  # Modify to display in other rectangles as needed

        if ranking_list:
            # Display the ranking list in another rectangle (example: rectangle2)
            display_ranking_list(ranking_list, amount_of_words, rectangle2)

        if general_statistics:
            # Display the general statistics in another rectangle (example: rectangle3)
            display_general_statistics(general_statistics, brute_force_statistics)

        if brute_force_statistics:
            # Display the general statistics in another rectangle (example: rectangle3)
            display_general_statistics(general_statistics, brute_force_statistics)

        if letter_heatmap:
            # Display the letter heatmap in another rectangle (example: rectangle3)
            display_graph(letter_heatmap, rectangle3)

        else:
            # Run the algorithm if data is not available
            algorithm(starting_word)
            graph_image = load_graph(starting_word)
            display_ranking_list(ranking_list, amount_of_words, rectangle2)
            display_general_statistics(general_statistics, brute_force_statistics)
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


"""Application starts here"""
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
