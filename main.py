import streamlit as st
# from PyPDF2 import PdfReader
import requests
from google.cloud import vision
# from google.cloud import translate_v2 as translate
from googletrans import Translator
import os
import io
import fitz
from PIL import Image
import re
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import plotly.graph_objects as go
from constants import THM_RESPONSE, GDRIVE_CREDS, SCOPE, CONTRACT_JSON_DATA
import subprocess
import json
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import matplotlib.pyplot as plt
from rapidfuzz import fuzz
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
from id_upload import extract_id_details
from vat_zakat_page import extract_vat_zakat_details
from gosi_extraction import extract_business_gosi_data, extract_consumer_gosi_data
from admin_dash_merged import admin_dash
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from BanksExtractor import *
import random
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import tempfile
import mimetypes
from common import set_custom_css
# import numpy as np

# Define fixed credentials
USERNAME = "sab"
PASSWORD = "ekyb-sandbox"

st.set_page_config(layout="wide")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header{visibility:hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 0

# if 'admin_step' not in st.session_state:
#     st.session_state.admin_step = 0

# Define a function to check credentials
def check_credentials(username, password):
    return username == USERNAME and password == PASSWORD

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vision_creds.json"

def extract_text_from_pdf(pdf_file):
    client = vision.ImageAnnotatorClient()

    try:
        # Read the PDF file
        pdf_content = pdf_file.read()

        # Convert the PDF to a valid image format (e.g., PNG)
        pdf_document = fitz.open(stream=io.BytesIO(pdf_content))
        all_text = []

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()

            # Convert pixmap to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Save the PIL Image as bytes (PNG)
            with io.BytesIO() as output:
                img.save(output, format="PNG")
                image_bytes = output.getvalue()

            # Use Google Cloud Vision to extract text from the image
            image = vision.Image(content=image_bytes)
            response = client.text_detection(image=image)
            text_annotations = response.text_annotations

            if text_annotations:
                extracted_text = text_annotations[0].description
                all_text.append(extracted_text)

        return "\n".join(all_text)
    
    except Exception as e:
        print(e)
        return None


def translate_arabic_to_english(arabic_text):
    try:
        translator = Translator()
        translated_text = translator.translate(arabic_text, src='ar', dest='en').text
        return translated_text
    
    except Exception as e:
        print(e)

def twitter_scrape(business_name):
    # command1 = f"twscrape add_accounts accounts.txt username:password:email:email_password"
    # command2 = f"twscrape login_accounts"
    subprocess.call(['twscrape', 'add_accounts', 'accounts.txt', 'username:password:email:email_password'])
    subprocess.call(['twscrape', 'login_accounts'])

    # subprocess.run(command1)
    # subprocess.run(command2)

    business_name = str(business_name)
    start_date = "2023-08-01"
    end_date = "2023-08-29"

    command = 'twscrape search "%s since:%s until:%s" --raw' % (business_name, start_date, end_date)
    # command = f'twscrape search "{business_name} since:2023-08-01 until:2023-08-29" --raw'
    # command = f'twscrape search "nymcard since:2023-08-01 until:2023-08-29" --raw'

    print(f"running command: {command}")
    try:
        result = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
        )
        # print(result)
        stdout, stderr = result.communicate()

        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")

        try:
            response_json = json.loads(stdout)
            tweet_list = []

            for entry in response_json.get("data", {}).get("search_by_raw_query", {}).get("search_timeline", {}).get("timeline", {}).get("instructions", []):
                if "entries" in entry:
                    for tweet_entry in entry["entries"]:
                        if "content" in tweet_entry and "itemContent" in tweet_entry["content"]:
                            tweet_data = tweet_entry["content"]["itemContent"]["tweet_results"]["result"]
                            full_text = tweet_data.get("legacy").get("full_text")
                            if full_text:
                                tweet_list.append(full_text)
            return tweet_list

        except json.JSONDecodeError as e:
            return []

    except Exception as e:
        return []

def instagram_scrape(business_name):
    api_url = "https://www.page2api.com/api/v1/scrape"
    payload = {
        "api_key": "9f68d79174d4e7eced231f2c8ae305730322a732",
        "url": f"https://www.instagram.com/explore/tags/{business_name}/",
        "parse": {
        "posts": [
            {
            "_parent": "article a[role=link]",
            "image": "img >> src",
            "url": "_parent >> href",
            "title": "img >> alt"
            }
        ]
        },
        "premium_proxy": "us",
        "real_browser": True,
        "scenario": [
        { "wait_for": "article a[role=link]" },
        {
            "loop": [
            { "execute_js": "document.querySelector('#scrollview + div')?.remove();" },
            { "execute_js": "document.querySelectorAll('article a[role=link] img').forEach(e => e.scrollIntoView({behavior: 'smooth'}))" },
            { "wait": 1 }
            ],
            "iterations": 2
        },
        { "execute": "parse" }
        ]
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    result = json.loads(response.text)
    ig_posts = []

    print(result)
    if result.get('result'):
        print(result)
        if result.get('result').get('posts'):
            for post in result['result']['posts']:
                ig_posts.append(post['title'])
    
    return ig_posts

def google_reviews_scrape(business_name):
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": business_name,
        "key": "AIzaSyC3jF85Z6qgAEBwqwCdP8j_YM_XQcvEH-s",
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("status") == "OK":
            place_id = data["results"][0]["place_id"]

            reviews_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
            reviews_params = {
                "place_id": place_id,
                "fields": "reviews",
                "key": "AIzaSyC3jF85Z6qgAEBwqwCdP8j_YM_XQcvEH-s",
            }

            reviews_response = requests.get(reviews_endpoint, params=reviews_params)
            reviews_data = reviews_response.json()

            reviews = reviews_data.get("result", {}).get("reviews", [])
            print(f"reviews: {reviews}")
            extracted_reviews_list = []

            for item in reviews:
                extracted_reviews_list.append(item['text'])

            return extracted_reviews_list
        else:
            return []

    except Exception as e:
        return []

def analyze_sentiment_bert(text):
    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)
    input_ids = tokenizer.encode(text, add_special_tokens=True, truncation=True, padding=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(input_ids)
    logits = outputs.logits
    prob = torch.softmax(logits, dim=1)[0]
    sentiment = "Positive" if prob[1] > 0.5 else "Negative"
    return sentiment, float(prob[1])

def eastern_arabic_to_english(eastern_numeral):
    arabic_to_english_map = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
        '/': '/'
    }
    english_numeral = ''.join([arabic_to_english_map[char] for char in eastern_numeral if char in arabic_to_english_map])
    return english_numeral

def gcloud_translate(text, src='ar', dest='en'):
    translate_client = translate.Client.from_service_account_json('translate_creds.json')
    result = translate_client.translate(text, source_language=src, target_language=dest)
    return result['translatedText']

def check_admin_credentials(username, password):
    if username == "admin" and password == "admin":
        return True
    return False
