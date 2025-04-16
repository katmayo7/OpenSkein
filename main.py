import yarn_tables

if __name__ == '__main__':

    """
    TO DO:
    --1) use functions to populate and work with databases [ done ]
    --2) interactive component to read input from command line to work with databases
    --3) develop front end UI to work with tables instead
    """

    # write code for working with command line for these

    yt = yarn_tables.YarnTable()
    yt.load_data()

    yt.save_data()
