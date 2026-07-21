import streamlit as st
import pandas as pd
from pathlib import Path

from enrichment.pipeline import EnrichmentPipeline
from enrichment.schema import PipelinePaths


st.title("Healthspan Horizons AI Contact Enrichment")

st.write(
    "Upload a CRM contact CSV to generate strategic partnership insights."
)


uploaded_file = st.file_uploader(
    "Upload contacts CSV",
    type=["csv"]
)


if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Contact Preview")
    st.dataframe(df.head())


    if st.button("Run AI Enrichment"):

        with st.spinner("Researching and enriching contacts..."):

            input_path = Path("uploaded_contacts.csv")
            output_path = Path("enriched_contacts.csv")

            df.to_csv(
                input_path,
                index=False
            )


            pipeline = EnrichmentPipeline(
                paths=PipelinePaths(
                    input_csv=str(input_path),
                    output_csv=str(output_path)
                )
            )


            result = pipeline.run()


            st.success(
                f"Completed enrichment for {len(result)} contacts"
            )


            with open(output_path, "rb") as file:

                st.download_button(
                    label="Download enriched CSV",
                    data=file,
                    file_name="enriched_contacts.csv",
                    mime="text/csv"
                )