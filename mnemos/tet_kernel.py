"""Minimal `.tet` kernel helpers for address/basis/operator normalization.

This module intentionally provides small, deterministic primitives that can be
used by future parser/runtime work:

- address parsing as recursive descent words,
- local-basis closure checks,
- basis-driven address expansion,
- morphism symbol normalization (`->` -> `>`).
"""

from __future__ import annotations

from itertools import product

GLOBAL_DIRECTIONS = ("w", "x", "y", "z")
CONTEXT_ARITY = {"P": 1, "E": 2, "F": 3, "T": 4}


class TetKernelError(ValueError):
    """Raised when a `.tet` kernel input is malformed."""


def normalize_morphism(expression: str) -> str:
    """Normalize legacy two-character morphism notation to `>`.

    The kernel prefers `>` while preserving all other symbols untouched.
    """

    return expression.replace("->", ">")


def parse_address(address: str) -> tuple[str, ...]:
    """Parse a dotted address into recursive descent symbols.

    Valid symbols are from the global tetrahedral alphabet: w, x, y, z.
    """

    raw = address.strip()
    if not raw:
        raise TetKernelError("address cannot be empty")

    parts = tuple(seg.strip() for seg in raw.split("."))
    if any(not seg for seg in parts):
        raise TetKernelError(f"invalid address segment in {address!r}")

    invalid = [seg for seg in parts if seg not in GLOBAL_DIRECTIONS]
    if invalid:
        raise TetKernelError(
            f"invalid direction(s) {invalid}; expected subset of {GLOBAL_DIRECTIONS}"
        )
    return parts


def validate_basis(context: str, basis: tuple[str, ...]) -> tuple[str, ...]:
    """Validate that basis size and members match a context arity.

    Contexts use arity mapping: P=1, E=2, F=3, T=4.
    """

    if context not in CONTEXT_ARITY:
        raise TetKernelError(f"unknown context {context!r}")

    if len(set(basis)) != len(basis):
        raise TetKernelError("basis entries must be unique")

    expected = CONTEXT_ARITY[context]
    if len(basis) != expected:
        raise TetKernelError(
            f"context {context} expects {expected} directions, got {len(basis)}"
        )

    invalid = [symbol for symbol in basis if symbol not in GLOBAL_DIRECTIONS]
    if invalid:
        raise TetKernelError(
            f"invalid basis direction(s) {invalid}; expected subset of {GLOBAL_DIRECTIONS}"
        )

    return basis


def address_in_basis(address: str, basis: tuple[str, ...]) -> bool:
    """Return True when an address is closed over the local basis."""

    parts = parse_address(address)
    allowed = set(basis)
    return all(part in allowed for part in parts)


def expand_basis_addresses(basis: tuple[str, ...], depth: int) -> tuple[str, ...]:
    """Enumerate addresses of exact depth over a validated local basis."""

    if depth <= 0:
        raise TetKernelError("depth must be >= 1")

    # Validate as generic basis against tetra alphabet.
    invalid = [symbol for symbol in basis if symbol not in GLOBAL_DIRECTIONS]
    if invalid:
        raise TetKernelError(
            f"invalid basis direction(s) {invalid}; expected subset of {GLOBAL_DIRECTIONS}"
        )
    if len(set(basis)) != len(basis):
        raise TetKernelError("basis entries must be unique")

    return tuple(".".join(parts) for parts in product(basis, repeat=depth))
