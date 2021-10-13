import io
from main import generate_parser, get_gpu, run_extract_data, upload
import os
import pytest
import time

parser = generate_parser()
test_folders = [entries for entries in os.listdir("tests/") if os.path.isdir(f"tests/{entries}")]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/{fold}"):
        test_folders.remove(fold)

"""@pytest.fixture(scope='module', params=test_folders)
def running_instance(request):
    assert os.getcwd() == '/home/jahooo/WEEE-Open/peracotta'
    running_process = subprocess.Popen(['./main.py', '-f', f'tests/{request.param}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return running_process

def test_integration(running_instance, capsys):"""



@pytest.fixture(scope="function", params=test_folders)
def args(request, monkeypatch):
    args = parser.parse_args(['-f', f'tests/{request.param}'])
    # the following function could prompt a menu requesting gpu location. Setting a value into stdin buffer just in case input is needed
    cli_input = io.StringIO('b')
    monkeypatch.setattr('sys.stdin', cli_input)
    get_gpu(args)
    return args


def test_get_gpu(args):    # checking that gpu_location is correctly read
    # checking mutual exclusion
    assert any([args.cpu, args.gpu, args.motherboard]) and len([val for val in (args.cpu, args.gpu, args.motherboard) if val is True]) <= 1


def test_upload_to_pytarallo(args, monkeypatch, capsys):  # testing pytarallo integration with peracotta
    # Expected Do you want to automatically upload? Yeah
    try:
        cli_input = io.StringIO(f'y\n\n')
        monkeypatch.setattr('sys.stdin', cli_input)
        upload(run_extract_data(args.files, args))
        #time.sleep(1)

    except EnvironmentError:
        # if this exception is raised probably bad config of peracotta/.env -> test must fail
        assert False
