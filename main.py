import logging
import coloredlogs
import sys
import traceback

from p2sh import p2sh
from p2wsh import p2wsh
from p2wsh_over_p2sh import p2wsh_over_p2sh
from p2tr_musig_option_1 import p2tr_musig_option_1
from p2tr_musig_option_2 import p2tr_musig_option_2
from p2tr_musig_option_3 import p2tr_musig_option_3
from p2tr_musig_option_4 import p2tr_musig_option_4


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(name='mylogger')


coloredlogs.install(logger=logger)
logger.propagate = False

coloredFormatter = coloredlogs.ColoredFormatter(
    fmt='%(message)s',
    level_styles=dict(
        debug=dict(color='white'),
        info=dict(color='blue'),
        warning=dict(color='yellow', bright=True),
        error=dict(color='red', bold=True, bright=True),
        critical=dict(color='black', bold=True, background='red'),
    ),
    field_styles=dict(
        asctime=dict(color='white'),
    )
)

ch = logging.StreamHandler(stream=sys.stdout)
ch.setFormatter(fmt=coloredFormatter)
logger.addHandler(hdlr=ch)
logger.setLevel(level=logging.INFO)

# logger.debug(msg="this is a debug message")
# logger.info(msg="this is an info message")
# logger.warning(msg="this is a warning message")
# logger.error(msg="this is an error message")
# logger.critical(msg="this is a critical message")

def main():
    print("########################################")
    print("Please select one of the following options")
    print("Please enter 1 for P2SH M of N")
    print("Please enter 2 for P2WSH M of N")
    print("Please enter 3 for P2WSH over P2SH M of N")
    print("Please enter 4 for P2TR")
    
    try:
        choice = int(input("Input: "))
        print("")
        if choice > 4 or choice < 1:
            raise Exception("Invalid Choice")
        if choice == 1:
            print("Executing P2SH M of N")
            p2sh(logger)
        elif choice == 2:
            print("Executing P2WSH")
            p2wsh(logger)
        elif choice == 3:
            print("Executing P2WSH over P2SH")
            p2wsh_over_p2sh(logger)
        elif choice == 4:
            print("Please enter 1 for choice 1")
            print("Please enter 2 for choice 2")
            print("Please enter 3 for choice 3")
            print("Please enter 4 for choice 4")
            print("Please enter 5 for choice 5")
            print("Please enter 6 for choice 6")
            choice = int(input("Input: "))
            print("")
            if choice > 6 or choice < 1:
                raise Exception("Invalid Choice")
            if choice == 1:
                print("Executing P2SH M of N")
                p2tr_musig_option_1(logger)
            elif choice == 2:
                print("Executing P2WSH")
                p2tr_musig_option_2(logger)
            elif choice == 3:
                print("Executing P2WSH")
                p2tr_musig_option_3(logger)
            elif choice == 4:
                print("Executing P2WSH")
                p2tr_musig_option_4(logger)
            elif choice == 5:
                print("Executing P2WSH")
                p2wsh(logger)
            elif choice == 6:
                print("Executing P2WSH")
                p2wsh(logger)
        else:
            raise Exception("Invalid Choice")
    except Exception as e:
        logger.error(msg=str(e))
        traceback.print_exc()
        # print(str(e))

if __name__ == '__main__':
    main()
