import os
import requests
import xml.etree.ElementTree as ET
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP settings for Outlook
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
smtp_username = os.environ.get("EMAIL")
smtp_password = os.environ.get("PASSWORD")

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

# Define a function to fetch and process data for a given agency
def fetch_and_process_data(url, agency_name):
    # Fetch the XML data from the URL
    response = requests.get(url)
    xml_data = response.text

    # Parse the XML data
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        send_email(f"Error - {agency_name}", f"Failed to parse XML from {agency_name} due to ParseError: {e}")
        return  # Exit the function if the XML couldn't be parsed

    # Initialize a list to store AI and machine learning projects for the current agency
    ai_ml_projects = []

    # Initialize email content
    email_content = f"Projects related to AI, Machine Learning, and AI from {agency_name}:\n\n"
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

    # Add the number of AI and machine learning projects to the email content
    num_projects = len(ai_ml_projects)
    email_content += f"\nNumber of AI and machine learning projects from {agency_name}: {num_projects}\n"

    # Send the email
    send_email(f"AI and ML Projects - {agency_name}", email_content)

# List of agency URLs
agency_urls = {
    "DOD": "https://www.sbir.gov/api/awards.xml?agency=DOD",
    "HHS": "https://www.sbir.gov/api/awards.xml?agency=HHS",
    "NASA": "https://www.sbir.gov/api/awards.xml?agency=NASA",
    "NSF": "https://www.sbir.gov/api/awards.xml?agency=NSF",
    "DOE": "https://www.sbir.gov/api/awards.xml?agency=DOE",
    "USDA": "https://www.sbir.gov/api/awards.xml?agency=USDA",
    "EPA": "https://www.sbir.gov/api/awards.xml?agency=EPA",
    "DOC": "https://www.sbir.gov/api/awards.xml?agency=DOC",
    "ED": "https://www.sbir.gov/api/awards.xml?agency=ED",
    "DOT": "https://www.sbir.gov/api/awards.xml?agency=DOT",
    "DHS": "https://www.sbir.gov/api/awards.xml?agency=DHS"
}

# Fetch and process data for each agency
for agency, url in agency_urls.items():
    fetch_and_process_data(url, agency)
