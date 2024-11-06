import pycode_similar
import ast

import tools
import preproc


def ast_diff(str1:bytes, str2:bytes, 
             diff_method: type[pycode_similar.UnifiedDiff] = pycode_similar.UnifiedDiff) -> float:
    res = pycode_similar.detect([str1, str2], diff_method)
    print(res[0][1][0].__str__())
    return res[0][1][0].plagiarism_percent


def ast_unified_diff(str1: bytes, str2: bytes) -> float:
    return ast_diff(str1, str2, pycode_similar.UnifiedDiff)


def ast_tree_diff(str1: bytes, str2: bytes) -> float:
    return ast_diff(str1, str2, pycode_similar.TreeDiff)





if __name__ == "__main__":
    data = tools.read_yandex_plag()
    code_str = data["plag_0"]

    # root_node = ast.parse(code_str)
    # collector = pycode_similar.BaseNodeNormalizer()
    # collector.visit(root_node)

    # root_node = ast.parse(code_str)
    # collector = pycode_similar.FuncNodeCollector(keep_prints=False)
    # collector.visit(root_node)
    # code_utf8_lines = code_str.splitlines(True)
    # func_info = [pycode_similar.FuncInfo(n, code_utf8_lines) for n in collector.get_function_nodes()]
    # if module_level:
    #     root_node = ast.parse(code_str)
    #     collector = ModuleNodeCollector(keep_prints=keep_prints)
    #     collector.visit(root_node)
    #     module_node = collector.get_module_node()
    #     module_node.endlineno = len(code_utf8_lines)
    #     module_info = FuncInfo(module_node, code_utf8_lines)
    #     func_info.append(module_info)
    # func_info_list.append((index, func_info))

    # print(collector)

    # for key in data:
        # data[key] = preproc.prep(data[key])
    
    print(ast_unified_diff(data["plag_123"], data["plag_1234"]))
    print(ast_tree_diff(data["plag_123"], data["plag_1234"]))
