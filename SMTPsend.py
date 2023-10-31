import os
import requests
import smtplib
import xml.etree.ElementTree as ET
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP settings for Outlook
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
smtp_username = "notifym3pl0x@outlook.com"
smtp_password = "a#h/-^bTVYBk9kN"

# Define a function to send email
def send_email(subject, content):
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = smtp_username  # Sending the email to yourself for this example
    message['Subject'] = subject
    message.attach(MIMEText(content, 'plain'))

    # Set up the SMTP server and send the email
    server = smtplib.SMTP(host=smtp_server, port=smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    text = message.as_string()
    server.sendmail(smtp_username, smtp_username, text)
    server.quit()
    print("Email sent successfully.")

# Define a function to fetch and process data for a given agency
def fetch_and_process_data(url, agency_name):
    # Fetch the XML data from the URL
    response = requests.get(url)
    xml_data = response.text

    # Parse the XML data
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"Failed to parse XML from {agency_name} due to ParseError: {e}")
        return ""  # Return an empty string if the XML couldn't be parsed

    # Initialize a list to store AI and machine learning projects for the current agency
    ai_ml_projects = []

    # Initialize email content for the current agency
    email_content = ""

    for item in root.findall(".//item"):
        firm = item.find("firm").text
        award_title = item.find("award_title").text
        abstract = item.find("abstract").text
        phase = item.find("phase").text

        # Check if the project is related to AI or Machine Learning
        if abstract and ("AI" in abstract or "Artificial Intelligence" in abstract or "Machine Learning" in abstract):
            ai_ml_projects.append({
                "firm": firm,
                "award_title": award_title,
                "abstract": abstract
            })
            email_content += f"Agency: {agency_name}\n"
            email_content += f"Phase: {phase}\n"
            email_content += f"Firm: {firm}\n"
            email_content += f"Award Title: {award_title}\n"
            email_content += "-------------------------------------\n"

    # Add the number of AI and machine learning projects to the email content if any were found
    if ai_ml_projects:
        num_projects = len(ai_ml_projects)
        email_content += f"\nNumber of AI and machine learning projects from {agency_name}: {num_projects}\n\n"
        return email_content
    else:
        return ""

# List of agency URLs
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

# Fetch and process data for each agency
cumulative_email_content = "Projects related to AI, Machine Learning, and AI from various agencies:\n\n"
for agency, url in agency_urls.items():
    agency_email_content = fetch_and_process_data(url, agency)
    if agency_email_content:
        cumulative_email_content += agency_email_content

# Send a single email with all the collected data
if cumulative_email_content != "Projects related to AI, Machine Learning, and AI from various agencies:\n\n":
    send_email("AI and ML Projects - All Agencies", cumulative_email_content)
