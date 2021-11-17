
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils import timing_decorator

@timing_decorator
def process_line(line, pipeline):
    pass

@timing_decorator
def process_file(filename: str, pipeline):
    with open(filename, 'r') as f:
        f.readline() # ignore header
        for line in f:
            process_line(line, pipeline)


def main():
    process_file("")

if __name__ == '__main__':
    main()