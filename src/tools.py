import pathlib
import time
import chardet


def read_code(path: pathlib.Path) -> str:
    with open(path, "rb") as file:
        encodings = chardet.detect_all(file.read())
    res = None
    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding["encoding"]) as file:
                res = file.read()
            break
        except Exception:
            continue
    if res is None:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            res = file.read()
    return res


def read_yandex(path: pathlib.Path, pref="") -> dict[str, str]:
    res = {}
    for file in path.iterdir():
        res[pref + file.with_suffix("").name] = read_code(file)
    return res


def read_yandex_plag(path=pathlib.Path("yandex_plag")) -> dict[str, str]:
    return read_yandex(path, "plag_")


def read_yandex_clear(path=pathlib.Path("yandex_clear")) -> dict[str, str]:
    return read_yandex(path, "clear_")


class PrintRunTime:
    def __init__(self, step_unit=1, max_count: int = None):
        self.start_time = time.time()
        self.count = 0
        self.last_dump_time = -1
        self.delay = 1
        self.step_unit = step_unit
        self.max_count = max_count

    def dump(self, pref: str = None):
        self.count += self.step_unit
        cur_time = time.time()
        if cur_time - self.last_dump_time < self.delay:
            return
        info = []
        if pref is not None:
            info.append(pref)
        info.append(f"total: {(cur_time - self.start_time):.2f}s.")
        sp = self.count / (0.01 + (cur_time - self.start_time))
        info.append(f"{sp:.2f}/s.")
        if self.max_count is not None:
            info.append(f"{int((self.max_count - self.count) / sp)}s. left")
        print("\t".join(info))
        self.last_dump_time = cur_time
