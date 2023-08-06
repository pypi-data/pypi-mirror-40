import collections
from functools import reduce
from io import TextIOBase
import json
import logging
import os
import re
from time import sleep
from datetime import datetime

aivdm_pattern = re.compile(r'([.0-9]+)?\s*(![A-Z]{5},\d,\d,.?,[AB12],[^,]+,[0-5]\*[0-9A-F]{2})')


class Bits:
    def __init__(self, *args):
        if len(args) == 0:
            self.contents = ""
        elif len(args) == 1:
            if isinstance(args[0], str):
                self.contents = args[0]
            elif isinstance(args[0], int):
                self.contents = "{:b}".format(args[0])
            elif isinstance(args[0], Bits):
                self.contents = args[0].contents
            else:
                raise ValueError("don't know how to parse {}".format(args[0]))
        elif len(args) == 2 and isinstance(args[0], int):
            format_string = "{:0" + str(args[1]) + "b}"
            self.contents = format_string.format(args[0])
        else:
            raise ValueError("don't know how to parse {}, {}".format(args[0], args[1]))

    def append(self, other):
        if not isinstance(other, Bits):
            raise ValueError
        self.contents += other.contents

    def __int__(self):
        return int(self.contents, 2)

    def __getitem__(self, given):
        return Bits(self.contents.__getitem__(given))

    def __add__(self, other):
        return Bits(self.contents + other.contents)

    def __len__(self):
        return self.contents.__len__()

    def __eq__(self, other):
        if isinstance(other, Bits):
            return self.contents.__eq__(other.contents)
        else:
            return int(self) == int(other)

    def __str__(self):
        return self.contents

    def __repr__(self):
        return "Bits({})".format(str(self))

    @classmethod
    def join(cls, array):
        return Bits(''.join(b.contents for b in array))


class StreamParser:
    """
    Used to parse live streams of AIS messages.
    """

    def __init__(self, default_to_current_time=False):
        self.default_to_current_time = default_to_current_time
        self.fragment_pool = {'A': FragmentPool(), 'B': FragmentPool()}
        self.sentence_buffer = collections.deque()

    def add(self, message_text):
        thing = parse_one(message_text, self.default_to_current_time)
        if isinstance(thing, Sentence):
            self.sentence_buffer.append(thing)
        elif isinstance(thing, SentenceFragment):
            pool = self.fragment_pool[thing.radio_channel]
            pool.add(thing)
            if pool.has_full_sentence():
                sentence = pool.pop_full_sentence()
                self.sentence_buffer.append(sentence)

    def next_sentence(self):
        return self.sentence_buffer.popleft()

    def has_sentence(self):
        return len(self.sentence_buffer) > 0


def parse_many(messages):
    p = StreamParser()
    result = []
    for m in messages:
        p.add(m)
        if p.has_sentence():
            result.append(p.next_sentence())
    return result


# based on https://en.wikipedia.org/wiki/NMEA_0183
def nmea_checksum(content):
    result = 0
    for c in content:
        result = result ^ ord(c)
    return result


def parse_one(string, default_to_current_time=False):
    m = aivdm_pattern.search(string)
    if not m:
        return None

    if m.group(1):
        time = datetime.fromtimestamp(float(m.group(1)))
    else:
        if default_to_current_time:
            time = datetime.now()
        else:
            time = None

    message = m.group(2)

    content, checksum = message[1:].split('*')
    fields = content.split(',')
    talker = fields[0][0:2]
    sentence_type = fields[0][2:]
    fragment_count = int(fields[1])
    radio_channel = fields[4]
    payload = NmeaPayload(fields[5], int(fields[6]))
    checksum_valid = nmea_checksum(content) == int(checksum, 16)
    if fragment_count == 1:
        return Sentence(talker, sentence_type, radio_channel, payload, [checksum_valid], time, [message])
    else:
        fragment_number = int(fields[2])
        message_id = int(fields[3])
        return SentenceFragment(talker, sentence_type, fragment_count, fragment_number,
                                message_id, radio_channel, payload, checksum_valid, time, message)


