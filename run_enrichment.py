#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from enrichment.pipeline import EnrichmentPipeline
from enrichment.schema import ENRICHMENT_COLUMNS, PipelinePaths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Enrich Healthspan Horizons newsletter contacts into a "
            "strategic partnership database."
        )
    )
    parser.add_argument(
        "--input",
        default="healthspan_contacts.csv",
        help="Path to CRM export CSV (default: healthspan_contacts.csv)",
    )
    parser.add_argument(
        "--output",
        default="enriched_contacts.csv",
        help="Path for enriched output CSV (default: enriched_contacts.csv)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline = EnrichmentPipeline(
        paths=PipelinePaths(input_csv=args.input, output_csv=args.output)
    )

    enriched = pipeline.run()
    row_count = len(enriched)

    print(f"Read:   {Path(args.input).resolve()}")
    print(f"Wrote:  {Path(args.output).resolve()}")
    print(f"Rows:   {row_count}")
    print(f"Added:  {len(ENRICHMENT_COLUMNS)} enrichment columns")
    print("Columns:")
    for column in ENRICHMENT_COLUMNS:
        print(f"  - {column}")


if __name__ == "__main__":
    main()

