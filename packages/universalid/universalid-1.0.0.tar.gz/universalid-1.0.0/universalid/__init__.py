"""
License: MIT
Author: Jakob Majkilde
"""
from datetime import datetime
from secrets import randbelow
from universalid.settings import Settings
from universalid.encode import Encode

name = "universalid"


class Unid:
    """
    Class here
    """
    time_sequence = 0  # Add a sequence number to make the datetime part unique when Unid's is created simultaneously

    @staticmethod
    def create(prefix=None, time=None):
        """
        Creates a 32-character combination of digits (0-9, A-Z), where:
            * First 20 digits: The specified prefix plus random digits
            * Next 7 digits: Date/time
            * Next 4 digits: microseconds
            * last digit: sequence number

        :param str prefix: Optional. Defaults to None. The resulting unid will start with the specified prefix
        :param datetime time: Optional. Defaults to datetime.utcnow()
        :return: new unique unid
        :rtype: str

        Examples:

        To create a new unid based on the current date/time

        .. code-block:: python

            >> Unid.create()
            'B90HSWB2RP1ISBQVGSBU0PK8L5T0HWY0'

        Create a unid with a custom prefix, e.g. a country code

        .. code-block:: python

           >> Unid.create('dk')
           'DK396ODJJ0QUE4APFO2H0PK8L8R5RB31'

        Create a unid based on a specific time

        .. code-block:: python

            >> Unid.create(time=datetime.datetime(2018, 12, 20, 11, 34, 15, 229884))
            'ODPN11WEQJWXVDOE3A390PK16P34XDO2'

        """
        time = time if time else datetime.utcnow()
        prefix = Unid._strip(prefix) if prefix else ""

        # start with the optional prefix (limited to the max length)
        unid = prefix[:Settings.CUSTOM_LENGTH]

        # add random chars
        size = Settings.CUSTOM_LENGTH - len(prefix)
        unid += Unid._get_random(size)

        # add the datetime
        unid += Encode.encode_time(time)

        # add the sequence
        unid += Encode.digit_to_char(Unid._inc_sequence())

        return unid.upper()

    @staticmethod
    def get_time(unid):
        """
        Extract the creation date/time from a given unid

        :param str unid: the unid
        :return:  the date/time from the unid
        :rtype: datetime

        >>> Unid.get_time("7ADQ2D6JCJXI2Q82J06X0PK16P34XDO1")
        datetime.datetime(2018, 12, 20, 11, 34, 15, 229884)

        """
        # decode the datetime
        date_str = unid[-12:-5]

        timestamp = Encode.str_to_int(date_str)
        date = datetime.fromtimestamp(timestamp)

        # decode the microseconds
        micro_str = unid[-5:-1]
        microsecond = Encode.str_to_int(micro_str)

        # return
        date = date.replace(microsecond=microsecond)
        return date

    @staticmethod
    def _inc_sequence():
        result = Unid.time_sequence
        Unid.time_sequence += 1
        if Unid.time_sequence == Settings.BASE:
            Unid.time_sequence = 0
        return result

    @staticmethod
    def _get_random(length):
        s = ""
        while len(s) < length:
            r = randbelow(Settings.BASE)
            s += Encode.digit_to_char(r)
        return s

    @staticmethod
    def _strip(value):
        result = ""
        for c in value:
            result += c if Encode.valid_char(c) else ''
        return result
