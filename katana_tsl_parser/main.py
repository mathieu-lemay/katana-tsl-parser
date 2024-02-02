#! /usr/bin/env python
import json
import sys
from copy import deepcopy
from pathlib import Path

from katana_tsl_parser.models import TslModel
from katana_tsl_parser.models.tsl import MAX_NAME_LENGTH

root = Path(__file__).parent.parent


def encode_name(name: str) -> list[str]:
    if len(name) > MAX_NAME_LENGTH:
        # EM101: Exception must not use a string literal, assign to variable first
        # TRY003: Avoid specifying long messages outside the exception class
        raise ValueError("Name too long")  # noqa: EM101, TRY003

    return [f"{ord(c):02x}" for c in name] + ["20"] * (16 - len(name))


def s(v: int) -> str:
    return f"{v:02x}"


def update_some_values(f: str) -> None:
    tsl = json.loads(Path(f).read_text())

    default_patch = tsl["data"][0][0]
    for v in (0, 1, 5, 10, 20, 42, 55, 100):
        patch = deepcopy(default_patch)

        val = s(v)
        patch["paramSet"]["UserPatch%PatchName"] = encode_name(f"Patch0[25]-{v:02}")
        patch["paramSet"]["UserPatch%Patch_0"][20] = val
        patch["paramSet"]["UserPatch%Patch_0"][21] = val
        patch["paramSet"]["UserPatch%Patch_0"][22] = val

        patch["paramSet"]["UserPatch%Patch_0"][25] = val

        tsl["data"][0].append(patch)

    Path("patches.tsl").write_text(json.dumps(tsl))


def main() -> None:
    if len(sys.argv) != 2:  # noqa: PLR2004: Magic value. Replace with proper cli.
        # EM102 Exception must not use an f-string literal, assign to variable first
        # TRY003: Avoid specifying long messages outside the exception class
        raise ValueError(f"Usage: {sys.argv[0]} tsl-file")  # noqa: EM102, TRY003

    f = Path(sys.argv[1])
    tsl = TslModel.model_validate_json(f.read_text())
    print(tsl.model_dump_json(indent=2))  # noqa: T201: print found


if __name__ == "__main__":
    main()
