import streamlit as st
from auditor import audit_job_posting

# Page Configuration
st.set_page_config(
    page_title="HR Algorithmic Bias & Compliance Auditor",
    page_icon="⚖️",
    layout="wide"
)

# Header & Context
st.title("⚖️️ HR Algorithmic Bias & Compliance Auditor")
st.markdown("""
*An automated audit engine evaluating job postings and candidate screening rubrics for adverse impact, demographic bias, and regulatory compliance under the **EU AI Act** and **EEOC standards**.*
""")

# Sidebar settings & sample loader
st.sidebar.header("Audit Configuration")
st.sidebar.info("Auditing against: EU AI Act High-Risk Employment Standards, EEOC Non-Discrimination, and Gender-Coded Lexicons.")

sample_biased_text = """We are looking for a rockstar digital native who can aggressively dominate our competitors. The ideal candidate graduated with an elite degree within the last 3 years, has native English fluency, and exhibits relentless energy and stamina to thrive in a high-pressure 60+ hour work week."""

sample_neutral_text = """We are seeking a Growth Marketing Specialist to expand our customer base and optimize digital campaigns. The ideal candidate brings demonstrable experience in B2B performance marketing, strong cross-functional communication skills, and data analysis proficiency. We welcome applicants with equivalent practical experience and offer flexible working arrangements."""

selected_template = st.sidebar.selectbox(
    "Load Sample Template:",
    ["Custom Input", "Sample Biased Posting", "Sample Neutral Posting"]
)

# Input columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Requisition Input")
    job_title = st.text_input("Job Title / Role Requisition", value="Growth Marketing Specialist")
    
    # Pre-populate based on template selection
    default_text = ""
    if selected_template == "Sample Biased Posting":
        default_text = sample_biased_text
    elif selected_template == "Sample Neutral Posting":
        default_text = sample_neutral_text

    text_input = st.text_area(
        "Job Description or Screening Rubric",
        value=default_text,
        height=320,
        placeholder="Paste your job description or candidate evaluation prompt here..."
    )

    audit_button = st.button("🔍 Run Compliance Audit", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 Audit Results & Risk Assessment")
    
    if audit_button:
        if not text_input.strip():
            st.warning("Please enter some text to audit.")
        else:
            with st.spinner("Analyzing text against bias taxonomies and regulatory rubrics..."):
                try:
                    result = audit_job_posting(job_title=job_title, text=text_input)
                    
                    score = result["overall_fairness_score"]
                    risk = result["risk_level"]
                    
                    # Top Metrics Display
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric(label="Overall Fairness Score", value=f"{score} / 100")
                    with m2:
                        if risk.lower() == "high":
                            st.error(f"⚠️ Regulatory Risk: **{risk}**")
                        elif risk.lower() == "medium":
                            st.warning(f"⚡ Regulatory Risk: **{risk}**")
                        else:
                            st.success(f"✅ Regulatory Risk: **{risk}**")
                    
                    st.divider()

                    # Executive Summary
                    st.markdown("#### Executive Summary")
                    st.write(result["summary"])

                    # Bias Flags Breakdown
                    st.markdown("#### Identified Bias Vectors & Proxies")
                    flags = result.get("flags", [])
                    if not flags:
                        st.success("No significant exclusionary markers detected!")
                    else:
                        for flag in flags:
                            with st.expander(f"🚩 **[{flag['category']}]** \"{flag['flagged_phrase']}\""):
                                st.markdown(f"**Compliance Issue:** {flag['explanation']}")
                                st.markdown(f"**Recommended Replacement:** `{flag['suggested_replacement']}`")

                    st.divider()

                    # Inclusive Rewrite
                    st.markdown("#### 💡 Proposed Inclusive Rewrite")
                    st.text_area("Approved Copy", value=result["inclusive_rewrite"], height=180)

                except Exception as e:
                    st.error(f"Audit failed: {e}")
    else:
        st.info("Paste your text on the left and click **Run Compliance Audit** to generate the assessment.")