import streamlit as st
import matplotlib.pyplot as plt
# ================= Page Config =================
st.set_page_config(
    page_title="Smart Civic Complaint System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)
import time
import os,re
import pandas as pd
from datetime import datetime

from src.complaint_classifier.classifier import predict_category
from src.routing.department_router import get_department
from src.recommender.recommendation_engine import get_recommendation
from src.image_classifier.predictor import predict_image
from src.validation.evidence_checker import check_evidence
from src.utils.pdf_export import generate_pdf
from src.utils.priority_engine import calculate_priority
from src.utils.duplicate_checker import find_similar_complaints
from src.utils.auth import authenticate_user
from src.database.db_manager import (
    create_database,
    insert_complaint,
    get_all_complaints,
    get_active_complaints,
    increase_report_count,
    log_activity,
    get_activity_log,
    update_status_with_log,
    get_complaint_by_id_and_phone,
    submit_feedback,
    get_feedback,
    reopen_complaint,
    escalate_complaint,
    get_all_users,
    update_after_image,
    get_before_after_images,
    get_all_feedback,
    get_average_rating,
    get_officer_performance,
    get_location_statistics
)
# ================= Session State =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "department" not in st.session_state:
    st.session_state.department = ""

if "tracked_complaint" not in st.session_state:
    st.session_state.tracked_complaint = None

if "tracked_complaint_id" not in st.session_state:
    st.session_state.tracked_complaint_id = None

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = {}

if "pending_complaint" not in st.session_state:
    st.session_state.pending_complaint = {}
    
if "open_complaint" not in st.session_state:
    st.session_state.open_complaint = -1

create_database()

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

:root{
    --bg:#09111f;
    --card:#172033;
    --primary:#3b82f6;
    --secondary:#8b5cf6;
    --text:#f8fafc;
}

/* ================= GLOBAL ================= */

html, body, [data-testid="stAppViewContainer"]{
    background:linear-gradient(180deg,#081120,#0a1324)!important;
    color:white!important;
    font-family:'Inter',sans-serif;
}

[data-testid="stHeader"],
#MainMenu,
footer,
header{
    visibility:hidden;
}

.block-container{
    padding-top:1rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#131a2b,#0b1120)!important;
    border-right:1px solid rgba(255,255,255,.05);
}

section[data-testid="stSidebar"] *{
    color:white!important;
}

div[role="radiogroup"] label{
    width:100%!important;
    height:48px;
    display:flex;
    align-items:center;
    border-radius:16px;
    margin-bottom:10px;
    padding-left:15px;
    background:#182235;
    border:1px solid rgba(255,255,255,.05);
    transition:.3s;
}

div[role="radiogroup"] label:hover{
    background:#26324f;
}

/* ================= HERO ================= */

.hero{
    background:linear-gradient(135deg,#2563eb,#3b82f6,#8b5cf6);
    padding:35px 45px;
    border-radius:28px;
    margin-bottom:25px;
    box-shadow:0 15px 40px rgba(0,0,0,.3);
}

.hero h1{
    color:white!important;
    font-size:2.5rem!important;
    font-family:'Space Grotesk',sans-serif!important;
}

.hero p{
    color:#dbeafe!important;
}

/* ================= BUTTONS ================= */

.stButton>button,
.stDownloadButton>button{
    width:100%;
    height:54px!important;
    border:none!important;
    border-radius:18px!important;

    background:linear-gradient(
        135deg,
        #3b82f6,
        #8b5cf6
    )!important;

    color:white!important;
    font-weight:600!important;
    font-size:16px!important;

    box-shadow:0 10px 25px rgba(59,130,246,.35);
}

.stButton button *,
.stDownloadButton button *{
    color:white!important;
}

.stDownloadButton svg{
    fill:white!important;
}

/* ================= LABELS ================= */

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *{
    color:white!important;
    font-weight:600!important;
}

label{
    color:white!important;
}

/* ================= INPUTS ================= */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input{
    background:#1a2335!important;
    color:white!important;
    caret-color:white !important;
    border:1px solid rgba(255,255,255,.15)!important;
    border-radius:18px!important;
}

input::placeholder,
textarea::placeholder{
    color:#cbd5e1!important;
}

/* ================= SELECTBOX ================= */

div[data-baseweb="select"]{
    background:#1a2335 !important;
    border-radius:16px !important;
    border:1px solid rgba(255,255,255,.1) !important;
}

/* Selected value inside box */
div[data-baseweb="select"] span{
    color:black !important;
    font-weight:500;
}

/* Dropdown menu */
div[role="listbox"]{
    background:#1a2335 !important;
}

/* Dropdown options */
div[role="option"]{
    background:#1a2335 !important;
}

/* Text inside dropdown options */
div[role="option"] span{
    color:white !important;
}

/* Hover effect */
div[role="option"]:hover{
    background:#26324f !important;
}
/* ================= FILE UPLOADER ================= */

[data-testid="stFileUploader"]{
    background:#172033!important;
    padding:20px!important;
    border-radius:22px!important;
    border:1px dashed rgba(255,255,255,.1)!important;
}

[data-testid="stFileUploaderDropzone"]{
    background:#1a2335!important;
    border-radius:18px!important;
    border:1px dashed rgba(255,255,255,.15)!important;
}

[data-testid="stFileUploader"] *,
[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploaderDropzoneInstructions"] *{
    color:white!important;
}

[data-testid="stFileUploader"] button{
    background:#3b82f6!important;
    color:white!important;
}

[data-testid="stFileUploader"] svg{
    fill:white!important;
}

/* ================= METRICS ================= */

div[data-testid="stMetric"]{
    background:linear-gradient(145deg,#1c2436,#131a2b);
    border-radius:22px;
    padding:18px;
    border:1px solid rgba(255,255,255,.05);
}

div[data-testid="stMetric"] *{
    color:white!important;
}

/* ================= EXPANDERS ================= */

details{
    background:#131a2b!important;
    border-radius:18px!important;
    border:1px solid rgba(255,255,255,.06)!important;
    overflow:hidden;
}

details summary{
    background: #172033 !important;
    color: white !important;
    font-weight: 600;
    padding: 14px 18px !important;
}
details summary * {
    color: white !important;
}

details[open] summary {
    background: #1f2b45 !important;
}

/* ================= TABLES ================= */

[data-testid="stDataFrame"]{
    border-radius:20px!important;
}

[data-testid="stDataFrame"] *{
    color:white!important;
}

/* ================= ALERTS ================= */

div[data-testid="stAlert"]{
    border-radius:18px!important;
}

div[data-testid="stAlert"] *{
    color:white!important;
}

/* ================= TIMELINE ================= */

.timeline-card{
    background:#1c2436;
    border:1px solid rgba(255,255,255,.05);
    padding:15px;
    border-radius:18px;
    margin-bottom:12px;
}

/* ================= SCROLLBAR ================= */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#3b82f6;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)
# ================= Hero =================
st.markdown("""
<div class="hero">
<h1>🏛 Smart Civic Complaint System</h1>

<p>
AI-powered complaint classification, routing,
evidence verification, officer monitoring,
and analytics dashboard.
</p>

</div>
""", unsafe_allow_html=True)


# ================= Sidebar =================
st.sidebar.markdown("# 🏛 Smart Civic")

st.sidebar.caption(
"AI-powered civic issue management system"
)

st.sidebar.metric(
    "📊 Total Complaints",
    len(get_all_complaints())
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Submit Complaint",
        "🔍 Track Complaint",
        "🔐 Login",
        "🏛 Department Panel",
        "📋 Complaint History",
        "📊 Analytics",
        "👑 Admin Panel"
    ],
    label_visibility="collapsed"
)


# ══════════════════════════════════════════════════════════════════════
# PAGE 1 — SUBMIT COMPLAINT
# ══════════════════════════════════════════════════════════════════════

if page == "🏠 Submit Complaint":

    st.header("📨 Submit a Civic Complaint")
    st.caption("Report civic issues and let AI classify and route them automatically.")
    complaints = get_all_complaints()
    with st.container(border=True):
        st.subheader("👤 Citizen Information")
        col1, col2 = st.columns(2)
        with col1:
            citizen_name = st.text_input("👤 Citizen Name")
            phone_number = st.text_input("📞 Phone Number")
        with col2:
            address = st.text_area("📍 Complaint Location",height=100)
    with st.container(border=True):
        st.markdown("📝 Complaint Details")
        complaint = st.text_area("Describe Your Complaint",height=150)

    st.write("")

    if st.button(
        "🔍 Analyze Complaint",
        use_container_width=True
    ):

        if not citizen_name:
            st.warning("Enter citizen name")
            st.stop()

        if not phone_number:
            st.warning("Enter phone number")
            st.stop()

        if not address:
            st.warning("Enter location")
            st.stop()

        if not complaint.strip():
            st.warning("Please enter a complaint.")
            st.stop()

        category = predict_category(complaint)
        department = get_department(category)
        recommendation = get_recommendation(category)
        severity, priority_score = calculate_priority(complaint)
        st.session_state.analysis_done = True
        st.session_state.analysis_result = {
            "category": category,
            "department": department,
            "recommendation": recommendation,
            "severity": severity,
            "priority": priority_score
        }
        st.session_state.pending_complaint = {
            "name": citizen_name,
            "phone": phone_number,
            "address": address,
            "complaint": complaint
        }
        st.rerun()
    # ==========================================
    # Show AI Analysis Result
    # ==========================================
    if st.session_state.get("analysis_done", False):
        result = st.session_state.analysis_result
        st.markdown("---")
        st.subheader("🤖 AI Analysis Result")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("📂 Category", result["category"])
            st.info(f"🏢 {result['department']}")
        with c2:
            st.metric("🎯 Priority Score",f"{result['priority']}/100")
            if result["severity"] == "High":
                st.error("🔴 High Severity")
            elif result["severity"] == "Medium":
                st.warning("🟡 Medium Severity")
            else:
                st.success("🟢 Low Severity")
        with c3:
            st.markdown("### 🤖 AI Recommendation")
            st.success(result["recommendation"])
        if result["category"] in ["Roads", "Sanitation"]:
            st.markdown("---")
            uploaded_file = st.file_uploader(
                "📷 Upload Complaint Image",
                type=["jpg", "jpeg", "png"],
                help="Required for Road and Sanitation complaints.",
                key="road_image"
            )

        else:
            uploaded_file = None
            st.info("📷 Image is not required for this complaint category.")
        
        if st.button("✅ Submit Complaint", use_container_width=True):
            # -----------------------------
            # Retrieve stored AI analysis
            # -----------------------------
            result = st.session_state.analysis_result
            data = st.session_state.pending_complaint

            category = result["category"]
            department = result["department"]
            recommendation = result["recommendation"]
            severity = result["severity"]
            priority_score = result["priority"]

            before_image_path = None
            image_category = "Not Provided"
            confidence = 0.0
            if category in ["Roads", "Sanitation"] and uploaded_file is None:
                st.warning("📷 Please upload an image before submitting.")
                st.stop()
            # -----------------------------
            # Save uploaded image (if any)
            # -----------------------------
            if uploaded_file is not None:
                os.makedirs("uploads", exist_ok=True)

                before_image_path = (
                    f"uploads/before_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                )

                with open(before_image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                with st.spinner("🤖 AI is analyzing the uploaded image..."):
                    image_category, confidence = predict_image(before_image_path)
            # -----------------------------
            # Evidence Verification
            # -----------------------------
            if category in ["Roads", "Sanitation"]:
                status = check_evidence(category, image_category)
            else:
                status = "Not Required"

            if category in ["Roads", "Sanitation"]:
                st.markdown("---")
                st.subheader("🤖 AI Image Verification")

                c1, c2 = st.columns(2)
                with c1:
                    st.metric(
                        "Detected Image",
                        image_category
                    )

                with c2:
                    st.metric(
                        "Confidence",
                        f"{confidence:.2f}%"
                    )

                if confidence >= 70:
                    st.success("✅ High confidence prediction")
                else:
                    st.warning("⚠ AI confidence is low.")

                if status == "Verified":
                    st.success("✅ Image matches the complaint.")

                elif status == "Needs Verification":
                    st.warning(
                        "⚠ AI is not fully confident.\n\n"
                        "Officer verification will be required."
                    )

                else:
                    st.error(
                        f"""
                    ❌ Image does not match the complaint.

                    Complaint Category : {category}

                    Please upload a relevant image.
                """
                    )


            # -----------------------------
            # Duplicate Detection
            # -----------------------------
            existing_rows = get_active_complaints()

            existing_texts = [row[4] for row in existing_rows]

            similar_complaint, similarity = find_similar_complaints(
                data["complaint"],
                existing_texts
            )

            duplicate_found = False
            duplicate_id = None

            # Check duplicate by location + category
            for row in existing_rows:

                existing_id = row[0]
                existing_address = str(row[3]).lower()
                existing_category = str(row[5]).lower()

                address_words = set(re.findall(r"\w+", data["address"].lower()))
                existing_words = set(re.findall(r"\w+", existing_address))

                common_words = address_words.intersection(existing_words)

                if (
                    existing_category == category.lower()
                    and len(common_words) >= 3
                ):
                    duplicate_found = True
                    duplicate_id = existing_id
                    break

            # Check duplicate by text similarity
            if similarity >= 70:

                duplicate_found = True

                for row in existing_rows:
                    if row[4] == similar_complaint:
                        duplicate_id = row[0]
                        break

            # Duplicate found
            if duplicate_found:

                increase_report_count(duplicate_id)
                log_activity(
                    duplicate_id,
                    action="Duplicate complaint linked",
                    note="Citizen reported the same issue.",
                    officer="Citizen"
                )
               
                st.success(f"""
                    ✅ Complaint Linked Successfully

                    🆔 Complaint ID: {duplicate_id}

                    📍 Similar issue already exists in this location.

                    👥 Your report has been added to the existing complaint.

                    📈 Report Count Increased

                    🚀 Priority has been updated.
                """)
                st.session_state.analysis_done = False
                st.session_state.analysis_result = {}
                st.session_state.pending_complaint = {}
                st.stop()

            # Possible duplicate
            elif similarity >= 40:

                st.warning(f"""
                    ⚠ Similar complaint detected

                    Similarity : {similarity}%

                    Existing Complaint:

                    {similar_complaint}

                    You can still submit if this is a different issue.
                """)

            # -----------------------------
            # Exact duplicate check
            # -----------------------------
            for row in get_all_complaints():

                if (
                    row[4].strip().lower() == data["complaint"].strip().lower()
                    and row[3].strip().lower() == data["address"].strip().lower()
                ):

                    st.warning("⚠ This complaint has already been submitted.")

                    st.stop()

            # -----------------------------
            # Save Complaint
            # -----------------------------
            insert_complaint(
                citizen_name=data["name"],
                phone_number=data["phone"],
                address=data["address"],
                complaint_text=data["complaint"],
                text_category=category,
                image_category=image_category,
                confidence=float(confidence),
                evidence_status=status,
                department=department,
                recommendation=recommendation,
                priority_score=priority_score,
                severity=severity,
                before_image=before_image_path
            )
        
            # -----------------------------
            # Activity Log
            # -----------------------------
            all_complaints = get_all_complaints()
        
            new_id = all_complaints[0][0]

            log_activity(
                new_id,
                action="Complaint submitted",
                note=data["complaint"],
                officer="Citizen"
            )

            # -----------------------------
            # Success
            # -----------------------------
            st.success(f"""
                ✅ Complaint Submitted Successfully

                Complaint ID : {new_id}

                Category : {category}

                Department : {department}

                Status : Pending
            """)
            st.info(f"""
                Use the following details to track your complaint:

                Complaint ID : {new_id}

                Phone Number : {data["phone"]}
            """)
            st.balloons()
            time.sleep(2)
            # Clear session state
            st.session_state.analysis_done = False
            st.session_state.analysis_result = {}
            st.session_state.pending_complaint = {}

            st.rerun()
# ══════════════════════════════════════════════════════════════════════
# PAGE 2 — Track Complaint
# ══════════════════════════════════════════════════════════════════════

elif page == "🔍 Track Complaint":

    st.title("🔍 Track Complaint Status")
    st.caption("View progress timeline, before-after images and feedback.")

    col1, col2 = st.columns(2)

    with col1:
        complaint_id = st.number_input(
            "🆔 Complaint ID",
            min_value=1,
            step=1
        )

    with col2:
        phone_number = st.text_input(
            "📞 Phone Number"
        ).strip()

    st.write("")

    if st.button(
        "🔍 Track Complaint",
        use_container_width=True
    ):
        if not phone_number:
            st.warning("Please enter your phone number.")
            st.stop()
        if not phone_number.isdigit() or len(phone_number) != 10:
            st.warning("Enter a valid 10-digit phone number.")
            st.stop()
        complaint = get_complaint_by_id_and_phone(
            complaint_id,
            phone_number
        )
        
        if complaint:
            st.session_state.tracked_complaint = complaint
            st.session_state.tracked_complaint_id = complaint_id

        else:
            st.session_state.tracked_complaint = None
            st.session_state.tracked_complaint_id = None

            st.error(
                "❌ Invalid Complaint ID or Phone Number"
            )

    complaint = st.session_state.tracked_complaint
    complaint_id = st.session_state.tracked_complaint_id

    if complaint:

        st.success("✅ Complaint Found")

        with st.container(border=True):

            st.subheader("📋 Complaint Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📂 Category", complaint[5])
                st.metric("👥 Reports", complaint[13])

            with col2:
                st.metric("🏢 Department", complaint[9])
                st.metric("⚡ Severity", complaint[12])

            with col3:

                status = complaint[14]

                if status == "Pending":
                    st.error("🔴 Pending")

                elif status == "In Progress":
                    st.warning("🟡 In Progress")

                elif status == "Resolved":
                    st.success("🟢 Resolved")

                elif status == "Reopened":
                    st.info("🔄 Reopened")

                elif status == "Escalated":
                    st.error("⚠ Escalated")

                st.caption(f"📅 Submitted : {complaint[18]}")
        
        
        before_image, after_image = get_before_after_images(complaint_id)

        st.markdown("---")
        st.subheader("📷 Before & After")
        col1, col2 = st.columns(2)
        with col1:

            st.markdown("#### 📍 Before")

            if before_image and os.path.exists(before_image):
                st.image(before_image, width=300)
            else:
                st.info("No complaint image uploaded.")

        with col2:

            st.markdown("#### ✅ After")

            if after_image and os.path.exists(after_image):
                st.image(after_image, width=300)
            else:
                st.info("Work not completed yet.")

        st.markdown("---")
        st.subheader("📜 Activity Timeline")
        st.caption("Complete history of actions performed on this complaint.")

        logs = get_activity_log(complaint_id)

        if logs:
            for entry in logs:

                if "submitted" in entry["action"].lower():
                    icon = "📌"
                elif "In Progress" in entry["action"]:
                    icon = "🚧"
                elif "Resolved" in entry["action"]:
                    icon = "✅"
                elif "Completion image" in entry["action"]:
                    icon = "📷"
                else:
                    icon = "📝"

                st.markdown(
                    f"""
                    <div class='timeline-card'>
                    {icon} <b>{entry['action']}</b><br>
                    <small style="color:#94a3b8;">{entry['timestamp']}</small>
                    </div>""",unsafe_allow_html=True)

                if entry["note"]:
                    st.caption(entry["note"])

        st.markdown("---")

        # ==========================
        # FEEDBACK SECTION
        # ==========================
        if complaint[14] == "Resolved":

            st.markdown("---")
            with st.container(border=True):
                st.subheader("⭐ Service Feedback")

                existing_feedback = get_feedback(complaint_id)

                if existing_feedback:

                    st.success("Feedback already submitted")

                    st.write(
                        f"⭐ Rating : {existing_feedback[0]}/5"
                    )

                    st.write(
                        f"💬 Comment : {existing_feedback[1]}"
                    )

                else:

                    rating = st.slider(
                        "⭐ Rate the Service",
                        1,
                        5,
                        5,
                        key=f"rating_{complaint_id}"
                    )

                    feedback_text = st.text_area(
                        "💬 Comments",
                        key=f"comment_{complaint_id}"
                    )

                    if st.button(
                        "Submit Feedback",
                        key=f"feedback_btn_{complaint_id}"
                    ):

                        submit_feedback(
                            complaint_id,
                            rating,
                            feedback_text
                        )

                        st.success(
                            "Thank you for your feedback!"
                        )

                        st.rerun()
        # ==========================
        # REOPEN COMPLAINT SECTION
        # ==========================
        if complaint[14] == "Resolved":
            st.markdown("---")
            with st.container(border=True):
                st.subheader("🔄 Reopen Complaint Request")
                reason = st.text_area("📝 Reason for reopening", key=f"reopen_reason_{complaint_id}")
                if st.button("Reopen Complaint", key=f"reopen_btn_{complaint_id}"):
                    if reason.strip():
                        reopen_complaint(complaint_id,reason)
                        st.success("Complaint reopened successfully.")
                        st.rerun()
                    else:
                        st.warning("Please provide a reason.")

# ═════════════════════════════════════════════════════════════════════
# PAGE 3 — COMPLAINT HISTORY
# ═════════════════════════════════════════════════════════════════════
elif page == "📋 Complaint History":
    if not st.session_state.logged_in:
        st.warning("🔒 Login required")
        st.stop()
    if st.session_state.role != "Admin":
        st.error("❌ Only admin can access this page")
        st.stop()
    
    st.header("📋 Complaint History")
    st.caption("Search, filter and export complaint records.")
    
    complaints = get_all_complaints()
    if complaints:
        df = pd.DataFrame(
            complaints,
            columns=[
                "ID", "Citizen Name", "Phone Number", "Address", "Complaint", "Category", "Image Category",
                "Confidence", "Evidence Status", "Department","Recommendation","Priority Score", "Severity",
                "Reports Count", "Status", "Before Image","After Image","Resolved At","Created At"
            ]
        )
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            st.metric("📋 Total",len(df))
        with c2:
            st.metric(
                "🔴 Pending",
                len(df[df["Status"]=="Pending"])
            )
        with c3:
            st.metric(
                "🟡 In Progress",
                len(df[df["Status"]=="In Progress"])
            )
        with c4:
            st.metric(
                "🟢 Resolved",
                len(df[df["Status"]=="Resolved"])
            )
      
        st.subheader("🔍 Search & Filter")

        col1,col2,col3 = st.columns([2.5,1.2,1.2])

        with col1:
            search_text = st.text_input("🔍 Search Complaint")
        with col2:
            selected_category = st.selectbox(
                "Category",
                ["All","Roads","Water","Drainage","Electricity","Sanitation"]
            )
        with col3:
            selected_status = st.selectbox(
                "Status",
                ["All","Pending","In Progress","Resolved","Reopened","Escalated"]
            )
        filtered_df = df.sort_values(by="Created At",ascending=False)
        if search_text:
            filtered_df = filtered_df[
                filtered_df.astype(str)
                .apply(lambda x: x.str.contains(search_text, case=False, na=False))
                .any(axis=1)
            ]
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["Category"] == selected_category]
        if selected_status != "All":
            filtered_df = filtered_df[filtered_df["Status"] == selected_status]
        if filtered_df.empty:
            st.warning("No complaints match the selected filters.")
            st.stop()
        st.caption(f"Showing {len(filtered_df)} of {len(df)} complaints.")
        
        # PDF Report
        st.subheader("📄 Export Reports") 
        os.makedirs("reports", exist_ok=True)
        pdf_path="reports/complaints_report.pdf"
        if st.button("📄 Generate PDF Report", use_container_width=True):
            generate_pdf(filtered_df, pdf_path)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "⬇ Download PDF",
                    pdf_file,
                    file_name="complaints_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        st.markdown("---")
        # Complaint Cards
        for _, row in filtered_df.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([4,2,2])
                # Left side
                with c1:
                    st.markdown(f"### 📌 Complaint #{row['ID']}")
                    st.markdown(f"**📝 Description**  \n{row['Complaint']}")
                    st.caption(f"📍 {row['Address']}")
                    st.caption(f"Submitted : {row['Created At']}")
                # Middle
                with c2:
                    st.write(f"**📂 Category:** {row['Category']}")
                    st.write(f"**🏢 Department:** {row['Department']}")
                    if row["Severity"] == "High":
                        st.error("🔴 High")
                    elif row["Severity"] == "Medium":
                        st.warning("🟡 Medium")
                    else:
                        st.success("🟢 Low")
                # Right
                with c3:
                    st.metric("👥 Citizens Reporting",row["Reports Count"])
                    if row["Status"]=="Pending":
                        st.error("🔴 Pending")
                    elif row["Status"]=="In Progress":
                        st.warning("🟡 In Progress")
                    elif row["Status"]=="Resolved":
                        st.success("🟢 Resolved")
                    elif row["Status"]=="Reopened":
                        st.info("🔄 Reopened")
                    elif row["Status"]=="Escalated":
                        st.error("⚠️ Escalated")
            st.markdown("")  

    else:
        st.info("No complaints found.")

# ══════════════════════════════════════════════════════════════════════
# PAGE 4 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════

elif page == "📊 Analytics":
    if not st.session_state.logged_in:
        st.warning("🔒 Login required")
        st.stop()

    if st.session_state.role != "Admin":
        st.error("❌ Only admin can access this page")
        st.stop()

    st.header("📊 Analytics Dashboard")
    st.caption("Complaint trends and department statistics.")

    complaints = get_all_complaints()

    if not complaints:
        st.info("No complaint data available.")
        st.stop()

    df = pd.DataFrame(
        complaints,
        columns=[
            "ID", "Citizen Name", "Phone Number", "Address", "Complaint", "Category", "Image Category",
            "Confidence", "Evidence Status", "Department","Recommendation", "Priority Score", "Severity", 
            "Reports Count", "Status", "Before Image","After Image","Resolved At", "Created At"
        ]
    )

    total       = len(df)
    roads       = len(df[df["Category"] == "Roads"])
    water       = len(df[df["Category"] == "Water"])
    electricity = len(df[df["Category"] == "Electricity"])
    drainage    = len(df[df["Category"] == "Drainage"])
    sanitation  = len(df[df["Category"] == "Sanitation"])
    pending_count     = len(df[df["Status"] == "Pending"])
    in_progress_count = len(df[df["Status"] == "In Progress"])
    resolved_count    = len(df[df["Status"] == "Resolved"])

    st.subheader("📈 Dashboard Overview")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.metric("📋 Total Complaints", total)
    with c2:
        st.metric("🟡 Pending", pending_count)
    with c3:
        st.metric("🔵 In Progress", in_progress_count)
    with c4:
        st.metric("🟢 Resolved", resolved_count)
    
    st.markdown("---")
    st.subheader("🏢 Department Statistics")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.metric("🛣 Roads", roads)
    with c2:
        st.metric("💧 Water", water)
    with c3:
        st.metric("⚡ Electricity", electricity)
    with c4:
        st.metric("🚰 Drainage", drainage)
    with c5:
        st.metric("🗑 Sanitation", sanitation)
    
    st.markdown("---")
    st.subheader("📊 Visual Analysis")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("📂 Complaint Categories")
        fig, ax = plt.subplots()
        df["Category"].value_counts().plot(
            kind="pie",
            autopct="%1.1f%%",
            ylabel="",
            ax=ax
        )
        ax.set_title("")
        st.pyplot(fig)
    with col2:
        st.subheader("📷 Evidence Status")
        st.bar_chart(df["Evidence Status"].value_counts())

    st.markdown("---")
    st.subheader("📌 Complaint Status Distribution")
    st.bar_chart(df["Status"].value_counts())

    st.markdown("---")
    st.subheader("🎯 Priority Distribution")
    high_priority = len(df[df["Priority Score"] >= 80])
    medium_priority = len(df[(df["Priority Score"] >= 60) &(df["Priority Score"] < 80)])
    low_priority = len(df[df["Priority Score"] < 60])
    c1,c2,c3 = st.columns(3)
    with c1:
        st.metric("🔴 High Priority",high_priority)
    with c2:
        st.metric("🟡 Medium Priority",medium_priority)
    with c3:
        st.metric("🟢 Low Priority",low_priority)
    
    st.markdown("---")
    st.subheader("🔥 Top Reported Complaints")
    top = df.sort_values(by=["Reports Count","Priority Score"],ascending=[False,False])
    st.dataframe(
        top[
            [
                "Complaint",
                "Reports Count"
            ]
        ].head(5),
        use_container_width=True
    )
    st.markdown("---")
    st.subheader("🕒 Recent Complaint Activity")
    recent = (df.sort_values(by="Created At",ascending=False).head(10))
    st.dataframe(
        recent[
            [
                "ID",
                "Category",
                "Severity",
                "Reports Count",
                "Status",
                "Created At"
            ]
        ],
        use_container_width=True
    )
##############################
# LOGIN PAGE
###############################
elif page == "🔐 Login":
    st.header("🔐 Login")
    st.caption("Officer and Admin access")
    left, center, right = st.columns([2,1.2,2])
    with center:
        with st.container(border=True):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password",type="password")
            login_clicked = st.button("🚀 Login",use_container_width=True)

    if login_clicked:

        user = authenticate_user(username, password)
        if user:
            if user[1] in ["Officer", "Admin"]:
                st.session_state.logged_in = True
                st.session_state.username = user[0]
                st.session_state.role = user[1]
                st.session_state.department = user[2]
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error("Citizen login is not supported.")
        else:
            st.error("Invalid Username or Password")

    if st.session_state.logged_in:

        st.success(f"👤 Logged in as : {st.session_state.username}")
        st.caption(f"🛡 Role : {st.session_state.role}")

        if st.button("🚪 Logout",use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.department = ""
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# PAGE 5 — DEPARTMENT PANEL  (replaces "Update Status")
# ══════════════════════════════════════════════════════════════════════

elif page == "🏛 Department Panel":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()
    if st.session_state.role != "Officer":
        st.error("Only officers can access this page")
        st.stop()
    st.header("🏛 Department Officer Panel")
    st.caption("Manage assigned complaints")
    c1,c2=st.columns([5,1])
    with c1:
        st.success( f"👤 Logged in as : {st.session_state.username}" )
    with c2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.department = ""
            st.rerun()
    
    st.subheader("📋 Complaint Queue")

    complaints = get_all_complaints()

    if not complaints:
        st.info("No complaints registered yet.")
        st.stop()

    df = pd.DataFrame(
        complaints,
        columns=[
            "ID", "Citizen Name", "Phone Number", "Address", "Complaint", "Category", "Image Category",
            "Confidence", "Evidence Status", "Department","Recommendation", "Priority Score", "Severity", 
            "Reports Count", "Status","Before Image","After Image","Resolved At", "Created At"
        ]
    )

    # ── Filters ────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Department: {st.session_state.department}")
    with col2:
        status_filter = st.selectbox(
            "📋 Filter by Status",
            ["All", "Pending", "In Progress", "Resolved","Reopened","Escalated"]
        )
    filtered = df[df["Department"] == st.session_state.department]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]

    st.info(f"📌 {len(filtered)} complaint(s) currently assigned to your department")
    st.markdown("---")

    if filtered.empty:
        st.warning("No complaints match the selected filters.")
        st.stop()

    pending = len(filtered[filtered["Status"]=="Pending"])
    progress = len(filtered[filtered["Status"]=="In Progress"])
    resolved = len(filtered[filtered["Status"]=="Resolved"])
    reopened = len(filtered[filtered["Status"]=="Reopened"])
    escalated = len(filtered[filtered["Status"]=="Escalated"])
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.metric("🔴 Pending", pending)
    with c2:
        st.metric("🟡 In Progress", progress)
    with c3:
        st.metric("🟢 Resolved", resolved)
    with c4:
        st.metric("🔄 Reopened", reopened)
    with c5:
        st.metric("⚠️ Escalated", escalated)
    # ── One card per complaint ─────────────────────────────────────────
    for _, row in filtered.iterrows():

        complaint_id = int(row["ID"])

        status_icon = {"Pending": "🔴", "In Progress": "🟡", "Resolved": "🟢","Reopened": "🔄","Escalated": "⚠️"}.get(row["Status"], "⚪")

        # Age in days
        try:
            created_dt = datetime.strptime(str(row["Created At"])[:19], "%Y-%m-%d %H:%M:%S")
            age_days = (datetime.now() - created_dt).days
        except Exception:
            age_days = 0
        # Automatic escalation
        if row["Status"] == "Pending" and age_days >= 2:
            escalate_complaint(complaint_id)
            st.rerun()
        if row["Status"] == "In Progress" and age_days >= 5:
            escalate_complaint(complaint_id)
            st.rerun()
        overdue_badge = (" 🔥 Overdue" if age_days >= 3 and row["Status"] not in ["Resolved"] else "")
        with st.expander(
            f"{status_icon} #{complaint_id} — {row['Category']} | {row['Status']}{overdue_badge}",
            expanded=(st.session_state.get("open_complaint",-1) == complaint_id)
        ):
            # ── Details ───────────────────────────────────────────────
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Complaint ID", complaint_id)
                st.subheader("📝 Complaint")
                st.info(row["Complaint"])
                st.divider()
                st.markdown("**👤 Citizen Name**")
                st.success(row["Citizen Name"])
                st.divider()
                with st.expander("📞 Contact Citizen"):
                    st.write(row["Phone Number"])
                st.divider()
                st.markdown("**📍 Location**")
                st.info(row["Address"])
                st.divider()
                # Show uploaded complaint image
                before_image = row["Before Image"]
                if (
                    row["Category"] in ["Roads", "Sanitation"]
                    and isinstance(before_image, str)
                    and os.path.exists(before_image)
                ):
                    st.markdown("### 📷 Complaint Image")
                    st.image(before_image,width=280)
                st.divider()
                st.info(f"📂 Category : {row['Category']}")
                st.success(f"🏢 Department : {row['Department']}")
                st.warning(f"👷 Officer : {st.session_state.username}")

                if row["Reports Count"] >= 5:
                    st.error("🚨 Multiple citizens reported this issue")
                elif row["Reports Count"] >= 3:
                    st.warning("⚠ Recurring complaint")
                else:
                    st.info("Normal complaint frequency")

            with col2:
                with st.container(border=True):
                    st.markdown("**🤖 AI Recommendation**")
                    st.success(row["Recommendation"])
                    st.markdown("**⏳ Expected Action**")
                    if row["Category"] == "Roads":
                        st.info("Repair team within 24-48 hours")
                    elif row["Category"] == "Sanitation":
                        st.info("Cleaning team within 12 hours")
                    elif row["Category"] == "Drainage":
                        st.info("Inspection team within 24 hours")
                    elif row["Category"] == "Water":
                        st.info("Water department response within 24 hours")
                    elif row["Category"] == "Electricity":
                        st.info("Electrical maintenance team within 6 hours")
                    st.markdown("**⚡ Severity**")
                    st.write(row["Severity"])
                    st.markdown("**🎯 Priority Level**")
                    st.progress(row["Priority Score"] / 100)
                    st.write(f"Priority Score : {row['Priority Score']}/100")
                    if row["Priority Score"] >= 80:
                        st.error(f"🔴 High Priority")
                    elif row["Priority Score"] >= 60:
                        st.warning(f"🟡 Medium Priority")
                    else:
                        st.success(f"🟢 Low Priority")

                    if row["Category"] in ["Roads", "Sanitation"]:

                        st.markdown("**🤖 AI Evidence Analysis**")
                        st.write(f"Evidence Status : {row['Evidence Status']}")

                        if row["Evidence Status"] == "Verified":
                            st.success("✅ AI image evidence verified")

                        elif row["Evidence Status"] == "Needs Verification":
                            st.warning("⚠ Physical inspection recommended")

                        else:
                            st.info("ℹ No image evidence submitted")

                    else:

                        st.info("📷 Image verification not required.")

                    st.markdown("**📅 Submitted**")
                    st.write(f"{row['Created At']}  ({age_days} day(s) ago)")
                    after_image = row["After Image"]
                    if (
                        row["Category"] in ["Roads", "Sanitation"]
                        and isinstance(after_image, str)
                        and os.path.exists(after_image)
                    ):
                        st.markdown("### ✅ Completion Proof")
                        st.image(after_image,width=280)

            st.markdown("---")

            # ── Action panel ──────────────────────────────────────────
            if row["Status"] == "Resolved":
                st.success("✅ Complaint has already been resolved.")
                st.info("No further updates are allowed.")
            else:
                st.markdown("---")
                with st.container(border=True):
                    st.subheader("✏️ Officer Actions")
                    a1, a2 = st.columns(2)
                    with a1:
                        officer_name = st.session_state.username
                        if row["Status"] == "Pending":
                            status_options = ["Pending", "In Progress"]
                        elif row["Status"] == "In Progress":
                            status_options = ["In Progress", "Resolved"]
                        elif row["Status"] == "Reopened":
                            status_options = ["Reopened", "In Progress", "Resolved"]
                        elif row["Status"] == "Escalated":
                            status_options = ["Escalated", "In Progress", "Resolved"]
                        else:
                            status_options = ["Resolved"]

                        new_status = st.selectbox(
                            "Update Status To",
                            status_options,
                            key=f"status_{complaint_id}"
                        )

                    with a2:
                        action_note = st.text_area(
                            "Action Note (required)",
                            placeholder="""
                                Examples:
                                • Team dispatched
                                • Site inspected
                                • Cleaning vehicle sent
                                • Repair work completed""",
                            key=f"note_{complaint_id}",
                            height=120
                        )

                    completion_image = None
                    if (new_status == "Resolved" and row["Category"] in ["Roads","Sanitation"]):
                        completion_image = st.file_uploader(
                            "📷 Upload Completion Image",
                            type=["jpg","jpeg","png"],
                            key=f"completion_{complaint_id}"
                        )
                    completed = st.checkbox(
                        "✔ Work Completed",
                        key=f"completed_{complaint_id}"
                    )
                    verified = st.checkbox(
                        "✔ Site Verified",
                        key=f"verified_{complaint_id}"
                    )
    
                    if st.button(
                        f"✅ Save Update — Complaint #{complaint_id}",
                        key=f"save_{complaint_id}"
                    ):
                        if not action_note.strip():
                            st.error("⚠ Action note is required.")
                            st.stop()

                        # Validation before resolving
                        if new_status == "Resolved":

                            if not completed:
                                st.error("✔ Please confirm that the work has been completed.")
                                st.stop()

                            if not verified:
                                st.error("✔ Please verify the site before resolving the complaint.")
                                st.stop()

                            if (
                                row["Category"] in ["Roads", "Sanitation"]
                                and completion_image is None
                            ):
                                st.error("📷 Please upload a completion image before resolving.")
                                st.stop()
                        
                        if (
                            new_status == "Resolved"
                            and row["Category"] in ["Roads", "Sanitation"]
                        ):
                            os.makedirs("uploads", exist_ok=True)

                            image_path = f"uploads/after_{complaint_id}.jpg"

                            with open(image_path, "wb") as f:
                                f.write(completion_image.getbuffer())

                            predicted_class, confidence = predict_image(image_path)
                            log_activity(
                                complaint_id,
                                action="AI verified completion image",
                                note=f"{predicted_class} ({confidence:.2f}%)",
                                officer="AI System"
                            )
                            
                            expected = {
                                "Roads": "Normal",
                                "Sanitation": "Normal"
                            }

                            if predicted_class != expected[row["Category"]]:

                                st.error(
                                    f"""
                            ❌ AI Verification Failed

                            Complaint Category : {row['Category']}

                            Expected Image : {expected[row['Category']]}

                            Detected Image : {predicted_class}

                            Confidence : {confidence:.2f}%

                            Please upload the correct completion image.
                            """
                                )

                                os.remove(image_path)
                                st.stop()

                            # Prevent updating to the same status
                            if new_status == row["Status"]:
                                st.warning("Complaint is already in this status.")
                                st.stop()

                            update_status_with_log(
                                complaint_id=complaint_id,
                                new_status=new_status,
                                note=action_note.strip(),
                                officer=officer_name
                            )
                            update_after_image(complaint_id,image_path)
                            log_activity(
                                complaint_id,
                                action="Completion image uploaded",
                                note="Officer uploaded proof after work completion",
                                officer=officer_name
                            )
                            st.success(f"✅ Complaint #{complaint_id} updated to {new_status}")

                            st.session_state[f"updated_{complaint_id}"] = True
                            st.session_state.open_complaint = complaint_id

                            st.rerun()
                        else:

                            if new_status == row["Status"]:
                                st.warning("Complaint is already in this status.")
                                st.stop()

                            update_status_with_log(
                                complaint_id=complaint_id,
                                new_status=new_status,
                                note=action_note.strip(),
                                officer=officer_name
                            )

                            st.success(f"✅ Complaint #{complaint_id} updated to {new_status}")

                            st.session_state[f"updated_{complaint_id}"] = True
                            st.session_state.open_complaint = complaint_id

                            st.rerun()
                    
            # ── Activity Timeline ─────────────────────────────────────
            st.markdown("---")
    
            st.subheader("📜 Activity History")
            st.caption("Every action performed on this complaint.")
            logs = get_activity_log(complaint_id)

            if not logs:
                st.caption("No activity recorded yet.")
            else:
                for entry in logs:
                    if "submitted" in entry["action"].lower():
                        icon = "📌"
                    elif "In Progress" in entry["action"]:
                        icon = "🚧"
                    elif "Resolved" in entry["action"]:
                        icon = "✅"
                    elif "Completion image" in entry["action"]:
                        icon = "📷"
                    elif "reopened" in entry["action"].lower():
                        icon = "🔄"
                    elif "Escalated" in entry["action"]:
                        icon = "⚠️"
                    elif "Assigned" in entry["action"]:
                        icon = "👷"
                    else:
                        icon = "📝"

                    st.markdown(
                        f"""
                        <div class='timeline-card'>
                        {icon} <b>{entry['action']}</b><br>
                        <small style="color:#94a3b8">{entry['timestamp']} • {entry['officer']}</small>
                        </div>
                        """,unsafe_allow_html=True)

                    if entry["note"]:
                        st.caption(entry["note"])

# ───────────────────────────────────────
# Admin Panel
# ───────────────────────────────────────
elif page == "👑 Admin Panel":
    if not st.session_state.logged_in:
        st.warning("🔒 Login required")
        st.stop()

    if st.session_state.role != "Admin":
        st.error("❌ Only admin can access this page")
        st.stop()

    st.title("👑 Admin Dashboard")
    st.caption("System monitoring and analytics")
    search = st.text_input("🔍 Search Complaint / Citizen / Location")
    complaints = get_all_complaints()

    if not complaints:
        st.info("No complaints found.")
        st.stop()

    df = pd.DataFrame(
        complaints,
        columns=[
            "ID",
            "Citizen Name",
            "Phone Number",
            "Address",
            "Complaint",
            "Category",
            "Image Category",
            "Confidence",
            "Evidence Status",
            "Department",
            "Recommendation",
            "Priority Score",
            "Severity",
            "Reports Count",
            "Status",
            "Before Image",
            "After Image",
            "Resolved At",
            "Created At"
        ]
    )
    if search:
        df = df[
            df.astype(str)
            .apply(lambda x: x.str.contains(search, case=False))
            .any(axis=1)
        ]
    # ================= Dashboard Metrics =================
    st.subheader("📊 System Overview")
    total = len(df)
    pending = len(df[df["Status"]=="Pending"])
    resolved = len(df[df["Status"]=="Resolved"])
    escalated = len(df[df["Status"]=="Escalated"])

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("📋 Total", total)

    with c2:
        st.metric("🔴 Pending", pending)

    with c3:
        st.metric("🟢 Resolved", resolved)

    with c4:
        st.metric("⚠️ Escalated", escalated)

    st.markdown("---")

    # ================= Escalated Complaints =================

    st.subheader("⚠️ Critical Escalations")

    escalated_df = df[df["Status"]=="Escalated"]

    if escalated_df.empty:
        st.success("No escalated complaints")
    else:
        st.dataframe(
            escalated_df[
                [
                    "ID",
                    "Category",
                    "Department",
                    "Severity",
                    "Status",
                    "Created At"
                ]
            ],
            use_container_width=True
        )

    st.markdown("---")

    # ================= High Priority Complaints =================
    avg_priority = round(df["Priority Score"].mean(),2)
    st.metric("Average Priority Score",avg_priority)
    st.subheader("🚨 High Priority Cases")

    high_df = df[df["Priority Score"] >= 80]

    if high_df.empty:
        st.success("No high priority complaints")
    else:
        st.dataframe(
            high_df[
                [
                    "ID",
                    "Category",
                    "Department",
                    "Priority Score",
                    "Status"
                ]
            ],
            use_container_width=True
        )

    st.markdown("---")

    # ================= Resolution Time Analytics =================
    st.subheader("⏱ Resolution Performance")
    resolved_df = df[
        (df["Status"]=="Resolved") &
        (df["Resolved At"].notna())
    ]

    if not resolved_df.empty:

        resolution_times = []

        for _, row in resolved_df.iterrows():

            created_time = datetime.strptime(
                str(row["Created At"]),
                "%Y-%m-%d %H:%M:%S"
            )

            resolved_time = datetime.strptime(
                str(row["Resolved At"]),
                "%Y-%m-%d %H:%M:%S"
            )

            hours_taken = (
                resolved_time-created_time
            ).total_seconds()/3600

            resolution_times.append(hours_taken)

        avg_hours = round(sum(resolution_times)/len(resolution_times),2)
        fastest = round(min(resolution_times),2)
        slowest = round(max(resolution_times),2)

        c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(
                "⏱ Average Resolution",
                f"{avg_hours} hrs"
            )

        with c2:
            st.metric(
                "⚡ Fastest Resolution",
                f"{fastest} hrs"
            )

        with c3:
            st.metric(
                "🐢 Slowest Resolution",
                f"{slowest} hrs"
            )

    else:
        st.info("No resolved complaints available.")

    st.markdown("---")
    # ================= Citizen Satisfaction =================
    st.markdown("---")
    st.subheader("⭐ Citizen Satisfaction Analytics")
    feedback_data = get_all_feedback()
    if feedback_data:
        avg_rating = get_average_rating()
        feedback_df = pd.DataFrame(
            feedback_data,
            columns=["Rating","Comment","Date"]
        )
    else:
        avg_rating = 0
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Average Rating", f"{avg_rating} / 5 ⭐")
    with c2:
        st.metric("Total Feedback", len(feedback_data))
    
    st.subheader("📊 Rating Distribution")
    rating_counts = (
    feedback_df["Rating"]
    .value_counts()
    .sort_index()
    )
    st.bar_chart(rating_counts)
    st.subheader("💬 Latest Feedback")
    for _, row in feedback_df.head(5).iterrows():
        st.success(f"⭐ {row['Rating']}/5\n\n{row['Comment']}")
    else:
        st.info("No feedback available yet.")

    # ================= Officer Performance =================
    st.markdown("---")
    st.subheader("👷 Officer Performance Analytics")
    performance_data = get_officer_performance()
    if performance_data:
        performance_df = pd.DataFrame(
            performance_data,columns=["Officer","Actions Taken"]
        )
        st.dataframe(performance_df,use_container_width=True)
        st.bar_chart(performance_df.set_index("Officer"))
    else:
        st.info("No officer activity available.")

    # ================= Complaint Hotspots =================
    st.markdown("---")
    st.subheader("📍 Complaint Hotspot Analysis")
    location_data = get_location_statistics()
    if location_data:
        hotspot_df = pd.DataFrame(location_data,columns=["Location","Complaints"])
        hotspot_df = hotspot_df.sort_values(by="Complaints",ascending=False)
        st.dataframe(hotspot_df.head(10),use_container_width=True)
        st.bar_chart(hotspot_df.set_index("Location"))
    else:
        st.info("No location data available.")


    # ================= Officer Management =================
    st.subheader("👮 Officer Management")

    users = get_all_users()

    user_df = pd.DataFrame(
        users,
        columns=[
            "Username",
            "Role",
            "Department"
        ]
    )
    st.dataframe(
    user_df,
    hide_index=True,
    use_container_width=True
    )
