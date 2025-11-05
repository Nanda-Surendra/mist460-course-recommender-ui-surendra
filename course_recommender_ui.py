import pandas as pd
import requests
import streamlit as st

# --- Configuration ---
FASTAPI_BASE_URL = "https://mist460-course-recommender-apis-surendra.azurewebsites.net/"  #"http://localhost:8000"  # or your server URL

#Call FastAPI endpoint and return a DataFrame.
def fetch_data(service_url: str, params: dict, method: str = "get") -> pd.DataFrame:
    if method == "get":
        response = requests.get(service_url, params=params)
    elif method == "post":
        response = requests.post(service_url, params=params)
    payload = response.json()
    rows = payload.get("data", [])
    df = pd.DataFrame(rows)
    return df

## Create a sidebar with a dropdown for the course recommender functionalities
with st.sidebar:
    st.title("Course Recommender Functionalities")

    #Dropdown for course recommender functionalities
    functionality = st.selectbox("Functionality", ["ValidateUser", "FindPrerequisites", "GetCoursesOffered", "CheckIfCompletedPrerequisites", 
    "EnrollInCourseOffering", "GetStudentEnrolledCourseOfferings", "DropFromCourseOffering"])
    if functionality == "ValidateUser":
        endpoint = "validate_user"
    elif functionality == "FindPrerequisites":
        endpoint = "find_prerequisites"
    elif functionality == "GetCoursesOffered":
        endpoint = "find_current_semester_course_offerings"
    elif functionality == "CheckIfCompletedPrerequisites":
        endpoint = "check_if_student_has_taken_all_prerequisites_for_course"
    elif functionality == "EnrollInCourseOffering":
        endpoint = "enroll_student_in_course_offering"
    elif functionality == "GetStudentEnrolledCourseOfferings":
        endpoint = "get_student_enrolled_course_offerings"
    elif functionality == "DropFromCourseOffering":
        endpoint = "drop_student_from_course_offering"

    # Save functionality to session state
    st.session_state.functionality = functionality

if st.session_state.functionality == "ValidateUser":

    st.set_page_config(page_title="Login User", layout="centered")
    st.title("Login User")

    # --- Form Inputs ---
    with st.form("login_form", clear_on_submit=False):
        c1, c2 = st.columns([1, 1])
        with c1:
            username = st.text_input("Username", placeholder="e.g., mjordan@wvu.edu", max_chars=20)
        with c2:
            password = st.text_input("Password", placeholder="e.g., 0x01", max_chars=20)

        submitted = st.form_submit_button("Login User")

    # --- Trigger search ---
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{endpoint}"
        df = fetch_data(service_url, {"username": username, "password": password})
        st.subheader("Results")
        if df.empty:
            st.info("Invalid username or password.")
        else:
            st.info("Login successful.")
            output_string = "App User ID: " + str(df["AppUserID"].values[0]) + " Fullname: " + str(df["FullName"].values[0]) + " is logged in."
            st.write(output_string)
            st.session_state.app_user_id = df["AppUserID"].values[0]

elif st.session_state.functionality == "GetCoursesOffered":

    st.set_page_config(page_title="Course Offered", layout="centered")
    st.title("Course Offerings Finder")

    # --- Form Inputs ---
    with st.form("search_form", clear_on_submit=False):
        c1, c2 = st.columns([1, 1])
        with c1:
            subject_code = st.text_input("Subject Code", placeholder="e.g., MIST", max_chars=20)
        with c2:
            course_number = st.text_input("Course Number", placeholder="e.g., 460", max_chars=20)

        submitted = st.form_submit_button("Get Courses Offered")

    # --- Trigger search ---
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{endpoint}"
        df = fetch_data(service_url, {"subjectCode": subject_code, "courseNumber": course_number})
        st.subheader("Results")
        if df.empty:
            st.info("No courses offered found.")
        else:
            st.dataframe(df, width="stretch")


