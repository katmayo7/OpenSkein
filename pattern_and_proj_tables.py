import pandas as pd
import os
import datetime as dt
from tabulate import tabulate

class PatternProjTables:

    def __init__(self, metric=False):
        self.patterns_file = 'data/patterns_table.pkl'
        self.projects_file = 'data/projects_table.pkl'

        self.project_table = None
        self.pattern_table = None

        self.metric = metric

    def load_data(self):
        if os.path.exists(self.patterns_file):
            self.pattern_table = pd.read_pickle(self.patterns_file)
            self.project_table = pd.read_pickle(self.projects_file)
        else:
            self.pattern_table = pd.DataFrame(columns=['DATE ADDED', 'PATTERN NAME', 'SUGGESTED YARN WEIGHT', 'SUGGESTED HOOK SIZE', 'TOTAL AMOUNT OF YARN (YDS)', 'TOTAL AMOUNT OF YARN (MS)', 'CATEGORY', 'NOTES', 'SOURCE'])            
            pattern_data_types = {'PATTERN NAME': 'str', 'SUGGESTED YARN WEIGHT': 'int', 'SUGGESTED HOOK SIZE': 'float', 'TOTAL AMOUNT OF YARN (YDS)': 'float', 'TOTAL AMOUNT OF YARN (MS)': 'float', 'CATEGORY': 'str', 'NOTES': 'str', 'SOURCE': 'str'}
            self.pattern_table = self.pattern_table.astype(pattern_data_types)
            self.pattern_table['DATE ADDED'] = pd.to_datetime(self.pattern_table['DATE ADDED'])

            self.project_table = pd.DataFrame(columns=['DATE LOGGED', 'PROJECT NAME', 'PATTERN NAME', 'YARN(S) USED (BRAND+COLOR)', 'YARN WEIGHT', 'AMOUNT OF YARN (PER YARN)', 'TOTAL AMOUNT OF YARN (YDS)', 'TOTAL AMOUNT OF YARN (MS)', 'DYE LOTS (PER YARN)',
                                                       'HOOK SIZE USED', 'MACHINE WASHABLE', 'NOTES'])
            project_data_types = {'PROJECT NAME': 'str', 'PATTERN NAME': 'str', 'YARN(S) USED (BRAND+COLOR)': 'str', 'YARN WEIGHT': 'int', 'AMOUNT OF YARN (PER YARN)': 'str', 'TOTAL AMOUNT OF YARN (YDS)': 'float', 'TOTAL AMOUNT OF YARN (MS)': 'float',
                                  'DYE LOTS (PER YARN)': 'str', 'HOOK SIZE USED': 'float', 'MACHINE WASHABLE': 'bool', 'NOTES': 'str'}
            self.project_table = self.project_table.astype(project_data_types)
            self.project_table['DATE LOGGED'] = pd.to_datetime(self.project_table['DATE LOGGED'])

    
    def save_data(self):
        if not os.path.exists('data/'):
            os.mkdir('data/')
        
        self.pattern_table.to_pickle(self.patterns_file)
        self.project_table.to_pickle(self.projects_file)

    def print_table(self, table):
        print('***********************************************************************************************************************************************************************************************************************')

        print_cols = []
        if self.metric:
            print_cols = [c for c in table.columns if '(YDS)' not in c]
        else:
            print_cols = [c for c in table.columns if '(MS)' not in c]
        
        with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
            print(table[print_cols])
        print('***********************************************************************************************************************************************************************************************************************')

    def get_project(self):

        return self.project_table

    def get_pattern(self):
        
        return self.pattern_table

    # search_name should be 'pattern name' if table is pattern table and 'project name' if table is project table
    def check_exists(self, table, search_name, pattern=True):
        if pattern:
            tmp_i = table[table['PATTERN NAME'] == search_name].index.tolist()
        else:
            tmp_i = table[table['PROJECT NAME'] == search_name].index.tolist()
        
        if len(tmp_i) > 1:
            print('!! Error: More than one entry matches this name.!!')
        
        if len(tmp_i) > 0:
            return tmp_i[0]

        return -1

    # combine new and old notes
    def format_long_form(self, old_info, new_info):
        if ', ' in old_info:
            old_info = set(old_info.split(', '))
        else:
            old_info = set(old_info.split(','))
        
        if ', ' in new_info:
            new_info = set(new_info.split(', '))
        else:
            new_info = set(new_info.split(','))

        union = list(old_info.union(new_info))
        union = [s + ', ' for s in union]

        return ''.join(union)

    # handles updates if entry already exists
    def add_helper(self, table, new_entry, testing=False, pattern_search=True):
        if pattern_search:
            tmp = self.check_exists(table, new_entry['PATTERN NAME'], pattern_search)
        else:
            tmp = self.check_exists(table, new_entry['PROJECT NAME'], pattern_search)

        if tmp == -1:
            return new_entry,-1
        
        print('It looks like you are trying to add a duplicate. This pattern is already logged as:')
        with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
            print(table.loc[tmp])
        print()

        text_fields = list(table.select_dtypes(include='object').columns)
        date_fields = ['DATE ADDED', 'DATE LOGGED']

        # update information for an existing entry
        info_diff = {}
        print('The following information will be updated: ')

        for col in table.columns.tolist():
            # check if this information changes with the update
            if col in text_fields and new_entry[col] != None:
                new_entry[col] = new_entry[col].lower()

            if col not in date_fields and new_entry[col] != table.loc[tmp][col] and new_entry[col] != None:
                info_diff[col] = new_entry[col]
                print(col, ': ', info_diff[col])

                # handle changes to notes section (add on or rewrite)
                result = None

                if col == 'NOTES' and not testing:
                    # if not testing code, let user decide how to handle
                    while result != 'overwrite' and result != 'extend':
                        result = input('Would you like to overwrite or extend previously logged notes? (overwrite/extend): ').lower()
                
                # if extending or testing, replace info_diff['NOTES'] with a combination of old and new Notes info
                if col == 'NOTES' and (result == 'extend' or testing == True):
                    info_diff[col] = self.format_long_form(table.loc[tmp]['NOTES'], new_entry['NOTES'])
            
        if len(info_diff) == 0:
            print('No information needs updating.')
            return None,tmp

        return info_diff,tmp
        
    def add_to_pattern(self, new_entry, run_test=False):
        # see if already exists, if so prep update steps
        new_data,ind = self.add_helper(self.pattern_table, new_entry, testing=run_test)

        if new_data == None:
            return

        # calculate meters from yards or vice versa if only one is provided
        yds_per_m = 1.09361
        ms_per_yd = 0.9144

        if 'TOTAL AMOUNT OF YARN (YDS)' in new_data and new_data['TOTAL AMOUNT OF YARN (YDS)'] == None:
            new_data['TOTAL AMOUNT OF YARN (YDS)'] = new_data['TOTAL AMOUNT OF YARN (MS)'] * yds_per_m
        elif 'TOTAL AMOUNT OF YARN (MS)' in new_data and new_data['TOTAL AMOUNT OF YARN (MS)'] == None:
            new_data['TOTAL AMOUNT OF YARN (MS)'] = new_data['TOTAL AMOUNT OF YARN (YDS)'] * ms_per_yd
        
        # updating an entry
        if ind > -1:
            for ne in new_data:
                self.pattern_table.loc[ind, ne] = new_data[ne]
        # adding a new entry
        else:
            new_data['DATE ADDED'] = dt.date.today()
            new_data['DATE ADDED'] = pd.to_datetime(new_data['DATE ADDED'])
            self.pattern_table.loc[len(self.pattern_table)] = new_data

    def add_to_project(self, new_entry, run_test=False):
        # required that the pattern is logged in the pattern database first
        pattern_i = self.check_exists(self.pattern_table, new_entry['PATTERN NAME'], True)

        if pattern_i == -1:
            print('** Error, must add pattern to pattern database before logging project!')
            return

        # see if already exists, if so prep update steps
        new_data,ind = self.add_helper(self.project_table, new_entry, testing=run_test, pattern_search=False)

        if new_data == None:
            return
        
        # calculate meters from yards or vice versa if only one is provided
        yds_per_m = 1.09361
        ms_per_yd = 0.9144

        if 'TOTAL AMOUNT OF YARN (YDS)' in new_data and new_data['TOTAL AMOUNT OF YARN (YDS)'] == None:
            new_data['TOTAL AMOUNT OF YARN (YDS)'] = new_data['TOTAL AMOUNT OF YARN (MS)'] * yds_per_m
        elif 'TOTAL AMOUNT OF YARN (MS)' in new_data and new_data['TOTAL AMOUNT OF YARN (MS)'] == None:
            new_data['TOTAL AMOUNT OF YARN (MS)'] = new_data['TOTAL AMOUNT OF YARN (YDS)'] * ms_per_yd
        
        # updating an entry
        if ind > -1:
            for ne in new_data:
                self.project_table.loc[ind, ne] = new_data[ne]
        # adding a new entry
        else:
            new_data['DATE LOGGED'] = dt.date.today()
            new_data['DATE LOGGED'] = pd.to_datetime(new_data['DATE LOGGED'])
            self.project_table.loc[len(self.project_table)] = new_data

    # remove by index or by pattern/project name
    def remove_table_entry(self, table, remove_i=None, remove_name=None, pattern_search=True):
        if remove_name != None:
            remove_i = self.check_exists(table, remove_name, pattern_search)
        
        table.drop(remove_i, inplace=True)