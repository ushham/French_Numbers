import argparse
import number_generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run french numbers code.')
    parser.add_argument('--mn', metavar='min_N', type=int, default=0, help='The min number that you will be asked (default 0)')
    parser.add_argument('--mx', metavar='max_N', type=int, default=100, help='The max number that you will be asked (default 100)')
    parser.add_argument('--r', metavar='--read_files', default=False, action='store', help='Allows you to choose if files are read, or generated (default)')
    parser.add_argument('--e', metavar='--export_data', default=True, action='store', help='Choose whether data is exported (export is default)')

    args = parser.parse_args()

    x = number_generator.Number_Gen(args.mn, args.mx, read_files=args.r, export_data=args.e)
    x.export_data()