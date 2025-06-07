from subprocess import check_output

def print_contents_of_cwd():
    # print('the directory contains: ')
    return check_output(['ls']).split()   

# print(print_contents_of_cwd())