def parse(message):
    if isinstance(message, list):
        return parse_many(message)
    else:
        return parse_one(message)


class NMEAThing:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


def _make_nmea_lookup_table():
    lookup = {}
    for val in range(48, 88):
        lookup[chr(val)] = Bits(val - 48, 6)
    for val in range(96, 120):
        lookup[chr(val)] = Bits(val - 56, 6)
    return lookup


_nmea_lookup = _make_nmea_lookup_table()


# noinspection PyCallingNonCallable
class NmeaPayload:
    """
    Represents the decoded heart of an AIS message. The BitVector class used
    is not very fast and a bit rough, but is adequate for now. If performance
    becomes an issue, it might be worth replacing. See
    http://stackoverflow.com/questions/20845686/python-bit-array-performant
    for options.
    """

    def __init__(self, raw_data, fill_bits=0):
        if isinstance(raw_data, Bits):
            self.bits = raw_data
        else:
            self.bits = self._bits_for(raw_data, fill_bits)

    @staticmethod
    def _bits_for(ascii_representation, fill_bits):
        result = Bits()
        for pos in range(0, len(ascii_representation) - 1):
            result.append(_nmea_lookup[ascii_representation[pos]])
        bits_at_end = 6 - fill_bits
        selected_bits = _nmea_lookup[ascii_representation[-1]][0:bits_at_end]
        result.append(selected_bits)
        return result

    def __len__(self):
        return len(self.bits)


message_type_json = json.loads(open(os.path.join(os.path.dirname(__file__), 'aivdm.json')).read())['messages']


