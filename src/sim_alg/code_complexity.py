import radon
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import os

def harvester_config():
    return Config(
        exclude=None,
        ignore=None,
        order=SCORE,
        no_assert=False,
        show_closures=False,
        min='A',
        max='F',
    )

def cc_harvester(dir):
    h = CCHarvester([dir], harvester_config())
    results = h._to_dicts()

    converter = {
        'A':1,
        'B':0.8,
        'C':0.6,
        'D':0.4,
        'E':0.2,
        'F':0
    }
    cc_dict = {}

    for sol in results:
        res = results[sol]
        if 'error' not in results[sol]:
            ranks = [converter[i['rank']] for i in res]
            avg_rank = round(sum(ranks)/len(ranks), 1)
        else:
            avg_rank = 0
        cc_dict[sol.replace(dir+'\\', '')] = avg_rank
    return cc_dict

def hal_harvester(dir):
    hal_vol_dict = {}
    for sol in os.listdir('clear'):
        with open(f'clear/{sol}', 'r', encoding='utf-8') as f:
            code = f.read()
        try:
            hal = radon.metrics.h_visit(code)
            vol = hal.total.volume
            dif = hal.total.difficulty
            vol_norm = round(min(vol, 20)/20, 2)
            dif_norm = round(min(dif, 3)/3, 2)
            hal_vol_dict[sol] = {'vol_norm': vol_norm,
                                'dif_norm': dif_norm}
        except:
            hal_vol_dict[sol] = {'vol_norm': 0,
                                'dif_norm': 0}
    return hal_vol_dict