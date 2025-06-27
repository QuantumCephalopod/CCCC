from importlib import util
from pathlib import Path
from types import SimpleNamespace

spec = util.spec_from_file_location("carbon_reader", Path(__file__).resolve().parents[1] / "carbon_reader.py")
carbon_reader = util.module_from_spec(spec)
spec.loader.exec_module(carbon_reader)


def test_preview(tmp_path, capsys):
    file = tmp_path / "sample.txt"
    file.write_text("b\na\nc\n")

    lines = carbon_reader.preview(file, lines=2, sort=True)
    assert lines == ["a", "b"]

    args = SimpleNamespace(carbon_file=file, lines=2, sort=True)
    carbon_reader._cmd_preview(args)
    captured = capsys.readouterr()
    assert captured.out.splitlines() == ["a", "b"]
