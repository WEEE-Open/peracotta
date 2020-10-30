from fuzzywuzzy import process


def norm(ex, li):
    reading = process.extractBests(ex, li, score_cutoff=75)
    candidates = [ex]
    normalized = ex
    max_n = len(reading)
    while reading != []:
        analysis = reading.pop()
        (name, points) = analysis
        if points < 100 and name not in candidates:
            candidates.append(name)
            tmp = process.extractBests(ex, li, score_cutoff=75)
            reading = reading + tmp
            if len(tmp) > max_n:
                max_n = len(tmp)
                normalized = name
    return (normalized, candidates)

if __name__ == '__main__':
    f = open("../brands", "r")
    li = list(f)
    double = li
    f.close()
    output = {}
    while double != []:
        (normalized, associated) = norm(double.pop(), li)
        if len(associated) > 1:
            for el in associated:
                if el in double:
                    double.remove(el)
            output[normalized] = associated
    f = open('../final', "w")
    f.write(str(output))
    f.close()