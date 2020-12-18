from extract_data import extract_and_collect_data_from_generated_files as get_result
import pytest

#checks about peracotta's output
def type_check(res):
	assert isinstance(res, list)
	assert res[0]["type"] == "I"
	for comp in res[1:]:
		assert comp["type"] == "P"
		for name in (comp["brand"].lower(), comp["model"].lower()):
			assert name != "" and name != "null" and name != "undefined" and name != "unknown"


def has_chassis_and_mobo(res):
	assert isinstance(res[0]["features"], dict) and isinstance(res[0]["contents"], list) and res[0]["contents"] != []
	mobo = res[0]["contents"][0]
	assert isinstance(mobo["features"],dict) and mobo["features"] != {} and isinstance(mobo["contents"], list)


item_keys = ["arrival-batch", "cib", "cib-old", "cib-qr", "data-erased", "mac", "notes",
			"os-license-code", "os-license-version", "other-code", "owner", "smart-data",
			"sn", "software", "surface-scan","type", "working", "wwn"]
bmv = ["brand", "model", "variant"]


def explore_item(param):
	assert ("features" in param) and isinstance(param["features"], dict)
	for k in param["features"].keys():
		if k == "type" and param["features"]["type"] == "I":
			pass
		else:
			assert k in (item_keys+bmv)

	if "contents" in param.keys():
		for new_param in param["contents"]:
			explore_item(new_param)



def check_product_keys(res):
	for product in res[1:]:
		for k in product["features"].keys():
			assert k not in item_keys

def check_item_keys(res):
	explore_item(res[0])