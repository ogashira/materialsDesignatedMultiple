import sys
from sql_query import *
from program_flow import *

def main()->None:

    is_a:bool = False
    if len(sys.argv) > 1:
        if sys.argv[1] == '-a':
            is_a = True

    program_flow:object = ProgramFlow()
    program_flow.start(is_a)


if __name__ == '__main__':
    main()
