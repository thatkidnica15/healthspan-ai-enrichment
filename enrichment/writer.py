from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_enriched_contacts(
    enriched: pd.DataFrame,
    output_path: str
) -> None:

    output_file = Path(output_path)

    enriched.to_csv(
        output_file,
        index=False
    )