elif st.session_state.functionality == "FindPrerequisites":

    st.set_page_config(page_title="Course Prerequisites", layout="centered")
    st.title("Course Prerequisites Finder")

    # --- Form Inputs ---
    with st.form("search_form", clear_on_submit=False):
        c1, c2 = st.columns([1, 1])
        with c1:
            subject_code = st.text_input("Subject Code", placeholder="e.g., MIST", max_chars=20)
        with c2:
            course_number = st.text_input("Course Number", placeholder="e.g., 460", max_chars=20)

        submitted = st.form_submit_button("Find Prerequisites")

    # --- Trigger search ---
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{endpoint}"
        df = fetch_data(service_url, {"subjectCode": subject_code, "courseNumber": course_number})
        st.subheader("Results")
        if df.empty:
            st.info("No prerequisites found.")
        else:
            st.dataframe(df, width='stretch')

elif st.session_state.functionality == "CheckIfCompletedPrerequisites":
    st.set_page_config(page_title="Check If Completed Prerequisites", layout="centered")
    st.title("Check If Completed Prerequisites")

    # --- Form Inputs ---
    with st.form("search_form", clear_on_submit=False):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            student_id = st.text_input("Student ID", value=st.session_state.app_user_id, disabled=True)
        with c2:
            subject_code = st.text_input("Subject Code", placeholder="e.g., MIST", max_chars=20)
        with c3:
            course_number = st.text_input("Course Number", placeholder="e.g., 460", max_chars=20)

        submitted = st.form_submit_button("Check If Completed Prerequisites")

    # --- Trigger search ---
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{endpoint}"
        df = fetch_data(service_url, {"studentID": student_id, "subjectCode": subject_code, "courseNumber": course_number})
        st.subheader("Results")
        if df.empty:
            st.info("Student has completed all prerequisites for the course.")
        else:
            st.dataframe(df, width="stretch")

elif st.session_state.functionality == "EnrollInCourseOffering":
    st.set_page_config(page_title="Enroll In Course Offering", layout="centered")
    st.title("Enroll In Course Offering")

    # --- Form Inputs ---
    with st.form("enroll_form", clear_on_submit=False):
        c1, c2 = st.columns([1, 1])
        with c1:
            student_id = st.text_input("Student ID", value=st.session_state.app_user_id, disabled=True)
        with c2:
            course_offering_id = st.text_input("Course Offering ID", max_chars=20)

        submitted = st.form_submit_button("Enroll In Course Offering")

    # --- Trigger search ---
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{endpoint}"
        df = fetch_data(service_url, {"studentID": student_id, "courseOfferingID": course_offering_id}, method="post")
        if "Enrolled" in df["EnrollmentResponse"].values[0]:
            st.success("Enrollment successful.")
        else:
            st.error("Enrollment failed.")
            st.write(df["EnrollmentResponse"].values[0])

elif st.session_state.functionality == "GetStudentEnrolledCourseOfferings":
    st.set_page_config(page_title="Get Student Enrolled Course Offerings", layout="centered")
    st.title("Get Student Enrolled Course Offerings")

    # --- Form Inputs ---
    with st.form("search_form", clear_on_submit=False):
        student_id = st.text_input("Student ID", value=st.session_state.app_user_id, disabled=True)

        submitted = st.form_submit_button("Get Student Enrolled Course Offerings")

    # --- Trigger search ---
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{endpoint}"
        df = fetch_data(service_url, {"studentID": student_id})
        st.subheader("Results")
        if df.empty:
            st.info("No courses enrolled.")
        else:
            st.dataframe(df, width="stretch")

elif st.session_state.functionality == "DropFromCourseOffering":
    st.set_page_config(page_title="Drop From Course Offering", layout="centered")
    st.title("Drop From Course Offering")

    # --- Form Inputs ---
    with st.form("drop_form", clear_on_submit=False):
        c1, c2 = st.columns([1, 1])
        with c1:
            student_id = st.text_input("Student ID", value=st.session_state.app_user_id, disabled=True)
        with c2:
            course_offering_id = st.text_input("Course Offering ID", placeholder="e.g., 123", max_chars=20)

        submitted = st.form_submit_button("Drop From Course Offering")

    # --- Trigger search ---
    if submitted:
        service_url = f"{FASTAPI_BASE_URL}/{endpoint}"
        
        df = fetch_data(service_url, {"studentID": student_id, "courseOfferingID": course_offering_id}, method="post")
        if df["EnrollmentStatus"].values[0] == "Dropped":
            st.success("Drop successful.")
        else:
            st.error("Drop failed.")