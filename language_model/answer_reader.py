from sagesutil import data_file
def answer_reader(year):
    f = data_file("data/answers/mystery%s.dat" % year)
    for line in f:
        parts = line.split('"')
        if len(parts) < 2: continue
        yield parts[1]
    f.close()
