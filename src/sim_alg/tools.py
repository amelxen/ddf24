import pathlib


def read_code(path: pathlib.Path) -> bytes:
    with open(path, "rb") as file:
        res = file.read()
    return res


def read_yandex(path: pathlib.Path, pref = "") -> dict[str, bytes]:
    res = {}
    for file in path.iterdir():
        res[pref + file.with_suffix("").name] = read_code(file)
    return res


def read_yandex_plag(path = pathlib.Path("yandex_plag")) -> dict[str, bytes]:
    return read_yandex(path, "plag_")


def read_yandex_clear(path = pathlib.Path("yandex_clear")) -> dict[str, bytes]:
    return read_yandex(path, "clear_")
