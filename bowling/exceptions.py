#!/usr/bin/env python3


class BowlingError(Exception):
    """Base class for exceptions in this module."""
    summary = 'введеный результат не соответствует правилам записи'

    def __str__(self):
        return self.summary


class InputError(BowlingError):
    summary = 'введеный результат содержит недопустимые символы'


class StrikeOnSecondPositionOfFrame(BowlingError):
    summary = 'страйк не может быть на второй позиции фрейма'


class FrameIsMoreThenNinePoints(BowlingError):
    summary = 'сумма 2х бросков фрейма не может быть больше 9'


class IncorrectFramesCount(BowlingError):
    summary = 'сумма фреймов должна быть 10'


class FrameStartsWithSpare(BowlingError):
    summary = 'фрейм не может начинаться со спэйра!'


# по хорошему, конечно, нужно переписать все исключения на ин. яз
class BowlingErrorInternational(BowlingError):
    """Base class for exceptions in this module."""
    summary = 'incorrect input'

    def __str__(self):
        return self.summary


class NotLatinSymbol(BowlingErrorInternational):
    summary = 'the use of non-latin characters is prohibited!'
