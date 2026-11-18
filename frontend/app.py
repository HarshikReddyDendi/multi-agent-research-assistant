
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Multi-Agent AI Research Assistant")

st.write(
    "Research complex topics using specialized AI agents "
    "for research, analysis, report generation, and quality review."
)

st.divider()

# Research input
topic = st.text_area(
    "Enter your research topic",
    placeholder="Example: Impact of Generative AI on Software Engineering in 2026",
    height=100
)

# Generate report
if st.button("🚀 Start Research", type="primary"):

    if len(topic.strip()) < 5:
        st.warning("Please enter a research topic with at least 5 characters.")

    else:
        try:
            with st.spinner(
                "AI agents are researching, analyzing, and preparing your report..."
            ):
                response = requests.post(
                    f"{API_URL}/research",
                    json={"topic": topic.strip()},
                    timeout=600
                )

            if response.status_code == 200:
                result = response.json()

                st.success("Research completed!")

                st.subheader("📊 Research Status")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Approved",
                    "Yes" if result["approved"] else "No"
                )

                col2.metric(
                    "Revisions",
                    result["revision_count"]
                )

                st.divider()

                st.subheader("📄 Final Research Report")

                st.markdown(result["final_report"])

                st.download_button(
                    label="⬇️ Download Research Report",
                    data=result["final_report"],
                    file_name="research_report.md",
                    mime="text/markdown"
                )

                with st.expander("View Quality Review"):
                    st.write(result["review_feedback"])

            else:
                st.error(
                    f"API Error ({response.status_code}): "
                    f"{response.text}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Start the backend server first."
            )

        except requests.exceptions.Timeout:
            st.error(
                "Research timed out. Check the backend terminal."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")
