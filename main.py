import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io
from collections import defaultdict

st.set_page_config(page_title="NSS Special Camp - Permission System", layout="wide")

# Streamlit app
st.title("NSS Special Camp - Class Permission Email System")
st.markdown("**For students attending NSS Special Camp (Week of 19th February 2025)**")

# Time slot mapping
time_slot_mapping = {
    1: "7:10 AM - 8:00 AM",
    2: "8:00 AM - 8:50 AM",
    3: "9:20 AM - 10:10 AM",
    4: "10:10 AM - 11:00 AM",
    5: "11:10 AM - 12:00 PM",
    6: "12:00 PM - 12:50 PM",
    7: "1:00 PM - 1:50 PM",
    8: "1:50 PM - 2:40 PM",
    9: "2:50 PM - 3:40 PM",
    10: "3:50 PM - 4:40 PM",
    11: "4:40 PM - 5:30 PM"
}

# User inputs for email credentials
outlook_user = st.text_input("Outlook Email Address", "")
outlook_password = st.text_input("Outlook Password", "", type="password")

# Sender information
st.subheader("📋 Sender Information")
col1, col2 = st.columns(2)
with col1:
    sender_designation = st.selectbox(
        "Who is sending this email?",
        ["HOD - AI & DS", "Associate HOD - AI & DS", "NSS Program Officer", "Faculty Coordinator", "Other"]
    )
    if sender_designation == "Other":
        sender_designation = st.text_input("Specify designation:", "")
    
    sender_name = st.text_input("Sender Name", "")

with col2:
    cc_emails_input = st.text_area(
        "CC Email Addresses (comma-separated, optional)",
        placeholder="email1@kluniversity.in, email2@kluniversity.in"
    )

