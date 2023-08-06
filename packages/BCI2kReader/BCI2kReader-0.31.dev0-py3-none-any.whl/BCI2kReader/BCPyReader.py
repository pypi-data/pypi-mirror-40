# -*- coding: utf-8 -*-

#   The BCPyReader is free software: you can redistribute it
#   and/or modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import io as io
from BCI2kReader.FileReader import bcistream


class BCI2kReader(io.IOBase):

    def __init__(self, filename, usecache=True):
        self.__reader = bcistream(filename)
        self.__states = None
        self.__signals = None
        self.__usecache = usecache

    def close(self):
        self.__reader.close()

    def _getclosed(self):
        return self.__reader.closed

    closed = property(_getclosed)

    def fileno(self):
        return self.__reader.file.fileno()

    def readable(self):
        return self.__reader.file.readable()

    def seek(self, offset, whence=0):
        if whence == io.SEEK_SET:
            wrt = 'bof'
        elif whence == io.SEEK_END:
            wrt = 'eof'
        elif whence == io.SEEK_END:
            wrt = 'cof'
        else:
            raise IOError('unknown search origin')

        self.__reader.seek(offset, wrt)

    def seekable(self):
        return True

    def tell(self):
        return self.__reader.tell()

    def writable(self):
        return False

    def usecache(self, flag):
        self.__usecache = flag

    def _parameters(self):
        return pd.DataFrame.from_dict(self.__reader.params)

    parameters = property(_parameters)

    def _signals(self):
        if self.__signals is not None:
            return self.__signals
        # save current position
        pos = self.tell()
        if self.__usecache:
            self.__signals, self.__states = self.__reader.decode('all')
            self.seek(pos, io.SEEK_SET)
            return self.__signals
        else:
            signalbuffer, statebuffer = self.__reader.decode('all')
            self.seek(pos, io.SEEK_SET)
            return signalbuffer

    signals = property(_signals)

    def _states(self):
        if self.__states is not None:
            return self.__states
        pos = self.tell()
        if self.__usecache:
            self.__signals, self.__states = self.__reader.decode('all')
            self.seek(pos, io.SEEK_SET)
            return self.__states
        else:
            signalbuffer, statebuffer = self.__reader.decode('all')
            self.seek(pos, io.SEEK_SET)
            return statebuffer
        # set position

    states = property(_states)

    def purge(self):
        self.__states = None
        self.__signals = None

    def _samplingrate(self):
        return self.__reader.samplingrate()

    samplingrate = property(_samplingrate)

    def read(self, nsamp=-1, apply_gain=True):
        if self.__states is not None and self.__usecache:
            pos = self.tell()
            if nsamp < 0:
                nsamp = self.__reader.samples()-pos
            return self.__signals[pos:pos+nsamp, :], self.__states[pos:pos+nsamp, :]
        else:
            return self.__reader.decode(nsamp, 'all', apply_gain)

    def readall(self, apply_gain=True):
        if self.__states is not None and self.__usecache:
            return self.__signals, self.__states
        else:
            if self.__usecache:
                self.__signals, self.__states = self.__reader.decode('all', 'all', apply_gain)
                return self.__signals, self.__states
            else:
                return self.__reader.decode('all', 'all', apply_gain)








