#Jack Dwyer 12-12-2012
def parse_line(line):
    try:
        url, name = line.split(None, 1)
        return (url, name.strip())
    except ValueError:
        return (line.strip(), )

def parse_settings(file):
    details = []
    for line in read_file(file):
        details.append(parse_line(line))
    return details

def read_file(file):
    with open(file, 'r') as f:
        line = f.readline()
        while (line):
            if not line:
                continue
            yield line
            line = f.readline()