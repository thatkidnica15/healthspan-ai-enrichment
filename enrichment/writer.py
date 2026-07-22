from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_enriched_contacts(
    enriched: pd.DataFrame,
    output_path: str
) -> None:

    output_file = Path(output_path).with_suffix(".xlsx")

    print("WRITING EXCEL FILE:", output_file)

    enriched.to_excel(
        output_file,
        index=False,
        engine="openpyxl"
    )

    print("EXCEL SAVED")