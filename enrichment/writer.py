from __future__ import annotations

from pathlib import Path

import pandas as pd

from enrichment.schema import ENRICHMENT_COLUMNS, validate_enrichment_columns


def write_enriched_contacts(df: pd.DataFrame, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    missing = validate_enrichment_columns(df.columns)
    if missing:
        raise ValueError(f"Output is missing enrichment columns: {', '.join(missing)}")

    source_columns = [column for column in df.columns if column not in ENRICHMENT_COLUMNS]
    ordered_columns = source_columns + list(ENRICHMENT_COLUMNS)
    df = df.reindex(columns=ordered_columns)
    df.to_csv(path, index=False)
    return path
