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

# Helper function to build responsive email template
def build_email_template(greeting, intro, body, closing, title="NSS Special Camp - Permission Request", title_color="Red", title_text_color="White"):
    """
    Builds a responsive email template with custom content and styling.
    
    Args:
        greeting (str): Email greeting
        intro (str): Opening message
        body (str): Main request content
        closing (str): Closing and signature
        title (str): Email header title
        title_color (str): Color name for header background
        title_text_color (str): Color name for header text
    
    Returns:
        str: Complete HTML email template
    """
    # Color mapping
    color_map = {
        "Red": "#d9534f",
        "Black": "#2c3e50",
        "White": "#ffffff",
        "Blue": "#3498db",
        "Green": "#27ae60",
        "Purple": "#9b59b6",
        "Gray": "#7f8c8d"
    }
    
    bg_color = color_map.get(title_color, "#d9534f")
    text_color = color_map.get(title_text_color, "#ffffff")
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            color: #2c3e50;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        .email-container {{
            max-width: 850px;
            margin: 20px auto;
            padding: 0;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
            overflow: hidden;
        }}
        .header {{
            background: {bg_color};
            padding: 25px;
            text-align: center;
            color: {text_color};
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .content {{
            padding: 30px;
        }}
        .content p {{
            margin-bottom: 15px;
            white-space: pre-wrap;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
            border-radius: 4px;
        }}
        /* Responsive Email-Safe Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
            background: #fff;
        }}
        table th {{
            background-color: #34495e;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #2c3e50;
        }}
        table td {{
            padding: 10px 8px;
            border: 1px solid #ecf0f1;
            word-wrap: break-word;
            vertical-align: top;
        }}
        table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        table tr:hover {{
            background-color: #e9ecef;
        }}
        /* Mobile-specific styles */
        @media only screen and (max-width: 600px) {{
            .email-container {{
                margin: 10px;
                border-radius: 8px;
            }}
            .content {{
                padding: 20px 15px;
            }}
            .header {{
                padding: 20px 15px;
            }}
            .header h1 {{
                font-size: 18px;
            }}
            table {{
                font-size: 11px;
                display: block;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            table th, table td {{
                padding: 8px 4px;
                font-size: 11px;
                min-width: 60px;
            }}
            .highlight {{
                padding: 10px;
                margin: 15px 0;
            }}
        }}
        .footer {{
            margin-top: 30px;
            padding: 20px 30px;
            background-color: #f8f9fa;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }}
        .signature {{
            margin-top: 25px;
            padding-top: 15px;
            border-top: 2px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        <div class="content">
            <p><b>{greeting}</b></p>
            
            <p>{intro}</p>
            
            <div class="highlight">
                <p><strong>We kindly request you to grant permission for their absence from the following class(es):</strong></p>
            </div>
            
            [student_table]
            
            <p>{body}</p>
            
            <div class="signature">
                <p>{closing}</p>
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

# Helper function to get email template (default or custom)
def get_email_template(custom_template=None, use_custom=False):
    """
    Returns the email template to use.
    If use_custom is True and custom_template is provided, returns custom template.
    Otherwise, returns the default template.
    
    Args:
        custom_template (str): Optional custom email template
        use_custom (bool): Flag to enable custom template
    
    Returns:
        str: Email template HTML
    """
    if use_custom and custom_template and custom_template.strip():
        return custom_template
    
    # Default template - hardcoded fallback
    return """
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
            margin: 0;
            padding: 0;
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
        /* Responsive Email-Safe Table */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
            background: #fff;
        }
        table th {
            background-color: #34495e;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #2c3e50;
        }
        table td {
            padding: 10px 8px;
            border: 1px solid #ecf0f1;
            word-wrap: break-word;
            vertical-align: top;
        }
        table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        table tr:hover {
            background-color: #e9ecef;
        }
        /* Mobile-specific styles */
        @media only screen and (max-width: 600px) {
            .email-container {
                margin: 10px;
                border-radius: 8px;
            }
            .content {
                padding: 20px 15px;
            }
            .header {
                padding: 20px 15px;
            }
            .header h1 {
                font-size: 18px;
            }
            table {
                font-size: 11px;
                display: block;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }
            table th, table td {
                padding: 8px 4px;
                font-size: 11px;
                min-width: 60px;
            }
            .highlight {
                padding: 10px;
                margin: 15px 0;
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

# Email Matter Customization Feature (Optional)
st.subheader("✉️ Email Content (Optional Customization)")

col_toggle, col_reset = st.columns([3, 1])
with col_toggle:
    use_custom_template = st.checkbox(
        "✏️ Edit Email Content",
        value=False,
        help="Enable this to customize the email message content. Leave unchecked to use the default content."
    )
with col_reset:
    if use_custom_template:
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.rerun()

custom_email_template = None
simple_greeting = None
simple_intro = None
simple_body = None
simple_closing = None
email_title = "NSS Special Camp - Permission Request"
email_title_color = "Red"
email_title_text_color = "White"

if use_custom_template:
    st.markdown("---")
    
    # Create tabs: Content Editor and Preview
    tab1, tab2 = st.tabs(["✏️ Edit Content", "👁️ Preview Email"])
    
    with tab1:
        st.info("📝 Edit the email message content below. All formatting and styling is handled automatically.")
        
        # Email Title and Color Selection
        st.markdown("### 🎨 Email Header Customization:")
        col_title, col_bg, col_text = st.columns([2, 1, 1])
        with col_title:
            email_title = st.text_input(
                "Email Title:",
                value="NSS Special Camp - Permission Request",
                help="The main title displayed at the top of the email",
                key="email_title"
            )
        with col_bg:
            color_options = {
                "Red": "#d9534f",
                "Black": "#2c3e50",
                "White": "#ffffff",
                "Blue": "#3498db",
                "Green": "#27ae60",
                "Purple": "#9b59b6",
                "Gray": "#7f8c8d"
            }
            email_title_color = st.selectbox(
                "Background Color:",
                options=list(color_options.keys()),
                index=0,
                help="Select the background color for the email title",
                key="email_title_color"
            )
        with col_text:
            text_color_options = {
                "White": "#ffffff",
                "Black": "#2c3e50",
                "Red": "#d9534f",
                "Blue": "#3498db",
                "Green": "#27ae60",
                "Purple": "#9b59b6",
                "Gray": "#7f8c8d"
            }
            email_title_text_color = st.selectbox(
                "Text Color:",
                options=list(text_color_options.keys()),
                index=0,
                help="Select the text color for the email title",
                key="email_title_text_color"
            )
        
        st.markdown("---")
        
        col_help1, col_help2 = st.columns(2)
        with col_help1:
            st.markdown("""
            **✨ Auto-Inserted Information:**
            - Faculty name
            - Course code & Section
            - Student details table
            """)
        with col_help2:
            st.markdown("""
            **📌 Your Information:**
            - Your name
            - Your designation
            - Your email address
            """)
        
        st.markdown("### 📧 Email Message:")
        
        simple_greeting = st.text_input(
            "1️⃣ Greeting:",
            value="Dear [faculty_name],",
            help="How you address the faculty member",
            key="email_greeting"
        )
        
        simple_intro = st.text_area(
            "2️⃣ Opening Message:",
            value="Greetings from NSS Unit, KL University!\n\nThis is to inform you that the following student(s) from your [course_code] - Section [section] class will be attending the NSS Special Camp during the week of 19th February 2025.",
            height=100,
            help="Introduction explaining the purpose of the email",
            key="email_intro"
        )
        
        st.info("ℹ️ The student details table will be automatically inserted here")
        
        simple_body = st.text_area(
            "3️⃣ Main Request:",
            value="The students are participating in this camp as part of their NSS commitment and community service responsibilities. We request you to kindly grant them permission and allow them to complete any missed assignments or assessments at a later date.\n\nAttached Documents: Official permission letter(s) and camp notification.",
            height=150,
            help="Your main message and request to the faculty",
            key="email_body"
        )
        
        simple_closing = st.text_area(
            "4️⃣ Closing & Signature:",
            value="We sincerely appreciate your understanding and cooperation in this matter.\n\nBest regards,\n[sender_name]\n[sender_designation]\nDepartment of AI & DS\nNSS Unit, KL University\nEmail: [sender_email]",
            height=120,
            help="Closing message and your signature",
            key="email_closing"
        )
        
        st.success("✅ Your custom email content is ready! Switch to the Preview tab to see how it looks.")
    
    with tab2:
        st.markdown("### 👁️ Email Preview")
        st.info("📨 This is how your email will appear to the recipient")
        
        # Build preview template using current text input values and customizations
        if simple_greeting and simple_intro and simple_body and simple_closing:
            preview_template = build_email_template(
                simple_greeting, 
                simple_intro, 
                simple_body, 
                simple_closing,
                email_title,
                email_title_color,
                email_title_text_color
            )
        else:
            preview_template = get_email_template()
        
        # Create a preview with sample data
        preview_html = preview_template.replace("[faculty_name]", "Dr. Sample Faculty") \
            .replace("[course_code]", "23EC1505") \
            .replace("[section]", "S1") \
            .replace("[student_table]", """
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
                        <tr>
                            <td>Sample Student</td>
                            <td>2200080137</td>
                            <td>19/02/2025</td>
                            <td>3</td>
                            <td>9:20 AM - 10:10 AM</td>
                            <td>Lecture</td>
                        </tr>
                    </tbody>
                </table>
            """) \
            .replace("[sender_name]", sender_name if sender_name else "Your Name") \
            .replace("[sender_designation]", sender_designation if sender_designation else "Your Designation") \
            .replace("[sender_email]", outlook_user if outlook_user else "your.email@kluniversity.in")
        
        st.components.v1.html(preview_html, height=800, scrolling=True)
    
    # Build custom email template with user's content (HTML remains hidden)
    # This runs regardless of which tab is active, ensuring template is always available
    if simple_greeting and simple_intro and simple_body and simple_closing:
        custom_email_template = build_email_template(
            simple_greeting,
            simple_intro,
            simple_body,
            simple_closing,
            email_title,
            email_title_color,
            email_title_text_color
        )
    
    st.markdown("---")

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
                
                # Prepare email body - use custom template if enabled, otherwise use default
                active_template = get_email_template(custom_email_template, use_custom_template)
                email_body = active_template.replace("[faculty_name]", faculty_name) \
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