class FieldDecoder:
    def __init__(self, name, start, end, data_type, description):
        self.name = name
        self.start = start
        self.end = end
        self.length = 1 + end - start
        self.bit_range = slice(start, end + 1)
        self.description = description
        self._decode = self._appropriate_decoder(data_type, name)
        self.short_bits_ok = data_type in ['s', 't']  # if we get partial text, that's better than nothing

    def _appropriate_decoder(self, data_type, name):
        if name == 'mmsi':
            return self._parse_mmsi
        elif name == 'lon' and data_type == 'I4':
            return self._parse_lon
        elif name == 'lat' and data_type == 'I4':
            return self._parse_lat
        elif name == 'lon' and data_type == 'I1':
            return lambda b: None  # Type 17 is weird; ignore for now
        elif name == 'lat' and data_type == 'I1':
            return lambda b: None  # Type 17 is weird; ignore for now
        elif data_type == 't' or data_type == 's':
            return self._parse_text
        elif data_type == 'I3':
            return lambda b: self._scaled_integer(b, 3)
        elif data_type == 'I1':
            return lambda b: self._scaled_integer(b, 1)
        elif data_type == 'I4':
            return lambda b: self._scaled_integer(b, 4)
        elif data_type == 'u':
            return lambda b: int(b)
        elif data_type == 'd':
            return lambda b: b
        elif data_type == 'U1':
            return lambda b: int(b) / 10.0
        elif data_type == 'e':
            return lambda b: "enum-{}".format(int(b))  # TODO: find and include enumerated types
        elif data_type == 'b':
            return lambda b: b == 1
        elif data_type == 'x':
            return lambda b: int(b)
        else:
            raise ValueError("Sorry, don't know how to parse '{}' for field '{}' yet".format(data_type, self.name))

    def decode(self, bits):
        bits_to_decode = bits[self.bit_range]
        if self.short_bits_ok or self.length == len(bits_to_decode):
            return self._decode(bits_to_decode)

    def _parse_mmsi(self, bits):
        return "%09i" % int(bits)

    def _parse_lon(self, bits):
        result = self._scaled_integer(bits, 4)
        if result is not None and result != 181.0 and -180 <= result <= 180.0:
            return result

    def _parse_lat(self, bits):
        result = self._scaled_integer(bits, 4)
        if result is not None and result != 91.0 and -90.0 <= result <= 90.0:
            return result

    def _twos_comp(self, val, length):
        if (val & (1 << (length - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << length)  # compute negative value
        return val

    def _scaled_integer(self, bits, scale):
        out = self._twos_comp(int(bits), len(bits))
        result = round(out / 60 / (10 ** scale), 4)
        return result

    def _parse_text(self, bits):
        def chunks(s, n):
            for i in range(0, len(s), n):
                yield s[i:i + n]

        raw_ints = [int(nibble) for nibble in chunks(bits, 6)]
        mapped_ints = [i if i > 31 else i + 64 for i in raw_ints]
        text = ''.join([chr(i) for i in mapped_ints]).strip()
        text = text.rstrip('@').strip()
        return text


class MessageDecoder:
    def __init__(self, message_info):
        self.field_decoders = []
        self.field_decoders_by_id = collections.OrderedDict()
        for field in message_info['fields']:
            name = field['member']
            decoder = FieldDecoder(name, field['start'], field['end'], field['type'], field['description'])
            self.field_decoders.append(decoder)
            self.field_decoders_by_id[name] = decoder

    def bit_range(self, name):
        return self.field_decoders_by_id[name].bit_range

    def decode(self, name, bits):
        if name in self.field_decoders_by_id:
            return self.field_decoders_by_id[name].decode(bits)

    def fields(self):
        return self.field_decoders_by_id.values()

    def field(self, key):
        if isinstance(key, int):
            return self.field_decoders[key]
        else:
            return self.field_decoders_by_id[key]


MESSAGE_DECODERS = {}
for message_type_id in range(1, 28):
    MESSAGE_DECODERS[message_type_id] = MessageDecoder(message_type_json[str(message_type_id)])


class SentenceFragment:
    def __init__(self, talker, sentence_type, total_fragments, fragment_number, message_id, radio_channel, payload,
                 checksum_valid, time=None, text=None):
        self.talker = talker
        self.sentence_type = sentence_type
        self.total_fragments = total_fragments
        self.fragment_number = fragment_number
        self.message_id = message_id
        self.radio_channel = radio_channel
        self.payload = payload
        self.checksum_valid = checksum_valid
        self.time = time
        self.text = text

    def initial(self):
        return self.fragment_number == 1

    def last(self):
        return self.fragment_number == self.total_fragments

    def key(self):
        key = (self.talker, self.sentence_type, self.total_fragments, self.message_id, self.radio_channel)
        return key

    def follows(self, other):
        return (self.fragment_number == other.fragment_number + 1) and self.key() == other.key()

    def bits(self):
        return self.payload.bits

    def check(self):
        return self.checksum_valid


class Field(object):
    def __init__(self, field_decoder, sentence):
        self.decoder = field_decoder
        self.sentence = sentence

    def name(self):
        return self.decoder.name

    def description(self):
        return self.decoder.description

    def value(self):
        return self.decoder.decode(self.sentence.message_bits())

    def bits(self):
        return self.sentence.message_bits()[self.decoder.bit_range]

    def valid(self):
        return len(self.sentence.message_bits()) > self.decoder.end


class Sentence:
    def __init__(self, talker, sentence_type, radio_channel, payload, checksum_valid, time=None, text=None):
        self.talker = talker
        self.sentence_type = sentence_type
        self.radio_channel = radio_channel
        self.payload = payload
        self.checksum_valid = checksum_valid
        self.time = time
        self.text = text
        self.type_num = int(self.payload.bits[0:6])

    def type_id(self):
        return self.type_num

    def check(self):
        return reduce(lambda a, b: a and b, self.checksum_valid)

    def location(self):
        lon = self['lon']
        lat = self['lat']
        if lon and lat:
            return lon, lat

    def message_bits(self):
        return self.payload.bits

    def __getitem__(self, item):
        return MESSAGE_DECODERS[self.type_num].decode(item, self.payload.bits)

    def field(self, key):
        return Field(MESSAGE_DECODERS[self.type_num].field(key), self)

    def fields(self):
        return [Field(fd, self) for fd in MESSAGE_DECODERS[self.type_num].fields()]

    @classmethod
    def from_fragments(cls, matching_fragments):
        first = matching_fragments[0]
        message_bits = reduce(lambda a, b: a + b, [f.bits() for f in matching_fragments])
        text = [f.text for f in matching_fragments]
        checksum_valid = [f.checksum_valid for f in matching_fragments]
        return Sentence(first.talker, first.sentence_type, first.radio_channel, NmeaPayload(message_bits),
                        checksum_valid, first.time, text)

    def __repr__(self):
        return "Sentence({}, {})".format(self.time, self.text)

    def __str__(self):
        return "Sentence(type {}, from {}, at {})".format(self.type_num, self['mmsi'], self.time)


class FragmentPool:
    """
    A smart holder for SentenceFragments that can tell when a valid message has been found.
    Unlike TCP fragments, AIS fragments arrive in order and soon, so this can be aggressive
    in discarding odd socks.
    """

    def __init__(self):
        self.fragments = []
        self.full_sentence = None

    def has_full_sentence(self):
        return self.full_sentence is not None

    def pop_full_sentence(self):
        if not self.full_sentence:
            raise ValueError
        result = self.full_sentence
        self.full_sentence = None
        return result

    def _has_complete_fragment_set(self):
        actual = sorted([f.fragment_number for f in self.fragments])
        expected = list(range(1, self.fragments[0].total_fragments + 1))
        return actual == expected

    def add(self, fragment):
        if len(self.fragments) > 0 and not fragment.follows(self.fragments[-1]):
            self.fragments.clear()

        self.fragments.append(fragment)

        if fragment.last() and self._has_complete_fragment_set():
            self.full_sentence = Sentence.from_fragments(self.fragments)
            self.fragments.clear()


def lines_from_source(source):
    if isinstance(source, TextIOBase):
        for line in source:
            yield line
    elif re.match("/dev/tty.*", source):
        yield from _handle_serial_source(source)
    elif re.match("https?://.*", source):
        yield from _handle_url_source(source)
    else:
        # assume it's a file
        yield from _handle_file_source(source)


def fragments_from_source(source):
    for line in lines_from_source(source):
        # noinspection PyBroadException
        try:
            m = aivdm_pattern.search(line)
            if m:
                yield m.group(0)
            else:
                logging.getLogger().warn("skipped: \"{}\"".format(line.strip()))
        except Exception:
            logging.getLogger().error("unexpected failure for line {} in source {}".format(line, source), exc_info=True)


def sentences_from_source(source):
    parser = StreamParser()
    for fragment in fragments_from_source(source):
        # noinspection PyBroadException
        try:
            parser.add(fragment)
            if parser.has_sentence():
                yield parser.next_sentence()
        except Exception:
            logging.getLogger().error("unexpected failure for fragment {} in source {}".format(fragment, source),
                                      exc_info=True)


# noinspection PyBroadException
def _handle_serial_source(source):
    import serial

    while True:
        # noinspection PyBroadException
        try:
            with serial.Serial(source, 38400, timeout=10) as f:
                while True:
                    raw_line = f.readline()
                    try:
                        yield raw_line.decode('ascii')
                    except Exception:
                        logging.getLogger().warn("Failure for input: \"{}\"".format(raw_line.strip()), exc_info=True)
        except Exception:
            logging.getLogger().error("unexpected failure", exc_info=True)
            sleep(1)


def _handle_url_source(source):
    import urllib.request

    while True:
        # noinspection PyBroadException
        try:
            # noinspection PyUnresolvedReferences
            with urllib.request.urlopen(source) as f:
                for line in f:
                    yield line.decode('utf-8')
        except Exception:
            logging.getLogger().error("unexpected failure in source {}".format(source), exc_info=True)
            sleep(1)


def _handle_file_source(source):
    with open(source) as f:
        for line in f:
            yield line
