from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseEnricher(ABC):
    """Interface for contact enrichment strategies."""

    @abstractmethod
    def enrich(self, contacts: pd.DataFrame) -> pd.DataFrame:
        """Return contacts with enrichment columns populated."""
