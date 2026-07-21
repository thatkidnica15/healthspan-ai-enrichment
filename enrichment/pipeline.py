from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from enrichment.enrichers.base import BaseEnricher
from enrichment.enrichers.openai_enricher import OpenAIEnricher
from enrichment.reader import read_contacts
from enrichment.schema import PipelinePaths
from enrichment.writer import write_enriched_contacts


@dataclass
class EnrichmentPipeline:
    paths: PipelinePaths
    enricher: BaseEnricher | None = None

    def __post_init__(self) -> None:
        if self.enricher is None:
            self.enricher = OpenAIEnricher()

    def run(self) -> pd.DataFrame:
        contacts = read_contacts(self.paths.input_csv)

        print("CONTACTS LOADED:", len(contacts))
        print("COLUMNS:", contacts.columns.tolist())
        print("FIRST ROW:", contacts.iloc[0].to_dict())

# contacts = contacts.head(5)
        print("USING ENRICHER:", type(self.enricher))

        enriched = self.enricher.enrich(contacts)

        print("ENRICHMENT COMPLETE")

        write_enriched_contacts(enriched, self.paths.output_csv)

        return enriched

    def summary(self) -> dict[str, str | int]:
        input_path = Path(self.paths.input_csv)
        output_path = Path(self.paths.output_csv)

        return {
            "input_file": str(input_path),
            "output_file": str(output_path),
            "input_exists": int(input_path.exists()),
            "input_bytes": input_path.stat().st_size if input_path.exists() else 0,
            "output_exists": int(output_path.exists()),
        }