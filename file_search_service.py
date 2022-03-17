import csv
import pickle
import time
from os.path import exists


def load_instr_pickle(filename):
    instr_fd = open(filename, 'rb+')
    instr_dict = pickle.load(instr_fd)
    instr_fd.close()
    return instr_dict


def create_new_instr_pickle(filename):
    instr_fd = open(filename, 'wb')
    instr_dict = {'get_data': True, 'city_name': 'Seattle'}
    pickle.dump(instr_dict, instr_fd)
    instr_fd.close()
    return instr_dict


def create_new_output_pickle(filename):
    out_fd = open(filename, 'wb')
    out_dict = {'city_name': instr_share['city_name'], 'done': False, 'date': [], 'price': []}
    pickle.dump(out_dict, out_fd)
    out_fd.close()


def clean_output(filename):
    out_fd = open(filename, 'rb+')
    out_share = {'city_name': instr_share['city_name'], 'done': False, "date": [1], "price": [2]}
    pickle.dump(out_share, out_fd)
    out_fd.close()


instruction_filename = 'instruction_share_microservice'
output_filename = 'output_share_microservice'


while True:
    # Check if instructions file exists
    # if exists ? load file : create file
    if exists(instruction_filename):
        instr_share = load_instr_pickle(instruction_filename)
    else:
        instr_share = create_new_instr_pickle(instruction_filename)
    # App will request new search with dict 'get_data' boolean
    # dict['get_data'] ?  loop through csv file : sleep()
    if instr_share['get_data']:
        # check if file exists, similar to instruction file
        if exists(output_filename):
            clean_output(output_filename)
            out_fd = open(output_filename, 'wb')
            with open('data/history.csv') as csvfile:
                my_file = csv.reader(csvfile, delimiter=',')
                header = next(my_file)
                dates = header[5:]
                prices = []
                for row in my_file:
                    if row[2] == instr_share['city_name']:
                        prices = row[5:]
                        out_share = {'city_name': instr_share['city_name'], 'done': True, "date": dates, "price": prices}
                        pickle.dump(out_share, out_fd)
            out_fd.close()

        else:
            create_new_output_pickle(output_filename)

        time.sleep(.5)
