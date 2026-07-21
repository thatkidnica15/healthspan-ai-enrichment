from __future__ import annotations

import pandas as pd

from enrichment.enrichers.base import BaseEnricher
from enrichment.schema import ENRICHMENT_COLUMNS, empty_enrichment_row


class StubEnricher(BaseEnricher):
    """
    Prepares enrichment columns without external lookups.

    Wire in LLM or web research enrichers here when ready.
    """

    def enrich(self, contacts: pd.DataFrame) -> pd.DataFrame:
        if contacts.empty:
            return pd.DataFrame(columns=list(contacts.columns) + list(ENRICHMENT_COLUMNS))

        enriched = contacts.copy()
        template = empty_enrichment_row()

        for column in ENRICHMENT_COLUMNS:
            if column not in enriched.columns:
                enriched[column] = template[column]

        return enriched
