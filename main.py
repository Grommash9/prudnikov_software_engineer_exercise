import sys
import re
from models import CashMachine, InsufficientFounds

try:
    filename = sys.argv[1]
except IndexError:
    print('Please add the file name after the script file name. For example use python3 main.py input.txt')
    sys.exit(-1)


def get_file_data(file_name):
    try:
        with open(file_name, 'r') as input_file:
            file_data = input_file.read()
            return file_data.split('\n')
    except FileNotFoundError:
        print(f'Cant find file {file_name} please check the input!')
        sys.exit(-1)


def exchange_operation_processing(operation_command):
    banknote_amount = float(operation_command.split(" ")[-1])
    try:
        coins_to_give = my_cash_machine.exchange(banknote_amount)
    except InsufficientFounds:
        print('CANNOT EXCHANGE')
        return
    print(f"< {my_cash_machine.get_str_for_money_dicts([coins_to_give])}")


def load_operation_processing(operation_command):
    number_of_coins, type_of_coin = map(float, operation_command.split(" ")[1:])
    my_cash_machine.add_coins(type_of_coin, number_of_coins)


if __name__ == '__main__':
    my_cash_machine = CashMachine()

    input_data_list = get_file_data(filename)
    for operation_id, operation in enumerate(input_data_list):
        match = re.match(r'^LOAD \d+ \d+\.?\d{0,2}$|^EXCHANGE \d+$', operation)
        if not match:
            print(f'Please check operation input in line {operation_id + 1} because script cant recognise it')
            sys.exit(-1)
        print(f"> {operation}")
        if operation.startswith('LOAD'):
            load_operation_processing(operation)
        else:
            exchange_operation_processing(operation)
        print(f'= {str(my_cash_machine)}')
