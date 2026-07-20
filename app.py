
import streamlit as st
import pandas as pd
from db import get_connection
import plotly.express as px

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

    cursor.execute("""SELECT
    job_title,
    company,
    location,
    posted_date,
    redirect_url
    FROM dim_jobs
    ORDER BY posted_date DESC
    LIMIT 10;
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

    
    roles = ["All Roles"] + [row[0] for row in cursor.fetchall()]
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
    #roles = ["All Roles"] + [row[0] for row in cursor.fetchall()]
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
    
    query += " AND job_title ILIKE %s"
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
    if jobs_df.empty:
        st.warning("No matching jobs found.")
    else:
        st.dataframe(
        jobs_df,
        use_container_width=True,
        height=500,
        hide_index=True
    )

    csv = jobs_df.to_csv(index=False).encode("utf-8")

    
    # -----------------------------
# Summary
# -----------------------------
    st.markdown("### 📊 Search Summary")
    st.success(f"Found {len(jobs_df)} matching jobs.")

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

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # Select Career
    # =====================================

    cursor.execute("""
        SELECT DISTINCT searched_role
        FROM dim_jobs
        ORDER BY searched_role
    """)

    roles = [row[0] for row in cursor.fetchall()]

    selected_role = st.selectbox(
        "Select Your Career",
        roles
    )

    st.markdown("---")

    # =====================================
    # Total Jobs
    # =====================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM dim_jobs
        WHERE searched_role=%s
    """, (selected_role,))

    total_jobs = cursor.fetchone()[0]

    # =====================================
    # Total Companies
    # =====================================

    cursor.execute("""
        SELECT COUNT(DISTINCT company)
        FROM dim_jobs
        WHERE searched_role=%s
    """, (selected_role,))

    total_companies = cursor.fetchone()[0]

    # =====================================
    # Total Locations
    # =====================================

    cursor.execute("""
        SELECT COUNT(DISTINCT location)
        FROM dim_jobs
        WHERE searched_role=%s
    """, (selected_role,))

    total_locations = cursor.fetchone()[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("💼 Jobs", total_jobs)
    col2.metric("🏢 Companies", total_companies)
    col3.metric("📍 Locations", total_locations)

    st.markdown("---")

    # =====================================
    # Top Hiring Companies
    # =====================================

    st.subheader("🏆 Top Hiring Companies")

    cursor.execute("""
        SELECT
            company,
            COUNT(*)
        FROM dim_jobs
        WHERE searched_role=%s
        GROUP BY company
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """, (selected_role,))

    companies = cursor.fetchall()

    companies_df = pd.DataFrame(
        companies,
        columns=[
            "Company",
            "Jobs"
        ]
    )

    st.bar_chart(
        companies_df.set_index("Company")
    )

    st.markdown("---")

    # =====================================
    # Top Skills
    # =====================================

    st.subheader("🔥 Most Demanded Skills")

    cursor.execute("""
        SELECT
            s.skill,
            COUNT(*) AS demand
        FROM fact_job_skills f
        JOIN dim_jobs j
        ON f.job_id=j.job_id
        JOIN dim_skills s
        ON f.skill_id=s.skill_id
        WHERE j.searched_role=%s
        GROUP BY s.skill
        ORDER BY demand DESC
        LIMIT 10
    """, (selected_role,))

    skills = cursor.fetchall()

    skills_df = pd.DataFrame(
        skills,
        columns=[
            "Skill",
            "Demand"
        ]
    )

    st.dataframe(
        skills_df,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        skills_df.set_index("Skill")
    )

    st.markdown("---")

    # =====================================
    # Top Hiring Cities
    # =====================================

    st.subheader("🌍 Top Hiring Locations")

    cursor.execute("""
        SELECT
            location,
            COUNT(*)
        FROM dim_jobs
        WHERE searched_role=%s
        GROUP BY location
        ORDER BY COUNT(*) DESC
    """, (selected_role,))

    cities = cursor.fetchall()

    city_df = pd.DataFrame(
        cities,
        columns=[
            "Location",
            "Jobs"
        ]
    )

    st.dataframe(
        city_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # =====================================
    # Learning Roadmap
    # =====================================

    st.subheader("📚 Suggested Learning Roadmap")

    # ==========================================
    # Suggested Learning Roadmap
    # ==========================================

    st.markdown("---")
    st.subheader("🛣 Suggested Learning Roadmap")

    roadmaps = {

        "Data Engineer": [
            "🐍 Learn Python for Data Engineering",
            "🗄 Master SQL & PostgreSQL",
            "⚙ Build ETL Pipelines",
            "📦 Learn Apache Airflow",
            "☁ Learn AWS / Azure / GCP",
            "🔥 Learn Apache Spark",
            "🏗 Data Warehouse & Star Schema",
            "📊 Build End-to-End Data Engineering Projects"
        ],

        "Data Scientist": [
            "🐍 Python Programming",
            "📊 Statistics & Probability",
            "🧹 Data Cleaning with Pandas",
            "📈 Data Visualization",
            "🤖 Machine Learning",
            "🧠 Deep Learning",
            "🚀 Model Deployment",
            "📂 Build Real-world ML Projects"
        ],

        "Machine Learning Engineer": [
            "🐍 Python",
            "📊 SQL",
            "🤖 Machine Learning",
            "🧠 TensorFlow / PyTorch",
            "⚙ MLOps",
            "🐳 Docker",
            "☁ Cloud Deployment",
            "🚀 Production ML Pipelines"
        ],

        "AI Engineer": [
            "🐍 Python",
            "📊 Mathematics",
            "🤖 Machine Learning",
            "🧠 Deep Learning",
            "💬 NLP",
            "👁 Computer Vision",
            "🤖 Generative AI",
            "🚀 LLM Applications"
        ],

        "Data Analyst": [
            "📊 Excel",
            "🗄 SQL",
            "🐍 Python",
            "📈 Power BI",
            "📉 Tableau",
            "📋 Business Analytics",
            "📊 Dashboard Building",
            "💼 Case Studies"
        ],

        "Cloud Engineer": [
            "🐧 Linux",
            "🌐 Networking",
            "☁ AWS",
            "🐳 Docker",
            "☸ Kubernetes",
            "⚙ Terraform",
            "🔒 Cloud Security",
            "🚀 CI/CD"
        ],

        "Analytics Engineer": [
            "SQL",
            "dbt",
            "Data Warehousing",
            "Python",
            "Power BI",
            "Snowflake",
            "Airflow",
            "Business Intelligence"
        ],

        "Business Intelligence Developer": [
            "SQL",
            "Power BI",
            "Tableau",
            "Data Warehousing",
            "DAX",
            "ETL",
            "Dashboard Design",
            "Business Reporting"
        ],

        "Big Data Engineer": [
            "Python",
            "SQL",
            "Hadoop",
            "Spark",
            "Kafka",
            "Hive",
            "Airflow",
            "Cloud Big Data"
        ],

        "Data Architect": [
            "SQL",
            "Database Design",
            "Data Modeling",
            "Data Warehouse",
            "Snowflake",
            "Cloud Architecture",
            "Governance",
            "Enterprise Data Systems"
        ]

    }

    steps = roadmaps.get(selected_role, [])

    if steps:

        for i, step in enumerate(steps, start=1):
            st.success(f"Step {i}: {step}")
            st.markdown("---")

    st.subheader("🎯 Career Progress")

    progress = st.progress(0)

    for i in range(8):
        progress.progress((i + 1) / 8)

    st.info("Complete each step above to become interview-ready for this role.")

    salary = {
        "Data Engineer": "₹6 - ₹18 LPA",
        "Data Scientist": "₹7 - ₹20 LPA",
        "Machine Learning Engineer": "₹8 - ₹22 LPA",
        "AI Engineer": "₹10 - ₹25 LPA",
        "Data Analyst": "₹4 - ₹10 LPA",
        "Cloud Engineer": "₹6 - ₹18 LPA",
        "Analytics Engineer": "₹8 - ₹20 LPA",
        "Business Intelligence Developer": "₹5 - ₹14 LPA",
        "Big Data Engineer": "₹8 - ₹22 LPA",
        "Data Architect": "₹15 - ₹35 LPA"
    }

    st.metric(
        "💰 Average Salary",
        salary.get(selected_role, "Not Available")
    )
# =================================================
# COMPANY PAGE
# =================================================

elif page == "🏢 Companies":

    st.title("🏢 Company Analytics")

    conn = get_connection()
    cursor = conn.cursor()

    # ======================================
    # KPI Cards
    # ======================================

    cursor.execute("SELECT COUNT(DISTINCT company) FROM dim_jobs")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM dim_jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT location) FROM dim_jobs")
    total_locations = cursor.fetchone()[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("🏢 Companies", total_companies)
    col2.metric("💼 Jobs", total_jobs)
    col3.metric("🌍 Locations", total_locations)

    st.markdown("---")

    # ======================================
    # Top Hiring Companies
    # ======================================

    st.subheader("🏆 Top Hiring Companies")

    cursor.execute("""
        SELECT
            company,
            COUNT(*) AS jobs
        FROM dim_jobs
        GROUP BY company
        ORDER BY jobs DESC
        LIMIT 10
    """)

    top_companies = cursor.fetchall()

    top_df = pd.DataFrame(
        top_companies,
        columns=[
            "Company",
            "Jobs"
        ]
    )

    st.bar_chart(
        top_df.set_index("Company")
    )

    st.markdown("---")

    # ======================================
    # Company Selection
    # ======================================

    cursor.execute("""
        SELECT DISTINCT company
        FROM dim_jobs
        ORDER BY company
    """)

    companies = [row[0] for row in cursor.fetchall()]

    selected_company = st.selectbox(
        "Select Company",
        companies
    )

    st.markdown("---")

    # ======================================
    # Company Summary
    # ======================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM dim_jobs
        WHERE company=%s
    """, (selected_company,))

    openings = cursor.fetchone()[0]

    st.metric(
        "Total Openings",
        openings
    )

    # ======================================
    # Roles Offered
    # ======================================

    st.subheader("💼 Roles Hiring")

    cursor.execute("""
        SELECT
            searched_role,
            COUNT(*)
        FROM dim_jobs
        WHERE company=%s
        GROUP BY searched_role
        ORDER BY COUNT(*) DESC
    """, (selected_company,))

    role_data = cursor.fetchall()

    roles_df = pd.DataFrame(
        role_data,
        columns=[
            "Role",
            "Jobs"
        ]
    )

    st.dataframe(
        roles_df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # Hiring Locations
    # ======================================

    st.subheader("📍 Hiring Locations")

    cursor.execute("""
        SELECT
            location,
            COUNT(*)
        FROM dim_jobs
        WHERE company=%s
        GROUP BY location
        ORDER BY COUNT(*) DESC
    """, (selected_company,))

    location_data = cursor.fetchall()

    location_df = pd.DataFrame(
        location_data,
        columns=[
            "Location",
            "Jobs"
        ]
    )

    st.dataframe(
        location_df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # Latest Jobs
    # ======================================

    st.subheader("🆕 Latest Openings")

    cursor.execute("""
        SELECT
            job_title,
            location,
            posted_date,
            redirect_url
        FROM dim_jobs
        WHERE company=%s
        ORDER BY posted_date DESC
        LIMIT 10
    """, (selected_company,))

    latest_jobs = cursor.fetchall()

    if len(latest_jobs) == 0:

        st.warning("No jobs found.")

    else:

        for job in latest_jobs:

            st.subheader(job[0])

            st.write(f"📍 {job[1]}")

            st.write(f"📅 Posted: {job[2]}")

            st.link_button(
                "Apply Now",
                job[3]
            )

            st.markdown("---")

    cursor.close()
    conn.close()
    

# =================================================
# MARKET PAGE
# =================================================

# =================================================
# MARKET INSIGHTS
# =================================================
# =================================================
# MARKET INSIGHTS
# =================================================

elif page == "📊 Market Insights":

    st.markdown("""
    <h1 style='text-align:center;color:#2563EB;'>
    📊 CareerPulse Data Engineering Dashboard
    </h1>

    <h4 style='text-align:center;color:gray;'>
    End-to-End Job Market Intelligence Platform
    </h4>
    """, unsafe_allow_html=True)

    st.markdown("---")

    conn = get_connection()
    cursor = conn.cursor()

    # ===========================================
    # PIPELINE STATUS
    # ===========================================

    st.subheader("🚀 Pipeline Status")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.success("API\n\n✅ Connected")

    with c2:
        st.success("Validation\n\n✅ Passed")

    with c3:
        st.success("Transformation\n\n✅ Completed")

    with c4:
        st.success("Warehouse\n\n✅ Loaded")

    with c5:
        st.success("Dashboard\n\n✅ Live")

    st.markdown("---")

    # ===========================================
    # DASHBOARD FILTERS
    # ===========================================

    st.subheader("🎯 Dashboard Filters")

    f1, f2 = st.columns(2)

    with f1:

        cursor.execute("""
        SELECT DISTINCT searched_role
        FROM dim_jobs
        ORDER BY searched_role
        """)

        roles = ["All Roles"] + [x[0] for x in cursor.fetchall()]

        selected_role = st.selectbox(
            "Job Role",
            roles
        )

    with f2:

        cursor.execute("""
        SELECT DISTINCT location
        FROM dim_jobs
        ORDER BY location
        """)

        locations = ["All Locations"] + [x[0] for x in cursor.fetchall()]

        selected_location = st.selectbox(
            "Location",
            locations
        )

    where_clause = " WHERE 1=1 "
    params = []

    if selected_role != "All Roles":
        where_clause += " AND searched_role=%s"
        params.append(selected_role)

    if selected_location != "All Locations":
        where_clause += " AND location=%s"
        params.append(selected_location)

    st.markdown("---")

    # ===========================================
    # WAREHOUSE KPIs
    # ===========================================

    cursor.execute("SELECT COUNT(*) FROM dim_jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT company) FROM dim_jobs")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT location) FROM dim_jobs")
    total_locations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM dim_skills")
    total_skills = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fact_job_skills")
    fact_records = cursor.fetchone()[0]

    warehouse_tables = 3

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric("💼 Total Jobs", total_jobs)

    with k2:
        st.metric("🏢 Companies", total_companies)

    with k3:
        st.metric("📍 Locations", total_locations)

    k4, k5, k6 = st.columns(3)

    with k4:
        st.metric("🛠 Skills", total_skills)

    with k5:
        st.metric("📦 Fact Records", fact_records)

    with k6:
        st.metric("🗄 Warehouse Tables", warehouse_tables)

    st.markdown("---")

    # ===========================================
    # DATA QUALITY DASHBOARD
    # ===========================================

    st.subheader("📋 Data Quality Dashboard")

    cursor.execute("""
    SELECT COUNT(*)
    FROM dim_jobs
    WHERE company IS NULL
    """)

    missing_company = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM dim_jobs
    WHERE location IS NULL
    """)

    missing_location = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM dim_jobs
    WHERE job_title IS NULL
    """)

    missing_title = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM
    (
        SELECT job_id
        FROM dim_jobs
        GROUP BY job_id
        HAVING COUNT(*)>1
    ) x
    """)

    duplicate_jobs = cursor.fetchone()[0]

    quality_score = round(
        (
            1 -
            (
                missing_company +
                missing_location +
                missing_title +
                duplicate_jobs
            ) /
            max(total_jobs,1)
        ) * 100,
        2
    )

    q1, q2, q3, q4, q5 = st.columns(5)

    q1.metric("Duplicate Jobs", duplicate_jobs)

    q2.metric("Missing Company", missing_company)

    q3.metric("Missing Location", missing_location)

    q4.metric("Missing Titles", missing_title)

    q5.metric("Warehouse Health", f"{quality_score}%")

    st.markdown("---")
    # ===========================================
    # TOP HIRING COMPANIES
    # ===========================================

    cursor.execute(f"""
    SELECT
        company,
        COUNT(*) AS jobs
    FROM dim_jobs
    {where_clause}
    GROUP BY company
    ORDER BY jobs DESC
    LIMIT 10
    """, tuple(params))

    company_df = pd.DataFrame(
        cursor.fetchall(),
        columns=["Company", "Jobs"]
    )

    # ===========================================
    # TOP SKILLS
    # ===========================================

    skill_query = """
    SELECT
        s.skill,
        COUNT(*) AS demand
    FROM fact_job_skills f
    JOIN dim_jobs j
        ON f.job_id = j.job_id
    JOIN dim_skills s
        ON f.skill_id = s.skill_id
    """

    skill_params = []

    if selected_role != "All Roles":
        skill_query += " WHERE j.searched_role = %s"
        skill_params.append(selected_role)

    if selected_location != "All Locations":
        if "WHERE" in skill_query:
            skill_query += " AND j.location = %s"
        else:
            skill_query += " WHERE j.location = %s"
        skill_params.append(selected_location)

    skill_query += """
    GROUP BY s.skill
    ORDER BY demand DESC
    LIMIT 10
    """

    cursor.execute(skill_query, tuple(skill_params))

    skill_df = pd.DataFrame(
        cursor.fetchall(),
        columns=["Skill", "Demand"]
    )

    # ===========================================
    # ROLE DISTRIBUTION
    # ===========================================

    cursor.execute(f"""
    SELECT
        searched_role,
        COUNT(*) AS jobs
    FROM dim_jobs
    {where_clause}
    GROUP BY searched_role
    ORDER BY jobs DESC
    """, tuple(params))

    role_df = pd.DataFrame(
        cursor.fetchall(),
        columns=["Role", "Jobs"]
    )

    # ===========================================
    # TOP LOCATIONS
    # ===========================================

    cursor.execute(f"""
    SELECT
        location,
        COUNT(*) AS jobs
    FROM dim_jobs
    {where_clause}
    GROUP BY location
    ORDER BY jobs DESC
    LIMIT 10
    """, tuple(params))

    location_df = pd.DataFrame(
        cursor.fetchall(),
        columns=["Location", "Jobs"]
    )

    # ===========================================
    # HIRING TREND
    # ===========================================

    trend_query = """
    SELECT
        DATE(posted_date),
        COUNT(*)
    FROM dim_jobs
    """

    trend_params = []

    if selected_role != "All Roles":
        trend_query += " WHERE searched_role=%s"
        trend_params.append(selected_role)

        if selected_location != "All Locations":
            trend_query += " AND location=%s"
            trend_params.append(selected_location)

    elif selected_location != "All Locations":
        trend_query += " WHERE location=%s"
        trend_params.append(selected_location)

    trend_query += """
    GROUP BY DATE(posted_date)
    ORDER BY DATE(posted_date)
    """

    cursor.execute(trend_query, tuple(trend_params))

    trend_df = pd.DataFrame(
        cursor.fetchall(),
        columns=["Date", "Jobs"]
    )

    st.subheader("📈 Business Intelligence Dashboard")

    # ===========================================
    # CHART 1
    # ===========================================

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            company_df,
            x="Jobs",
            y="Company",
            orientation="h",
            title="🏆 Top Hiring Companies",
            template="plotly_white",
            text="Jobs"
        )

        fig.update_layout(
            height=450,
            title_x=0.15
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            skill_df,
            x="Demand",
            y="Skill",
            orientation="h",
            title="🔥 Most Demanded Skills",
            template="plotly_white",
            text="Demand"
        )

        fig.update_layout(
            height=450,
            title_x=0.15
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ===========================================
    # CHART 2
    # ===========================================

    left, right = st.columns(2)

    with left:

        fig = px.pie(
            role_df,
            names="Role",
            values="Jobs",
            hole=0.45,
            title="👨‍💻 Role Distribution",
            template="plotly_white"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            location_df,
            x="Jobs",
            y="Location",
            orientation="h",
            title="🌍 Top Hiring Locations",
            template="plotly_white",
            text="Jobs"
        )

        fig.update_layout(
            height=450,
            title_x=0.15
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ===========================================
    # HIRING TREND
    # ===========================================

    fig = px.line(
        trend_df,
        x="Date",
        y="Jobs",
        markers=True,
        title="📈 Hiring Trend",
        template="plotly_white"
    )

    fig.update_layout(
        height=500,
        title_x=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")
    # ===========================================
    # WAREHOUSE INSIGHTS
    # ===========================================

    st.subheader("📦 Warehouse Insights")

    cursor.execute(f"""
    SELECT company, COUNT(*) AS jobs
    FROM dim_jobs
    {where_clause}
    GROUP BY company
    ORDER BY jobs DESC
    LIMIT 1
    """, tuple(params))

    top_company = cursor.fetchone()

    cursor.execute("""
    SELECT
    s.skill,
    COUNT(*) AS demand
FROM fact_job_skills f
JOIN dim_skills s
    ON f.skill_id = s.skill_id
GROUP BY s.skill
ORDER BY demand DESC
LIMIT 1;
    """)

    top_skill = cursor.fetchone()

    cursor.execute(f"""
    SELECT location, COUNT(*) AS jobs
    FROM dim_jobs
    {where_clause}
    GROUP BY location
    ORDER BY jobs DESC
    LIMIT 1
    """, tuple(params))

    top_city = cursor.fetchone()

    cursor.execute(f"""
    SELECT searched_role, COUNT(*) AS jobs
    FROM dim_jobs
    {where_clause}
    GROUP BY searched_role
    ORDER BY jobs DESC
    LIMIT 1
    """, tuple(params))

    top_role = cursor.fetchone()

    a, b, c, d = st.columns(4)

    with a:
        st.info(f"""
### 🏢 Top Company

**{top_company[0] if top_company else 'N/A'}**
""")

    with b:
        st.info(f"""
### 🔥 Top Skill

**{top_skill[0] if top_skill else 'N/A'}**
""")

    with c:
        st.info(f"""
### 🌍 Top City

**{top_city[0] if top_city else 'N/A'}**
""")

    with d:
        st.info(f"""
### 💼 Top Role

**{top_role[0] if top_role else 'N/A'}**
""")

    st.markdown("---")

    # ===========================================
    # RECENT JOBS
    # ===========================================

    st.subheader("📋 Latest Jobs in Warehouse")

    cursor.execute(f"""
    SELECT
        job_title,
        company,
        location,
        posted_date
    FROM dim_jobs
    {where_clause}
    ORDER BY posted_date DESC
    LIMIT 10
    """, tuple(params))

    latest_jobs = cursor.fetchall()

    latest_df = pd.DataFrame(
        latest_jobs,
        columns=[
            "Job Title",
            "Company",
            "Location",
            "Posted Date"
        ]
    )

    st.dataframe(
        latest_df,
        use_container_width=True,
        hide_index=True,
        height=350
    )

    # ===========================================
    # DOWNLOAD REPORT
    # ===========================================

    csv = latest_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Latest Jobs",
        data=csv,
        file_name="market_insights_jobs.csv",
        mime="text/csv",
        key="market_download"
    )

    st.markdown("---")

    # ===========================================
    # PIPELINE SUMMARY
    # ===========================================

    st.subheader("🚀 Pipeline Execution Summary")

    p1, p2, p3 = st.columns(3)

    with p1:

        st.success(f"""
### API Layer

✔ Jobs Ingested

**{total_jobs}**
""")

    with p2:

        st.success(f"""
### Warehouse

✔ Fact Records

**{fact_records}**
""")

    with p3:

        st.success(f"""
### Data Quality

✔ Health Score

**{quality_score}%**
""")

    st.markdown("---")

    # ===========================================
    # DATA ENGINEERING ARCHITECTURE
    # ===========================================

    st.subheader("🏗 Data Engineering Pipeline")

    st.code("""
Adzuna API
     │
     ▼
Raw API Data
     │
     ▼
Validation & Cleaning
     │
     ▼
Skill Extraction
     │
     ▼
PostgreSQL Data Warehouse
     │
     ├──────────────┐
     ▼              ▼
Star Schema      Analytics
     │
     ▼
CareerPulse Dashboard
""")

    st.markdown("---")

    # ===========================================
    # FOOTER
    # ===========================================

    st.caption(
        "CareerPulse • End-to-End Data Engineering Project • "
        "Python • PostgreSQL • SQL • Streamlit • Plotly"
    )

    cursor.close()
    conn.close()