# Define the email template for faculty permission
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NSS Special Camp - Permission Request</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            color: #2c3e50;
            line-height: 1.6;
        }
        .email-container {
            max-width: 850px;
            margin: 20px auto;
            padding: 0;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #d9534f 0%, #c9302c 100%);
            padding: 25px;
            text-align: center;
            color: white;
        }
        .header img {
            display: block;
            margin: 0 auto 15px;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }
        .content {
            padding: 30px;
        }
        .content p {
            margin-bottom: 15px;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }
        table th {
            background-color: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        table td {
            padding: 10px 12px;
            border-bottom: 1px solid #ecf0f1;
        }
        table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        table tr:hover {
            background-color: #e9ecef;
        }
        @media only screen and (max-width: 600px) {
            .email-container {
                margin: 0;
                border-radius: 0;
            }
            .content {
                padding: 15px;
            }
            table {
                font-size: 12px;
            }
            table th,
            table td {
                padding: 8px 6px;
                font-size: 11px;
            }
            .header h1 {
                font-size: 18px;
            }
        }
        .footer {
            margin-top: 30px;
            padding: 20px 30px;
            background-color: #f8f9fa;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }
        .signature {
            margin-top: 25px;
            padding-top: 15px;
            border-top: 2px solid #e9ecef;
        }
        .header img {
            display: none;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <img src="https://i.imgur.com/jkpf1qu.png" alt="NSS Logo" width="180">
            <h1>NSS Special Camp - Permission Request</h1>
        </div>
        <div class="content">
            <p>Dear <b>[faculty_name]</b>,</p>
            
            <p>Greetings from NSS Unit, KL University!</p>
            
            <div class="highlight">
                <p><strong>Subject:</strong> Permission Request for Students Attending NSS Special Camp</p>
            </div>
            
            <p>This is to inform you that the following student(s) from your <b>[course_code] - Section [section]</b> class will be attending the <strong>NSS Special Camp</strong> during the week of <b>19th February 2025</b>.</p>
            
            <p>We kindly request you to grant permission for their absence from the following class(es):</p>
            
            [student_table]
            
            <p>The students are participating in this camp as part of their NSS commitment and community service responsibilities. We request you to kindly grant them permission and allow them to complete any missed assignments or assessments at a later date.</p>
            
            <p><strong>Attached Documents:</strong> Official permission letter(s) and camp notification.</p>
            
            <p>We sincerely appreciate your understanding and cooperation in this matter.</p>
            
            <div class="signature">
                <p><strong>Best regards,</strong><br>
                <b>[sender_name]</b><br>
                [sender_designation]<br>
                Department of AI & DS<br>
                NSS Unit, KL University<br>
                Email: [sender_email]</p>
            </div>
        </div>
        <div class="footer">
            <p><strong>NSS Unit - KL University</strong></p>
            <p>Instagram: <a href="https://www.instagram.com/klef_nss_official/">@klef_nss_official</a> | 
            Telegram: <a href="https://t.me/+k_Bt9R_WDxVjNGJl">@KLEF_NSS_Y23 BATCH</a></p>
        </div>
    </div>
</body>
</html>
"""

with st.sidebar:
    st.header("📖 Instructions")
    st.write("""
    **Required Columns in your file:**
    1. `student_name` - Student's full name
    2. `student_id` - University ID number
    3. `date` - Date of class (DD/MM/YYYY)
    4. `time_slot` - Slot number (1-11)
    5. `course_code` - Course code (e.g., 23EC1505)
    6. `section` - Section number
    7. `faculty_name` - Main faculty name
    8. `hour_type` - Lecture/Practical/Skill
    9. `faculty_type` - A/B/C
    10. `alt_faculty_name` - If B/C, their name (else leave empty)
    11. `faculty_email` - Main faculty email
    12. `alt_faculty_email` - If B/C, their email (else leave empty)
    
    **Note:** The system will group students by faculty, course, and section automatically.
    """)
    
    # Create sample data
    sample_data = pd.DataFrame({
        "student_name": ["Rahul Kumar", "Priya Sharma", "Amit Patel"],
        "student_id": ["2200080137", "2200080234", "2200080137"],
        "date": ["19/02/2025", "19/02/2025", "20/02/2025"],
        "time_slot": [3, 4, 5],
        "course_code": ["23EC1505", "23EC1505", "23CS2401"],
        "section": ["S1", "S1", "S2"],
        "faculty_name": ["Dr. Ramesh", "Dr. Ramesh", "Prof. Suresh"],
        "hour_type": ["Lecture", "Practical", "Lecture"],
        "faculty_type": ["A", "B", "A"],
        "alt_faculty_name": ["", "Dr. Mohan", ""],
        "faculty_email": ["ramesh@kluniversity.in", "ramesh@kluniversity.in", "suresh@kluniversity.in"],
        "alt_faculty_email": ["", "mohan@kluniversity.in", ""]
    })
    
    csv_buffer = io.StringIO()
    sample_data.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.markdown("### 📥 Sample Data Format")
    st.dataframe(sample_data, width='stretch')
    
    st.download_button(
        label="📂 Download Sample CSV",
        data=csv_data,
        file_name="nss_camp_sample.csv",
        mime="text/csv"
    )

# Upload CSV or Excel
uploaded_file = st.file_uploader(
    "📤 Upload CSV or Excel file with student class details",
    type=["csv", "xlsx", "xls"]
)

# File uploader for attachments
attachment_files = st.file_uploader(
    "📎 Upload Permission Letter(s) / Camp Notification (PDF, DOCX, JPG, PNG, etc.)",
    type=None,
    accept_multiple_files=True
)

if uploaded_file and sender_name and outlook_user:
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file, engine="openpyxl")
        
        # Clean column names
        data.columns = data.columns.str.strip()
        
        # Required columns validation
        required_columns = [
            "student_name", "student_id", "date", "time_slot", "course_code",
            "section", "faculty_name", "hour_type", "faculty_type",
            "alt_faculty_name", "faculty_email", "alt_faculty_email"
        ]
        
        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
        else:
            # Clean data
            data = data.dropna(subset=["student_name", "student_id", "date", "time_slot", 
                                       "course_code", "section", "faculty_name", "faculty_email"])
            
            # Convert time slots to readable format
            data['time_slot'] = data['time_slot'].astype(int)
            data['time_range'] = data['time_slot'].map(time_slot_mapping)
            
            # Fill empty alt faculty fields
            data['alt_faculty_name'] = data['alt_faculty_name'].fillna('')
            data['alt_faculty_email'] = data['alt_faculty_email'].fillna('')
            
            st.success(f"✅ Successfully loaded {len(data)} records")
            st.write("📊 **Data Preview:**")
            st.dataframe(data.head(10), width='stretch')
            
            # Group by faculty_email, course_code, and section
            grouped = data.groupby(['faculty_email', 'course_code', 'section', 'faculty_name'])
            
            st.write(f"📧 **Total emails to be sent:** {len(grouped)}")
            
            # Prepare emails
            emails_to_send = []
            
            for (faculty_email, course_code, section, faculty_name), group in grouped:
                # Build student table
                table_rows = ""
                for idx, row in group.iterrows():
                    alt_info = ""
                    if row['faculty_type'] in ['B', 'C'] and row['alt_faculty_name']:
                        alt_info = f"<br><small><i>({row['faculty_type']} Faculty: {row['alt_faculty_name']})</i></small>"
                    
                    table_rows += f"""
                    <tr>
                        <td>{row['student_name']}</td>
                        <td>{row['student_id']}</td>
                        <td>{row['date']}</td>
                        <td>{row['time_slot']}</td>
                        <td>{row['time_range']}</td>
                        <td>{row['hour_type']}{alt_info}</td>
                    </tr>
                    """
                
                student_table = f"""
                <table>
                    <thead>
                        <tr>
                            <th>Student Name</th>
                            <th>ID Number</th>
                            <th>Date</th>
                            <th>Slot</th>
                            <th>Time</th>
                            <th>Hour Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                """
                
                # Prepare email body
                email_body = html_template.replace("[faculty_name]", faculty_name) \
                    .replace("[course_code]", course_code) \
                    .replace("[section]", section) \
                    .replace("[student_table]", student_table) \
                    .replace("[sender_name]", sender_name) \
                    .replace("[sender_designation]", sender_designation) \
                    .replace("[sender_email]", outlook_user)
                
                # Collect all unique alt faculty emails from this group
                alt_emails = group[group['alt_faculty_email'] != '']['alt_faculty_email'].unique().tolist()
                
                emails_to_send.append({
                    "To": faculty_email,
                    "CC": alt_emails,
                    "Subject": f"Permission Request: NSS Special Camp - {course_code} Section {section}",
                    "Body": email_body,
                    "Course": f"{course_code} - {section}",
                    "Faculty": faculty_name
                })
            
            # Display email preview
            st.write("### 📨 Email Preview")
            for idx, email in enumerate(emails_to_send, 1):
                with st.expander(f"Email {idx}: {email['Faculty']} - {email['Course']}"):
                    st.write(f"**To:** {email['To']}")
                    if email['CC']:
                        st.write(f"**CC:** {', '.join(email['CC'])}")
                    st.write(f"**Subject:** {email['Subject']}")
            
            # Send emails button
            if st.button("📤 Send All Permission Emails", type="primary"):
                if not outlook_password:
                    st.error("❌ Please enter your Outlook password")
                else:
                    # Parse CC emails
                    additional_cc = []
                    if cc_emails_input.strip():
                        additional_cc = [email.strip() for email in cc_emails_input.split(',') if email.strip()]
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    success_count = 0
                    fail_count = 0
                    
                    for idx, email_data in enumerate(emails_to_send):
                        try:
                            msg = MIMEMultipart()
                            msg["Subject"] = email_data["Subject"]
                            msg["From"] = outlook_user
                            msg["To"] = email_data["To"]
                            
                            # Combine CCs
                            all_cc = email_data["CC"] + additional_cc
                            all_cc = list(set(all_cc))  # Remove duplicates
                            
                            if all_cc:
                                msg["CC"] = ", ".join(all_cc)
                            
                            msg["X-Priority"] = "2"  # High Priority
                            msg["Importance"] = "High"
                            
                            msg.attach(MIMEText(email_data["Body"], "html"))
                            
                            # Attach files
                            if attachment_files:
                                for file in attachment_files:
                                    part = MIMEBase("application", "octet-stream")
                                    part.set_payload(file.read())
                                    encoders.encode_base64(part)
                                    part.add_header("Content-Disposition", f"attachment; filename={file.name}")
                                    msg.attach(part)
                                    file.seek(0)
                            
                            # Send email
                            recipients = [email_data["To"]] + all_cc
                            
                            with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
                                server.starttls()
                                server.login(outlook_user, outlook_password)
                                server.sendmail(outlook_user, recipients, msg.as_string())
                            
                            success_count += 1
                            status_text.success(f"✅ Email {idx + 1}/{len(emails_to_send)} sent to {email_data['To']}")
                            
                        except Exception as e:
                            fail_count += 1
                            status_text.error(f"❌ Failed to send to {email_data['To']}: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(emails_to_send))
                    
                    st.success(f"🎉 **Process Complete!** Sent: {success_count} | Failed: {fail_count}")
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align:center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
        <p style='font-size:16px; color:#2c3e50; margin-bottom: 10px;'>
            <b>NSS Special Camp Permission System</b>
        </p>
        <p style='font-size:14px; color:gray;'>
            Made with ❤️ from <b>Intelligentsia Club</b><br>
            Department of AI & DS<br><br>
            Enhanced by <b>Aravind</b> (2200080137)<br>
            Contact: <a href='https://t.me/iarvn1' target='_blank'>@iarvn1</a> on Telegram
        </p>
    </div>
""", unsafe_allow_html=True)