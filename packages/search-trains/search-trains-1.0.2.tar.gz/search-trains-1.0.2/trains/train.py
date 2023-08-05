from tabulate import tabulate
from train_functions import *
import sys
import os


def show(msg, function, headers, tablefmt='grid', **kwargs):

    """This Function used to add prompt messages and fetching the details from train_functions
    then returns the output.

    """

    try:
        if kwargs:
            while True:
                keyword = kwargs['keyword'](msg + ': ')
                if keyword:
                    trains_list = fetch_train_suggestions(keyword)
                    if 'no connection' in trains_list:
                        print '''
                            \nConnection Error!!!

                            Possible Reasons:

                                1. Check your Network connection is turned off.
                                2. Check your Internet Connection.
                                3. Server  maybe exceeded with max requests, try again after some time.
                                '''
                        sys.exit()

                    elif not trains_list:
                        continue

                    print tabulate(trains_list, headers=['STATION CODE', 'STATION NAME'], tablefmt=tablefmt)
                    while True:
                        option = raw_input('\n[!]Choose an option: ').strip().upper()
                        if option:
                            return option
        else:
            print '\n\nChoose a %s: ' % msg
            print tabulate(list(function()), headers=headers, tablefmt=tablefmt)
            while True:
                option = raw_input('\n[!]Choose an option: ').strip().upper()
                if option:
                    return option
    except KeyboardInterrupt:
        print '\n'
        sys.exit()


def main():

    while True:
        print '\n'
        print 'Welcome to Train Availability Checking'.center(70, '*')

        print '@@Coded By: Naveen Tummidi\n'

        from_code = show('\nStarting Station Code/Name(Ex:CHE/Srikakulam)', fetch_train_suggestions, ['STATION CODE', 'STATION NAME'], keyword=raw_input)
        to_code = show('\nEnding Station Code/Name(Ex:BZA/Vijayawada)', fetch_train_suggestions, ['STATION CODE', 'STATION NAME'], keyword=raw_input)
        date_range = show('Date Value(Ex:1)', get_travel_dates, ['VALUE', 'DATE RANGE'])
        travel_class = show('Class(Ex: SL)', get_travel_classes, ['CLASS', 'CLASS NAME'])

        available_trains = list(search_trains(from_code, to_code, travel_class=travel_class, date_range=date_range))
        if not available_trains[0]:
            print 'No Trains found on this Route'
            print tabulate(available_trains, headers=['TRAIN NO', 'TRAIN NAME', 'DEPARTURE TIME', 'ARRIVAL TIME'], tablefmt='grid')
            return

        print tabulate(available_trains, headers=['TRAIN NO', 'TRAIN NAME', 'DEPARTURE TIME', 'ARRIVAL TIME'], tablefmt='grid')

        while True:
            try:
                train_no = raw_input('\n[+]Enter a Train number for Train Details(Ex:06337): ').strip().lower()
                if not train_no:
                    continue

                else:
                    train_details = get_train_information(train_no)
                    print tabulate(list(train_details), headers=['TRAIN NO', 'TRAIN NAME', 'START STATION', 'END STATION', 'RUNNING DAYS', 'TRAVEL CLASS', 'TRAIN TYPE'], tablefmt='grid')

                    feedback = raw_input('\ntype back to go to main menu or type quit to exit: ')
                    if feedback.lower().strip('"') != 'quit':
                        os.system('clear')
                        break
                    else:
                        return
            except KeyboardInterrupt:
                return


if __name__ == '__main__':
    main()
