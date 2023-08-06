
from bgpack.unpack import IUnpacker, UnpackerError


class UnpackerSingleValue(IUnpacker):

    def get(self, start=None, stop=None):
        """
        Get values for positions between start and stop

        Args:
            start (int, optional): starting position for the query
            stop (int, optional): end position for the query

        Yield:
            tuple: position, value (or (v1, v2, ...))

        This is the right reader to return single values.
        This is the faster than unpacking multiple values when the reader comes from multi values
        """
        start = start if start is not None else self.start  # start or self.start is not valid because it will not work with 0
        stop = stop if stop is not None else self.stop  # stop or self.stop is not valid because it will not work with 0

        if start < self.init or stop > self.end:
            raise UnpackerError('Range outside limits {}-{}'.format(self.init, self.end))
        elif stop < self.start or start > self.stop:  # only asking for default values
            i = start
            while i <= stop:
                yield i, self.default_value
                i += 1
        else:

            i = start

            first_limit = stop if stop < self.start - 1 else self.start - 1
            while i <= first_limit:
                yield i, self.default_value
                i += 1

            byte_starting = (i - self.start) * self.nbytes
            byte_starting = byte_starting if byte_starting >= 0 else 0

            self.mm.seek(byte_starting + self.offset)

            second_limit = stop if stop <= self.stop else self.stop
            while i <= second_limit:
                yield i, self.index[self.mm.read(self.nbytes)]
                i += 1

            while i <= stop:
                yield i, self.default_value
                i += 1


class Unpacker(IUnpacker):

    def get(self, start=None, stop=None):
        """
        Get values for positions between start and stop

        Args:
            start (int, optional): starting position for the query
            stop (int, optional): end position for the query

        Yield:
            tuple: position, value1, value2...

        """
        start = start if start is not None else self.start  # start or self.start is not valid because it will not work with 0
        stop = stop if stop is not None else self.stop  # stop or self.stop is not valid because it will not work with 0
        if start < self.init or stop > self.end:
            raise UnpackerError('Range outside limits {}-{}'.format(self.init, self.end))
        elif stop < self.start or start > self.stop:  # only asking for default values
            i = start
            while i <= stop:
                yield (i,) + self.default_value
                i += 1
        else:

            i = start

            first_limit = stop if stop < self.start - 1 else self.start - 1
            while i <= first_limit:
                yield (i,) + self.default_value
                i += 1

            byte_starting = (i - self.start) * self.nbytes
            byte_starting = byte_starting if byte_starting >= 0 else 0

            self.mm.seek(byte_starting + self.offset)

            second_limit = stop if stop <= self.stop else self.stop
            while i <= second_limit:
                yield (i,) + self.index[self.mm.read(self.nbytes)]
                i += 1

            while i <= stop:
                yield (i,) + self.default_value
                i += 1
