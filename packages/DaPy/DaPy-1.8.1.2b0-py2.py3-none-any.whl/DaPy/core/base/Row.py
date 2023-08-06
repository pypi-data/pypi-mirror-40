from copy import copy
from collections import Iterable, OrderedDict
from .tools import _str_types

__all__ = ['Row']

class Row:
    def __init__(self, sheet, line):
        self._sheet = sheet
        self._line = line

    @property
    def columns(self):
        return self._sheet.columns

    @property
    def data(self):
        if isinstance(self._sheet.data, list):
            return self._sheet.data[self._line]
        return [seq[self._line] for seq in self._sheet.values()]

    def __getattr__(self, index):
        if index in self.columns:
            return self.data[self.columns.index(index)]
        raise AttributeError('has not attribute or column named %s.' % index)

    def __contains__(self, y):
        return y in self.data

    def __delitem__(self, y):
        if y in self.columns:
            self._sheet.__delitem__(y)
        else:
            self._sheet.__delitem__(self.columns[y])

    def __len__(self):
        return self._sheet.shape.Ln

    def __iter__(self):
        '''for value in row -> iter values
        '''
        for value in self.data:
            yield value

    def __repr__(self):
        return '%s' % str(self.data)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.data[index]
        
        if isinstance(index, _str_types):
            return self.data[self.columns.index(index)]
        
        if isinstance(index, slice):
            if None == index.start and None == index.stop:
                return self.data

            if None == index.start:
                if isinstance(index.stop, _str_types):
                    return self.data[:self.columns.index(index.stop)+1]
                return self.data[:index.stop]

            if None == index.stop:
                if isinstance(index.start, _str_types):
                    return self.data[self.columns.index(index.start):]
                return self.data[index.start:]

            if isinstance(index.start, _str_types):
                return self.data[self.columns.index(index.start):
                                  self.columns.index(index.stop)+1]
            return self.data[index]
        raise AttributeError('unknow statement row[%s]' % index)

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise NotImplementedError('unsupported set multiple values at the same time')
        
        elif isinstance(index, int):
            if isinstance(self._sheet.data, OrderedDict):
                self._sheet.data[self.columns[index]][self._line] = value
            else:
                self.data[index] = value
            if value == self._sheet._miss_symbol:
                self._sheet._miss_value[index] += 1
                
        else:
            raise ValueError('unknow statement row[%s] = %s' % (index, value))

    def _get_new_column(self, value):
        col = [self._sheet.miss_symbol] * self._sheet.shape.Ln
        col[self._line] = value
        return col
    
    def append(self, value):
        append_col = self._get_new_column(value)
        self._sheet.append_col(append_col)

    def count(self, value):
        return self.data.count(value)

    def extend(self, iterable):
        extend_col = [[self._sheet.miss_symbol] * len(iterable)\
                      for i in range(self._sheet.shape.Ln)]
        extend_col[self._line] = list(iterable)
        self._sheet.extend_col(extend_col)

    def index(self, value):
        return self.data.index(value)

    def insert(self, index, value):
        append_col = self._get_new_column(value)
        self._sheet.insert_col(index, append_col)

    def pop(self, index):
        return self._sheet.pop_col(index)[self._line]

    def remove(self, value):
        index = self.data.index(value)
        self._sheet.pop_col(index)