st.markdown(
    """
    <style>
    .viewerBadgeContainer { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)
# Hide the "Made with Streamlit" footer
st.markdown(
    """
    <style>
    .viewerBadge { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

def login_page():
    set_custom_css()
#     # Apply the custom CSS styles
#     custom_css = """
#     <style>
#     .creds {
#     align:center;
#     color: #5e4fa2;
# }
# </style>
# """
    # logo_url='https://objectstorage.me-jeddah-1.oraclecloud.com/n/idcsprod/b/me-jeddah-idcs-1-9E6C09D36371AB1B7C12FA52FA120B95980D070A43765EF7F2A2F0B0F82948E6/o/images/202109131530/1631547034999/Alraedah-Logo-Landscape-2.jpg'
    # logo_url = "https://hala.com/assets/images/logos/logo.svg"
    logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/SABB_Bank_Logo.svg/1200px-SABB_Bank_Logo.svg.png"
    # st.markdown(custom_css, unsafe_allow_html=True)
  # Center the image dynamically based on screen width
    st.markdown(
    f"""
    <style>
    .center-image {{
        display: flex;
        justify-content: center;
    }}
    </style>
    <div class="center-image">
        <img src="{logo_url}" width="200" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)
# Create the styled title
    st.markdown('<h1 class="title">Login</h1>', unsafe_allow_html=True)
    # Use st.empty() to create placeholders for input fields and messages
    placeholder = st.empty()
   # Create a custom container for the login form with a background image
   
    st.markdown(
    """
    <div class="login" style="background-image: url('ekyb_background-image.jpg'); background-size: cover; background-attachment: fixed;">
        <div style="padding: 20px;">
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)  
    # tab1, tab2 = st.tabs(["User Login", "Admin Login"])
    # # active_tab = st.radio("Select an option", tabs)
    # with tab1:
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown('<h2 class="creds">Enter your Credentials</h2>', unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit and check_credentials(username, password):
        st.success("Login successful! Proceed to the CR verification screen.")
        st.session_state.step = 1
        st.session_state.login_page = True
        st.experimental_rerun()
    elif submit and not check_credentials(username, password):
        st.error("Login failed. Please check your credentials.")

    # with tab2:
    #     admin_placeholder = st.empty()
    #     with admin_placeholder.form("admin_login"):
    #         st.markdown('<h2 class="creds">Enter Admin Credentials</h2>', unsafe_allow_html=True)
    #         admin_username = st.text_input("Username")
    #         admin_password = st.text_input("Password", type="password")
    #         submit = st.form_submit_button("Login")

    #     if submit and check_admin_credentials(admin_username, admin_password):
    #         st.success("Admin Login successful! Redirecting to Admin Dashboard.")
    #         st.session_state.admin_step = 1
    #         st.session_state.admin_login_page = True
    #         st.experimental_rerun()
    #     elif submit and not check_admin_credentials(admin_username, admin_password):
    #         st.error("Admin Login failed. Please check your credentials.")

# # Login Page
# def login_page():
#     st.title("Login Page")
#     # Use st.empty() to create placeholders for input fields and messages
#     placeholder = st.empty()
#     with placeholder.form("login"):
#         st.markdown("#### Enter your credentials")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         submit = st.form_submit_button("Login")
    
#     if submit and check_credentials(username, password):
#         # placeholder.empty()
#         st.session_state.step = 0
#         st.success("Login successful! Proceed to the CR verification screen.")
        
#         st.session_state.login_page = True
    
#     elif submit and not check_credentials(username, password):
#         st.error("Login failed. Please check your credentials.")

steps = ["", "CR verification", "Contract Issuing", "VAT/Zakat", "Gosi", "ID Verification", "Simah", "Expense Analysis", "Web Analysis", "Address verification", "Social Checks ", "Fraud Analysis", "PEP & AML"]

def show_progress():
    progress_html = "<div style='display: flex; justify-content: space-between; align-items: left; width: 100%;'>"
    
    # Define the CSS media query to hide steps on small screens
    hide_on_small_screen = """
        @media (max-width: 768px) {
            .step {
                display: none;
            }
        }
    """

    progress_html += f"<style>{hide_on_small_screen}</style>"

    for i, step in enumerate(steps):
        checkpoint_style = "background-color: rgba(0, 255, 0, 0.6); font-size: 12px; padding: 2px;" if i <= st.session_state.step else ""
        if i > 0:
            progress_html += (
                f"<div class='step' style='flex: 1; text-align: center; color: #555555; font-size: 13.5px; padding: 7px;'>{step}</div>"
                f"<div style='display: flex; flex-direction: column; align-items: center;'>"
                f"<div style='width: 12px; height: 12px; background-color: #aaaaaa; border-radius: 50%; {checkpoint_style}'></div>"
                f"<div style='font-size: 12px; color: #555555;'>{i}</div>"
                f"</div>"
            )
        else:
            progress_html += f"<div style='flex: 1; text-align: center; align:left color: #555555; font-size: 13.5px; padding: 7px;'>{step}</div>"
    
    progress_html += "</div>"
    st.markdown(progress_html, unsafe_allow_html=True)

# Function to display a progress bar
def show_progress_bar():
    progress_value = st.session_state.step / (len(steps) - 1)  # Start from 0 and go to 1
    st.progress(progress_value)

def get_response_from_wathq(cr_number):
    url = f"https://api.wathq.sa/v5/commercialregistration/fullinfo/{cr_number}"
    headers = {
        'accept': 'application/json',
        'apiKey': 'hJVHxlkXtTD0SQlyVKqs67f4wvLYhIv1'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        print(f"\n\n Data: {data}")
        translator = Translator()
        wathq_parsed_response = {
            "cr_number": data["crNumber"],
            "business_name": translator.translate(data["crName"], src='ar', dest='en').text,
            "cr_expiry_date": data["expiryDate"],
            "business_owner_1": translator.translate(data["parties"][1]["name"], src='ar', dest='en').text,
            "owners_iaqama_id": data["parties"][1]["identity"]["id"],
            "address": translator.translate(data["address"]["general"]["address"], src='ar', dest='en').text
        }
        return data, wathq_parsed_response
    except Exception as e:
        print(e)
        return {}, {}

def smart_ocr_on_cr_doc(pdf_text1, pdf_text2):
    fields = {
        'cr_number': '',
        'business_name': '',
        'business_address': '',
        'business_owner_1': '',
        'business_owner_2': ''
    }

    cr_pattern = r'Commercial Registry:\s+(\d+)'
    business_name_pattern = r"(?<=company's (?:trade name|brand name) )([^C]+) Company"
    # business_name_pattern = r"(?<=trade name of the company is)([^C]+) Company"
    pattern = r'The trade name of the company is\s(.*?)\s\d{2}/\d{2}/\d{4}'
    business_owner_1_pattern = r'Managers([^0-9]+)'
    business_owner_2_pattern = r''
    expiry_date_pattern = r'certificate expires on (\d{2}/\d{2}/\d{4}).*?'
    location_pattern = r'company Head office:\s(.*?)\sP\.O\. Box'

    if pdf_text1 and pdf_text2:
        cr_match = re.search(cr_pattern, pdf_text1, re.IGNORECASE)
        business_name_match = re.search(f'{business_name_pattern}', pdf_text1)
        business_owner_1_match = re.search(business_owner_1_pattern, pdf_text2)
        expiry_date_match = re.search(expiry_date_pattern, pdf_text2)
        location_match = re.search(location_pattern, pdf_text2)

        if cr_match:
            cr_number = cr_match.group(1)
            fields['cr_number'] = cr_number
        
        if business_name_match:
            business_name = business_name_match.group(1) if business_name_match.group(1) else business_name_match.group(2)
            # business_name = business_name_match.group(1)
            fields['business_name'] = business_name
        
        if business_owner_1_match:
            business_owner_1 = business_owner_1_match.group(1)
            fields['business_owner_1'] = business_owner_1
        
        if expiry_date_match:
            hijri_date = expiry_date_match.group(1)
            print(f"date: {hijri_date}")
            fields['expiry_date_hijri'] = hijri_date
        
        if location_match:
            location = location_match.group(1)
            fields['location'] = location

    return fields

def verify_business_details(ocr_result, wathq_result):
    flag = True

    flag = ocr_result['cr_number'] == wathq_result['cr_number']
    flag = fuzzy_match_fields(ocr_result['business_name'], wathq_result['business_name'])
    flag = fuzzy_match_fields(ocr_result['business_owner_1'], wathq_result['business_owner_1'])
    print(f"Flag: {flag}")
    return flag

def upload_to_drive(data, file_name):
    credentials = Credentials.from_service_account_file('gdrive_creds.json')  # Replace with your JSON credentials
    drive_service = build('drive', 'v3', credentials=credentials)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(data)
        temp_file_path = temp_file.name

    # r_no = random.randint(10**9, 10**10 - 1)

    file_metadata = {
        'name': file_name
        }  # Replace with your folder ID
    
    mime_type, _ = mimetypes.guess_type(file_name)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    print(f"mime type: {mime_type}")

    media = MediaFileUpload(temp_file_path, mimetype=mime_type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    drive_service.permissions().create(
        fileId=file.get('id'),
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()

    return file.get('id')  

def cr_entry_page():
    st.session_state['gsheet_data'] = {}
    #global st.session_state['gsheet_data']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    st.session_state['gsheet_data']['Timestamp'] = timestamp
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">C/R - Verification</h1>',unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload a C/R Document(PDF only)", type=["pdf"])
    submit_button = st.button("Submit")

    if submit_button:
        if not pdf_file:
            st.error("Please upload a PDF document before submitting.")
        else:
            with st.spinner("Fetching data..."): 
                business_details_container = st.empty()
                pdf_text = extract_text_from_pdf(pdf_file)
                translated_pdf_text1 = translate_arabic_to_english(pdf_text)
                translated_pdf_text2 = gcloud_translate(pdf_text)
                # st.write(translated_pdf_text2)
                ocr_result = smart_ocr_on_cr_doc(translated_pdf_text1, translated_pdf_text2)
                st.session_state['gsheet_data']['CR_DATA'] = json.dumps(ocr_result)
                cr_number = ocr_result.get('cr_number')
                business_name = ocr_result.get('business_name')
                business_owner_1 = ocr_result.get('business_owner_1')
                expiry_date_hijri = ocr_result.get('expiry_date_hijri')
                location = ocr_result.get('location')

            non_optional_keys = ["cr_number", "business_name", "business_owner_1"]
            empty_string_keys = [key for key, value in ocr_result.items() if key in non_optional_keys and value == '']

            if empty_string_keys:
                st.error("Please upload a Valid CR Document PDF")
            else:
                uploaded_pdf_content = pdf_file.read()
                file_name = pdf_file.name
                file_id = upload_to_drive(uploaded_pdf_content, file_name)
                pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
                st.session_state['gsheet_data']['CR_PDF'] = pdf_file_url

                matches = re.findall(r'\w+\s+\w+', business_owner_1)
                if len(matches) >= 2:
                    result1 = matches[0]
                    result2 = matches[1]
                    business_owner_name = result1
                else:
                    business_owner_name = business_owner_1
                
                st.session_state.owner_name = business_owner_name
                st.session_state.cr_number = cr_number

                # Clear the previous business details
                business_details_container.empty()

                # Display the new business details
                with st.expander("Extracted Details from CR"):
                    st.write(f"CR Number: {cr_number}")
                    st.write(f"Business Name: {business_name}")
                    st.write(f"Business Owner: {business_owner_1}")
                    if expiry_date_hijri:
                        st.write(f"CR Expiry Date: {expiry_date_hijri}")
                    if location:
                        st.write(f"Business Address: {location}")
            
                with st.spinner("Verifying Details..."):
                    cr_number = ocr_result['cr_number']
                    raw_result, wathq_result = get_response_from_wathq(cr_number)
                    print(f"\n\nwathq result: {wathq_result}")
                    
                    if raw_result:
                        st.session_state['gsheet_data']['CR_DATA_WATHQ'] = json.dumps(raw_result)
                        with st.expander("Complete Verification"):
                            st.json(raw_result)
                    else:
                        st.session_state['gsheet_data']['CR_DATA_WATHQ'] = ''

                    print(f"\n\n1st: {st.session_state['gsheet_data']}\n")
                    if wathq_result:
                        if verify_business_details(ocr_result, wathq_result):
                            business_details_container.empty()
                            st.subheader("Verified Details")
                            st.success(f"CR Number: {cr_number} ✅")
                            st.success(f"Business Name: {business_name} ✅")
                            st.success(f"Business Owner: {business_owner_name} ✅")
                            if expiry_date_hijri:
                                st.success(f"CR Expiry Date: {expiry_date_hijri} ✅")
                            elif wathq_result.get('cr_expiry_date'):
                                st.success(f"CR Expiry Date: {wathq_result['cr_expiry_date']} ✅")
                            if location:
                                st.success(f"Business Address: {location} ✅")
                            elif wathq_result.get('address'):
                                st.success(f"Business Address: {wathq_result['address']} ✅")

                            st.session_state.next_button_enabled = True
                            st.session_state.step += 1

                        else:
                            st.subheader("Verification Failed")
                            st.error(f"CR Number: {cr_number} ❌")
                            st.error(f"Business Name: {business_name} ❌")
                            st.error(f"Business Owner: {business_owner_1} ❌")
                            st.error(f"CR Expiry Date: {expiry_date_hijri} ❌")
                            st.error(f"Business Address: {location} ❌")
                            
                    else:
                        st.subheader("Verified Details")
                        st.success(f"CR Number: {cr_number} ✅")
                        st.success(f"Business Name: {business_name} ✅")
                        st.success(f"Business Owner: {business_owner_name} ✅")
                        if expiry_date_hijri:
                            st.success(f"CR Expiry Date: {expiry_date_hijri} ✅")
                        elif wathq_result.get('cr_expiry_date'):
                            st.success(f"CR Expiry Date: {wathq_result['cr_expiry_date']} ✅")
                        if location:
                            st.success(f"Business Address: {location} ✅")
                        elif wathq_result.get('address'):
                            st.success(f"Business Address: {wathq_result['address']} ✅")
                        
                        st.session_state.next_button_enabled = True
                        st.session_state.next_page = "wathq_contract"

                        st.session_state.next_button_enabled = True
                        st.session_state.step += 1

            if st.session_state.get("next_button_enabled"):
                if st.button("Next"):
                    print(f"step: {st.session_state.step}")
            # st.session_state.next_page = "similar_web_page"

def generate_wathq_contract_data(complete_data):
    filled_data = json.loads(CONTRACT_JSON_DATA)
    import random
    # Mapping contract data
    filled_data["contract"]["basicInfo"]["contractNumber"] = str(random.randint(10**9, 10**10 - 1))
    filled_data["contract"]["basicInfo"]["contractCopyNumber"] = str(random.randint(10**9, 10**10 - 1))
    filled_data["contract"]["basicInfo"]["establishmentDate"] = complete_data["company"]["startDate"]  # Mapping establishmentDate from company startDate
    filled_data["contract"]["basicInfo"]["companyAddress"] = complete_data["address"]["general"]["address"]
    filled_data["contract"]["crInfo"]["crNo"] = str(complete_data["crNumber"])
    filled_data["contract"]["crInfo"]["companyFullName"] = complete_data["crName"]
    filled_data["contract"]["companyForm"]["companyFormDescriptionAr"] = complete_data["businessType"]["name"]
    filled_data["contract"]["activities"][0]["activityDescriptionAr"] = complete_data["activities"]["isic"][0]["name"]

    # Mapping company capital data
    filled_data["contract"]["companyCapital"]["capital"] = complete_data["capital"]["paidAmount"]
    filled_data["contract"]["companyCapital"]["cashCapital"] = complete_data["capital"]["paidAmount"]
    filled_data["contract"]["companyCapital"]["totalCashContribution"] = complete_data["capital"]["paidAmount"]
    filled_data["contract"]["companyCapital"]["contributionValue"] = complete_data["capital"]["share"]["sharesCount"]

    # Mapping partners data
    # for i, partner in enumerate(complete_data["parties"]):
    # print(f"i val: {i}")
    partner = complete_data["parties"][1]
    filled_data["partners"]["individualsPartners"][0]["partnerBasicInfo"] = {}
    filled_data["partners"]["individualsPartners"][0]["partnerBasicInfo"]["identifierNo"] = partner["identity"]["id"]
    filled_data["partners"]["individualsPartners"][0]["partnerBasicInfo"]["birthDate"] = partner.get("birthDate")
    filled_data["partners"]["individualsPartners"][0]["partnerBasicInfo"]["firstNameAr"] = partner["name"]
    filled_data["partners"]["individualsPartners"][0]["partnerBasicInfo"]["genderDescriptionAr"] = partner["relation"]["name"]
    filled_data["partners"]["individualsPartners"][0]["partnerBasicInfo"]["nationalityDescriptionAr"] = partner["nationality"]["name"]

    # Mapping managers data
    # for i, manager in enumerate(complete_data["parties"]):
    # if manager["relation"]["name"] == "مدير":
    filled_data["managers"][0]["managerBasicInfo"]["identifierNo"] = partner["identity"]["id"]
    filled_data["managers"][0]["managerBasicInfo"]["birthDate"] = partner.get("birthDate")
    filled_data["managers"][0]["managerBasicInfo"]["firstNameAr"] = partner["name"]
    filled_data["managers"][0]["managerBasicInfo"]["genderDescriptionAr"] = partner["relation"]["name"]
    filled_data["managers"][0]["managerBasicInfo"]["nationalityDescriptionAr"] = partner["nationality"]["name"]

    # Convert the filled data back to JSON
    filled_json_result = json.dumps(filled_data, indent=4, ensure_ascii=False)

    # Printing the filled JSON
    print(filled_json_result)

    return filled_json_result

def wathq_contract_issuing():
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Contract Issuing - Wathq</h1>',unsafe_allow_html=True)
    cr_number = st.session_state.get('cr_number')
    cr_number = st.text_input("CR Number", cr_number)
    submit_button = st.button("Get Results")
    
    if submit_button:
        with st.spinner(f"Fetching data for {cr_number} ..."):
            time.sleep(2)
            wathq_data = st.session_state['gsheet_data'].get('CR_DATA_WATHQ')
            wathq_data = json.loads(wathq_data)
            wathq_contract_data = generate_wathq_contract_data(wathq_data)

            with st.expander("Wathq Contract Verification", expanded=True):
                st.json(wathq_contract_data)
        
                st.session_state.next_button_enabled = True
                st.session_state.next_page = "vat_page"

                st.session_state.next_button_enabled = True
                st.session_state.step += 1

            if st.session_state.get("next_button_enabled"):
                if st.button("Next"):
                    print(f"step: {st.session_state.step}")

def vat_zakat_page():
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Zakat/VAT - Verification</h1>',unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload a VAT/Zakat Document(PDF only)", type=["pdf"])
    submit_button = st.button("Submit")

    if submit_button:
        if not pdf_file:
            st.error("Please upload a PDF document before submitting.")
        else:
            with st.spinner("Reading ZAKAT/VAT Document..."):
                pdf_text = extract_text_from_pdf(pdf_file)
                ocr_result = extract_vat_zakat_details(pdf_text)
                st.session_state['gsheet_data']['VAT_Data'] = json.dumps(ocr_result)

                uploaded_pdf_content = pdf_file.read()
                file_name = pdf_file.name  # Get the file name
                file_id = upload_to_drive(uploaded_pdf_content, file_name)
                pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
                st.session_state['gsheet_data']['VAT_PDF'] = pdf_file_url

                print(f"\n\n2nd: {st.session_state['gsheet_data']}")

                with st.expander("Extracted Details from Zakat/VAT"):
                    df = pd.DataFrame([ocr_result])
                    st.write(df)
                
                st.session_state.next_button_enabled = True
                st.session_state.next_page = "gosi_page"

                st.session_state.next_button_enabled = True
                st.session_state.step += 1

            if st.session_state.get("next_button_enabled"):
                if st.button("Next"):
                    print(f"step: {st.session_state.step}")

def business_gosi_page():
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">GOSI Data Verification</h1>',unsafe_allow_html=True)
    gosi_type = st.selectbox("Select GOSI Type", ("Business GOSI", "Customer/Personal GOSI"))

    if gosi_type == "Business GOSI":
        pdf_file = st.file_uploader("Upload Business GOSI Document(PDF only)", type=["pdf"])
        submit_button = st.button("Submit")

        if submit_button:
            if not pdf_file:
                st.error("Please upload a PDF document before submitting.")
            else:
                with st.spinner("Reading GOSI Document..."):
                    pdf_text = extract_text_from_pdf(pdf_file)
                    ocr_result = extract_business_gosi_data(pdf_text)
                    st.session_state['gsheet_data']['BUSINESS_GOSI_Data'] = json.dumps(ocr_result)

                    uploaded_pdf_content = pdf_file.read()
                    file_name = pdf_file.name  # Get the file name
                    file_id = upload_to_drive(uploaded_pdf_content, file_name)
                    pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
                    st.session_state['gsheet_data']['BUSINESS_GOSI_PDF'] = pdf_file_url

                    st.session_state['gsheet_data']['CUSTOMER_GOSI_Data'] = json.dumps(ocr_result)
                    st.session_state['gsheet_data']['CUSTOMER_GOSI_Data'] = pdf_file_url

                    print(f"\n\n3rd: {st.session_state['gsheet_data']}")

                    with st.expander("Extracted Details from GOSI Document"):
                        df = pd.DataFrame([ocr_result])
                        st.write(df)
                    
                    st.session_state.next_button_enabled = True
                    st.session_state.next_page = "consumer_gosi"

                    st.session_state.next_button_enabled = True
                    st.session_state.step += 1

                if st.session_state.get("next_button_enabled"):
                    if st.button("Next"):
                        print(f"step: {st.session_state.step}")

    elif gosi_type == "Customer/Personal GOSI":
        pdf_file = st.file_uploader("Upload Customer's GOSI Document(PDF only)", type=["pdf"])
        submit_button = st.button("Submit")

        if submit_button:
            if not pdf_file:
                st.error("Please upload a PDF document before submitting.")
            else:
                with st.spinner("Reading GOSI Document..."):
                    pdf_text = extract_text_from_pdf(pdf_file)
                    ocr_result = extract_consumer_gosi_data(pdf_text)
                    st.session_state['gsheet_data']['BUSINESS_GOSI_Data'] = json.dumps(ocr_result)
                    

                    uploaded_pdf_content = pdf_file.read()
                    file_name = pdf_file.name  # Get the file name
                    file_id = upload_to_drive(uploaded_pdf_content, file_name)
                    pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
                    st.session_state['gsheet_data']['BUSINESS_GOSI_PDF'] = pdf_file_url

                    st.session_state['gsheet_data']['CUSTOMER_GOSI_Data'] = json.dumps(ocr_result)
                    st.session_state['gsheet_data']['CUSTOMER_GOSI_PDF'] = pdf_file_url

                    print(f"\n\n3rd: {st.session_state['gsheet_data']}")
                    with st.expander("Extracted Details from GOSI Document"):
                        df = pd.DataFrame([ocr_result])
                        st.write(df)
                    
                    st.session_state.next_button_enabled = True
                    st.session_state.next_page = "idv_page"

                    st.session_state.next_button_enabled = True
                    st.session_state.step += 1

                if st.session_state.get("next_button_enabled"):
                    if st.button("Next"):
                        print(f"step: {st.session_state.step}")

def display_details_in_table(details, id_number):
    df = pd.DataFrame(details, index=[f"ID{id_number}"])
    st.table(df)  

def idv_page():
    #global st.session_state['gsheet_data']
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Business Stakeholders Verification</h1>',unsafe_allow_html=True)
    uploaded_ids = []
    image_id_urls = []

    st.header("Upload IDs")
    num_ids_to_upload = st.number_input("How many IDs do you want to upload? (1-3)", 1, 3, 1)

    for i in range(num_ids_to_upload):
        uploaded_id = st.file_uploader(f"Upload National ID {i+1}", type=["jpg", "png"])

        if uploaded_id:
            uploaded_id_content = uploaded_id.read()

            with st.spinner("Fetching data..."):
                extracted_details = extract_id_details(uploaded_id_content)
                uploaded_ids.append(extracted_details)

            file_name = uploaded_id.name  # Get the file name
            file_id = upload_to_drive(uploaded_id_content, file_name)
            file_url = f"https://drive.google.com/uc?id={file_id}"
            image_id_urls.append(file_url)

    if hasattr(st.session_state, 'owner_name'):
        matching_name = st.session_state.owner_name

    name_matched = any(fuzzy_match_fields(id_data.get("Name", ""), matching_name) >= 70 for id_data in uploaded_ids)

    flag = False
    with st.expander("Extracted Details"):
        for i, id_data in enumerate(uploaded_ids, start=1):
            st.subheader(f"Details from ID {i}")
            display_details_in_table(id_data, i)
            flag = True

            # Check if the extracted name matches business owner name using fuzzy matching
            name = id_data.get("Name", "")
            id_number = id_data.get("ID Number", "")

            st.session_state.id_name = name
            st.session_state.id_number = id_number

            similarity = fuzzy_match_fields(name, matching_name)

            if similarity >= 70:
                st.success("ID verified")
            else:
                st.warning(f"Please Upload ID of {matching_name}")

    # Display the warning message outside the expander
    if not name_matched:
        st.warning(f"Please Upload ID of {matching_name}")

    # Only display the "Next" button if the name matches business owner name

    # st.session_state.next_button_enabled = name_matched
    st.session_state.next_button_enabled = flag        

    # Display the "Next" button below the expander
    if st.session_state.get("next_button_enabled"):
        id_data_json = ", ".join([json.dumps(data) for data in uploaded_ids])
        id_image_combined = ', '.join(image_id_urls)

        st.session_state['gsheet_data']['ID_Data'] = id_data_json
        st.session_state['gsheet_data']['ID_Image'] = id_image_combined
        print(f"\n\n3rd: {st.session_state['gsheet_data']}")
        st.session_state.step += 1
        if st.button("Next"):
            # Set the next page to "similar_web_page" (you can change this as needed)
             print(f"step: {st.session_state.step}")

def simah_page():
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Simah Verification</h1>',unsafe_allow_html=True)

    active_product_summary_df = pd.DataFrame({
        "Product Type": ["Loan","Credit Card","Mobile No."],
        "Creditor": ["*****","*****","*****"],
        "Account Number": ["0000759****","0000759****","0000759****"],
        "Installment Amount": ["472,309.00","175,000.00","3,988.00"],
        "Credit Limit": ["42,309.00","15,000.00","5,000.00"],
        "Outstanding Balance": ["20,000.00","5000.00","1,000.00"],
        "Last Reported": ["16/6/2011","6/7/2012","14/12/2013"],
        "Payment Status": ["Current","Overdue","Current"]
    })

    default_product_summary_df = pd.DataFrame({
        "Product Type": ["Loan","Credit Card","Mobile No."],
        "Creditor": ["*****","*****","*****"],
        "Account Number": ["0000759****","0000759****","0000759****"],
        "Date Reported": ["16/6/2011","6/7/2012","14/12/2013"],
        "Total Default Amount": ["42,309.00","15,000.00","5,000.00"],
        "Outstanding Default": ["0.00","5,000.00","1,000.00"],
        "Default Status": ["Fully Paid","*****","*****"],
        "Settlement Date": ["4/9/2012","",""]
    })

    active_product_loan_df1 = pd.DataFrame({
        "Account Number ": ["30***** "],
        "Date of Issuance": ["25/12/2014"],
        "Credit limit": ["10,300.00 "],
        "Installment Number": ["24"],
        "Installment Amount": ["700"],
        "Payment Frequency": ["Monthly"],
        "Type of Guarantee": ["Cash"],
        "Expiry Date": ["25/12/2014"]
    })
    active_product_loan_df2 = pd.DataFrame({
        "Outstanding Balance": ["10,300.00"],
        "Past Due Balance": ["0.00"],
        "Last Amount Paid": ["0.00"],
        "Last payment Date": ["25/12/2014"],
        "Next Due Date": ["25/12/2014"],
        "As Of Date ": ["25/12/2014"],
        "Salary Assignment": ["No"],
        "Closed Date": ["4/9/2012"]
    })
    credit_card_default_product_df1 = pd.DataFrame({
        "Account Number ": ["30***** "],
        "Date of Issuance": ["25/12/2014"],
        "Credit limit": ["10,300.00 "],
        "Installment Number": ["24"],
        "Installment Amount": ["700"],
        "Payment Frequency": ["Monthly"],
        "Type of Guarantee": ["Cash"],
        "Expiry Date": ["25/12/2014"]
    })
    credit_card_default_product_df2 = pd.DataFrame({
        "Outstanding Balance": ["10,300.00"],
        "Past Due Balance": ["0.00"],
        "Last Amount Paid": ["0.00"],
        "Last payment Date": ["25/12/2014"],
        "Next Due Date": ["25/12/2014"],
        "As Of Date ": ["25/12/2014"],
        "Salary Assignment": ["No"],
        "Closed Date": ["4/9/2012"]
    })
    if st.button("Get Simah Report"):
        id_name = ""
        if hasattr(st.session_state, 'id_name'):
            id_number = st.session_state.id_number
            id_name = st.session_state.id_name
            id_name = f"for {id_name.lower()}"

        with st.spinner(f"Getting Simah Report {id_name}..."):
                time.sleep(3)
        with st.spinner("Generating Results..."):
                time.sleep(2)
        with st.expander("Simah Report", expanded=True):
            st.info(f"Person Name: {id_name}\tId number: {id_number}")
            with st.container():
                    st.markdown("<h4 style='color: #3498db;'>Active Product Summary</h4>", unsafe_allow_html=True)
                    st.dataframe(active_product_summary_df)

            with st.container():
                    st.markdown("<h4 style='color: #3498db;'>Default Product Summary</h4>", unsafe_allow_html=True)
                    st.dataframe(default_product_summary_df)

            with st.container():
                    st.markdown("<h4 style='color: #3498db;'>Active Product Loan</h4>", unsafe_allow_html=True)
                    st.dataframe(active_product_loan_df1)
                    st.dataframe(active_product_loan_df2)
                
            with st.container():
                    st.markdown("<h4 style='color:#3498db;'>Credit Card Default Product</h4>", unsafe_allow_html=True)
                    st.dataframe(credit_card_default_product_df1)
                    st.dataframe(credit_card_default_product_df2)
            
        st.session_state.next_button_enabled = True
        # st.session_state.next_page = "idv_page"
        st.session_state.step += 1

        if st.session_state.get("next_button_enabled"):
            if st.button("Next"):
                print(f"step: {st.session_state.step}")


def analyze_bank_statement(pdf_file):
    pdf_bytes = pdf_file.read()
    extractor = BankExtractor()
    result, expense_result = extractor.extract(pdf_bytes=pdf_bytes)
    
    return result, expense_result

def expense_benchmarking_page():
    #global st.session_state['gsheet_data']
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Revenue/Cash Flow Analysis</h1>',unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Bank Statement (PDF only)", type=["pdf"])
    
    if st.button("Submit"):
        if uploaded_file is not None:
            with st.spinner("Reading Bank Statement..."):
                data, expense_category_data = analyze_bank_statement(uploaded_file)
                if not data:
                    st.error("We do not support this bank statement format yet.")
                else:
                    uploaded_pdf_content = uploaded_file.read()
                    file_name = uploaded_file.name  # Get the file name
                    file_id = upload_to_drive(uploaded_pdf_content, file_name)
                    pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
                    st.session_state['gsheet_data']['BANK_STATEMENT'] = pdf_file_url

                    with st.spinner("Analyzing Results..."):
                        # st.write(f"Expense categories: {expense_data}")
                        
                        months = []
                        rev_values = []
                        exp_values = []
                        cash_flow_values = []

                        if 'rev_by_month' in data:
                            rev_data = data['rev_by_month']
                            months = list(rev_data.keys())
                            rev_values = [rev_data[month] for month in months]
                            if data.get('Revenue'):
                                data['Revenue'] = data['Revenue'].abs()
                        
                        if 'exp_by_month' in data:
                            exp_data = data['exp_by_month']
                            months = list(exp_data.keys())
                            exp_values = [abs(exp_data[month]) for month in months]
                            if data.get('Expense'):
                                data['Expense'] = data['Expense'].abs()
                        
                        if 'free cash flows' in data:
                            cash_flow_data = data['free cash flows']
                            cash_flow_values = [cash_flow_data[month] for month in months]
                            if data.get('Free Cash Flow'):
                                data['Free Cash Flow'] = data['Free Cash Flow']

                        max_len = max(len(rev_values), len(exp_values), len(cash_flow_values))
            
                        rev_values.extend([0] * (max_len - len(rev_values)))
                        exp_values.extend([0] * (max_len - len(exp_values)))
                        cash_flow_values.extend([0] * (max_len - len(cash_flow_values)))

                        # Create a DataFrame with default values
                        expense_data = {
                            'Month': months,
                            'Revenue': rev_values,
                            'Expense': exp_values,
                            'Free Cash Flow': cash_flow_values
                        }

                        st.session_state['gsheet_data']['Expense_Data'] = json.dumps(expense_data)
                        print(f"\n\n4th: {st.session_state['gsheet_data']}\n")
                        data = pd.DataFrame(expense_data)

                        # Filter out rows with missing data
                        data = data.dropna()
                        
                
                        with st.expander("View Month-wise Results"):
                            html_table = data.to_html(index=False, header=True)
                            st.markdown(f'<style>table {{ width: 100%; margin-bottom: 10px; }}</style>', unsafe_allow_html=True)
                            st.markdown(html_table, unsafe_allow_html=True)
                            # st.write(data)

                        hover_template = '<b>%{y}</b><br>Negative: -%{customdata}' if data['Free Cash Flow'].min() < 0 else '<b>%{y}</b>'

                        tab1, tab2 = st.tabs(["Expense/Revenue", "Categorization"])

                        with tab1:
                            fig = px.bar(data, x='Month', y=['Revenue', 'Expense', 'Free Cash Flow'],
                                title='Monthly Revenue, Expense, and Free Cash Flow Analysis',
                                barmode='relative', color_discrete_map={'Free Cash Flow': 'rgba(220,0,0,0.5)',
                                                                        'Expense': 'rgba(102,51,153,0.5)',
                                                                        'Revenue': 'rgba(182, 208, 226,0.8)'})

                            fig.update_layout(
                                xaxis=dict(showgrid=False),
                                yaxis=dict(showgrid=False),
                                plot_bgcolor='white',
                                # width=950,
                                # height=700,
                                # margin=dict(l=400),
                            )

                            fig.update_traces(marker=dict(color=['rgba(0,215,0,0.65)' if val >= 0 else 'rgba(250,0,0,0.5)' for val in data['Free Cash Flow']]),
                            selector=dict(name='Free Cash Flow'))
                            # Define a minimum height for the chart (adjust this value as needed)
                            min_chart_height = 800  # You can change this value
                            # Use use_container_width=True for automatic width adjustment
                            st.plotly_chart(fig, use_container_width=True, use_container_height=False, height=min_chart_height)

                        with tab2:
                            expense_category_data = json.loads(expense_category_data)
                            categories = [item["category"] for item in expense_category_data["expenses"]]
                            amounts = [item["amount"] for item in expense_category_data["expenses"]]
                            percentages = [item["percentage"] for item in expense_category_data["expenses"]]

                            # Generating dynamic colors list with transparency
                            colors = []
                            for i in range(len(categories)):
                                color = "rgba(" + str(random.randint(0, 255)) + "," + str(random.randint(0, 255)) + "," + str(random.randint(0, 255)) + ",0.4)"
                                colors.append(color)

                            # Creating a Plotly donut chart
                            fig1 = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=0.5, marker=dict(colors=colors))])
                            fig1.update_layout(title_text="Expense Categorization", margin=dict(l=50))
                            st.plotly_chart(fig1, use_container_width=True, use_container_height=False, height=min_chart_height)

                        st.session_state.next_button_enabled = True
                        st.session_state.step += 1

                    if st.session_state.get("next_button_enabled"):
                        if st.button("Next"):
                            print(f"step: {st.session_state.step}")
        else:
            st.error("Please upload a Bank statement PDF before submitting.")

def verify_address(address):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    api_key = "AIzaSyC3jF85Z6qgAEBwqwCdP8j_YM_XQcvEH-s"

    params = {
        "address": address,
        "key": api_key,
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        if response.status_code == 200:
            if data['status'] == 'OK':
                return data
            else:
                return False
        else:
            return False
    
    except Exception as e:
        return False

def check_address_length(address):
    split_by_space = address.split()

    result = [item.split(',') for item in split_by_space]

    return len(result) >= 5

def get_google_search_results(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None

def get_company_address(company_name):
    company_name = company_name.lower().strip()
    print(f"company: {company_name}")
    search_query1 = f"{company_name} saudi address"
    search_query2 = f"{company_name} dubai address"
    search_results1 = get_google_search_results(search_query1)
    print(f"len 1: {len(search_results1)}")
    search_results2 = get_google_search_results(search_query2)
    print(f"len 2: {len(search_results2)}")

    if search_results1:
        soup = BeautifulSoup(search_results1, "html.parser")
        address = soup.find("div", {"class": "sXLaOe"})
        if address:
            address = address.get_text()
            print(f"addr1: {address}")
            return address
        else:
            try:
                soup = BeautifulSoup(search_results2, "html.parser")
                address = soup.find("div", {"class": "sXLaOe"}).get_text()
                print(f"addr2: {address}")
                return address
            except:
                return None    
    else:
        try:
            soup = BeautifulSoup(search_results2, "html.parser")
            address = soup.find("div", {"class": "sXLaOe"}).get_text()
            print(f"addr2: {address}")
            return address
        except AttributeError:
            return None

def fuzzy_match_fields(field1, field2, threshold=70):
    similarity = fuzz.partial_ratio(field1, field2)
    print(similarity)
    return similarity >= threshold

def check_address_from_google(company_name, company_address):
    google_address = get_company_address(company_name)
    print(f"address: {google_address}")
    if google_address:
        if fuzzy_match_fields(company_address.lower(), google_address.lower()):
            return True, google_address
        else:
            return False, ''
    else:
        return False, ''

def address_verification_page():
    #global st.session_state['gsheet_data']
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Address Verification</h1>',unsafe_allow_html=True)

    address = st.text_input("Enter address of the business", placeholder="Eg. Al Salam Tecom Tower, Dubai Media City, UAE")
    address_dict = {
        'user_address': address,
    }

    if st.button("Submit"):
        if address and check_address_length(address):
            is_address_verified = False
            is_address_valid = False

            data = verify_address(address)
            if data:
                if hasattr(st.session_state, 'company_name'):
                    company_name = st.session_state.company_name
                    company_name = company_name.lower()
                    with st.spinner(f"checking {company_name}'s address on google"):
                        google_address_result, address = check_address_from_google(company_name, address)
                        address_dict['google_address'] = address
                        st.session_state['gsheet_data']['Address'] = json.dumps(address_dict)
                        is_address_valid = google_address_result

                country_name = data['results'][0]['address_components'][-1]['short_name']
                if country_name == 'SA' or country_name == 'AE':
                    is_address_verified = True
        
            if is_address_verified or is_address_valid:
                st.success("Address verification   ✅")
                st.success("Address validation     ✅")

                st.session_state.next_button_enabled = True
                st.session_state.step += 1
                # st.session_state.next_page = "sentiment_scrape"

                if st.button("Next"):
                    print(f"step: {st.session_state.step}")
            else:
                st.error("Address verification Failed    ❌")
                st.error("Address validation Failed      ❌")
                st.write("Please Re-enter full address of the Company")
        else:
            st.error("Please enter complete Address before submitting")   

def verify_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_company_name(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')

            if title_tag:
                company_name = title_tag.text.strip()
                return True, company_name

        else:
            pattern = r'https://|www\.|\.com|\.sa|\.ae|en'
            cleaned_url = re.sub(pattern, '', url).strip('/')
            parts = cleaned_url.split('/')
            if parts:
                keyword = parts[-1]
                return True, keyword
            else:
                return False, ""
    
    except Exception as e:
        pattern = r'https://|www\.|\.com|\.sa|\.ae|en'
        cleaned_url = re.sub(pattern, '', url).strip('/')
        parts = cleaned_url.split('/')
        if parts:
            keyword = parts[-1]
            return True, keyword
        else:
            return False, ""

def generate_fake_similar_web_data(WEB_ANALYSIS_DATA, WEB_AVERAGE_DURATION_DATA):
    traffic_data, duration_data = WEB_ANALYSIS_DATA, WEB_AVERAGE_DURATION_DATA

    traffic_dates = [entry["date"] for entry in traffic_data]
    avg_traffic = [entry["traffic"] for entry in traffic_data]

    duration_dates = [entry["date"] for entry in duration_data]
    avg_duration = [entry["average_visit_duration"] for entry in duration_data]

    # st.set_page_config(layout="wide")
    tab1, tab2, tab3 = st.tabs(["Traffic", "Bounce Rate", "Demographics"])

    with tab1:
        # Create the first chart for average traffic month-wise
        fig1 = px.bar(
            x=traffic_dates,
            y=avg_traffic,
            labels={'x':'Date', 'y':'Average Traffic'},
            title='Average Traffic Month-wise',
        )

        fig1.update_layout(
            xaxis=dict(showgrid=False, gridwidth=1, title_font=dict(size=12)),
            yaxis=dict(showgrid=False, gridwidth=1, range=[500, 1500], title_font=dict(size=12)),
            plot_bgcolor='white',
            font=dict(size=12),
            # width=950,
            # height=700,
            # margin=dict(l=350),
        )
        fig1.update_traces(marker_color='rgba(102,51,153,0.5)')
        st.plotly_chart(fig1, use_container_width=True, use_container_height=True)
        #  # Use use_container_width=True for automatic width and height adjustment
        # st.plotly_chart(fig1, use_container_width=True, use_container_height=True)
        # # Custom CSS for centering the chart on small screens
        # st.markdown("""
        # <style>
        #     @media (max-width: 768px) {
        #         .stPlotlyChart {
        #             margin: 0 auto;
        #         }
        #     }
        # </style>
        # """, unsafe_allow_html=True)

    with tab2:
        # Create the second chart for average visit duration
        fig2 = px.bar(
            x=duration_dates,
            y=avg_duration,
            labels={'x':'Date', 'y':'Bounce Rate'},
            title='Bounce Rate Month-wise',
        )

        fig2.update_layout(
            xaxis=dict(showgrid=False, gridwidth=1, title_font=dict(size=12)),
            yaxis=dict(showgrid=False, gridwidth=1, range=[0, 80], title_font=dict(size=12)),
            plot_bgcolor='white',
            font=dict(size=12),
            # width=950,
            # height=700,
            # margin=dict(l=350),
        )
        fig2.update_traces(marker_color='rgba(182, 208, 226,0.8)')  # The last value (0.5) controls transparency
        
        st.plotly_chart(fig2,use_container_width=True,user_container_height=True)
    
    with tab3:
        gender_data = np.random.choice(['Male', 'Female'], size=1000)
        gender_labels, gender_counts = np.unique(gender_data, return_counts=True)

        # Calculate the number of samples needed for each age range
        total_samples = 100  # Total number of samples
        samples_18_27 = int(0.20 * total_samples)  # 20% for 18-27
        samples_28_37 = int(0.30 * total_samples)  # 30% for 28-37
        samples_38_47 = int(0.15 * total_samples)  # 15% for 38-47
        samples_48_57 = int(0.15 * total_samples)  # 15% for 48-57
        samples_58_67 = total_samples - samples_18_27 - samples_28_37 - samples_38_47 - samples_48_57

        # Generate random data for the age distribution graph
        age_data = np.concatenate([
            np.random.randint(18, 28, size=samples_18_27),
            np.random.randint(28, 38, size=samples_28_37),
            np.random.randint(38, 48, size=samples_38_47),
            np.random.randint(48, 58, size=samples_48_57),
            np.random.randint(58, 68, size=samples_58_67)
        ])

        # Create age bins and calculate the age distribution
        age_bins = [18, 28, 38, 48, 58, 68]
        age_labels = [f'{i} - {i+9}' for i in range(20, 60, 10)]
        age_counts, _ = np.histogram(age_data, bins=age_bins)
        age_percentage = age_counts / age_counts.sum() * 100

        # Create a bar chart for age distribution with y-axis from 0 to 100
        fig_age = go.Figure(data=[go.Bar(x=age_labels, y=age_percentage)])
        fig_age.update_layout(title='Age Distribution (Percentage)',yaxis=dict(range=[0, 100]))
        fig_age.update_traces(marker=dict(color='rgba(0, 0, 220, 0.6)'))

        # Create two columns layout
        col1, col2 = st.columns(2)

        # Display the age distribution bar chart in the first column
        col1.plotly_chart(fig_age,use_container_width=True,user_container_height=True)

        # Display the gender distribution pie chart in the second column
        fig_gender = go.Figure(data=[go.Pie(labels=gender_labels, values=gender_counts)])
        fig_gender.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig_gender.update_layout(title='Gender Distribution')

        col2.plotly_chart(fig_gender,use_container_width=True,user_container_height=True)


def save_data_to_sheet(url, timestamp, traffic_data, duration_data, sheet):
    traffic_json = json.dumps(traffic_data)
    duration_json = json.dumps(duration_data)
    data = [url, timestamp, traffic_json, duration_json]
    sheet.append_row(data)

def get_data_from_sheet(url, sheet):
    data = sheet.get_all_values()
    for row in data:
        if row[0] == url:
            timestamp, traffic_json, duration_json = row[1], row[2], row[3]
            traffic_data = json.loads(traffic_json)
            duration_data = json.loads(duration_json)
            
            return timestamp, traffic_data, duration_data
    return None, None, None

def similar_web_page():
    #global st.session_state['gsheet_data']
    show_progress_bar()
    show_progress()
    set_custom_css()
    scope = SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_dict(GDRIVE_CREDS, scope)
    client = gspread.authorize(creds)
    sheet = client.open("streamlit_data").worksheet('similar_web_data')

    st.markdown('<h1 class="title">Web Traffic Analysis</h1>',unsafe_allow_html=True)
    company_url = st.text_input("Enter Business Url: ", placeholder="Eg. https://nymcard.com")
    st.session_state['gsheet_data']['Company_Url'] = company_url
    submit_button = st.button("Submit")
    
    if company_url and submit_button:
        if verify_url(company_url):
            with st.spinner("Checking url..."):
                time.sleep(1)
            status, company_name = extract_company_name(company_url)
            st.session_state['gsheet_data']['Company_Name'] = company_name
            if status:
                with st.spinner("Fetching Results..."):
                    st.session_state.company_url = company_url
                    st.session_state.company_name = company_name
                    api_key = '8522d7f391074950a906f0ee4c77268d'
                    api_url = f'https://api.similarweb.com/v5/website/{company_url}/total-traffic-and-engagement/visits?api_key={api_key}&start_date=2023-01&end_date=2023-08&country=sa&granularity=monthly&main_domain_only=false&format=json&show_verified=false&mtd=false&engaged_only=false'
                    try:
                        response = requests.get(api_url)
                        if response.status_code == 200:
                            data = response.json()
                            # Check if data for the same URL exists in the sheet
                            saved_timestamp, saved_traffic_data, saved_duration_data = get_data_from_sheet(company_url, sheet)
                            if saved_timestamp:
                                print("Using saved data from the sheet")
                                # Use saved data
                                timestamp = saved_timestamp
                                traffic_data = saved_traffic_data
                                duration_data = saved_duration_data
                            else:
                                # Generate fake data if not found and save it to the sheet
                                timestamp = str(datetime.now())
                                traffic_data = generate_fake_traffic_data()
                                duration_data = generate_fake_duration_data()
                                save_data_to_sheet(company_url, timestamp, traffic_data, duration_data, sheet)
                            st.write(data)

                        else:
                            saved_timestamp, saved_traffic_data, saved_duration_data = get_data_from_sheet(company_url, sheet)
                            if saved_timestamp:
                                print("Using saved data from the sheet")
                                # Use saved data
                                timestamp = saved_timestamp
                                traffic_data = saved_traffic_data
                                duration_data = saved_duration_data
                                generate_fake_similar_web_data(traffic_data, duration_data)
                            else:
                                # Generate fake data if not found and save it to the sheet
                                timestamp = str(datetime.now())
                                traffic_data = generate_fake_traffic_data()
                                duration_data = generate_fake_duration_data()
                                save_data_to_sheet(company_url, timestamp, traffic_data, duration_data, sheet)
                                generate_fake_similar_web_data(traffic_data, duration_data)

                        st.session_state.next_button_enabled = True
                        st.session_state.step += 1
                        # st.session_state.next_page = "address_verification_page"
                        if st.session_state.get("next_button_enabled"):
                            if st.button("Next"):
                                print(f"step: {st.session_state.step}")

                    except Exception as e:
                        saved_timestamp, saved_traffic_data, saved_duration_data = get_data_from_sheet(company_url, sheet)
                        if saved_timestamp:
                            print("Using saved data from the sheet")
                            # Use saved data
                            timestamp = saved_timestamp
                            traffic_data = saved_traffic_data
                            duration_data = saved_duration_data
                            generate_fake_similar_web_data(traffic_data, duration_data)
                        else:
                            # Generate fake data if not found and save it to the sheet
                            timestamp = str(datetime.now())
                            traffic_data = generate_fake_traffic_data()
                            duration_data = generate_fake_duration_data()
                            save_data_to_sheet(company_url, timestamp, traffic_data, duration_data, sheet)
                            generate_fake_similar_web_data(traffic_data, duration_data)
                    
                        st.session_state.next_button_enabled = True
                        st.session_state.step += 1
                        # st.session_state.next_page = "address_verification_page"
                        if st.session_state.get("next_button_enabled"):
                            if st.button("Next"):
                                print(f"step: {st.session_state.step}")

            else:
                st.error("Please enter a valid URL")
        else:
            st.error("Please enter a complete valid URL of the company")
    elif submit_button and not company_url:
        st.error("Please enter a URL of the company before submitting")

# Call this function to generate fake traffic data
def generate_fake_traffic_data():
    traffic_dates = pd.date_range(start="2023-01-01", end="2023-08-01", freq="MS")
    traffic_data = [{"date": str(date), "traffic": random.uniform(1000, 1500)} for date in traffic_dates]
    return traffic_data

# Call this function to generate fake duration data
def generate_fake_duration_data():
    duration_dates = pd.date_range(start="2023-01-01", end="2023-08-01", freq="MS")
    duration_data = [{"date": str(date), "average_visit_duration": f"{round(random.uniform(0, 30),2)}%"} for date in duration_dates]
    return duration_data


def render_progress_bar(value):
    progress_bar = f"""
    <style>
    @media screen and (max-width: 768px) {{
        .progress-container {{
            width: 100%;
        }}
        .progress-bar {{
            width: {value}%;
            font-size: 10px;
        }}
    }}
    </style>
    """
    # A custom HTML/CSS implementation of a progress bar
    progress_bar = f"""
    <div style="width: 100%; background-color: #f0f0f0; height: 14px; border-radius: 10px;">
        <div style="width: {value}%; background-color: #00cc00; height: 100%; border-radius: 10px; font-size:12px; text-align: center; color: white;">
            {value}%
        </div>
    </div>
    """
    return progress_bar

def calculate_overall_sentiment(prob1, prob2, prob3):
    # Calculate the average probability
    avg_prob = (prob1 + prob2 + prob3) / 3
    # Determine the overall sentiment based on the average probability
    overall_sentiment = "Positive" if avg_prob > 0.5 else "Negative"
    return avg_prob, overall_sentiment

def sentiment_scrape():
    #global st.session_state['gsheet_data']
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Social Check Result</h1>',unsafe_allow_html=True)

    if st.button("Get Analysis"):
        if hasattr(st.session_state, 'company_url'):
            company_url = st.session_state.company_url
            
        if hasattr(st.session_state, 'company_name'):
            company_name = st.session_state.company_name
            company_name = company_name.lower().replace("for ","").strip()
            st.write(f"Getting Results for {company_name}")
            
            scrapes = {}
            sentiments = {}

            # tweet_list = twitter_scrape(company_name)
            # ig_post_list = instagram_scrape(str(company_name))
            # google_reviews_list = google_reviews_scrape(company_name)

            # if company_name=='nymcard':
            ig_post_list = [
                "Visa And NymCard Launch Plug & Play End-To-End Issuance Platform To Help #Fintech swiftly launch payment credentials as part of Visa’ Ready To Launch (VRTL) program Read more 🌐 : https://technologyplus.pk/2023/08/28/visa-and-nymcard-launch-plug-play-end-to-end-issuance-platform-to-help-fintech/ Follow on FB 👍 : https://lnkd.in/diKN5pSG . . . . . . . . . . Visa NymCard #Visa #NymCard Umar S. Khan Omar Onsi #BusinessAdministration #education #educationalcontent #educationconsultant #petrol_price_in_Pakistan #today_petrol_rate_in_pakistan_2023 #diesel_price_in_Pakistan",
                "Explore NymCard’s Dubai office, a perfect reflection of their innovative and ambitious nature. The contemporary design promotes collaboration and creativity, while sustainable materials and natural light enhance well-being. Located in a prestigious location, this inspiring workspace embodies NymCard’s dedication to revolutionising the fintech industry. Photocredits: @chrisgoldstraw #JTCPLDesigns_HTSInteriors #OfficeDesigners #UAEArchitecture #UAEDesigners #Design #JTCPLDesigns #OfficeDesign #JTCPL_interiors #Modern #OfficeInteriors #WorkPlace #OfficeDecor #Minimal #Bespokelnteriors #InteriorDetails #InteriorForInspo #InteriorDesire #NymCard #ModernRetro #Finance #DubaiOffice",
                "The new office of NymCard is a testament to the company's commitment to innovation and excellence. The workspace provides a practical and inspiring environment that encourages collaboration and productivity. Attention to detail is evident in every aspect, from the layout to the materials used. This office reflects NymCard’s values and vision, focusing on both functionality and aesthetics. Overall, it's a workspace that truly embodies the brand's identity. Photocredits: @chrisgoldstraw #JTCPLDesigns_HTSInteriors #OfficeDesigners #UAEArchitecture #UAEDesigners #Design #JTCPLDesigns #OfficeDesign #JTCPL_interiors #Modern #OfficeInteriors #WorkPlace #OfficeDecor #Minimal #Bespokelnteriors #InteriorDetails #InteriorForInspo #InteriorDesire #NymCard #ModernRetro #Finance #DubaiOffice",
                "Step into NymCard’s Dubai office, featuring distinct areas for meetings, collaboration, and focus. The modern crisp white open ceiling is complemented by retro cork cladding motifs and pastel stretched fabric panels that also serve as acoustic treatments. The space seamlessly blends aesthetics and functionality, providing an ideal workspace for the team. Photocredits: @chrisgoldstraw #JTCPLDesigns_HTSInteriors #OfficeDesigners #UAEArchitecture #UAEDesigners #Design #JTCPLDesigns #OfficeDesign #JTCPL_interiors #Modern #OfficeInteriors #WorkPlace #OfficeDecor #Minimal #Bespokelnteriors #InteriorDetails #InteriorForInspo #InteriorDesire #NymCard #ModernRetro #Finance #DubaiOffice",
                "@nymcard Acquires @spotiime To Offer BNPL-in-a-Box For Banks and Financial Institutions NymCard, the leading payments infrastructure provider in the MENA region, has completed the acquisition of Spotii, a prominent Buy Now Pay Later (BNPL) Fintech operating in key markets including KSA, UAE, and Bahrain. #nymcard #spotii #bnpl #fintechs #financialservices #financialinclusion #bankingnews #bankingindustry #digitaltransformation #digitalpayment #servicesasabusiness #digitalplatform #dailynewspk #news",
                "Visa And NymCard Launch Plug & Play End-To-End Issuance Platform To Help #Fintech swiftly launch payment credentials as part of Visa’ Ready To Launch (VRTL) program Read more 🌐 : https://technologyplus.pk/2023/08/28/visa-and-nymcard-launch-plug-play-end-to-end-issuance-platform-to-help-fintech/ Follow on FB 👍 : https://lnkd.in/diKN5pSG . . . . . . . . . . Visa NymCard #Visa #NymCard Umar S. Khan Omar Onsi #BusinessAdministration #education #educationalcontent #educationconsultant #petrol_price_in_Pakistan #today_petrol_rate_in_pakistan_2023 #diesel_price_in_Pakistan",
                "Dollar East Exchange Company (Private) Limited and United Bank Limited (UBL) recently signed a Memorandum of Understanding (MOU). Read more 🌐 : https://technologyplus.pk/2023/09/01/ubl-and-dollar-east-exchange-extend-their-strategic-partnership/ Follow on FB 👍 : https://lnkd.in/diKN5pSG . . . . . . . . . . UBL - United Bank Limited Dollar East Exchange Company #fintech #partnership #collaboration #reallife #transactional #growth #DigiKhata #KuudnaPakistan #Fintech #FintechNews #Visa #NymCard #BusinessAdministration #education #educationalcontent #educationconsultant #petrol_price_in_Pakistan #today_petrol_rate_in_pakistan_2023 #diesel_price_in_Pakistan",
                "The goal was to create a workspace that fosters creativity, productivity, and embodies the NymCard brand ethos. The result is a workspace featuring bespoke niches and curves that enhance collaboration and efficiency in designated activity zones. Photocredits: @chrisgoldstraw #JTCPLDesigns_HTSInteriors #OfficeDesigners #UAEArchitecture #UAEDesigners #Design #JTCPLDesigns #OfficeDesign #JTCPL_interiors #Modern #OfficeInteriors #WorkPlace #OfficeDecor #Minimal #Bespokelnteriors #InteriorDetails #InteriorForInspo #InteriorDesire #NymCard #ModernRetro #Finance #DubaiOffice",
                "NymCard’s Dubai office: where innovation meets inspiration. The space reflects the brand's creative identity with pastel highlights, layered design, and distinct areas for various activities. It's the perfect workspace for one of the UAE's fastest-growing fintech companies to celebrate success. Photocredits: @chrisgoldstraw #JTCPLDesigns_HTSInteriors #OfficeDesigners #UAEArchitecture #UAEDesigners #Design #JTCPLDesigns #OfficeDesign #JTCPL_interiors #Modern #OfficeInteriors #WorkPlace #OfficeDecor #Minimal #Bespokelnteriors #InteriorDetails #InteriorForInspo #InteriorDesire #NymCard #ModernRetro #Finance #DubaiOffice"
            ]

            tweet_list = [
                "NymCard joins Visa’s Ready To Launch program https://t.co/HTzaaIAbZE \n@Visa \n#pakistanbanks\n#creditcardsinpakistan",
                "#Dubai @Visa @VisaNews #digitalpayments #Visa #VisaReadyToLaunch #VRTL #fintech #NymCard #seamless #payment @NymCard #bank @BCWGlobal \n\nhttps://t.co/Z0nR6WDL4U",
                "We're thrilled to announce that we're Golden Sponsors of Seamless KSA, coming up on the 4th - 5th of Sept! Come meet our team and discover how NymCard can help banks and financial institutions fast-track digital transformation.\n#SeamlessKSA #bankingasaservice #saudiarabia https://t.co/YDzimiH8Dw",
                "We’re excited to announce @NymCard as Seamless Saudi Arabia Gold Sponsor 🎉 \n\nFind them at stand D52 on 4 - 5 September on the #SeamlessKSA expo floor! Have you got your free expo ticket yet? \n\nRegister now and we’ll see you there: https://t.co/gxLbQestA8 https://t.co/fTVUl5ckLP",
                "🤖 We asked ChatGPT for the most imaginative use cases for Buy-Now-Pay-Later (BNPL) and here's what it revealed! \n\nLearn about NymCard's white-label BNPL: https://t.co/teGSEYQSrG\n\n#BNPL #FinancialInnovation #NymCard #FinancialFreedom #UAE52 #TodayForTomorrow #paymentsmadesimple https://t.co/AGJk36JC6o",
                "BNPL Report: June 19 – China BNPL boom, retail #BNPL merchant tips, NymCard grabs Spotti, Sipay buys Sileon, credit reports, Klarna donations tool, Singapore regs, Affirm investment appeal? #fintech #banking https://t.co/cws8LZXwGV https://t.co/oscDDqv3WR"
            ]

            google_reviews_list = ["", "", ""]
            
            ig_post_list = ig_post_list[:3]
            tweet_list = tweet_list[:3]
            
            # if str(company_name).lower()=='alraedah':
            #     tweet_list = ['#Alraedah #Finance signs an agreement with Saudi Kuwaiti Finance House https://t.co/sxaXrp7KaH https://t.co/UnOZmGZhWj', 'Alraedah Finance and Saudi Kuwaiti Finance House (SKFH) signed a strategic agreement to establish a closed-ended investment fund which aims to invest SAR 300 million to support SMEs\nhttps://t.co/9krf5YJMls\n@AlRaedahFinance \n#economy #intlbm #investment #products #sustainable https://t.co/Ya0mho8N2E', 'Alraedah Finance signs an agreement with Saudi Kuwaiti Finance House - ZAWYA https://t.co/NKQaoYmoLs', '#روضة_بداية_الرائدة \n#العودة_للدارسة \n#العودة_للدراسة https://t.co/ccrHY8myPX']
            
            print(f"tweet list: {tweet_list}\nig_post list : {ig_post_list}")

            max_len = max(len(tweet_list), len(ig_post_list), len(google_reviews_list))
            
            tweet_list.extend([''] * (max_len - len(tweet_list)))
            ig_post_list.extend([''] * (max_len - len(ig_post_list)))
            google_reviews_list.extend([''] * (max_len - len(google_reviews_list)))

            print(f"tweet list updated: {tweet_list}\nig_post list updated: {ig_post_list}")

            scrapes['Twitter'] = tweet_list
            scrapes['Instagram'] = ig_post_list
            scrapes['Google'] = google_reviews_list

            st.session_state['gsheet_data']['Social_Check'] = json.dumps(scrapes)

            data = {}
            # if any(item.strip() for item in tweet_list):
            data['Twitter'] = tweet_list

            # if any(item.strip() for item in ig_post_list):
            data['Instagram'] = ig_post_list
            
            # if any(item.strip() for item in google_reviews_list):
            data['Google Reviews'] = google_reviews_list

            with st.expander(f"Extracted Data for {company_name}"):
                df = pd.DataFrame(data)
                html_table = df.to_html(index=False, header=True)
                st.markdown(html_table, unsafe_allow_html=True)

            all_tweet_texts = " ".join(tweet_list)
            sentiment, prob1 = analyze_sentiment_bert(all_tweet_texts)

            all_ig_texts = " ".join(ig_post_list)
            sentiment, prob2 = analyze_sentiment_bert(all_ig_texts)

            all_gr_texts = " ".join(google_reviews_list)
            sentiment, prob3 = analyze_sentiment_bert(all_gr_texts)

            avg_prob, overall_sentiment = calculate_overall_sentiment(prob1, prob2, prob3)

            sentiments['Twitter'] = prob1
            sentiments['Instagram'] = prob2
            sentiments['Google'] = prob3
            sentiments['Average'] = avg_prob

            st.session_state['gsheet_data']['Sentiments'] = json.dumps(sentiments)

            fig = make_subplots(rows=4, cols=1, subplot_titles=("Overall Sentiment", "Tweets", "Instagram", "Google Reviews"))

            progress_bar_html = render_progress_bar(int(avg_prob * 100))
            st.components.v1.html(progress_bar_html, height=21)
            fig.add_trace(go.Scatter(x=[1], y=[1], text="", mode="text", hoverinfo="none", showlegend=False), row=1, col=1)

            # Add text labels for "Positive" and "Negative" along with their numbers (increase font size)
            fig.add_annotation(
            text=f"<b>Positive:</b> {int(avg_prob * 100)}%",
            xref="paper", yref="paper",
            x=0.5, y=0.95,
            showarrow=False,
            font=dict(size=17, color="green")
            )
            fig.add_annotation(
                text=f"<b>Negative:</b> {int((1 - avg_prob) * 100)+1}%",
                xref="paper", yref="paper",
                x=0.5, y=0.90,
                showarrow=False,
                font=dict(size=17, color="red")
            )  

            fig.update_xaxes(showticklabels=False, showgrid=False, row=1, col=1)
            fig.update_yaxes(showticklabels=False, showgrid=False, row=1, col=1)

            # Plot 2: Tweets Sentiment
            labels_tweets = ["Positive", "Negative"]
            values_tweets = [prob1, 1 - prob1]
            fig.add_trace(go.Bar(x=labels_tweets, y=values_tweets, showlegend=False, marker=dict(color=['rgba(0, 128, 0, 0.5)', 'rgba(255, 0, 0, 0.5)'])), row=2, col=1)

            # Plot 3: Instagram Sentiment
            ig_labels = ["Positive", "Negative"]
            ig_values = [prob2, 1 - prob2]
            fig.add_trace(go.Bar(x=ig_labels, y=ig_values, showlegend=False, marker=dict(color=['rgba(0, 128, 0, 0.5)', 'rgba(255, 0, 0, 0.5)'])), row=3, col=1)

            # Plot 4: Google Reviews Sentiment
            gr_labels = ["Positive", "Negative"]
            gr_values = [prob3, 1 - prob3]
            fig.add_trace(go.Bar(x=gr_labels, y=gr_values, showlegend=False, marker=dict(color=['rgba(0, 128, 0, 0.5)', 'rgba(255, 0, 0, 0.5)'])), row=4, col=1)

            # Update subplot layout
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)

            # fig.update_layout(title="Sentiment Distribution")
            # min_height=700
            fig.update_layout(title="Sentiment Distribution",height=700,margin=dict(l=20, r=20, t=60, b=30))
            st.plotly_chart(fig, use_container_width=True, use_container_height=True)
            # st.plotly_chart(fig, use_container_width=True, use_container_height=False,height=min_height)

            st.session_state.next_button_enabled = True
            st.session_state.step += 1
            # st.session_state.next_page = "address_verification_page"
            if st.session_state.get("next_button_enabled"):
                if st.button("Next"):
                    print(f"step: {st.session_state.step}")

def thm_verification():
    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">Fraud Analysis</h1>',unsafe_allow_html=True)
    if st.button("Get Analysis"):
        with st.spinner("Identifying Device.."):
            time.sleep(1)

        with st.spinner("Fetching Results..."):
            time.sleep(1)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Device Fingerprint")
            st.write("Device ID:", THM_RESPONSE["device_fingerprint"]["device_id"])  # Display the device ID
            st.write("")
            st.write("")
        
        with col2:
            st.subheader("Identity Verification")
            st.write("User Behavior Match:", THM_RESPONSE["identity_verification"]["user_behavior_match"])
            st.write("Identity Verified:", THM_RESPONSE["identity_verification"]["identity_verified"])

        with col1:
            st.subheader("Geolocation")
            st.write("Country:", THM_RESPONSE["geolocation"]["country"])
            st.write("Latitude:", THM_RESPONSE["geolocation"]["latitude"])
            st.write("Longitude:", THM_RESPONSE["geolocation"]["longitude"])

        with col2:
            st.subheader("Bot Detection")
            st.write("Is Bot:", THM_RESPONSE["bot_detection"]["is_bot"])

        st.session_state.next_button_enabled = True
        st.session_state.step += 1
        # st.session_state.next_page = "address_verification_page"
        if st.session_state.get("next_button_enabled"):
            if st.button("Next"):
                print(f"step: {st.session_state.step}")

def world_check():

    show_progress_bar()
    show_progress()
    set_custom_css()
    st.markdown('<h1 class="title">AML/PEP/Sanctions Screening</h1>',unsafe_allow_html=True)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(GDRIVE_CREDS, SCOPE)
    client = gspread.authorize(creds)
    gsheet = client.open("streamlit_data").worksheet('flow_data')
    print(st.session_state['gsheet_data'])
    # gsheet.append_row(list(st.session_state['gsheet_data'].values()), value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS', table_range="A1")
    st.session_state['gsheet_data'] = {}

    company_name = ""
    if hasattr(st.session_state, 'company_name'):
        company_name = st.session_state.company_name
        company_name = company_name.lower()
        
    if st.button("Get Results"):
        with st.spinner(f"Extracting Results for {company_name}.."):
            time.sleep(2)

        time.sleep(2)

        col1, col2 = st.columns(2)
        with col1:
            st.success("AML ✅")
            st.success("PEP ✅")
            st.success("Sanctions ✅")

            # if st.button('Back to CR page'):
            #     st.session_state.admin_step = 1
            #     st.session_state.login_page = True

def add_repayment_method_page():
    repayment_dict = {}
    set_custom_css()
    st.markdown('<h1 class="title">Add Repayment Method</h1>',unsafe_allow_html=True)
    st.markdown('<span style="text-align:center;">We accept any debit/credit card</span>',unsafe_allow_html=True)
    with st.form("repayment_form"):
        card_number = st.text_input("Card Number", placeholder="0000 0000 0000 0000")
        card_number_validation = None
        exp_input = st.text_input("Expiration (MM//YY)",placeholder="MM/YY")
        exp_validation = None
        cvv_input = st.text_input("CVV", placeholder="123", type="password")
        cvv_validation = None
        confirm = st.form_submit_button("Confirm Details")
    if confirm:
        card_number = card_number.replace(" ", "")
        if not card_number.isdigit() or len(card_number) != 16:
            card_number_validation = "Card number must have exactly 16 digits ."
        if not re.match(r'^\d{2}/\d{2}$', exp_input):
            exp_validation = "Please enter the expiration in the format MM/YY."
        else:
            month, year = exp_input.split('/')
            current_year = datetime.now().year
            if not (1 <= int(month) <= 12):
                exp_validation = "The month should be between 1 and 12."
            elif int(year) < current_year % 100:
                exp_validation = "This card is expired,Please use a Valid card."
        if not cvv_input.isdigit() or len(cvv_input) != 3:
            cvv_validation = "CVV must be a 3-digit number."
    if card_number_validation:
        st.error(card_number_validation)

    if exp_validation:
        st.error(exp_validation)

    if cvv_validation:
        st.error(cvv_validation)
    # Disable "Confirm Details" button if any field does not meet the desired format
    if card_number_validation or exp_validation or cvv_validation:
        st.write("Please correct the errors before submitting.")
        confirm = False
    else:
        confirm=True

        if confirm and card_number and exp_input and cvv_input:
            st.session_state.step_business += 1
            repayment_dict['card_number'] = card_number
            repayment_dict['expiration'] = exp_input
            repayment_dict['cvv'] = cvv_input
            st.session_state['gsheet_data']['repayment'] = repayment_dict
            print(f"\nUpdated dict: {st.session_state['gsheet_data']}")
            st.experimental_rerun()

        elif confirm and (not card_number or not exp_input or not cvv_input):
            st.error("Please Complete All Details Before Submitting")

# if st.session_state.admin_step == 1:
#     st.session_state.login_page = True
#     st.session_state.step=15
    # admin_dash()

if 'login_page' not in st.session_state:
    login_page()
elif st.session_state.step == 1:
    cr_entry_page()
elif st.session_state.step == 2:
    wathq_contract_issuing()
elif st.session_state.step == 3:
    vat_zakat_page()
elif st.session_state.step == 4:
    business_gosi_page()
# elif st.session_state.step == 5:
#     consumer_gosi_page()
elif st.session_state.step == 5:
    idv_page()
elif st.session_state.step == 6:
    simah_page()
elif st.session_state.step == 7:
    expense_benchmarking_page()
elif st.session_state.step == 8:
    similar_web_page()
elif st.session_state.step == 9:
    address_verification_page()
elif st.session_state.step ==10:
    sentiment_scrape()
elif st.session_state.step == 11:
    thm_verification()
elif st.session_state.step == 12:
    world_check()
# elif st.session_state.step == 15:
#     admin_dash()
