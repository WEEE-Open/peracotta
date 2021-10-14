import io
import os
import pytest
import time
from main import generate_parser, get_gpu, run_extract_data, upload


parser = generate_parser()
test_folders = [entries for entries in os.listdir("tests/") if os.path.isdir(f"tests/{entries}")]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/{fold}"):
        test_folders.remove(fold)


@pytest.fixture(params=test_folders)
def args(request, monkeypatch):
    args = parser.parse_args(['-f', f'tests/{request.param}'])
    # the following function could prompt a menu requesting gpu location.
    # Setting a value into stdin buffer just in case input is needed
    cli_input = io.StringIO('b')
    monkeypatch.setattr('sys.stdin', cli_input)
    get_gpu(args)
    return args


def test_get_gpu(args):  # checking that gpu_location is correctly read
    # checking mutual exclusion
    assert any([args.cpu, args.gpu, args.motherboard]) \
           and len([val for val in (args.cpu, args.gpu, args.motherboard) if val is True]) <= 1


def test_upload_pytarallo(args, monkeypatch, capsys):  # testing pytarallo integration with peracotta

    def auto_bulk_id():  # testing straight upload with automatic bulk_id
        cli_input = io.StringIO(f'y\n\n')
        monkeypatch.setattr('sys.stdin', cli_input)
        upload(run_extract_data(args.files, args))
        assert 'all went fine' in capsys.readouterr().out.lower()

    def fixed_bulk_id():  # testing automatic upload with a fixed bulk_id
        identifier = f'{args.files}{time.time()}'
        cli_input = io.StringIO(f'y\n{identifier}\n')
        monkeypatch.setattr('sys.stdin', cli_input)
        upload(run_extract_data(args.files, args))
        assert 'all went fine' in capsys.readouterr().out.lower()
        return identifier

    def overwrite_bulk_id(identifier):  # testing the overwrite of a bulk_id with an upload
        cli_input = io.StringIO(f'y\n{identifier}\ny\n')
        monkeypatch.setattr('sys.stdin', cli_input)
        upload(run_extract_data(args.files, args))
        output = capsys.readouterr().out.lower()
        assert 'do you want to try overwriting' in output
        assert 'all went fine' in output

    def change_identifier(old_identifier):  # testing an upload with a new identifier after a failure
        cli_input = io.StringIO(f'y\n{old_identifier}\nn\n{args.files}{time.time()}')
        monkeypatch.setattr('sys.stdin', cli_input)
        upload(run_extract_data(args.files, args))
        output = capsys.readouterr().out.lower()
        assert 'do you want to use another identifier' in output
        assert 'all went fine' in output

    try:

        auto_bulk_id()
        overwrite_id = fixed_bulk_id()
        overwrite_bulk_id(overwrite_id)
        change_identifier(overwrite_id)

    except EnvironmentError:
        # if this exception is raised probably bad config of peracotta/.env -> test must fail
        assert False
