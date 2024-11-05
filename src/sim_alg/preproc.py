import re


def remove_spaces(code: bytes) -> bytes:
    res = re.sub(br"\s", br"", code)
    return res


def remove_doc_string(code: bytes) -> bytes:
    res = re.sub(br"(\n|\r)\s*\"\"\"([^\"]|(\"{1,2}))*\"\"\"", br"", code)
    res = re.sub(br"(\n|\r)\s*\'\'\'([^\"]|(\"{1,2}))*\'\'\'", br"", res)
    return res


def remove_comments(code: bytes) -> bytes:
    res = re.sub(br"#[^\n\r]*", br"", code)
    return res


def prep(code: bytes) -> bytes:
    res = remove_comments(code)
    res = remove_doc_string(res)
    res = remove_spaces(res)
    return res
