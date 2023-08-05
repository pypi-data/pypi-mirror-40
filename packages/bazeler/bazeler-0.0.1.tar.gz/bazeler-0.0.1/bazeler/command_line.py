import argparse
import sys
from bazeler import bazilla

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root')
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--search_paths', default='')
    parser.add_argument('--permissive', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--ignore', default='', type=str, help='Comma-delimited targets to ignore')
    sys.exit(bazilla.bazilla(**vars(parser.parse_args())))
