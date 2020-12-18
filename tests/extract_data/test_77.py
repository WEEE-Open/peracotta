from tests.extract_data.megatest9000 import *
import os

#TODO: Add directories dinamically
@pytest.fixture(scope="module", params=["77","asdpc"])
def res(request):
    path = f"tests/{request.param}"
    return get_result(directory=path, has_dedicated_gpu=False, gpu_in_cpu=False, cleanup=True)


def test_77_type_check(res):
    type_check(res)


def test_77_has_chassis_and_mobo(res):
    has_chassis_and_mobo(res)


def test_77_check_product_keys(res):
    check_product_keys(res)


def test_77_check_item_keys(res):
    explore_item(res[0])

#cleanup test: see the parts that needs cleanup
def test_77_cleanup(res):
    assert res[0]["features"] == {"type": "case",
                                  "brand": "Chassis Manufacture",
                                  "sn": "Chassis Serial Number"}
