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
from constants import THM_RESPONSE, GDRIVE_CREDS, SCOPE, CONTRACT_JSON_DATA
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import tempfile
import mimetypes

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

def gcloud_translate(text, src='ar', dest='en'):
    translate_client = translate.Client.from_service_account_json('translate_creds.json')
    result = translate_client.translate(text, source_language=src, target_language=dest)
    return result['translatedText']

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
