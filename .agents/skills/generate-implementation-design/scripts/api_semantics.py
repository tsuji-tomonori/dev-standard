"""generatorと独自adapter検査で同じ実装由来意味モデルを共有する。"""
import json


def enrich(model, root, exported, helper):
    """選択されたフロー・例外・検証単位だけを実sourceから再構成する。"""
    operations = model['operations']
    if model.get("semantic_contract"):
        try:
            import copy
            model = copy.deepcopy(model)
            operations = model["operations"]
            contract = model["semantic_contract"]
            if set(contract["operations"]) != set(exported):
                raise ValueError("semantic operation inventory differs from OpenAPI")
            layout = helper("api_layout")
            flow = helper("api_flow")
            index = layout.Index(root, model["python_root"])
            if contract.get("sql_models"):
                helper("sql_models").inspect(root, contract["sql_models"], layout.confined)
            for operation in operations:
                selected = contract["operations"][operation["id"]]
                if index.paths[index.owner_module(selected["handler"])] != operation["source"]["path"]:
                    raise ValueError("flow handler differs from operation source")
                actual = flow.inspect(index, selected)
                operation["sequence"] = flow.mermaid(actual)
                operation["flow_evidence"] = actual
        except (ValueError, KeyError, SyntaxError) as exc:
            raise ValueError(f"API semantic contract: {exc}") from exc
    if model.get("error_contract"):
        try:
            import copy
            model = copy.deepcopy(model)
            operations = model["operations"]
            layout = helper("api_layout")
            errors = helper("api_errors")
            index = layout.Index(root, model["python_root"])
            contract = model["error_contract"]
            if set(contract["operations"]) != set(exported):
                raise ValueError("exception operation inventory differs from OpenAPI")
            seen_descriptions = {}
            for operation in operations:
                selected = contract["operations"][operation["id"]]
                if index.paths[index.owner_module(selected["handler"])] != operation["source"]["path"]:
                    raise ValueError("exception handler differs from operation source")
                actual = errors.inspect(index, selected)
                operation["exception_paths"] = actual
                operation["errors"] = json.dumps(actual, ensure_ascii=False)
                if not actual and not contract["operations"][operation["id"]].get("no_exceptions_reason"):
                    raise ValueError("no exception paths requires a concrete scope reason")
                for case in operation["cases"]:
                    units = [errors.gwt(root, identity, layout.confined) for identity in case["tests"]]
                    for unit in units:
                        signature = tuple(unit[phase] for phase in ["given", "when", "then"])
                        if signature in seen_descriptions and seen_descriptions[signature] != unit["test"]:
                            raise ValueError("duplicate verification-unit descriptions across tests")
                        seen_descriptions[signature] = unit["test"]
                    case["verification_units"] = units
                    for phase in ["given", "when", "then"]:
                        case[phase] = " / ".join(unit[phase] for unit in units)
                for path in actual:
                    operation["messages"] = [m for m in operation["messages"] if m["id"] != path["log_id"]]
                    operation["messages"].append({"id": path["log_id"], "level": path["level"], "template": path["message"],
                        "condition": path["exception"] + " / " + path["outcome"], "operator_action": path["operator_action"],
                        "fields": [], "no_fields_reason": "型付きcontextの静的検査結果: " + path["context_type"], "source": path["log_source"]})
        except (ValueError, KeyError, SyntaxError) as exc:
            raise ValueError(f"API exception contract: {exc}") from exc
    return model
