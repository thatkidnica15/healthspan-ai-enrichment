from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

ENRICHMENT_COLUMNS: tuple[str, ...] = (
    "Verified Current Role",
    "Expertise Area",
    "Organization Description",
    "Industry Sector",
    "Organization Type",
    "Partnership Category",
    "Strategic Value Score",
    "Potential Collaboration",
    "Outreach Recommendation",
    "Research Notes",
)

# Brevo / Healthspan Horizons CRM export headers mapped to canonical names.
SOURCE_COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "contact_id": ("CONTACT ID", "contact_id", "Contact ID"),
    "email": ("EMAIL", "Email", "email", "Email Address"),
    "first_name": ("FIRSTNAME", "First Name", "first_name", "FirstName"),
    "last_name": ("LASTNAME", "Last Name", "last_name", "LastName"),
    "job_title": ("JOB_TITLE", "Job Title", "job_title", "Title", "Role"),
    "organization": ("ORGANIZATION", "Organization", "Company", "company"),
    "org_type": ("ORG_TYPE", "Organization Type", "org_type"),
    "linkedin": ("LINKEDIN", "LinkedIn", "linkedin"),
    "lifecycle_stage": ("LIFECYCLE_STAGE", "Lifecycle Stage"),
    "contact_stage": ("CONTACT_STAGE_CATEGORY", "Contact Stage"),
    "primary_interest": ("PRIMARY_INTEREST_CATEGORY", "Primary Interest"),
    "secondary_interests": ("SECONDARY_INTERESTS_MULTI", "Secondary Interests"),
    "partnership_interest": ("PARTNERSHIP_INTEREST", "Partnership Interest"),
    "white_paper_segment": ("WHITE_PAPER_SEGMENTATION", "Segment"),
    "gated_content": ("GATED_PUBLICATION_POST_TITLE", "Gated Content"),
    "signup_date": ("SIGNUP_DATE", "SIGNUP_DATE", "Subscription Date", "ADDED_TIME"),
    "talk_to_team": ("TALK_TO_TEAM", "Talk to Team"),
    "compass_demo_status": ("COMPASS_DEMO_STATUS", "Compass Demo Status"),
}


@dataclass(frozen=True)
class PipelinePaths:
    input_csv: str = "healthspan_contacts.csv"
    output_csv: str = "enriched_contacts.csv"


@dataclass(frozen=True)
class EnrichmentField:
    name: str
    description: str
    value_type: str


ENRICHMENT_FIELD_DEFINITIONS: tuple[EnrichmentField, ...] = (
    EnrichmentField(
        "Verified Current Role",
        "Current professional title verified against public sources.",
        "text",
    ),
    EnrichmentField(
        "Expertise Area",
        "Primary domain of expertise (e.g. longevity science, policy, investing).",
        "text",
    ),
    EnrichmentField(
        "Organization Description",
        "Brief summary of the contact's organization and mission.",
        "text",
    ),
    EnrichmentField(
        "Industry Sector",
        "High-level sector classification (e.g. biotech, academia, media).",
        "text",
    ),
    EnrichmentField(
        "Organization Type",
        "Entity type (e.g. startup, nonprofit, hospital, fund).",
        "text",
    ),
    EnrichmentField(
        "Partnership Category",
        "Recommended partnership lane for Healthspan Horizons.",
        "text",
    ),
    EnrichmentField(
        "Strategic Value Score",
        "Numeric score from 1-10 indicating partnership priority.",
        "integer",
    ),
    EnrichmentField(
        "Potential Collaboration",
        "Concrete collaboration ideas aligned with Healthspan Horizons goals.",
        "text",
    ),
    EnrichmentField(
        "Outreach Recommendation",
        "Suggested outreach angle, channel, and timing.",
        "text",
    ),
    EnrichmentField(
        "Research Notes",
        "Free-form notes from enrichment research.",
        "text",
    ),
)


def empty_enrichment_row() -> dict[str, str]:
    return {column: "" for column in ENRICHMENT_COLUMNS}


def validate_enrichment_columns(columns: Sequence[str]) -> list[str]:
    return [column for column in ENRICHMENT_COLUMNS if column not in columns]
