from google.cloud import vision
import os
import io
from PIL import Image
import fitz
import re
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from hijri_converter import convert
# from google.cloud import translate_v2 as translate
from collections import OrderedDict
from googletrans import Translator

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vision_creds.json"

    
def eastern_arabic_to_english(eastern_numeral):
    arabic_to_english_map = {
        '٠': '0', '۰': '0',
        '١': '1', '۱': '1',
        '٢': '2', '۲': '2',
        '٣': '3', '۳': '3',
        '٤': '4', '۴': '4',
        '٥': '5', '۵': '5',
        '٦': '6', '۶': '6',
        '٧': '7', '۷': '7',
        '٨': '8', '۸': '8',
        '٩': '9', '۹': '9',
        '/': '/'
    }

    # If the character is an Eastern Arabic numeral, convert it to English; otherwise, keep it unchanged.
    english_numeral = ''.join([arabic_to_english_map[char] if char in arabic_to_english_map else char for char in eastern_numeral])
    
    return english_numeral

def replace_persian_with_english(text):
    persian_to_english_digits = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3',
        '۴': '4', '۵': '5', '۶': '6', '۷': '7',
        '۸': '8', '۹': '9'
    }
    
    return ''.join(persian_to_english_digits.get(char, char) for char in text)


def persian_to_gregorian(persian_date):
    try:
        # Replace Persian numbers with English numbers
        persian_date = replace_persian_with_english(persian_date)

        # Split the Persian date
        year, month, day = map(int, persian_date.split('/'))

        # Convert the Persian date to Gregorian
        gregorian_date = JalaliDate(year, month, day).to_gregorian()

        # Format the result as a string
        return f"{gregorian_date.year:04d}/{gregorian_date.month:02d}/{gregorian_date.day:02d}"
    except:
        return persian_date
    
def hijri_to_gregorian(hijri_date):
    try:
        # Split the hijri date
        year, month, day = map(int, hijri_date.split('/'))

        # Convert the hijri date to Gregorian
        gregorian_date = convert.Hijri(year, month, day).to_gregorian()
        
    # Format the result as a string
        return f"{gregorian_date.year}/{gregorian_date.month:02}/{gregorian_date.day:02}"
    except:
        return hijri_date

def extract_business_gosi_data(text):
    # translate_client = translate.Client.from_service_account_json('translate_creds.json')
    # translated_text = translate_client.translate(text, source_language='ar', target_language='en')
    # translated_text = translated_text['translatedText']

    translator = Translator()
    translated_text = translator.translate(text, src='ar', dest='en').text

    arabic_dates = []
    arabic_numbers = []

    # Regular expression to identify Arabic dates and Arabic numerals in the specified formats
    arabic_date_pattern = r'(\d{4}/\d{1,2}/\d{1,2}|[۰-۹]{4}/[۰-۹]{1,2}/[۰-۹]{1,2})'

    words = text.split()
    for word in words:
        if re.match(arabic_date_pattern, word):  # Check if the word matches the Arabic date pattern
            english_date = eastern_arabic_to_english(word)
            date = hijri_to_gregorian(english_date)
            date_object = datetime.strptime(date, '%Y/%m/%d')
            # Convert the datetime object to the desired format
            formatted_date = date_object.strftime('%d/%m/%Y')
            # arabic_dates.append(word)
            arabic_dates.append(formatted_date)
        elif any(char in '٠١٢٣٤٥٦٧٨٩' for char in word):  # Check if the word contains Arabic numerals
            arabic_numbers.append(eastern_arabic_to_english(word))

    try:
        expiry_date = arabic_dates[0]
    except:
        expiry_date = ''
    
    try:
        issue_date = arabic_dates[1]
    except:
        issue_date = ''

    try:
        cr_number = arabic_numbers[0]
    except:
        cr_number = ''
    
    company_name_match = re.search(r'establishment:\s(.*?)\sCompany', translated_text)

    if company_name_match:
        company_name = company_name_match.group(1)
    else:
        company_name = ''
    
    gosi_business_data = {
        'gosi_issue_date': issue_date,
        'gosi_expiry_date': expiry_date,
        'cr_number': cr_number,
        'company_name': company_name
    }

    return gosi_business_data

def extract_consumer_gosi_data(text):
    # translate_client = translate.Client.from_service_account_json('translate_creds.json')
    # translated_text = translate_client.translate(text, source_language='ar', target_language='en')
    # translated_text = translated_text['translatedText']

    translator = Translator()
    translated_text = translator.translate(text, src='ar', dest='en').text

    arabic_dates = []
    arabic_numbers = []
    numbers = []

    # Regular expression to identify Arabic dates and Arabic numerals in the specified formats
    arabic_date_pattern = r'(\d{4}/\d{1,2}/\d{1,2}|[۰-۹]{4}/[۰-۹]{1,2}/[۰-۹]{1,2})'

    words = text.split()
    for word in words:
        if re.match(arabic_date_pattern, word):  # Check if the word matches the Arabic date pattern
            date = eastern_arabic_to_english(word)
            arabic_dates.append(date)
        elif any(char in '٠١٢٣٤٥٦٧٨٩' for char in word):  # Check if the word contains Arabic numerals
            numbers.append(word)
            arabic_numbers.append(eastern_arabic_to_english(word))
    
    print()
    print(numbers)
    print()
    print(arabic_dates)
    print()
    print(arabic_numbers)

    try:
        pattern = r'(?:establishment\s*:\s*([^\d]+))|(?:establishment\s*([^\d]+))'
        matches = re.findall(pattern, translated_text, re.IGNORECASE)
        company_list = [item for tup in matches for item in tup if item.strip()]
        print(company_list)
    except:
        company_list = []
    
    try:
        person_name_pattern = r'Social Insurance(?:\sfor\s\w+)?(.*?)(?:\d+)?\sEmployer number'
        person_name_match = re.search(person_name_pattern, translated_text, re.IGNORECASE)
        person_name = person_name_match.group(1).strip()
        person_name = re.sub(r'(subscriber number|\d+|General Organization for Social Insurance|Employer number|for the|name of the)', '', person_name, flags=re.IGNORECASE)
        person_name = person_name.strip()
    except:
        person_name = ''

    try:
        id_numbers = re.findall(r'\b\d{8}\b|\b\d{9}\b|\b\d{10}\b', translated_text)
        result = list(OrderedDict.fromkeys(id_numbers))
        national_id_number = result[-1]
        subscriber_number = result[0]
        last_employer_id_no = result[1]
    except:
        national_id_number, subscriber_number, last_employer_id_no = '', '', ''
    
    try:
        date_objects = [datetime.strptime(date, '%Y/%m/%d') for date in arabic_dates]
        date_objects.sort()
        dob = date_objects[0]
        dob = dob.strftime('%Y/%m/%d')
        dob = hijri_to_gregorian(dob)
    except:
        dob = ''

    try:
        company = company_list[-1]
    except:
        company = ''

    gosi_consumer_data = {
        'person_name': person_name,
        'subscriber_number': subscriber_number,
        'id_number': national_id_number,
        'dob': dob,
        'last_employer': company,
        'last_employer_id': last_employer_id_no
    }

    return gosi_consumer_data
