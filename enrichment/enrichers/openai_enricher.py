from __future__ import annotations

import json
import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from enrichment.enrichers.base import BaseEnricher
from enrichment.schema import ENRICHMENT_COLUMNS
from enrichment.tavily_researcher import TavilyResearcher

load_dotenv()


class OpenAIEnricher(BaseEnricher):

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.researcher = TavilyResearcher()


    def enrich(self, contacts: pd.DataFrame) -> pd.DataFrame:

# contacts = contacts.head(5)
        enriched = contacts.copy()

        for column in ENRICHMENT_COLUMNS:
            enriched[column] = None
             enriched[column] = enriched[column].astype(object)
             
        for index, row in enriched.iterrows():

            name = f"{row.get('first_name', '')} {row.get('last_name', '')}"
            organization = row.get("organization", "")
            job_title = row.get("job_title", "")

            print("\nRESEARCHING:", name, organization)

            research = self.researcher.research_contact(
                name,
                organization,
                job_title
            )

            print("TAVILY RESULT:")
            print(research[:300])

            prompt = f"""
You are researching a contact for Healthspan Horizons.

Analyze this person and return ONLY valid JSON.

Name:
{name}

Organization:
{organization}

Job Title:
{job_title}

LinkedIn:
{row.get('linkedin', '')}

Primary Interest:
{row.get('primary_interest', '')}

Public research:
{research}

Return JSON with exactly these fields:

{{
"Verified Current Role": "",
"Expertise Area": "",
"Organization Description": "",
"Industry Sector": "",
"Organization Type": "",
"Partnership Category": "",
"Strategic Value Score": 0,
"Potential Collaboration": "",
"Outreach Recommendation": "",
"Research Notes": ""
}}

Strategic Value Score must be an integer from 1-10.
"""

            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                response_format={
                    "type": "json_object"
                },
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            result = response.choices[0].message.content.strip()

            print("GPT RESPONSE:")
            print(result)

            try:
                data = json.loads(result)

            except json.JSONDecodeError:
                print("INVALID JSON RESPONSE")
                print(result)
                enriched.loc[index, "Research Notes"] = result
                continue

            print("FIELDS RECEIVED:")
            print(data.keys())

            
            for column in ENRICHMENT_COLUMNS:
                value = data.get(column, "")
                
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)

                enriched.loc[index, column] = str(value)
                
        return enriched