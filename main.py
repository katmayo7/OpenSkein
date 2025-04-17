import yarn_tables

def view(table_names, filter=None):
    pass

def add(table_name):
    pass

def check_validity(input_string):
    pass

if __name__ == '__main__':

    """
    TO DO:
    --1) use functions to populate and work with databases [ done ]
    --2) interactive component to read input from command line to work with databases
    --3) develop front end UI to work with tables instead
    """
    set_metric = False

    yt = yarn_tables.YarnTables(metric=set_metric)
    yt.load_data()

    ci_input = None

    """
    --view tables
    ----just one
    ----separately
    ----multiple

    --add to a table
    ----specify which table
    ----input requested information
    ----same thing as modifying and deleting for now

    --
    """

    valid_inputs = ['exit', 'view', 'add', 'filter']

    while ci_input != 'exit':
        print('What would you like to do?')
        print('----view: to view tables')
        print('----add: to add to a table')
        print()

        ci_input = input('Type desired action: ')

        if ci_input == 'view':
            pass
        elif ci_input == 'add':
            pass



    #yt.save_data()
