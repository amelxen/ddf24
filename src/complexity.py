
def count_tokens(sample: list[str], max_count = 400) -> float:
    return min(1., len(sample) / max_count)

if __name__ == "__main__":
    import tools
    import normalization
    import sim_alg
    from model import aggregate
    import csv

    data_clear = tools.read_yandex_clear()
    data_plag = tools.read_yandex_plag()
    data = data_clear.copy()
    data.update(data_plag)

    # data = dict(list(data.items())[:20])
    data_tokens = {}

    for key in data:
        try:
            toks = normalization.str_tokenize(normalization.str_normalization(data[key], normalization.Normalizer, True))
            data_tokens[key] = toks
        except Exception:
            pass
    
    # mat = sim_alg.levenshtein.levenshtein_dist_ratio_array(data_tokens, data_tokens, True)
    # maxx = aggregate.agg_max(mat)
    
    res = ["name,lev,lcs,ast_str,comp,label"]
    # for target in maxx:
    #      res.append(f"{target},{maxx[target]:.3f},{count_tokens(data_tokens[target]):.3f},{str(0) if target.startswith('plag') else str(1)}")
    # m = 0
    with open("C:\\vscode_projects\\yandex_plag\\ddf24\\test.csv", "r") as file:
        file.readline()
        reader = csv.reader(file)
        for row in reader:
            try:
                res.append(f"{','.join(row[:-1])},{count_tokens(data_tokens[row[0]]):.3f},{row[-1]}")
            except Exception:
                print(row[0])
                continue
    
    with open("C:\\vscode_projects\\yandex_plag\\ddf24\\test1.csv", "w") as file:
        file.write('\n'.join(res))
