from extract_data import extract_and_collect_data_from_generated_files as get_result
import os
import pytest

def is_product(component : dict):
	# check if brand and model exist
	if "brand" not in component.keys() or "model" not in component.keys():
		return False
	# check if brand or model has a not valid value
	candidates = [component["brand"].lower(), component["model"].lower()]
	for candidate in candidates:
		if isinstance(candidate, str) and (
				candidate == "" or candidate == "null" or candidate == "unknown" or candidate == "undefined"):
			return False
	# if all conditions are False, the product should be added
	return True


test_folders = [dir for dir in os.listdir("tests/") if os.path.isdir(f"tests/{dir}")]
for fold in set(test_folders):
	if "baseboard.txt" not in os.listdir(f"tests/{fold}"):
		test_folders.remove(fold)


@pytest.fixture(scope="module", params=test_folders)
def res(request):
    path = f"tests/{request.param}"
    return get_result(directory=path, has_dedicated_gpu=False, gpu_in_cpu=False, cleanup=True)

#checks about peracotta's output
def test_type_check(res):
	assert isinstance(res, list)
	assert res[0]["type"] == "I"
	for comp in res[1:]:
		assert comp["type"] == "P"
		for name in (comp["brand"].lower(), comp["model"].lower()):
			assert name != "" and name != "null" and name != "undefined" and name != "unknown"


def test_has_chassis_and_mobo(res):
	assert isinstance(res[0]["features"], dict) and isinstance(res[0]["contents"], list) and res[0]["contents"] != []
	mobo = res[0]["contents"][0]
	assert isinstance(mobo["features"],dict) and mobo["features"] != {} and isinstance(mobo["contents"], list)


item_keys = ["arrival-batch", "cib", "cib-old", "cib-qr", "data-erased", "mac", "notes",
			"os-license-code", "os-license-version", "other-code", "owner", "smart-data",
			"sn", "software", "surface-scan", "type", "working", "wwn"]
bmv = ["brand", "model", "variant"]


def explore_item(param):
	assert ("features" in param) and isinstance(param["features"], dict)
	for k in param["features"].keys():
		if k == "type" and param["features"]["type"] == "I":
			pass
		#if is not a product (no brand or model) all the keys are in item
		elif is_product(param["features"]):
			assert k in (item_keys+bmv)

	if "contents" in param.keys():
		for new_param in param["contents"]:
			explore_item(new_param)



def test_check_product_keys(res):
	for product in res[1:]:
		for k in product["features"].keys():
			assert k not in item_keys

def test_check_item_keys(res):
	explore_item(res[0])

def explore_cleanup(param):
	if isinstance(param, list):
		for p in param:
			explore_cleanup(p)

	elif isinstance(param, dict):
		for k, v in param.items():
			if k == "features":
				explore_cleanup(param["features"])
			elif k == "contents":
				explore_cleanup(param["contents"])
			else:
				assert ("human_readable" not in k)
				if isinstance(v, str):
					assert v != ""
				elif isinstance(v, int):
					assert v > 0


def test_cleanup(res):
	explore_cleanup(res)

