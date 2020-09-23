# -*- coding: utf-8 -*-


import argparse

from bowling_tournament.bowling_tournament import BowlingTournament, BowlingTournamentInternational
from bowling.bowling import conf_logger

parser = argparse.ArgumentParser(description='try to score bowling tournament results')
parser.add_argument('--input', type=str, action="store", dest='tournament_file', required=True,
                    help='result of bowling tournament')
parser.add_argument('--output', type=str, action="store", dest='output_file', required=True,
                    help='output file with results')
parser.add_argument('--intl', type=bool, action="store", dest='international_rules', required=False,
                    help='check rules')

try:
    conf_logger('t_logs.log')
    args = parser.parse_args()
    if args.international_rules:
        print('международные правила')
        bowling_tournament = BowlingTournamentInternational()
        bowling_tournament.write_file(tournament_file=args.tournament_file, output_file=args.output_file)
        bowling_tournament.print_stats()

    else:
        print('обычные правила')
        bowling_tournament = BowlingTournament()
        bowling_tournament.write_file(tournament_file=args.tournament_file, output_file=args.output_file)
        bowling_tournament.print_stats()

except SystemExit as err:
    print('Ошибка запуска скрипта:', err)

if __name__ == '__main__':
    pass
