from fuzzywuzzy import process

def get_normalized(el: str, li: list):
    reading = process.extractBests(el, li, score_cutoff=75)
    candidates = [el]
    best_n = el
    max_n = len(reading)

    while reading != []:
        (new,points) = reading.pop()
        if points < 100 and new not in candidates:
            candidates.append(new)
            tmp = process.extractBests(new, li, score_cutoff=75)
            reading = reading + tmp
            if len(tmp) > max_n:
                best_n = new
    return (best_n, candidates)


def write_csv(out: dict):
    f = open("n_alpha.csv", "w")
    f.write("Old;Normalized\n")
    for k in out.keys():
        for n in out[k]:
            f.write(n+';'+k+'\n')

if __name__ == "__main__":
    f = open("brands.txt", "r")
    li = list(f)
    f.close()
    for i in range(0, len(li)):
        li[i] = li[i].replace('\n', '')
    double = li
    output = {}
    for el in double:
        (res, l_res) = get_normalized(el, li)
        if len(l_res) > 1:
            output[res] = l_res
            for name in l_res:
                if name in double:
                    double.remove(name)
    write_csv(output)