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


def create_csv(out: dict):
    f = open("../final.csv", "w")
    f.write("Old Value;Normalized form\n")
    for k in out.keys():
        for v in out[k]:
            f.write(v+';'+k+'\n')
    f.close()

if __name__ == '__main__':
    f = open("brands.txt", "r")
    li = list(f)
    for i in range(0,len(li)):
        li[i] = li[i].replace('\n', '')
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
    create_csv(output)