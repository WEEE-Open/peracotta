import os
import pytest

import peracommon


def is_product(component: dict):
    # check if brand and model exist
    if "brand" not in component.keys() or "model" not in component.keys():
        return False

    return True


test_folders = [
    entries
    for entries in os.listdir("tests/source_files")
    if os.path.isdir(f"tests/source_files/{entries}")
]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/source_files/{fold}"):
        test_folders.remove(fold)


@pytest.fixture(scope="module", params=test_folders)
def do_it(request):
    # noinspection DuplicatedCode
    parsers = {
        peracommon.ParserComponents.CPU,
        peracommon.ParserComponents.GPU,
        peracommon.ParserComponents.MOTHERBOARD,
        peracommon.ParserComponents.RAM,
        peracommon.ParserComponents.CASE,
        peracommon.ParserComponents.PSU,
    }

    path = f"tests/source_files/{request.param}"
    try:
        with open(os.path.join(path, "gpu_location.txt"), "r") as f:
            gpu_flag = f.readline()
            if gpu_flag == "cpu":
                where = peracommon.GpuLocation.CPU
            elif gpu_flag == "gpu":
                where = peracommon.GpuLocation.DISCRETE
            else:
                where = peracommon.GpuLocation.MOTHERBOARD
    except FileNotFoundError:
        where = peracommon.GpuLocation.NONE

    result = peracommon.call_parsers(path, parsers, where)
    result = peracommon.split_products(result)
    result = peracommon.make_tree(result)
    return result


# checks about peracotta's output
def test_type_check(res):
    assert isinstance(res, list)
    assert res[0]["type"] == "I"
    for comp in res[1:]:
        assert comp["type"] == "P"
        for name in (comp["brand"].lower(), comp["model"].lower()):
            assert name not in ("", "null", "undefined", "unknown")


def test_has_chassis_and_mobo(res):
    assert (
        isinstance(res[0]["features"], dict)
        and isinstance(res[0]["contents"], list)
        and res[0]["contents"] != []
    )
    mobo = res[0]["contents"][0]
    assert (
        isinstance(mobo["features"], dict)
        and mobo["features"] != {}
        and isinstance(mobo["contents"], list)
    )


item_keys = [
    "arrival-batch",
    "cib",
    "cib-old",
    "cib-qr",
    "data-erased",
    "mac",
    "notes",
    "os-license-code",
    "os-license-version",
    "other-code",
    "owner",
    "smart-data",
    "sn",
    "software",
    "surface-scan",
    "working",
    "wwn",
]
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
        assert param != dict()
        for k, v in param.items():
            if k == "features":
                assert isinstance(param["features"], dict)
                explore_cleanup(param["features"])
            elif k == "contents":
                assert isinstance(param["contents"], list)
                explore_cleanup(param["contents"])
            else:
                assert "human_readable" not in k
                assert v is not None
                if isinstance(v, str):
                    assert v != ""
                elif isinstance(v, int):
                    assert v > 0


def test_cleanup(res):
    assert isinstance(res, list)
    explore_cleanup(res)
