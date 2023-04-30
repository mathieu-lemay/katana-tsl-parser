import json
from pathlib import Path

import pytest

from katana_tsl_parser.models import TslModel


@pytest.fixture()
def snapshots_folder() -> Path:
    return Path(__file__).parent / "snapshots"


def test_parse_model_v1(snapshots_folder: Path) -> None:
    tsl = TslModel.parse_file((snapshots_folder / "factory_v1.tsl"))

    with (snapshots_folder / "factory_v1.json").open() as f:
        expected = json.load(f)

    assert tsl.dict() == expected
