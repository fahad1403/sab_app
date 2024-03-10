import re
# import streamlit as st
from datetime import datetime, timedelta
# import pandas as pd
# from google.cloud import translate_v2 as translate
from googletrans import Translator

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

def extract_vat_zakat_details(text):
    ## VAT/ZAKAT FORMAT 1
    print(f"\n\nDATA: {text}\n\n")
    vat_registration_number = re.search(r'\b\d{15}\b', text)
    cr_number = re.findall(r'\b\d{10}\b', text)
    tax_period = re.search(r'\b(quarterly|annually|monthly)\b', text, re.IGNORECASE)
    # taxpayer_name = re.search(r'VAT\s(.*?)\s\d{10}', text)
    taxpayer_name = re.search(r'(?:VAT\s(.*?)\s\d{10})|(?:\d{2}/\d{2}/\d{4}\s+(.*?)\s+\d{14})', text, re.MULTILINE)
   
    print(f"\n\nExtracted data: {text}\n\n")
    print(f"tax payer name: {taxpayer_name}")

    try:
        vat_registration_number = vat_registration_number.group(0) if vat_registration_number else None
    except:
        vat_registration_number = ''

    try:
        cr_number_result = [number for number in cr_number if not number.startswith(vat_registration_number[:10])]
        cr_number_result = list(set(cr_number_result))
        cr_number = cr_number_result[0]
    except:
        cr_number = ''

    try:
        date_pattern = r'(\d{4}/\d{2}/\d{2})'
        dates = re.findall(date_pattern, text)
        date_objects = [datetime.strptime(date, '%Y/%m/%d') for date in dates]
        sorted_dates = sorted(date_objects)
        sorted_dates_as_strings = [date.strftime('%Y/%m/%d') for date in sorted_dates]
        vat_registration_date = sorted_dates_as_strings[0]
        due_date = sorted_dates_as_strings[-1]

        if (sorted_dates[-1] - sorted_dates[0]) < timedelta(days=6*30):
            due_date = ''
    except:
        vat_registration_date, due_date = '', ''

    try:
        tax_period = tax_period.group(0) if tax_period else None
    except:
        tax_period = ''

    try:
        taxpayer_name = taxpayer_name.group(1) if taxpayer_name.group(1) else taxpayer_name.group(2)
    except:
        taxpayer_name = ''

    vat_zakat = {
        'vat_reg_date': vat_registration_date,
        'vat_exp_date': due_date,
        'vat_reg_number': vat_registration_number,
        'cr_number': cr_number,
        'tax_period': tax_period,
        'tax_payer_name': taxpayer_name
    }

    empty_count = sum(1 for value in vat_zakat.values() if not value)
    print(f"empty: {empty_count}")

    if empty_count >= 4:
        ## VAT/ZAKAT FORMAT 2 - NEW
        translator = Translator()
        translated_text = translator.translate(text, src='ar', dest='en').text

        vat_registration_number_new = re.search(r'\b\d{15}\b', translated_text)
        cr_number_new = re.findall(r'\b\d{10}\b', translated_text)
        tax_period_new = re.search(r'\b(quarterly|annually|monthly)\b', translated_text, re.IGNORECASE)
        taxpayer_name_new = re.search(r'(?:\|\sVAT\s(.*?)\s)|(?:taxpayer\s\/\s(.*?)company)', translated_text)
        dates = re.findall(r'(\d{2}/\d{2}/\d{4})', translated_text)

        print(f"tax payer name: {taxpayer_name_new}")

        try:
            vat_registration_number_new = vat_registration_number_new.group(0) if vat_registration_number_new else None
        except:
            vat_registration_number_new = ''
        
        try:
            cr_number_result = [number for number in cr_number_new if not number.startswith(vat_registration_number_new[:10])]
            cr_number_result = list(set(cr_number_result))
            cr_number_new = cr_number_result[0]
        except:
            try:
                arabic_numbers = []
                words = text.split()
                for word in words:
                    if any(char in '٠١٢٣٤٥٦٧٨٩' for char in word):
                        arabic_numbers.append(eastern_arabic_to_english(word))
                print(f"numbers: {arabic_numbers}")
                cr_number_new = arabic_numbers[-5].replace('/','1')
            except:
                cr_number_new = ''
            
        try:
            date_objects = [datetime.strptime(date, '%m/%d/%Y') for date in dates]
            sorted_dates = sorted(date_objects)
            sorted_dates_as_strings = [date.strftime('%m/%d/%Y') for date in sorted_dates]
            vat_registration_date_new = sorted_dates_as_strings[0]
            due_date_new = sorted_dates_as_strings[-1]
        except:
            vat_registration_date_new, due_date_new = '', ''

        try:
            tax_period_new = tax_period_new.group(0) if tax_period_new else None
        except:
            tax_period_new = ''
        
        try:
            taxpayer_name_new = taxpayer_name_new.group(0).replace('taxpayer / ','').replace(', company','') if taxpayer_name_new else None
        except:
            taxpayer_name_new = ''

        vat_zakat = {
        'vat_reg_date': vat_registration_date_new,
        'vat_exp_date': due_date_new,
        'vat_reg_number': vat_registration_number_new,
        'cr_number': cr_number_new,
        'tax_period': tax_period_new,
        'tax_payer_name': taxpayer_name_new
        }


    return vat_zakat
