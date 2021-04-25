from fuzzywuzzy import process


def get_normalized(starting_name: str, names_coll: list):
    reading = process.extractBests(starting_name, names_coll, score_cutoff=75)
    candidates = [starting_name]
    best_n = starting_name
    max_n = len(reading)

    while reading:
        (new, points) = reading.pop()
        if points < 100 and new not in candidates:
            candidates.append(new)
            tmp = process.extractBests(new, li, score_cutoff=75)
            reading = reading + tmp
            if len(tmp) > max_n:
                best_n = new
    return best_n, candidates


def write_csv(out: dict):
    with open("n_alpha.csv", "w") as f:
        f.write("Old;Normalized\n")
        for norm_form in out.keys():
            for brand in out[norm_form]:
                f.write(f"{brand};{norm_form}\n")


if __name__ == "__main__":
    with open("brands.txt", "r") as f:
        li = list(f)
    for i in range(len(li)):
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
