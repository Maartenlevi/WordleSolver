# WordleSolver

## Description

WordleSolver is a Python project that aims to solve the Wordle game. It uses various algorithms and database connections to predict the best possible guess. The project also includes a graphical user interface (GUI) built with Tkinter to display the results.

## Required packages:

  - tkinter - For creating the graphical user interface (GUI).
  - os - For interacting with the operating system, such as checking if a file exists.
  - matplotlib - For creating graphs and heatmaps.
  - psycopg2 - For database connection

## Database setup

  1. Setup a database using the create scripts in "Data/Database setup".
  2. Make a file called "config.env" in which you put your database credentials, like so:
        DB_NAME = WordleSolver
        DB_USER = postgres
        DB_PASSWORD = '@your_password'
        DB_HOST = localhost
        DB_PORT = 5432
  3. Run Words_in_database.py, letter_frequency.py and run_words to fill the database with data.
  4. Run Main.py
