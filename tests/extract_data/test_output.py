from main import extract_and_collect_data_from_generated_files as get_result
import os
import pytest


def is_product(component: dict):
    # check if brand and model exist
    if "brand" not in component.keys() or "model" not in component.keys():
        return False
    # check if brand or model has a not valid value
    candidates = [component["brand"].lower(), component["model"].lower()]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate in ("", "null", "unknown", "undefined", "no enclosure"):
            return False
    # if all conditions are False, the product should be added
    return True


test_folders = [entries for entries in os.listdir("tests/") if os.path.isdir(f"tests/{entries}")]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/{fold}"):
        test_folders.remove(fold)


@pytest.fixture(scope="module", params=test_folders)
def res(request):
    path = f"tests/{request.param}"
    with open(os.path.join(path, "gpu_location.txt"), "r") as f:
        gpu_flag = f.readline()
    has_dedicated_gpu = False
    gpu_in_cpu = False
    if gpu_flag == "cpu":
        gpu_in_cpu = True
    elif gpu_flag == "gpu":
        has_dedicated_gpu = True
    return get_result(directory=path, has_dedicated_gpu=has_dedicated_gpu, gpu_in_cpu=gpu_in_cpu, gui=False)


# checks about peracotta's output
def test_type_check(res):
    assert isinstance(res, list)
    assert res[0]["type"] == "I"
    for comp in res[1:]:
        assert comp["type"] == "P"
        for name in (comp["brand"].lower(), comp["model"].lower()):
            assert name not in ("", "null", "undefined", "unknown")


def test_has_chassis_and_mobo(res):
    assert isinstance(res[0]["features"], dict) and isinstance(res[0]["contents"], list) and res[0]["contents"] != []
    mobo = res[0]["contents"][0]
    assert isinstance(mobo["features"], dict) and mobo["features"] != {} and isinstance(mobo["contents"], list)


item_keys = ["arrival-batch", "cib", "cib-old", "cib-qr", "data-erased", "mac", "notes",
             "os-license-code", "os-license-version", "other-code", "owner", "smart-data",
             "sn", "software", "surface-scan", "working", "wwn"]
both = ["brand", "model", "variant", "type"]


def explore_item(param):
    assert isinstance(param["features"], dict) and ("features" in param.keys())
    for k in param["features"].keys():
        if k == "type" and param["features"]["type"] == "I":
            pass
        # if is not a product (no brand or model) all the keys are in item
        elif is_product(param["features"]):
            assert k in (item_keys + both)

    if "contents" in param.keys():
        assert isinstance(param["contents"], list)
        for new_param in param["contents"]:
            explore_item(new_param)


def test_check_product_keys(res):
    for product in res[1:]:
        for k in product["features"].keys():
            assert k not in item_keys or k == "type"


def test_check_item_keys(res):
    explore_item(res[0])


def explore_cleanup(param):
    if isinstance(param, list):
        for p in param:
            assert isinstance(p, dict)
            explore_cleanup(p)

    elif isinstance(param, dict):
        for k, v in param.items():
            if k == "features":
                assert isinstance(param["features"], dict)
                explore_cleanup(param["features"])
            elif k == "contents":
                assert isinstance(param["contents"], list)
                explore_cleanup(param["contents"])
            else:
                assert ("human_readable" not in k)
                assert v is not None
                if isinstance(v, str):
                    assert v != ""
                elif isinstance(v, int):
                    assert v > 0


def test_cleanup(res):
    assert isinstance(res, list)
    explore_cleanup(res)
