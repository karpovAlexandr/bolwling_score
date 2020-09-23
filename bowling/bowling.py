#!/usr/bin/env python3
import logging
import re

from bowling.exceptions import BowlingError, InputError, FrameIsMoreThenNinePoints, StrikeOnSecondPositionOfFrame, \
    IncorrectFramesCount, FrameStartsWithSpare, NotLatinSymbol

log = logging.getLogger('bowling_tournament')


def conf_logger(logs_file):
    file_handler = logging.FileHandler(filename=logs_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    file_handler.setLevel(logging.ERROR)
    log.addHandler(file_handler)


class Game:
    """
    Base class for games
    """

    def __init__(self):
        pass

    def check_game_result_format(self, game_result):
        """
        проверяем формат записи результата игры
        :return:
        """
        pass

    def string_parser(self, game_result):
        """
        парсим строчку по каждому символу
        :return:
        """
        pass

    def get_score(self, game_result):
        """
        считаем очки
        :return:
        """
        pass


class BowlingGame(Game):
    def __init__(self):
        super().__init__()
        self.frames = 10
        self.frames_list = []

    @staticmethod
    def is_it_latin(char):
        """ прооверяем на литиницу """
        if char == 'х':
            raise NotLatinSymbol

    @staticmethod
    def is_it_allowed_symbols(game_result):
        """
        проверяем строку на допустимые символы
        :param game_result: строка с результатом игры
        :return: None
        """
        pattern = 'XxХх1-9-/'
        if re.findall(f'([^{pattern}])', game_result):
            raise InputError

    @staticmethod
    def is_it_valid_frame(frame):
        """
        проверяем отдельно взятый фрейм
        :param frame:
        :return:
        """

        if frame[0] == '/':
            raise FrameStartsWithSpare
        elif frame[1] == 'x' or frame[1] == 'х':
            raise StrikeOnSecondPositionOfFrame
        elif frame[1] == '/':
            return True
        elif frame[0] == '-' or frame[1] == '-':
            return True
        elif (int(frame[0]) + int(frame[1])) >= 10:
            raise FrameIsMoreThenNinePoints
        else:
            return True

    def is_it_correct_frames_number(self, game_result, string_number=1):
        """
        отсекаем единичные страйки, все остальное рассматриваем как фрейм
        :param string_number: номер строки
        :param game_result: результат нашей игры
        :return:
        """
        game_result = list(game_result.lower())
        frames = 0
        is_it_even_char = False
        for i in range(len(game_result)):
            if is_it_even_char:
                frame = [game_result[i - 1], game_result[i]]
                try:
                    if self.is_it_valid_frame(frame):
                        frames += 1
                        self.frames_list.append(frame)
                        is_it_even_char = False
                        continue
                except BowlingError as err_msg:
                    # обнуляем результат некорректного фрейма
                    frames += 1
                    is_it_even_char = False
                    err = ''.join(game_result)
                    log.exception(f'в строке №{string_number} некорректный фрейм {frame} в строке {err} - {err_msg}\n'
                                  f'\n')
                    game_result[i - 1], game_result[i] = '-', '-'
                    self.frames_list.append(['-', '-'])
                    continue
            elif game_result[i] == 'x' or game_result[i] == 'х':
                try:
                    self.is_it_latin(game_result[i])
                except NotLatinSymbol as err_msg:
                    log.exception(f'в строке №{string_number} обнаружена ошибка - {err_msg} \n'
                                  f'\n')
                    game_result[i] = 'x'
                frames += 1
                self.frames_list.append([game_result[i]])
                is_it_even_char = False
            else:
                is_it_even_char = True

        if frames != self.frames:
            raise IncorrectFramesCount
        game_result = ''.join(game_result)
        return game_result

    def check_game_result_format(self, game_result, string_number=1):
        """
        проверяем строку результата, если проблема с конкретным фреймом - обнуляем
        если проблема со строкой, количество фреймов отличается от заданого или строка содержит недопустимые сиволы
        - обнуляем строку
        :param string_number: номер строки
        :param game_result: результат игры
        :return:
        """
        super().check_game_result_format(game_result)
        # ошибка не критичная, можно легко исправить
        try:
            self.frames_list = []
            self.is_it_allowed_symbols(game_result)
            game_result = self.is_it_correct_frames_number(game_result, string_number)
        except (InputError, IncorrectFramesCount) as crit_error:
            log.exception(f'в строке №{string_number} найдена серьёзная ошибка записи результата: \n'
                          f'{crit_error}\n'
                          f'результат обнуляется\n'
                          f'\n')
            game_result = '--' * self.frames
            self.frames_list = ['--'] * self.frames
        return game_result

    def points_for_strike(self, step):
        point_pack = ['20']
        return point_pack

    def points_for_spare(self, step):
        point_pack = ['15']
        return point_pack

    def frame_to_points(self, frame, step):
        if 'x' in frame:
            points = self.points_for_strike(step)
            if '/' in points:
                points = ['x', '10']
            return points
        elif '/' in frame:
            points = self.points_for_spare(step)
            return points
        else:
            return frame

    def get_score(self, game_result):
        """ считаем """
        super().get_score(game_result)
        game_points_list = []
        for i in range(self.frames):
            frame = self.frames_list[i]
            game_points_list.append(self.frame_to_points(frame, i))
        total_score = 0
        for points in game_points_list:
            for char in points:
                if char == 'x':
                    total_score += 10
                elif char.isdigit():
                    total_score += int(char)
                elif char == '-':
                    pass
                else:
                    print('что то здесь не так')
        return total_score

    def run(self, game_result, string_number=1):
        game_result = self.check_game_result_format(game_result, string_number)
        self.string_parser(game_result)
        result = self.get_score(game_result)
        return result, game_result


class BowlingGameInternational(BowlingGame):
    """
    переопределяем метод подсчета очков
    """

    def points_for_strike(self, step):
        try:
            if 'x' in self.frames_list[step + 1]:
                point_pack = ['x', 'x', self.frames_list[step + 2][0]]
                return point_pack
            else:
                point_pack = ['x', self.frames_list[step + 1][0],
                              self.frames_list[step + 1][1]]
                return point_pack
        except IndexError:
            try:
                point_pack = ['x', self.frames_list[step + 1][0],
                              self.frames_list[step + 1][1]]
                return point_pack
            except IndexError:
                point_pack = ['x']
                return point_pack

    def points_for_spare(self, step):
        try:
            point_pack = ['10', self.frames_list[step + 1][0]]
            return point_pack
        except IndexError:
            point_pack = ['10']
            return point_pack

    def run(self, game_result, string_number=1):
        game_result = self.check_game_result_format(game_result, string_number)
        self.string_parser(game_result)
        result = self.get_score(game_result)
        return result, game_result


if __name__ == '__main__':
    pass
