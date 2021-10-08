import io

from main import generate_parser, get_gpu, run_extract_data, upload
import os
import pytest

parser = generate_parser()
test_folders = [entries for entries in os.listdir("tests/") if os.path.isdir(f"tests/{entries}")]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/{fold}"):
        test_folders.remove(fold)

@pytest.fixture(scope="function", params=test_folders)
def args(request, monkeypatch):
    args = parser.parse_args(['-f', f'tests/{request.param}'])
    # the following function could prompt a menu requesting gpu location. Setting a value into stdin buffer just in case input is needed
    monkeypatch.setattr('sys.stdin', io.StringIO('b'))
    get_gpu(args)
    return args


def test_get_gpu(args):    # checking that gpu_location is correctly read
    # checking mutual exclusion
    assert any([args.cpu, args.gpu, args.motherboard]) and len([val for val in (args.cpu, args.gpu, args.motherboard) if val is True]) <= 1

