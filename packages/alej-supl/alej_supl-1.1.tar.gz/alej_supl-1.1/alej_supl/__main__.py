import datetime
import argparse
from classes import Connection, PageNotFoundError
from functions import print_changes_per_day

def main():
    parser = argparse.ArgumentParser(description='A terminal app to show the supplementation for Gymnázium Nad Alejí school')

    parser.add_argument('-c', '--class_code', default=None,
                        help='Your class code.')
    parser.add_argument('-d', '--date', default=None,
                        help='Date in format "%%d%%m%%y"')
    parser.add_argument('-w', '--week', action='store_true',
                        help='Use if you want all changes for the next week.')

    parser.set_defaults(class_code='O8.B')

    args = parser.parse_args()

    if args.date:
        date = datetime.datetime.strptime(str(args.date), '%d%m%y')
    else:
        date = datetime.datetime.today()

    if args.week:
        for i in range(7):
            try:
                cur_date = (date + datetime.timedelta(days=i))
                conn = Connection(cur_date)
                print_changes_per_day(
                    cur_date, conn.get_changes(args.class_code))
            except PageNotFoundError:
                print(cur_date.strftime('%d, %b %Y'))
                print('   Page not found.')
    else:
        try:
            conn = Connection(date)
            print_changes_per_day(date, conn.get_changes(args.class_code))
        except PageNotFoundError:
            print(date.strftime('%d, %b %Y'))
            print('   Page not found.')


if __name__ == "__main__":
    main()
