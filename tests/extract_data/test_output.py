import os

import pytest

import peracommon


def is_product(component: dict):
    # check if brand and model exist
    if "brand" not in component.keys() or "model" not in component.keys():
        return False

    return True


# noinspection DuplicatedCode
test_folders = [entries for entries in os.listdir("tests/source_files/") if os.path.isdir(f"tests/source_files/{entries}")]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/source_files/{fold}"):
        test_folders.remove(fold)


@pytest.fixture(params=test_folders)
def res(request):
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

    result = peracommon.call_parsers(path, parsers, where, False)
    result = peracommon.split_products(result)
    result = peracommon.make_tree(result)

    return result


def test_type_check(res):
    assert isinstance(res, list)
    _recursive_type_check(res)


def _recursive_type_check(res):
    for thing in res:
        assert thing["type"] in ("I", "P")
        if thing["type"] == "I":
            assert "brand" not in thing
            assert "model" not in thing
            assert "variant" not in thing
            assert "contents" in thing
            assert "features" in thing
            _recursive_type_check(thing["contents"])
        if thing["type"] == "P":
            assert "brand" in thing
            assert "model" in thing
            assert "variant" in thing
            assert "contents" not in thing
            assert "features" in thing
            for name in (thing["brand"].lower(), thing["model"].lower()):
                assert name not in ("", "null", "undefined", "unknown")


def test_has_chassis_and_mobo(res):
    components = set()

    for thing in res:
        assert "features" in thing
        assert "type" in thing["features"]
        components.add(thing["features"]["type"])

    assert len(components) > 0
    assert "motherboard" in components
    assert "case" in components


def test_check_product_keys(res):
    here = {
        "brand",
        "model",
        "variant",
        "arrival-batch",
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
    }

    assert isinstance(res, list)
    for thing in res:
        if thing["type"] == "P":
            for k in thing["features"].keys():
                assert k not in here


def test_cleanup(res):
    assert isinstance(res, list)
    _assert_cleanup_recursive(res)


def _assert_cleanup_recursive(res):
    for thing in res:
        for k, v in thing["features"].items():
            _assert_value_makes_sense(v)

            if "brand" in thing:
                _assert_value_makes_sense(thing["brand"])
            if "model" in thing:
                _assert_value_makes_sense(thing["model"])
            if "variant" in thing:
                _assert_value_makes_sense(thing["variant"])

            if "contents" in thing:
                _assert_cleanup_recursive(thing["contents"])


def _assert_value_makes_sense(v):
    assert v is not None
    if isinstance(v, str):
        assert v != ""
    elif isinstance(v, int):
        assert v > 0
    elif isinstance(v, float):
        assert v > 0
