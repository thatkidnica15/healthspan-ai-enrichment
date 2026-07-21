from __future__ import annotations

from pathlib import Path

import pandas as pd

from enrichment.schema import SOURCE_COLUMN_ALIASES


def _is_export_header_row(line: str) -> bool:
    normalized = line.strip().upper()
    return normalized.startswith("CONTACT ID,") or normalized.startswith("CONTACT ID;")


def _detect_header_row_index(path: Path) -> int:
    with path.open(encoding="utf-8-sig") as handle:
        for index, line in enumerate(handle):
            if _is_export_header_row(line):
                return index
    return 0


def read_contacts(input_path: str | Path) -> pd.DataFrame:
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.stat().st_size == 0:
        return pd.DataFrame()

    header_row = _detect_header_row_index(path)
    df = pd.read_csv(
        path,
        dtype=str,
        keep_default_na=False,
        skiprows=range(header_row),
    )
    return normalize_source_columns(df)


def normalize_source_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map: dict[str, str] = {}

    for canonical, aliases in SOURCE_COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in df.columns and canonical not in rename_map.values():
                rename_map[alias] = canonical
                break

    if rename_map:
        df = df.rename(columns=rename_map)

    return df
