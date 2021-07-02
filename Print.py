from termcolor import colored


def print_error(text):
    print(colored(f'-------------------\n{text}\nPlease try again\n-------------------',
                  'red'))


def print_success(text):
    print(colored(f'--------------------\n{text}!\n--------------------', 'blue'))
