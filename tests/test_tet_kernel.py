from importlib import util
from pathlib import Path

import pytest

spec = util.spec_from_file_location(
    "tet_kernel", Path(__file__).resolve().parents[1] / "mnemos" / "tet_kernel.py"
)
tet_kernel = util.module_from_spec(spec)
spec.loader.exec_module(tet_kernel)

TetKernelError = tet_kernel.TetKernelError
address_in_basis = tet_kernel.address_in_basis
expand_basis_addresses = tet_kernel.expand_basis_addresses
normalize_morphism = tet_kernel.normalize_morphism
parse_address = tet_kernel.parse_address
validate_basis = tet_kernel.validate_basis


def test_parse_address_valid():
    assert parse_address("w.x.y") == ("w", "x", "y")


def test_parse_address_rejects_invalid_symbol():
    with pytest.raises(TetKernelError):
        parse_address("w.q")


def test_validate_basis_enforces_arity():
    assert validate_basis("E", ("w", "y")) == ("w", "y")
    with pytest.raises(TetKernelError):
        validate_basis("E", ("w", "x", "y"))


def test_address_in_basis_closure():
    assert address_in_basis("w.y.w", ("w", "y")) is True
    assert address_in_basis("w.x", ("w", "y")) is False


def test_expand_basis_addresses_depth_two():
    assert expand_basis_addresses(("w", "y"), 2) == (
        "w.w",
        "w.y",
        "y.w",
        "y.y",
    )


def test_normalize_morphism():
    assert normalize_morphism("L->F") == "L>F"
    assert normalize_morphism("a->b->c") == "a>b>c"
