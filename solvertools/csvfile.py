"""
This module provides support for reading CSV files (or similarly
formatted files) with convenient syntax.
"""

import csv


class CSVRow:

    def __init__(self, cols, header=None):
        self.__cols = cols
        self.__header = header
        if header is not None:
            assert len(cols) == len(header), "CSV row length does not match CSV header"

    def __len__(self):
        return len(self.__cols)

    def __getitem__(self, idx):
        return self.__cols[idx]

    def __setitem__(self, idx, val):
        self.__cols[idx] = val

    def __iter__(self):
        return iter(self.__cols)

    def __getattr__(self, name):
        if self.__header is None:
            raise AttributeError, "CSV file has no header line"
        if name in self.__header:
            return self.__cols[self.__header[name]]
        else:
            raise AttributeError, "CSV file has no column named %s" % repr(name)

def read_csv(path):
    fin = open(path, 'rb')

    # Try to guess the format of the CSV file
    sample = fin.read(1024)
    dialect = csv.Sniffer().sniff(sample)
    has_header = csv.Sniffer().has_header(sample)
    fin.seek(0)

    header = None

    reader = csv.reader(fin, dialect)
    lines = iter(reader)
    if has_header:
        xs = lines.next()
        header = {}
        for i in range(len(xs)):
            header[xs[i].strip('_').lower()] = i

    return (CSVRow(cols, header) for cols in lines)
