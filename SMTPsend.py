import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import threading
import requests
import smtplib
import xml.etree.ElementTree as ET
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
smtp_username = "notifym3pl0x@outlook.com"
smtp_password = "a#h/-^bTVYBk9kN"

def send_email(subject, content, recipient_email):
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(content, 'plain'))
    server = smtplib.SMTP(host=smtp_server, port=smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, recipient_email, message.as_string())
    server.quit()
    messagebox.showinfo("Email Sent", f"Email sent to {recipient_email}")

def fetch_and_process_data(url, agency_name):
    response = requests.get(url)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    ai_ml_projects = []
    email_content = ""
    for item in root.findall(".//item"):
        firm = item.find("firm").text
        award_title = item.find("award_title").text
        abstract = item.find("abstract").text
        phase = item.find("phase").text
        if abstract and ("AI" in abstract or "Artificial Intelligence" in abstract or "Machine Learning" in abstract):
            ai_ml_projects.append({
                "firm": firm,
                "award_title": award_title,
                "abstract": abstract,
                "phase": phase
            })
            email_content += f"Agency: {agency_name}\nPhase: {phase}\nFirm: {firm}\nAward Title: {award_title}\n-------------------------------------\n"
    if ai_ml_projects:
        num_projects = len(ai_ml_projects)
        email_content += f"\nNumber of AI and machine learning projects from {agency_name}: {num_projects}\n\n"
        return email_content
    else:
        return ""

agency_urls = {
    "DOD": "https://www.sbir.gov/api/awards.xml?agency=DOD",
    "HHS": "https://www.sbir.gov/api/awards.xml?agency=HHS",
    "NASA": "https://www.sbir.gov/api/awards.xml?agency=NASA",
    "NSF": "https://www.sbir.gov/api/awards.xml?agency=NSF",
    "DOE": "https://www.sbir.gov/api/awards.xml?agency=DOE",
    "USDA": "https://www.sbir.gov/api/awards.xml?agency=USDA",
    "EPA": "https://www.sbir.gov/api/awards.xml?agency=EPA",
    "ED": "https://www.sbir.gov/api/awards.xml?agency=ED",
    "DOT": "https://www.sbir.gov/api/awards.xml?agency=DOT",
    "DHS": "https://www.sbir.gov/api/awards.xml?agency=DHS"
}

def create_sidebar(root):
    sidebar = tk.Frame(root, width=200, bg='#0078D7', height=500, relief='sunken', borderwidth=2)
    sidebar.pack(expand=False, fill='y', side='left', anchor='nw')
    settings_button = tk.Button(sidebar, text="Settings", bg='#0078D7', fg='white', relief='flat')
    settings_button.pack(fill='x')
    agency_selection_button = tk.Button(sidebar, text="Agency Selection", bg='#0078D7', fg='white', relief='flat')
    agency_selection_button.pack(fill='x')
    scheduling_button = tk.Button(sidebar, text="Scheduling", bg='#0078D7', fg='white', relief='flat')
    scheduling_button.pack(fill='x')
    notification_settings_button = tk.Button(sidebar, text="Notification Settings", bg='#0078D7', fg='white', relief='flat')
    notification_settings_button.pack(fill='x')
    application_settings_button = tk.Button(sidebar, text="Application Settings", bg='#0078D7', fg='white', relief='flat')
    application_settings_button.pack(fill='x')
    language_frame = tk.Frame(sidebar, bg='#0078D7')
    language_frame.pack(expand=True, anchor='s', fill='x', side='bottom')
    language_en_button = tk.Button(language_frame, text="EN", bg='#0078D7', fg='white', relief='flat')
    language_en_button.pack(side='left', fill='x')
    language_es_button = tk.Button(language_frame, text="ES", bg='#0078D7', fg='white', relief='flat')
    language_es_button.pack(side='right', fill='x')
    return sidebar

def create_main_panel(root):
    main_panel = tk.Frame(root, bg='white')
    main_panel.pack(expand=True, fill='both', side='right')
    label_agency = tk.Label(main_panel, text="Select Agency Alert Presets", font=("Helvetica", 16), bg='white')
    label_agency.pack(pady=(5, 10))
    agency_frame = tk.Frame(main_panel, bg='white')
    agency_frame.pack()
    agencies = [
        "DHS (Department of Homeland Security)", 
        "DOD (Department of Defense)", 
        "DOE (Department of Energy)", 
        "DOT (Department of Transportation)", 
        "ED (Department of Education)", 
        "EPA (Environmental Protection Agency)", 
        "HHS (Department of Health and Human Services)", 
        "NASA (National Aeronautics and Space Administration)", 
        "NSF (National Science Foundation)", 
        "USDA (Department of Agriculture)"
    ]
    agency_vars = {agency: tk.BooleanVar(value=False) for agency in agencies}
    for agency in agencies:
        tk.Checkbutton(agency_frame, text=agency, variable=agency_vars[agency], bg='white').pack(anchor='w')
    label_calendar = tk.Label(main_panel, text="Select Notification Date", font=("Helvetica", 16), bg='white')
    label_calendar.pack(pady=(5, 10))
    calendar_frame = tk.Frame(main_panel, bg='white')
    calendar_frame.pack()
    today = datetime.date.today()
    cal = Calendar(calendar_frame, selectmode='day', year=today.year, month=today.month, day=today.day, mindate=today)
    cal.pack(pady=20)
    label_email = tk.Label(main_panel, text="Enter recipient's email:", font=("Helvetica", 16), bg='white')
    label_email.pack(pady=(5, 10))
    email_entry = tk.Entry(main_panel, font=("Helvetica", 14), width=30)
    email_entry.pack(pady=(0, 10))
    submit_button = tk.Button(main_panel, text="Send Email", command=lambda: threading.Thread(target=submit_action, args=(email_entry.get(), agency_vars, cal.get_date(), root)).start())
    submit_button.pack(pady=(5, 10))
    return main_panel, agency_vars, cal

def submit_action(recipient_email, agency_vars, selected_date, root):
    if not recipient_email or "@" not in recipient_email:
        messagebox.showerror("Error", "Please enter a valid email address.")
        return
    selected_agencies = [agency for agency, var in agency_vars.items() if var.get()]
    if not selected_agencies:
        messagebox.showinfo("No Selection", "Please select at least one agency.")
        return
    content = f"Selected Date: {selected_date}\n\n"
    for agency in selected_agencies:
        email_content = fetch_and_process_data(agency_urls[agency.split(" (")[0]], agency)
        if email_content:
            content += email_content
    if content:
        send_email("Agency Notification", content, recipient_email)
    else:
        messagebox.showinfo("No Data", "No data available to send.")

def main():
    root = tk.Tk()
    root.title('Settings Panel')
    sidebar = create_sidebar(root)
    main_panel, agency_vars, cal = create_main_panel(root)
    root.mainloop()

if __name__ == "__main__":
    main()
