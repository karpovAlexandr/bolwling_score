from os.path import normpath

from bowling.bowling import BowlingGame

from bowling.bowling import BowlingGameInternational


class BowlingTournament(BowlingGame):
    def __init__(self):
        super().__init__()
        self.tour_results = ['Noname', 0]
        self.tour = None
        self.string_number = 0
        self.stats = {}

    def is_it_frame_string(self, line):
        line = line.split()
        players_name = line[0]
        game_result = line[1]
        game_score, game_result = self.run(game_result=game_result, string_number=self.string_number)
        if game_score > self.tour_results[1]:
            self.tour_results[0] = players_name
            self.tour_results[1] = game_score
        if players_name in self.stats.keys():
            self.stats[players_name][0] += 1
        else:
            self.stats[players_name] = [0, 0]
            self.stats[players_name][0] = 1
        return game_score, game_result, players_name

    def line_parser(self, line):
        if line.startswith('winner'):
            self.stats[self.tour_results[0]][1] += 1
            output = f'winner is {self.tour_results[0]} \n'
        elif line.startswith('### Tour'):
            self.tour = line[:-1]
            self.tour_results = ['Noname', 0]
            output = line
        elif line == '\n':
            output = line

        else:
            game_score, game_result, players_name = self.is_it_frame_string(line)
            player = f'{players_name:<10}'
            game = f'{game_result:^20}'
            score = f'{game_score:^6}'
            output = f'{player} {game} {score} \n'
        return output

    def write_file(self, tournament_file, output_file):
        with open(output_file, 'w', encoding='utf8') as outputfile:
            with open(tournament_file, 'r', encoding='utf8') as input_file:
                for line in input_file:
                    self.string_number += 1
                    output = self.line_parser(line)
                    outputfile.write(output)

    def sort_stat(self):
        stats = []
        for key, value in self.stats.items():
            new_dict = {
                'name': key,
                'games': value[0],
                'wins': value[1],
            }
            stats.append(new_dict)

        self.stats = sorted(stats, key=lambda x: x['wins'], reverse=True)

    def print_stats(self):
        self.sort_stat()
        print(f'+{"-":-^10}+{"-":-^18}+{"-":-^14}+')
        print(f'|{"Игрок": ^10}|{"сыграно матчей": ^18}|{"всего побед": ^14}|')
        print(f'+{"-":-^10}+{"-":-^18}+{"-":-^14}+')
        for player_stat in self.stats:
            print(f'|{player_stat["name"]: ^10}|{player_stat["games"]: ^18}|{player_stat["wins"]: ^14}|')
        print(f'+{"-":-^10}+{"-":-^18}+{"-":-^14}+')


class BowlingTournamentInternational(BowlingTournament, BowlingGameInternational):
    """класс для международных турниров по боулину"""


if __name__ == '__main__':
    file = normpath('../tournament.txt')
    tournament = BowlingTournament()
    tournament.write_file(tournament_file=file, output_file='tournament_result.txt')
    tournament.print_stats()
