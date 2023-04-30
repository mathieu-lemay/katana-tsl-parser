import json
from pathlib import Path

import pytest

from katana_tsl_parser.models import TslModel


@pytest.fixture()
def snapshots_folder() -> Path:
    return Path(__file__).parent / "snapshots"


def test_parse_model_v1(snapshots_folder: Path) -> None:
    tsl = json.loads((snapshots_folder / "factory_v1.tsl").read_text())
    tsl_model = TslModel.decode_tsl(tsl)

    with (snapshots_folder / "factory_v1.json").open() as f:
        expected = json.load(f)

    assert tsl_model.dict() == expected


def test_parse_model_v2_temp(snapshots_folder: Path) -> None:
    tsl = json.loads((snapshots_folder / "temp_v2.tsl").read_text())
    tsl_model = TslModel.decode_tsl(tsl)

    with (snapshots_folder / "temp_v2.json").open() as f:
        expected = json.load(f)

    assert tsl_model.dict() == expected
