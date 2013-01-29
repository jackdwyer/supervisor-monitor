#Jack Dwyer 12-12-2012
import yaml

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
            
def read_yaml():
    #Test function
    supervisors = {}
    with open("settings.yaml", 'r') as f:
        config = yaml.load(f)
    
    for k, vl in config.items():
        if k == "DEFAULTS":
            continue
        supervisors[k]  = vl
    
    return supervisors

if __name__ == "__main__":
    supervisors = read_yaml()
    print supervisors