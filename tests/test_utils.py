import os
from bit_scrapper.utils.writer import write_csv, write_json

data = [{"a": 1, "b": 2}]

def test_write_json_creates_file(tmp_path):
    file = tmp_path / "data.json"
    write_json(data, str(file))
    assert file.exists()

def test_save_csv_creates_file(tmp_path):
    file = tmp_path / "data.csv"
    write_csv(data, str(file))
    assert file.exists()