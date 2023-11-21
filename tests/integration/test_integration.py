import io
import os
import sys
import time

import pytest
from dotenv import load_dotenv

import peracotta.commons as commons


def import_executable(name):
    import importlib.machinery
    import importlib.util

    spec = importlib.util.spec_from_loader(name, importlib.machinery.SourceFileLoader(name, f"{os.path.dirname(__file__)}/../../{name}"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module


peracruda = import_executable("peracruda")


test_folders = [entries for entries in os.listdir("tests/source_files/") if os.path.isdir(f"tests/source_files/{entries}")]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/source_files/{fold}"):
        test_folders.remove(fold)

# @pytest.fixture(params=test_folders)
# def args(request, monkeypatch):
#     parser = peracruda.generate_parser()
#     args = parser.parse_args(["-f", f"tests/source_files/{request.param}"])
#     # the following function could prompt a menu requesting gpu location.
#     # Setting a value into stdin buffer just in case input is needed
#     cli_input = io.StringIO("b")
#     monkeypatch.setattr("sys.stdin", cli_input)
#     return args

# def test_get_gpu(args):  # checking that gpu_location is correctly read
#     # checking mutual exclusion
#     assert [args.cpu, args.gpu, args.motherboard].count(True) <= 1


@pytest.fixture(params=test_folders)
def args2(request):
    # noinspection DuplicatedCode
    parsers = {
        commons.ParserComponents.CPU,
        commons.ParserComponents.GPU,
        commons.ParserComponents.MOTHERBOARD,
        commons.ParserComponents.RAM,
        commons.ParserComponents.CASE,
        commons.ParserComponents.PSU,
    }

    path = f"tests/source_files/{request.param}"
    try:
        with open(os.path.join(path, "gpu_location.txt"), "r") as f:
            gpu_flag = f.readline()
            if gpu_flag == "cpu":
                where = commons.GpuLocation.CPU
            elif gpu_flag == "gpu":
                where = commons.GpuLocation.DISCRETE
            else:
                where = commons.GpuLocation.MOTHERBOARD
    except FileNotFoundError:
        where = commons.GpuLocation.NONE

    return path, parsers, where


@pytest.fixture(autouse=True)
def load_dotenv_for_upload():
    load_dotenv()


@pytest.mark.upload
def test_upload_pytarallo(args2, monkeypatch, capsys):  # testing pytarallo integration with peracotta
    def auto_bulk_id():  # testing straight upload with automatic bulk_id
        cli_input = io.StringIO("y\n\n")
        monkeypatch.setattr("sys.stdin", cli_input)
        peracruda.upload_to_tarallo(result)
        assert "all went fine" in capsys.readouterr().out.lower()

    def fixed_bulk_id():  # testing automatic upload with a fixed bulk_id
        identifier = f"{args2[0]}{time.time()}"
        cli_input = io.StringIO(f"y\n{identifier}\n")
        monkeypatch.setattr("sys.stdin", cli_input)
        peracruda.upload_to_tarallo(result)
        assert "all went fine" in capsys.readouterr().out.lower()
        return identifier

    def overwrite_bulk_id(
        identifier,
    ):  # testing the overwrite of a bulk_id with an upload
        cli_input = io.StringIO(f"y\n{identifier}\ny\n")
        monkeypatch.setattr("sys.stdin", cli_input)
        peracruda.upload_to_tarallo(result)
        output = capsys.readouterr().out.lower()
        assert "do you want to try overwriting" in output
        assert "all went fine" in output

    def change_identifier(
        old_identifier,
    ):  # testing an upload with a new identifier after a failure
        cli_input = io.StringIO(f"y\n{old_identifier}\nn\n{args2[0]}{time.time()}")
        monkeypatch.setattr("sys.stdin", cli_input)
        peracruda.upload_to_tarallo(result)
        output = capsys.readouterr().out.lower()
        assert "do you want to use another identifier" in output
        assert "all went fine" in output

    try:
        result = commons.call_parsers(args2[0], args2[1], args2[2])
        result = commons.split_products(result)
        result = commons.make_tree(result)

        auto_bulk_id()
        overwrite_id = fixed_bulk_id()
        overwrite_bulk_id(overwrite_id)
        change_identifier(overwrite_id)

    except EnvironmentError:
        # if this exception is raised probably bad config of peracotta/.env -> test must fail
        assert False, "Bad peracotta .env configuration"
