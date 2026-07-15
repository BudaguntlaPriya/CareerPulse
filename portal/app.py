
import streamlit as st
import pandas as pd
from db import get_connection

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="CareerPulse",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("CareerPulse")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔍 Search Jobs",
        "🎯 Career Guidance",
        "🏢 Companies",
        "📊 Market Insights"
    ]
)

# =================================================
# HOME PAGE
# =================================================

if page == "🏠 Home":

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM dim_jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT company) FROM dim_jobs")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM dim_skills")
    total_skills = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT location) FROM dim_jobs")
    total_locations = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            job_title,
            company,
            location,
            searched_role,
            posted_date
        FROM dim_jobs
        ORDER BY posted_date DESC
    """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    st.title("📊 CareerPulse")
    st.subheader("Job Market Intelligence Platform")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Jobs", total_jobs)
    col2.metric("Companies", total_companies)
    col3.metric("Skills", total_skills)
    col4.metric("Locations", total_locations)

    st.markdown("---")

    st.subheader("Latest Jobs")

    if len(jobs) == 0:

        st.warning("No jobs found.")

    else:

        st.success(f"{len(jobs)} jobs found")

    for job in jobs:

        title = job[0]
        company = job[1]
        location = job[2]
        posted = job[3]
        link = job[4]

        with st.container():

            st.subheader(title)

            st.write(f"🏢 **Company:** {company}")

            st.write(f"📍 **Location:** {location}")

            st.write(f"📅 **Posted Date:** {posted}")

            st.link_button(
                "🔗 Apply Now",
                link
            )

            st.markdown("---")

# =================================================
# SEARCH PAGE
# =================================================



elif page == "🔍 Search Jobs":

    st.title("🔍 Search Jobs")

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Job Roles
    # -----------------------------
    cursor.execute("""
        SELECT DISTINCT searched_role
        FROM dim_jobs
        ORDER BY searched_role
    """)

    roles = [row[0] for row in cursor.fetchall()]

    selected_role = st.selectbox(
        "Select Job Role",
        roles
    )

    # -----------------------------
    # Companies
    # -----------------------------
    cursor.execute("""
        SELECT DISTINCT company
        FROM dim_jobs
        WHERE searched_role = %s
        ORDER BY company
    """, (selected_role,))

    companies = ["All Companies"] + [row[0] for row in cursor.fetchall()]

    selected_company = st.selectbox(
        "Select Company",
        companies
    )
    # -----------------------------
    # Locations
    # -----------------------------
    cursor.execute("""
    SELECT DISTINCT location
    FROM dim_jobs
    WHERE searched_role = %s
    ORDER BY location""", (selected_role,))

    locations = ["All Locations"] + [row[0] for row in cursor.fetchall()]

    selected_location = st.selectbox(
    "Select Location",
    locations
)
    


    # -----------------------------
    # Search Box
    # -----------------------------
    search_text = st.text_input(
        "🔍 Search Job Title",
        placeholder="Enter job title..."
    )

    # -----------------------------
    # Jobs Query
    # -----------------------------
    query = """
    SELECT
    job_title,
    company,
    location,
    posted_date,
    redirect_url
    FROM dim_jobs
    WHERE searched_role = %s"""

    params = [selected_role]

    # Company Filter
    if selected_company != "All Companies":
        query += " AND company = %s"
        params.append(selected_company)

    # Location Filter
    if selected_location != "All Locations":
        query += " AND location = %s"
        params.append(selected_location)

# Job Title Search
    query += " AND LOWER(job_title) LIKE LOWER(%s)"
    params.append(f"%{search_text}%")

# Sort by latest jobs
    query += " ORDER BY posted_date DESC"

    cursor.execute(query, tuple(params))

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

# -----------------------------
# Display Jobs
# -----------------------------
    jobs_df = pd.DataFrame(
    jobs,
    columns=[
        "Job Title",
        "Company",
        "Location",
        "Posted Date",
        "Apply Link"
    ]
)
    # -----------------------------
# Summary
# -----------------------------
    st.markdown("### 📊 Search Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Jobs Found", len(jobs_df))

    with col2:
        st.metric("Companies", jobs_df["Company"].nunique())

    with col3:
        st.metric("Locations", jobs_df["Location"].nunique())

    st.markdown("---")
    st.dataframe(
    jobs_df,
    use_container_width=True,
    height=500,
    hide_index=True
)
    csv = jobs_df.to_csv(index=False).encode("utf-8")

    st.download_button(
    label="📥 Download Search Results",
    data=csv,
    file_name="careerpulse_jobs.csv",
    mime="text/csv"
) 
   



# =================================================
# CAREER PAGE
# =================================================

elif page == "🎯 Career Guidance":

    st.title("🎯 Career Guidance")

    st.info("Coming Soon...")

# =================================================
# COMPANY PAGE
# =================================================

elif page == "🏢 Companies":

    st.title("🏢 Companies")

    st.info("Coming Soon...")

# =================================================
# MARKET PAGE
# =================================================

elif page == "📊 Market Insights":

    st.title("📊 Market Insights")

    st.info("Coming Soon...")

