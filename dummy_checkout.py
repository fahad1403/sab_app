import streamlit as st
import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
import json
from vat_zakat_page import extract_vat_zakat_details
from gosi_extraction import *
from utility import *
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.set_page_config(page_title='Secure Checkout', layout='wide')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vision_creds.json"

def transition_page():
    st.text_input(label='Some Label', value='', label_visibility='collapsed')
    st.write("Continuing to SAB..")

    html = """
        <style>
            .st-emotion-cache-10434yk{
                margin-left:60px;
                border-color: rgb(93, 63, 211) rgb(230, 230, 250) rgb(230, 230, 250) !important;
            }

            .st-emotion-cache-inkacd{
                margin-left:60px;
                border-color: rgb(93, 63, 211) rgb(230, 230, 250) rgb(230, 230, 250) !important;
            }

            p{
                font-size:20px;
                margin-left:10px;
            }
        </style>
        """

    st.markdown(html, unsafe_allow_html=True)

    with st.spinner("Loading SAB portal..."):
        time.sleep(3)
        st.session_state.checkout_step = 20
        st.rerun()

def signup_page():
    # placeholder = st.empty()
    # with placeholder.container():
    #     html = """
    #         <html>
    #             <head>
    #                 <style>
    #                     body {
    #                         font-family: Arial, sans-serif;
    #                         margin: 0;
    #                         padding: 0;
    #                         background-color: #f0f2f6;
    #                     }
    #                     .container {
    #                         background-color: #fff;
    #                         border-radius: 10px;
    #                         width: 300px;
    #                         margin: 0px auto;
    #                         padding: 10px;
    #                     }
    #                     .logo {
    #                         text-align: left;
    #                         margin-left:-10px;
    #                         margin-bottom: 40px;
    #                     }
    #                     h2 {
    #                         text-align: center;
    #                         color: #333;
    #                         margin-bottom: 30px;
    #                     }
    #                     .htext {
    #                         margin-top:30px;
    #                         text-align: left;
    #                         color: #333;
    #                         margin-left:-10px;
    #                         margin-bottom: 30px;
    #                         font-size: 30px;
    #                     }
    #                     input[type=text], input[type=password] {
    #                         width: 125%;
    #                         padding: 15px;
    #                         margin: 10px 0;
    #                         display: inline-block;
    #                         border: none;
    #                         border-radius: 7px;
    #                         box-sizing: border-box;
    #                         background-color: #f3f3f4;
    #                         color: lightgray;
    #                     }
    #                     .footer {
    #                         text-align: center;
    #                         margin-left: 30px;
    #                         margin-top: 20px;
    #                         margin-bottom: 10px;
    #                         color: #a0a0a0;
    #                     }
    #                     a {
    #                         color: #01394D;
    #                     }
    #                     a:hover {
    #                         color: #c53030;
    #                     }
    #                     .st-emotion-cache-10434yk{
    #                         margin-left:60px;
    #                         border-color: rgb(93, 63, 211) rgb(230, 230, 250) rgb(230, 230, 250) !important;
    #                     }
    #                     .st-emotion-cache-inkacd{
    #                         margin-left:60px;
    #                         border-color: rgb(93, 63, 211) rgb(230, 230, 250) rgb(230, 230, 250) !important;
    #                     }
    #                     p{
    #                         font-size:20px;
    #                         margin-left:10px;
    #                     }
    #                 </style>
    #             </head>
    #             <body>
    #                 <div class="container" style="margin-left:10px;">
    #                 </div>
    #             </body>
    #         </html>
    #     """

    #     st.markdown(html, unsafe_allow_html=True)

    #     with st.spinner("Loading SAB portal"):
    #         time.sleep(100)
    #         placeholder = st.empty()
    
    # placeholder = st.empty()
    
    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 300px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .logo {
                        text-align: left;
                        margin-left:-10px;
                        margin-bottom: 40px;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 30px;
                    }
                    .htext {
                        margin-top:30px;
                        text-align: left;
                        color: #333;
                        margin-left:-10px;
                        margin-bottom: 30px;
                        font-size: 30px;
                    }
                    input[type=text], input[type=password] {
                        width: 100%;
                        padding: 15px;
                        margin: 10px 0;
                        display: inline-block;
                        border: none;
                        border-radius: 7px;
                        box-sizing: border-box;
                        background-color: #f3f3f4;
                        color: lightgray;
                    }
                    .footer {
                        text-align: center;
                        margin-left: 30px;
                        margin-top: 20px;
                        margin-bottom: 10px;
                        color: #a0a0a0;
                    }
                    a {
                        color: #01394D;
                    }
                    a:hover {
                        color: #c53030;
                    }
                </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="logo">
                        <img src="data:image/png;base64,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" alt="Logo">
                    </div>
                    <p class="htext" style="font-weight:light;">Welcome to SAB</p>
                    <form action="/signup" method="post">
                        <input type="text" id="userId" name="userId" placeholder="Enter your userID" required>
                        <input type="password" id="password" name="password" placeholder="Enter your password" required>
                        <input type="password" id="confirm" name="confirm" placeholder="Confirm password" required>
                        <div class="footer" style="margin-right: -10px; margin-top: 120px;">By continuing, you agree with our <a href="/terms">Terms & Conditions</a></div>
                    </form>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .stButton>button {
    border: none;
    border-radius: 25px;
    cursor: pointer;
    display: flex;
    width: 100%;
    border: none;
    #    margin-top: 150px;
    background-color: #e53e3e;
    color: white;
    padding: 14px 28px;
    font-size: 36px;
    cursor: pointer;
    text-align: center;
        }
    </style>
    """,unsafe_allow_html=True
    )

    # # Continue button
    if st.button('Continue'):
        st.session_state.checkout_step = 2
        st.rerun()

    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 300px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .footer {
                        text-align: center;
                        margin-left: 30px;
                        margin-top: 0px;
                        margin-bottom: 10px;
                        color: #a0a0a0;
                    }
                    a {
                        color: #01394D;
                    }
                    a:hover {
                        color: #c53030;
                    }
                </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="footer">
                        Already have an account? <a href="/login">Login</a>
                    </div>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)


def docunent_upload_page():
    st.session_state['gsheet_data'] = {}
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    st.session_state['gsheet_data']['Timestamp'] = timestamp

    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 300px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .logo {
                        text-align: left;
                        margin-left:-10px;
                        margin-bottom: 40px;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 30px;
                    }
                    .htext {
                        margin-top:30px;
                        text-align: left;
                        color: #333;
                        margin-left:-10px;
                        margin-bottom: 30px;
                        font-size: 30px;
                    }
                    input[type=text], input[type=password] {
                        width: 100%;
                        padding: 15px;
                        margin: 10px 0;
                        display: inline-block;
                        border: none;
                        border-radius: 7px;
                        box-sizing: border-box;
                        background-color: #f3f3f4;
                        color: lightgray;
                    }
                    .footer {
                        text-align: center;
                        margin-left: 30px;
                        margin-top: 20px;
                        margin-bottom: 10px;
                        color: #a0a0a0;
                    }
                    a {
                        color: #01394D;
                    }
                    a:hover {
                        color: #c53030;
                    }
                </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="logo">
                        <img src="data:image/png;base64,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" alt="Logo">
                    </div>
                    <p class="htext" style="font-weight:light;">Upload Documents</p>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)

    custom_css = """
    <style>
    .st-emotion-cache-1gulkj5{
        background-color: white !important;
        margin-bottom: -70px !important;
    }

    .st-emotion-cache-16idsys p{
        font-size: 18px;
        margin-left:10px;
    }

    .st-emotion-cache-9ycgxx{
        color:white;
    }

    .st-emotion-cache-1aehpvj{
        color:white;
    }

    .st-emotion-cache-7ym5gk{
        position:absolute;
        display: inline;
        margin-top: -50px;
        margin-left:180px;
        border: 0.5px solid red;
        border-radius: 100px;
        color:#d3d3d3;
        width:120px;
    }
    </style>
    """

    # Inject custom CSS with components.html to affect Streamlit's default styles
    st.markdown(custom_css, unsafe_allow_html=True)

    cr_doc_file = st.file_uploader("Trade License", type=["pdf"])
    if cr_doc_file:
        ## document extraction and save step
        pdf_text = extract_text_from_pdf(cr_doc_file)
        translated_pdf_text1 = translate_arabic_to_english(pdf_text)
        translated_pdf_text2 = gcloud_translate(pdf_text)
        # st.write(translated_pdf_text2)
        ocr_result = smart_ocr_on_cr_doc(translated_pdf_text1, translated_pdf_text2)
        st.session_state['gsheet_data']['CR_DATA'] = json.dumps(ocr_result)

        uploaded_pdf_content = cr_doc_file.read()
        file_name = cr_doc_file.name
        file_id = upload_to_drive(uploaded_pdf_content, file_name)
        pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
        st.session_state['gsheet_data']['CR_PDF'] = pdf_file_url

        cr_number = ocr_result['cr_number']
        raw_result, wathq_result = get_response_from_wathq(cr_number)
        
        if raw_result:
            st.session_state['gsheet_data']['CR_DATA_WATHQ'] = json.dumps(raw_result)
        else:
            st.session_state['gsheet_data']['CR_DATA_WATHQ'] = ''

        st.success("Completed ✅")
        # st.experimental_rerun()

    st.markdown("<hr style='border: 0.5px solid lightgray; margin-top:-22px;'>", unsafe_allow_html=True)  # Add line break

    vat_doc_file = st.file_uploader("VAT Certificate", type=["pdf"])
    if vat_doc_file:
        pdf_text = extract_text_from_pdf(vat_doc_file)
        print(f"\nPDF TEXT: {pdf_text}")
        ocr_result = extract_vat_zakat_details(pdf_text)
        print(f"\nPDF TEXT: {ocr_result}")
        st.session_state['gsheet_data']['VAT_Data'] = json.dumps(ocr_result)

        uploaded_pdf_content = vat_doc_file.read()
        file_name = vat_doc_file.name  # Get the file name
        file_id = upload_to_drive(uploaded_pdf_content, file_name)
        pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
        st.session_state['gsheet_data']['VAT_PDF'] = pdf_file_url
        st.success("Completed ✅")

    st.markdown("<hr style='border: 0.5px solid lightgray; margin-top:-22px;'>", unsafe_allow_html=True)  # Add line break

    gosi_doc_file = st.file_uploader("Gosi Document", type=["pdf"])
    if gosi_doc_file:
        st.session_state.checkout_step = 5

        pdf_text = extract_text_from_pdf(gosi_doc_file)
        ocr_result = extract_business_gosi_data(pdf_text)
        st.session_state['gsheet_data']['BUSINESS_GOSI_Data'] = json.dumps(ocr_result)

        uploaded_pdf_content = gosi_doc_file.read()
        file_name = gosi_doc_file.name  # Get the file name
        file_id = upload_to_drive(uploaded_pdf_content, file_name)
        pdf_file_url = f"https://drive.google.com/uc?id={file_id}"
        st.session_state['gsheet_data']['BUSINESS_GOSI_PDF'] = pdf_file_url

        st.session_state['gsheet_data']['CUSTOMER_GOSI_Data'] = json.dumps(ocr_result)
        st.session_state['gsheet_data']['CUSTOMER_GOSI_Data'] = pdf_file_url

        st.success("Completed ✅")

    st.markdown("<hr style='border: 0.5px solid lightgray; margin-top:-22px;'>", unsafe_allow_html=True)  # Add line break

    st.markdown("""
        <style>
        .stButton>button {
        border: none;
        border-radius: 25px;
        cursor: pointer;
        margin-left:0px;
        display: flex;
        width: 100%;
        border: none;
        margin-top: 150px;
        background-color: #e53e3e;
        color: white;
        padding: 14px 28px;
        font-size: 36px;
        cursor: pointer;
        text-align: center;
            }
        </style>
        """,unsafe_allow_html=True
        )

    # # Continue button
    # if st.session_state.checkout_step == 6:
    if st.button('Continue'):
        print(f"step old: {st.session_state.checkout_step}")
        st.session_state.checkout_step = 7
        print(f"step: {st.session_state.checkout_step}")
        st.experimental_rerun()


if 'checkout_step' not in st.session_state:
    st.session_state.checkout_step = 0

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header{visibility:hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def checkout_page():
    placeholder = st.empty()
    with placeholder.container():
        image_html = """
            <style>
            /* Make sure the body has no margin and the image is displayed at the top */
            body {
                margin: 0;
                padding: 0;
            }
            /* Style for the image */
            .header-img {
                width: 400px;
                margin-top: -110px;
                margin-left: -20px;
                margin-right: 0px;
                display: block; /* This removes any extra space below the image */
            }
            </style>
            <img class="header-img" src="data:image/png;base64,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rt5luGtpDVojrenZPX53257APQ21DrVb9uruLdsH9kn3Pd+fuv/mgfADTQeZB2sPWR6qPEw/XFqH1E2r66vPrO9oSG5oPxJ2pKnRu/HwUcejO46ZHqs4rnN86QnqifknBk4Wnew/JT7VezrjdGfTpKZ7Z8aeud4c09x6NvzshXPB586cZ50/ecHnwrGLXhePXGJeqr/sfrmuxa3l8O9uvx9udW+tu+JxpaHNs62xfXT7iat+V09fC7x27jrn+uUbkTfabybcvH1r/K2O2/zb3Xdy7ry6W3D387059wn3Sx9oPCh/aPiw6g/bP/Z2uHccfxT4qOVx3ON7nbzOF0/ynnzpmv+U9rT8mcmz6m6X7mM9wT1tz8c973ohfvG5t+RPzT8rX9q8PPSX/18tfWP7ul5JXg28XvxG/82Ot65vm/qj+x++y333+X3pB/0POz8yP57/lPTp2eepX0hf1n61/dr4Lfzb/YHcgQExV8KV/wpgsKHp6QC83gEALRkAOtyfUccp9n9yQxR7VjkC/wkr9ohycwegFv6/x/TCv5tbAOzbBrdfUF99PADRNADiPQE6atRQG9yryfeVMiPCfcDmyK9puWng35hiz/lD3j+fgUzVFfx8/hdap3w4BHcqKwAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAFCaADAAQAAAABAAAAvQAAAAANN3SoAABAAElEQVR4Aey9B4BdV3muvTS9afpopFHvXbIkW5LlKrnbVNtUA7kkEEiAwJ/wk+TmAjfthgsJf3JvIJRAGsUYg7GNi1xlW7Jsq/c26l2a3rv+9137LGnPnn3OVI1m5ryfdM6Zs8+uz9577bW+9a7vG1W08oFLRiYCIiACIiACIiACIiACIiACIiACIiACIiACIhC3BBLi9sh14CIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgApaAnIS6EERABERABERABERABERABERABERABERABEQgzgnISRjnF4AOXwREQAREQAREQAREQAREQAREQAREQAREQATkJNQ1IAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAJxTkBOwji/AHT4IiACIiACIiACIiACIiACIiACIiACIiACIiAnoa4BERABERABERABERABERABERABERABERABEYhzAnISxvkFoMMXAREQAREQAREQAREQAREQAREQAREQAREQATkJdQ2IgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIQJwTkJMwzi8AHb4IiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIyEmoa0AEREAEREAEREAEREAEREAEREAEREAEREAE4pyAnIRxfgHo8EVABERABERABERABERABERABERABERABERATkJdAyIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIQ5wTkJIzzC0CHLwIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAJyEuoaEAEREAEREAEREAEREAEREAEREAEREAEREIE4JyAnYZxfADp8ERABERABERABERABERABERABERABERABEZCTUNeACIiACIiACIiACIiACIiACIiACIiACIiACMQ5ATkJ4/wC0OGLgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgJyEugZEQAREQAREQAREQAREQAREQAREQAREQAREIM4JyEkY5xeADl8EREAEREAEREAEREAEREAEREAEREAEREAE5CTUNSACIiACIiACIiACIiACIiACIiACIiACIiACcU5ATsI4vwB0+CIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgJ6GuAREQAREQAREQAREQAREQAREQAREQAREQARGIcwJyEsb5BaDDFwEREAEREAEREAEREAEREAEREAEREAEREAE5CXUNiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiECcE5CTMM4vAB2+CIiACIiACIiACIiACIiACIiACIiACIiACMhJqGtABERABERABERABERABERABERABERABERABOKcgJyEcX4B6PBFQAREQAREQAREQAREQAREQAREQAREQAREQE5CXQMiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiEOcE5CSM8wtAhy8CIiACIiACIiACIiACIiACIiACIiACIiACchLqGhABERABERABERABERABERABERABERABERCBOCcgJ2GcXwA6fBEQAREQAREQAREQAREQAREQAREQAREQARGQk1DXgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAjEOQE5CeP8AtDhi4AIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiICchLoGREAEREAEREAEREAEREAEREAEREAEREAERCDOCchJGOcXgA5fBERABERABERABERABERABERABERABERABOQk1DUgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAnFOQE7COL8AdPgiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiICehrgEREAEREAEREAEREAEREAEREAEREAEREAERiHMCchLG+QWgwxcBERABERABERABERABERABERABERABERABOQl1DYiACIiACIiACIiACIiACIiACIiACIiACIhAnBOQkzDOLwAdvgiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAjISahrQAREQAREQAREQAREQAREQAREQAREQAREQATinICchHF+AejwRUAEREAEREAEREAEREAEREAEREAEREAEREBOQl0DIiACIiACIiACIiACIiACIiACIiACIiACIhDnBOQkjPMLQIcvAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAnIS6hoQAREQAREQAREQAREQAREQAREQAREQAREQgTgnICdhnF8AOnwREAEREAEREAEREAEREAEREAEREAEREAERkJNQ14AIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIxDkBOQnj/ALQ4YuACIiACIiACIiACIiACIiACIiACIiACIiAnIS6BkRABERABERABERABERABERABERABERABEQgzgnISRjnF4AOXwREQAREQAREQAREQAREQAREQAREQAREQATkJNQ1IAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAJxTkBOwji/AHT4IiACIiACIiACIiACIiACIiACIiACIiACIiAnoa4BERABERABERABERABERABERABERABERABEYhzAnISxvkFoMMXAREQAREQAREQAREQAREQAREQAREQAREQATkJdQ2IgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIQJwTkJMwzi8AHb4IiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIyEmoa0AEREAEREAEREAEREAEREAEREAEREAEREAE4pyAnIRxfgHo8EVABERABERABERABERABERABERABERABERATkJdAyIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAoNKIC0tzfAlGzoE5CQcOudCeyICIiACIiACIiACIiACIiACIiACIiACcUFg4ezpZs2KJSY3Nzsujnc4HKSchMPhLGkfRUAEREAEREAEREAEREAEREAEREAEREAEROAqEki6iuvWqkVABERABERABERABERABERABERABERABETgMoE7blxmMjDM+CuffsTMnjrJrHt7q7lYUWV+/OTzZsuOvZfn0x+DT0BKwsFnri2KgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIwJAiICXhkDod2hkREAEREAEREAEREAEREAEREAEREAERGHkE7rxpuclMSzXf+PJnTUFuzuUDvH3FUvv31Ikl5vjZc+bHTzxnNm3bc/l3/TF4BKQkHDzW2pIIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIDEkCUhIOydOinRIBERABERABERABERABERABERABERCB4U/gnluX24P46h980ioIC6JkM148Z4aZN2OKycvONodXnzE/e+5ls2ffoeEPYBgdgZyEw+hkaVdFQAREQAREQAREQAREQAREQAREQAREYDgRyExLt7vLIcbRHIScITkpyb5yR2eZorwcOzR5OB3nSNjXUUUrH7g0Eg5ExyACIiACIiACIiACIiACIiACIiACIiACIjA0CNx320q7I9/+sz+yn7EchP49bm1rM3y9s3OfOXLyrHn+zXfMujc3+2fR31eJgJSEVwmsVisCIiACIiACIiACIiACIiACIiACIiAC8UogK90pCLN7hSCoKMxIS+vV8pq57wTkJOw7Oy0pAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiLgI/Cu1avst7/64qd9U3v/5/yZU82sqZPM2KICs/r668xzUBS+sv6d3q9IS/SYgJyEPUalGUVABERABERABERABERABERABERABERABGIR6KuCMLhOpyjMGZ1pYxRmpKUGZ9H3ASYgJ+EAA9XqREAEREAERCAlOcnk5ow2aajIlIwpNIkJCWby+HH2c9K4sRFAXkjgIyfP2O+HI5+nzpw3ra2tprKm1rS1twumCMQNAd4ntLkzp5n0tBSrHEhLSbEZDpMSE01mZrrhZ2Njk2nvaDd1DU2mqbnZnDx73lysrDJnL5abCxcrTAd+a2vv6DG3xMQEM2VCiQ2UvnzRvNDl9h05ZqfvOnDYNDU1h86jiQNHYMqkEjMeqpG8nGyTn5PTZcUV1dXm8InTprqu3pw5d7HL75ogAiIgAiIw+ASSUf+95YbFdsNf+MQHBnQHJowdY7Mip6ammPnTp5q9eC4//eLrA7oNrcwjICehrgQREAEREAERGGACo+DsoHMjE/FTipDFjU7DqSVj7edsDJmgXbrkOQk7Io7Amto6O72srMIkjLJ/6k0E4pJAQe5ok56aambAcZeGxsDYwgLrHMzJyTIpyHpYW19v2traTRUc6fWNzaa1pdVc6ugwNXAYJeDmuXSpdzdQYkKiGZ2RbhjvaNp458TvjP5ieUXnCfp2VQl4WS1zce7z7fkPbiwVZWpZRZVpwrmXiYAIiIAIDA0CycnJZmxBvt2ZmZMnDOhOUUHI16SSYnSmt6FzsHpA16+VXSEgJ+EVFgP210RUaj/10AOmuaXFPPnyG6YdDcD9h48P2Pq1IhEQAREQgaFFYNSoUXDsjTLjUXG5/YYlZkxBrlmzcplVDrJCkwCnYTo+qZRKg/PDM89J6JyG993qZX+rbWi0P//6xddMdW29efWdbaYCjWHnVBxaR669EYH+E1i9cqldyUffc4/9nDFxPO6VUSZndJb9ngqHO40qQjoBqbDl/dAKRyGdg6uWLoTTsM1UwGlYWV1r3ti806zfssOUVVWbih40IujUZ6MjOyvTvPeuW+22gm8NUCzSNmzfIyVhEM5V+D5h3BizdP5sqEknmtlTJ3fZwt7So6YBilL2qByFolB29QlkwZFOy8aQvwTci0Frbm6Bitdz1rMBLxMBEYgfAlQQ3rZ8iX1uf/5jD13VA59QXARFYbZhx2Ex6tt7Dx8zT0UUhaorDwx6OQkHhmOntWSmp5lFs6aZGjTuclHhbIKzUCYCIiACIjDyCeRlj7ZKpPHFheZ6NHB7YlzGb66Cs2XXPlOdVW+cg8Q/j/4WgZFEoDiiOli+YI49rDH5eYZDgHtqxZEZ6+Bgp+Po1NkLZuf+Q6amvqFHq6DjkSrC7MxMMx7hAcKMyjbZ4BEYnZGJocajTXF+fug5uQDFNZ1WKUnJg7dTcb4lOulpGWjnuNAAfiSj0O9FYQQ7zGQiIALxRYAKwnFQ/eej3J4xaWAVhEGS7HTnazLC99TVNZgydAa6Usfrfg8uoe+9JSAnYW+JxZifCsL3rL7JFKFyO3PKBCgJW80XPvGwVYJ8s+5n9sF57OTZGGvQTyIgAiIgAsOJAIMpp6YkmxkYQnzT0kVmyrhis2LxXJMSUT715VioSqTdsep6q0hPxrrOIc7as69vNNXVNXaYZTvUGjIRGK4E6GBIwTDid62+2R7CI++5237mQqFE66uPgUOTue7bll9nJkMZ+Nau/Wbz7r3mfHmlOa76l2WrNxHoK4Hr5s2yi37w/tUmI9VTFfrXtQfqznrECX1s7SumGfecTAREYOQTyIWib+70KSYHwqiPPHCHdd4N1lGzI2k+Yhgnox7OzoljZ86Zl9a/jZEGxqqaB2s/RuJ25CQcwLNKBeGdGDLDm4S94LSJCLB5oaLSjH0izyoK5SQcQOBalQiIgAhcYwIcRkyl3wSoj+5YsQTDHthJNHFA9mrmZG89NbUNpryqxmzesx89pvVI2AAHoXyEA8JYKxl8AnSB0xFONdKKhZ5ycEWUZCG93TsqnfhiHKRpE0tMGxKYVFZV2dXISdhbmppfBDoTmIxOMNqaFcugFsru/CO+ZY/OMOVQ9KzduMmUyUnYhY8miMBIJEAF4WwoB+mwu37h3EE9xHR0DKaPKbAdi4zvvQfh3V7e8M6g7sNI3ZichANwZufMnGruWHn9ZQWhk+O7VTN4PWNNVWH48ZbdB9zkYfs5DnEAqJyZO2OKyUrPMPnoQUhOSsTQIL4STHVNnWloasLx1tkg4pQAs9LAbIB1PRz6M2zhaMdFQATiisA0qMbvvvF6M33SeOscZNkYzejca0fG1ZPnLthZWGbSJqEzicYhj2E2e9okDKFsNvfetNwcg2Jx0+79UEV5GZHD5tc0ERjKBKggvOvmGxC3aDTUtwt7tKtuCD6HE/M+snE+4Wikk56voHEaHZHXzZlpiuC433vomBmNocSnzl80B0qPBWfXdxEQAREQAREQgV4QoIJwPnwgU0rGmQ/ev8YmG+vF4gM6K8P2zJ0+1WY+LvvQ+zxF4Rtvmw5IChkCQdZ7AnIS9p5ZlyWKEC8lqCD0z5SCRiOlsOehKBwJRqVkdmaGWThjqlVMThhbZKXFVNPQWXgGlfBKOAg5PO4cYsakYjheK4IZI5ennIQj4QLQMYiACFwmQDXFjdfNN+OKCqyK8PIPIX/Q0dHW3mYzcvJnBnmmOSeh/RLyVoDsyIjLjI6ZyYZx0Q4ePxUylyaJwPAgwKH4i2ZOt0lC6FzvjTEhXAsSIiTDwc77p6t70FsbHYR8TYADnq+MlFRz9kKZVRvISdgb4ppXBERABERABLoSSIGCcA5GvExDuLXrI/GEu841OFMYamRcUT4clSlmDcKNUFH4ChSFXpzUwdmHkbYVOQn7cUadgnAmJLaMQRhUEDL73lHEwKnG8LBv/+fjpr7Ry1jZj01e00XvX3OTSUfl/jZk7ixE78EY9M5ziDUDh9I5mJDgZR3My842re2tprGxxTQiGyCzc5LBPmQeWrdpmw0ueurM+Wt6LAO58Xtv9zKS5mXndFrtG5u227iU5ZVViovQiYy+iMDwJ5CJgPl8TSkZa3svWUEJs/PlFeadnftMc2ur2bB1j83Keg7TaE45OLnYG8L10N232OlLkPAkBZ0rQVs8ayaSopSY9dt3m30Hj1hFFTNJykRgOBCgcnbS+LF29MFdq26wIxKi7TeTjzD4+FOvrMcohBZz4PhJG4uzqr4OGY07TAochBy5MGFMkcmH43zp/Flm6vhxuCczkMwirctqmSn33ltX2Fihm3E/MityfSSLeJeZNUEEREAEREAERCCUwBh0ijPrPBWED9+72jrmQme8BhOzMtPN7GmTbT2j/MPvt4rCta9tRIzCS3juK+N6b05J11ZIb5aO83mdgpDOMheD0I+ETkLGI6SC8I23t/h/GpZ/UzmYDznv7fDQjy3Mj3oMwUydbaiMk0U+0pQfP33WZh8aSU5CKiJoE9EI8RvVCjVwjlYh0YAa8n4y+lsEhj8BDivOgaK6AGUiey+jWRNU1Dv3l5ra+kbz5IvrbEWlHg4Qv7kyc8m8GXbyApQpYU7C4sJchLXIwbDJDDvEUuWKn6L+HuoEkuDUK87PtR2MDHIey1qhFuQwoa27D5rKmhqzccce04x7ic5D1iecg52NAWZTLMjLtsOMkuBcD3MSZmMExHzUYY6cOmuzGLfAaS8nYawzoN9EQAREQAREoCuB0VkZZu6USWbqhHFmGTq1h5JRsEUfBTvuV8NfsbcUMQptIhM6CYfSng79fZGTsA/niFmMGWR7AcbhT0QQX6rp/NaE4TAXyquseu6nz7w87BWE1y+eZ2+2Zeipz0UMoSyoZ8KMzsCOSx1WUemPEcTKPPr8zRT08r9r9Sqz/8hJk4Cb+CLiFJ4YAXG13HCpWZEkA44Nh2UzDgKHPMlEQARGFoH0tLTLDruwI2PctEbEYWVW1Q1wcNApwWGSLraaf5lGG47BmFff3mon3w61dlISsr9iKIe//GDlpyPhksmGWioXzsnqujrTjm10Z3TOMLB0dnaWGY+hl6n4uyAvx5bVGWleeU6HI50ydQ31dnWHT5y2n0eOnbKf/e2B9eLWJplCjJsuQmIvJq3Ixf7QGZqWmma33dbWahWXldW1lhc/6RA6j2Gi5EaHa09sJeLcpaelgF+KdaYGlzl49IS5gFAYXF8rzks0y0JFeExBvt1XPuuDxvL9NMJr8LweOnK808+8Pmgrly7A8aV2+o1fGLeXy9OBXIM4vtnI6sv5iosKwSXTOrwyEfOX56MWsXwP41l5PHJOuqwME5hlOwvOY6tunTjOZvjNw1B4ZvvLSPfOMYfq0uh0ox05ccb2rJ87X2Y5h12bdsYBemOW7uUL5yEWYZYd9hu2Wh4r7Zdr19nj3naw1DoGrXPQ1jGoL0TwEu8DHbFVYNliXt64xRw6esqsvG4eXgus0pD3jzNyoJKxENf94rkzTBkSATFecn+MDaVRo+D4hKqC11sxrpVUNEzScR6ZYbm2ocFmJz93sdwbUYHzXINQLH011iSonkzEuZ6Ceiht2iTvMzsry37ndlnlqIMzlfd0GfjwvJ9AxsdGxDVlbGib+MjO3fs3lkeJqNOlYgRJCeJT876mOpR8szK8zNQJYEK7UFFuPxl6hkYOjMlai87TwejgcLwYA3MFrgla2L3I6bwnOjoume17DpiWluhlAhWsHDUzrrjQ5KD8ykacS14HDLeTivLGWQsUK03NTWDeZCpqam3G35PoJOc2+CzoiXVXhrQjKQ/v2V0HjphzKIe6s3w46Flf5b6yoylo7MgqPXbCnqOLULvzeTMO4YRoC2Z5neELI5/+e8u/nkKExuDzZfXyJWaWL4HXqXMXcQ/UIj55lanHdmQiIALDj0Aenp9syzMO4ZoblxqOHByqRifhJNTb6IN4/92rUZdqME++9PpQ3d0huV9yEvbhtPAGeQQpvqkgnBRQj3F1zahgnDx73ioIH3/2pT5sYWgtsmrxfBQEWegtmBNasXB7yyyCdBSystjZScjA4sZMxrA8viaNK0XjuQnxAo6NDCfhxPEWAQtNvzHLGx3GrLDLREAERhaB9PRUONpy0UAM7zRhY5iOjXNwEm7esTfmwTchLAPttXe22U86/zIxZJKOH7+T0CaHwhyj0VHDMpnhHNjo7864HCtM4+GAWonMc0zgMA8KrJTUZFOEY6DDpR2xEumQO4uGPG3tei873Akor2j9dRImJibZISlTUGlbgBi9hdjudDg42BDOR0a8NvDic4HJrUrhDGOCikOIvcgytAaNbDoVeuokvHXZIqt6H42OGjIM2m9efsM001mC443lJOTys5EltzAvz9xy/aLgauz+vA0HMCufQSchE2vQ7l213Gb8Cy58MeK8OXb6nOckhJOnAByWzZtlJpUUY7jMJDO2oMCcuXARrzLzHGLrxHISJsFZUwCnYHFhnrkDDXQe9wzsO51GdMrSeF3RnAP4BZzjBnAow2gHz+Fgf75qb3RUL18016SBjf+69m+Q5532+AuvwpFbaR1LvC6D5hya5eDIV1V1tXXOMQa0dWTgHvE7Mrg9Oj3G4FwymckxhDzZ1M19Gdxm8DsdLVzn/OmTcT+ONotmzzB5cIDmYdQEt332YplNWLd1z0FzAnXCowbnuh9OQlYmWLeik2dBRIl5983L7W65kQx0YvFYz4Mdy6A9pUfsiAaWE3QYUqHZLychtsZ9YGfxfJQhDDdzK9Qa1qEERSeNf9N2HjhsP7ftO2g/27Ft1o/rcb/gdr76FuFFJ/m9GN5Oo+M8zHhPsIzbe+hoTCdhUlIynGBJZiacbRzePgGOUg5lp4OealVnLPurUG5dQPl/BA5+jiq6iLKV13JPnYTdlSF0/rJjpwKjVXriJCyCk/Am1OcZ15YO3qCdQWdBEx3bcGLSSZiIMmUq6uy096+52X5OgUOY5r+37ITIG8t1Pl/WrFjaKQb5RoTIOHrqjC0z5ST0E9PfIjB8CDA+9grEHlwyf6ZN2DqU95xJY1mXYme0wRhGdtjLSdi7M9a19ty75eNq7tlo2CzEqzsFISuDPxsBCsIlC+fY88tKPVUrrlLgKud7UJlio+MAeu/ZY95AVQYqWWPQ0zAaSpcSpCQvGVNoFRHsvXfGispKBPpvgUNxPeL2sYEa1ghw8/s/6YCkUYVCY6ORlaRLqHFGhAV2+kC9sXHNIKisVLMxyW2w4i0TARGIbwJsiLM8itYHwN9YZqaiUWkTlKDw6M7R5pxg//XUC7ZDho69MGfKO3v2mXI0DGMpXnh2MtCQz0elbtrEErMKZS4z0U9GpYlOBjoH2ZjPiCjenJLQNXRdQ78I6ijabyI9sBfKPDWQndiDtzxsnw7PhbOmmUWzZthhIOPG5JtMbJcNdjqzqLxiOU4+bEDn43nBz7kzpthpVLFwaOiTcO7RqAKMZawYclhrXk4OzkHXak7hllzrNKUiKJbx/LFSPBbDyefAaRc0OtiOQR2UVtdVKeiS0kyfPB7hSJB1JmBUH9FxUwwHXn1dg7n1huvMYjBiIjA+b7ndLDxHW6Gu5LPHPfMCqzFZcEyQExU8tyxdZJWEdL7SOcikOrwO3bLcJi0zoizk9UGn0SSo0ui8WffWZqt+bYKzlk7bgTLuC5OV0Kk2FdcihwRHs43bd9mfONKAsYx5XfTEmppb7bP5OOpf2/cfggN6gpkBR07QyIKM68G+r0ZnLhOnfPC+O+wxTSpBYhRcz2PhJGMYAjrOeMx0MvOe5r1WhWPZi0Dqe48cg7PkbK86SFkGUCHK8/W+O24By2SzdO5Mu/vTwZNGdSaN22WhxNiMvKddZ+UEOOfpgN2wbZcpr6pGRzaUXShDempUDLLcKMQwrrtWXW+Pm85RcpgMZ5lzHHJ9TknoOovpuKbRectYkE+/9iZG2DSZY3CeUWl3tYyqztVQu2RnZpklcL7TWKb6zQ05fxFOeIaHaUMZFGauHFsJJ9t0dAzznNMpz/KSL7JxdWQuz7KMdd3xcMZNhmON7GdieB6dhi9t3GTrvOcueB0yYdvjtO7KEF5b7OigU64nxmufzuTC3Fzch+O6LMJGNY/FKdt5HtkZRXPlH0cT0ahoDTM6NsmBz5yWlpbLsxyHkrUKDvKw8vjyTPpDBERgSBPgs+Pt3ftNM8o3Pu9y0Lk5D/WPoWhUc1fX1GO0xwXzzGsb7ciEobifQ3mfotfUhvJeX6N9o4OwJwrCXQgoPxIUhCsjmYqWQ3nCRoszV2fffegIKpoXzNPr3jTn0UPaAFULGzOT0eAoQoOFysPrF8xGcFNjh/i45VlxuhFDP86ioUcnHIdfoKbjfo756RrMbsgzGzjskm5HJfry+KOYa+jdj6xwc1t0YtbgxWPHoOrerURzi4AIjEgCXnkU7ibkEAc6DFJSkqwjjJ0r3TkJOTyZ9rOn1lrnINVhrszzA2Tj0MVs808P/k1n0FQ4zG5essB89sPvsw4E1/AMznvle6H9cw5UQrTFEWfE5p2eGpLDxXrTUVIAx+RYqO7vuvF689Ddt8NBhKy0MZxEdqO+N3bQUAFVhu2+A9UerXsn4VgktCg0hXjWsOEbNHZacXq0hq6bnw4FzlsCp6bj4X7jJxv+HC7sdw64390x0lHFzrKgpSHbLh0ldGZWY1g1Y+fce8sK60Czjp7IAnQS0mHqnLnB9dARRXXQ5PHF5pF33xP8OfT7RAw5py2a7Q0hpCqqCU7CvQdLTQWG4Vrn8wA6CeksovMgG89SxjCKZRu3eee4Ao2R3iiOqKrCbWEVezv2ldrndpiTMBMKYGY7Lq/u+7BfOoc4pPIjD9xpM5rzOnEOsbBjc5y37j1oJmKY6tqNm3vlJGRZQvUwR698+uF3Wef++Mgw0LDt+ac5BjddtwgOV4SDwbmgoovXbm+chF6sx3QzHeeP+8BjZiMxlo1DRzHtukgZwnoUy8Hz6GiowDV/EQ6zq+okxDV3380rbEggtw/B/aXTjnb45GmrXG1jnTLEXDn23tU3WYc+y1HXkRIye5dJdNjSEb+39Kg5ePS4vd+6dRJGysloZYiLz5kdcf532WhgAp8HHH5XDEdvWHnGZ42NdxtxAI7Cdefq/mHzB1Zvv7oOieA+7Tx42KrU2VkgEwERGJ4EKtF5xxfVxqzX8Vk6VJ2ELMtZb2Soludf39hjMdLwPDNXZ6/lJOwBV8Yg5BDjBQh6zQQl9Jz7zQ6HQg/kcQxfeemtrVbS6v99uP3tGqUc7kRjr7XfSk+cspWdnVASnjh7DirCRltgdEQaFeyNZUVwP2KbtKJSyOUnYcgCG2SMP0VlAxtQVEmUsEcfy5+PxKzxb4cVMMY/oM0FexorybQ8NIxo1Yhtwoovt8lK2BFU9NjAodPSOhDtXFfecuDsZOV2Ioc9o1HljI3zcjSO2ChhAzQXSgEqHjhvMVQALGjo/L2EbVGBwCFySxCjkeaSDrh1uc8Vi+bbODSTsJ5WDOXbvveQHU53EcOAovVWu2X1KQIiMLQJMIkClRGMLRdmLEdZ5pUgXtmtGP7J5wQzvFP5UV7hxUJzquzg8mxMc3mqqPDRxbgO6quiLZ8OxQjVeVOgFrkZQ29ZiaPjKZYjo8tGIhOcc2r1iqV2yjk47Dhksg5lbqxhi1Q+seyng2Q2YlPROUQeLP97Y+RAZRYVkWtWLrOLnsc+0M5hGO5wNWLgaxHUVVTnMEYkz09P6WTg+VkMhSOVoWTM+Gh9NSo6ec3dtGQRYtk1mrVUVSF+nnPq9HW9bjkquqjGZNIdns+wY6STj3b41Gn72doS7qyxP8Z449BLDlPnM7q9nXdJZ+PoBw7FZYy03hqd/rSl6Pyko9wNN+7peqjknTl1AobTnzWl406h3lJnamvroy7O64EKPp7r25ZTEefFnKTTsLeWmAjuHQmILTfVJnkph5OO54J1rwbUwaKZ24diOPxWLJgHZVyhdcD2xkHm1s3t0RbOmW7jI55Hveostn8Emau7U0W7dfTkk+pa1i05zIxDgsOc+CxDaa9v3mE/bf0PZXlQucr7KhGK48VzZphZGL5PB1tfyzEuVwzH6i3XL7Yq2aNQIfM66tcQdLv3ehMBERCBwSNQjTrgdnYqop7A+iUVyK7zcfD2InxLjBHNDtizqB++vmmHOYM2Pb9bQVL4IpoahYCchFHA+CczSQkVhAxcHhaDsAaVPFZKd8KJ9J3/+qV/0WH5t2vE3bHyerv/HEbht617D1gF4bOvv2XOYGhP0FyMoDPnLph3tu+2DbylGOpBhxudhDauFhyAzAi6GA2ki6gohjkJGQ9l7lTPUfnl3/mg3cwNGPpMc0oLDl1hQ5lZk/n348+/ak5BWvz6lp2mIiQo+Tg02Nlof+ie283DeDnj0JsdGKJUivO4futOKCDnmA/df4cdajwOKhA6Rr/zk19bRyQbIYy78u0//4Jd3FV83brc5+994F3uT/v5jR/8BElbjpuNTXtNFRySMhEQgeFLoA4dCozhVIVKUpixXGDjlCqyL37sIdso/OFjT9vhh29V7raLtKPsCjMqTvpjrLCNRzl3C5w+v/+h91rFS/cKwvAtMl4g7Y8+8bD93Lxnv1XcHEClK5aTkMNlOSzzXbffaFavWGY7hvoy1IzPIx4PHTJfijwHqGKnDWcnIZ0vdBrcvmKJdcZxeJ5TH9qD6+aNDsLb4Wzgcu+Cuqk/5tR9n/nIe21cYTovdkEheam5A/sWfo32Znt0Es6FMpVqLPfsDi5f3+A529/e5ilW6aDsi506c8FUwAlP9QDjRQaNnYqsK1SikdNby8CwedrH33OPvbcZ243K2J7aFHRO8sUhUGUVFWYvEujEchKSFZVZdK5+/mMP2uvDH7qlp9vlfF69y5jb4WykcShpERzTr6O+c/T4aTst7M06KbEPS+fOsvvATgPWf/pi7tw/dNftdnGy42iUnz5TH1qX7Ms2uAwTDjEGIYdgr4DKNszYkKT98BdP2s+zGPobFiuQwgCqOB+4baUtx6gg7c05tyvHm3seUF35Gai6GaPw7e3I2A1Fzt4+XItuvfoUAREQgcEmcBqiKL5K4BfJQXnLMAYfQviNoWAUCLFuvvfwUfO9R5+w5TpHSMh6T0BOwhjMGIOQFQSnIHRxfNwiTkF4EI6ll0eAgtAdVwEqpDSqN2iuz5o9noj+B7XeOVTA0fPbeiXeiJ0x8EavPSv6zKr35vZdVjnISqmzY4jLw9+DsY/YUGKvdRbirNyGLJ80DlGmuX2xX/DGBiSbMGxEssG6bMEs68ytQc84sx5y21REdLHAitgzz0Y0428x++LsaRO93nLsS9DYGR7NMRicV99FQARGJgEqn6qRZKMc5ct59FTSEUKnQdDYqGSMvazMdDtMjY3TvEgZy4QUNA67ozGLL811ftgvvXizw5uxPWaVZAKMBbOmWAeha5y7VTGDLBOUcNgyYxvSWCSyDHRDY6nA8ZvrPFoCZ0ENYugdR2cMFdFBNSOfG1QZLZw9zcyYOAFDUvLt96D6yfX21kO5xuPn73SaMckAn7tcBzuWLhsKXv5OW4zEE7QXN2yyn8PxzUtM4x0jn10czslnLJX5rXi2tvJ5i2coM/DW4Hw5xzFVolRVzkSsw2VQswcTMdjnLpKIMR5YKbIX8xlbVV1rEaUiAy9t7tTJ9pMqeMeUE+gAoiJ/PpT7fM5t33fItEWcd3aBPr4l4FxS2RctsyxXy2uKdvl6iuJAtzPFeKNCjKw4nDWoCuNinMZj5LXfW2PiNRrvczp5GfOIIQQYp4mjJhgXktct70P+Hs1svXLmdFNWU2tK4SgMGusXzCBcgJETyxfNsaNXOHwzbJ1U4tHYkUlzsZO9fUmwIyLY0cv7119v4UgJJqs5iOUuYB1czjnOuB7/PjBsDJV0OahnBTsbeL7o6GLDjPUtWmOkk2MyGpA0V3+zX3xvMxA3Mgf1PNbfKlBu8Jrtj9qDCXEYO3AaFNRU14aFGnCbZyINWlmk/HPKQvc7ldAsk26ASIBxtplEiOeWQ3D9xvKLKhVmYqeynEYmWSjHipDJnez9zwVypZORWZFvRf2WcTfpKKW5zN72yxB4I5OLcGbSNu/aZz8LUTbTqCgN69SohmiCy52ESIDXlLNjp84hHmMF7s3e33duHfoUAREYWgSYqX7nocPIDl9nfSUMJzATiutrYXx+MYkcO3xee2e7DWnGkT6sV8n6RqCrB6Rv6xmRS92xYhniKC3tVkFIB+FIUBC6k+gah6y4+Y0PfFawt+0/aLbu2m8DnPt/D/7tOQDbzRbE4WF8IQ61YS+6M1aobGwtVLL9xsbSMjRECxBc+XOPPGh/CjYw3fyugcMhIDTXwM3NyTSnz5WZX73yhtlTU+pm7/TprzDb3nJUMOfPmIze4iW2QZOPDIXh5lUS/cuHzdfd72HLaJoIiMDwIMB4UHwxUcIBNPSL0aD3NwbdUXDIrStTZ8M5wwoLVSS0lxGbjPbmNq/BymyztLb2xivOEjulZ290sFH5dzsanx97z912uK8bIsk1sPGK/9bp9DqSRnGI3aZI48+plu6DYobm9tl+wZtLNvFBKKzpHHxy3QZTFzJU0mb5hOrvvltWIsHBDVYJ5d8Htz42rBlQmvHR3tmxDw3wBJv1lg6U21cstQ5CKr+dsdR1wwbfd+ctdvLf/+hn7udh98mkIn6jk4UOJy9eW43NOswht40tyGANh1ZDkzcklA7CZYjxduN1C6GGX+Nfhf2bSjkmRGEIDiabocNsN+KB0VyW48999P32OxOZuGcoJ1DpR7sNCsXZUyea03AeHT8RXWVmZ+7BG7eRh+syO8SJ7hY/DwcCjfWG/hjVYHyxsXAG19dA2vWIs+w3OnDpcGQStyoMHV48e4aN4cZzmxLDSTgTTnwOLz+F2HxvRoa7+tfrOZKSDFVnn/vIg/a6jxb/bx/UErR/f+I5+1kLZyv36QaMhmDHxYP33GYz8NKh46+TLME1tBiONCZTOQ0nVRXu5ZbWKx2qdFLynmeyEe4Dj2ms7360G8MbyxSGjKFz+5l1G+3kCjg/aQ/edav9jOYkXDZ/tv390edfgfqz0lShbGzpuOJYsj/24i0NjuilcGaynH13FHWtc0L+52+et2s+CTVMmHGocgZCNrz/rpttwiUqOtnhE7Tyqlo4+c7jHjtirMKZZSxmmoowRSsWz+vyXKCzls5Ljqr5Q9yHvO7f2LzdrnaoOQkZQqg0ojL9+TMv2X1kPHFaUf6NoU5CPtt4PfBZ5u5pzs8Mz7xfaqWaJA6ZCIwIAryfn1/3FhSFY9Dhk2E7kq6Vk5DP/FPonNh7+FhEQdgWdaTPiIA/CAchJ2EIZKcgnGWzEuZdzgToZg0qCOlFH0nGHtQwY6wiNnCb0XDpjdKFPa3noBSpRaOQ63BW34iGDCqmTHhCcxXYVDjrqFZxAZDd/PzcBocjjT0FtPzc0bZ3dz5Un075yOkTxxabtORUm2WZlTJW2liZjWasTLORT7UD18PYg+fQQKJSoA4qjjMXy2wGZ/aQlqFh3YwGHRvZtKWRiq5LpuK2cRAxGdm4owqEla3TUAmxkhTssXbz61MERGD4EGB5wjKL4Qc2YtjYLDhVxo0psioRJmmIZlSiuLJq2sTxdjbXcGXZRzuGhit7RU9H1BgMFN0T50k+FIpzGDcLQ1HpUGPmUb+xY4aNNZZnm/YcQBbLZpTNnnNmFIYf0pHwJo6FtnSe14B3iQ/cerLQWKYTgqpwZpUP7ts4KEwmYoi1dZRgH4IqRiYqaGhqMUdOn0HjeIeN4cukARToJGN+lqO1eDZMHj/G3IkYhFRPMb6i31xQfA5Bpg21xrV/X7v7m/tONf3u0iM2Vh7VpTxPPP9tbRwaC5UWnkOn0OlFyx6dCcfNDCQIK46s+oqyidckEzFs2r3PxsPdi/AWfN5cQEgPWkNE4fXCm1vsdw4bpeOOPP3nifHcqDpMx3ORHWjcv1jPT7uyGG+M6cZrPi21q5PFLeayzLrvQ/mz9MRpq4jasuegzQRLJxGdZCdxjqgQpYOOQ1TZaemuUf/x0GnO38mX3Fkz4T3ljIo4FxqF9xH5+c1zJnsdDa+87dVDTp6/aGehg5jnag+SY9A5OwGNt1NjLhg6OP11O6dKLIbSl8PNj5zGqAufAyc1FdmaUY6UFHn38mgoof3mFKt0Sr6AGJbMiLszEgagPhKnde2bXidIMVR4tJLiglDHEtXGVKaRIeRn/s306G+GMWAcaWY1Z/ZhKvii2Y4DXqex4xVtPsYhZ2bf0RnMXIxyDOWj33jcdqgwEpFs2n0Q9+d5hLo5D/beXHVgUI/yddbkiSgLkWU9JanTtcBnB8vorPQMjFyZZBc6jOtqKBkVztURhe+hk55SlepwWjR1DuN7MynO0TNnUef1rknOX1ZRY+vSra396wTgumQiIAJDi4CnKDxiVeG70ClJBTVHtAyGMZ4tnx0MO7Z+6y5bp21AOeR/pg7GfozEbchJGHJWnYJwJh7uY0IqGy4G4UhTEDoUjCUVZnRwsXJaC299U8SxFzZfcJrLhhScHvadDj02Jt5/9622gusUhK6B8sSLr9vFXnnLa+SwN5xKnb/4g9+53PDmDPOmTzFtU9qt2oWxeFjZcesI2y4VQHxxHlbyOHyQ6iA6OFlx41ASNr7oHOWQGlbuvh+JZfO3/8/v21UGnYRr128yDO7KYUBUifCTccyaUXjJREAEhj8BlhdHjp00P0V5cTuU5wvQWcHkArGchCzjnOJwFbIO09znhyJDsdZhqAQbW1SCscG1vaU0PGxCACEbtmsQS3YOYrnSWRG0owjx8MSLr0EhVmaeeeXN4M/2++5II3oxjoUWdBI6VdAsZMTNxbHuxLPAH1dtztQpZsXCOXaYY9g+ULF0Ftt/9e1tiPP6uG1s+mOBsfH825c3mEUYSrsMjkoO8Qs6CZ2qyiWyGs5OQsbKoaryl8+9atbDaUqnMxWq0Yyxkd+9ZpUN3+Gej5yX1yKfc+dwLTJ+LpnuLT0Wupp9UD3RluM8kWVWxoROTsKZGAY6HUqoIjgRT+KagefGPvvsQn14o7OKQ1WpMo1mPO7hYusweoTDRH/w2FOGjSNXv3CO1k88eD+UuGMxKmEpVG2eA8h/bJlwtHNoN5O3sX7Cc+dv0LAOdB1UiVQcMjFN0FgPYVZt2g8QcynMjkQcTnRmFaFOx/Ps3xfuK18zJpXY+lwz1nkSjkJneVCVch/mIZZk2D44xSqHWv/Djx+1nRiMA+W3DQgaT1uA+hitKH95Jyeh6xieAlZ0Zp9C529fsh3T4ToJWTa5nU+8717bseDWbTfse3vy5TfsN8bcjGWLoEhk1u/xcPS65E3++ctw3BwhsxYhD3757Ev2/PlD5/DeZNl1Gzo6KDjgte93GHP/WD5Sd7gGzw7asxElpn871/JvXpNUNtPc5+xJ3vXchmR8YVZTX2+H328/cMQcDhlKH7aMpomACAxvAqwDvvDG24gHiwQmxUgahfb0YDkJ6SBku/z1zTvNDx970vopOJJC1n8CchL6GDKLMStvrGywQhtM2EEFIYfunIeziElKDmOY1Ei0aMHl21CJ5PE71cvVOHZWnPAfjZujJgENi4v5ngKCsZlormeSvQS0i6ikcZgaG1mMGUnVA3vI+eLFzRhIrJxRMcMe9u6M6z2OijLjde09TCVgM1Q3F61ShT2qdJLyxZ10Q2qiKXzY0GMFnbEa2GBrhHqGy4bFSepuv/S7CIjA0CTA8pCqr4raGrMVGcwL0bimAjk1OQUKkiyrNqQjoCc2CuUWLQdqMT6L2FHFsqMSFZ7yzGpThmdPtCygLDuphOb2nVLRbdM6IeCI4NBVqgg5zLg7o7MplrHBy2HHLoi/a5Snp6fafYjmKGV2WcbgYqcL2fmdI2573F+qsE9AoUVHRlgjnfOGqc3dOobL52kowHg+GEO3Cc/XaAodqiwZD46xzqhAozLJb4yJxw5Mdkyx0ux3vPrn8/9Nxxyft3TS+OOLOZXZ6Mw0qzRkhbu17cooAP86evq391y+onoMLkdH21A39+ymg4idplSS+Y3XLe+DyupqO1SV9ZJwI4dLGHKK+IU4l7yPbL0iMnMiFL2MKZiTlRW+OKYyQVtPjM5MGpV+3A7jQ7KjwhnLCiYYSovEq3TTea0VIuQLy6IwY5nHzlQ6j3jdRqsHcVkmhqOxLuR3pNmJeCMzqvVc+eemd/fJa8qL+TfazIk4M+mcc2WRf3lXnp3yqdv8v7u/3bIMt8Ph98EYjG4+duLwOmDMK698db9EPlFl5XReIxx94q6dwFz2q0tG47bN5WQiIAIiMBwJnMAIGMbrPh6JUeti+Q70sdAfwXpOGUZK7EGHKDvB+RyN9Sxy+8CRK7SUUV69o/WSV/cegDxt3opHyHvnWuYIOai+HsanHnoAsUem2YZZmILwQnmVjT3y0giLQRjkxYxwYcaKDh1trVF6EMOW6cs0Zib86+/+u20c5iKwut84PM1vTHFOO/uJclR8E5B1LweVRsS2QsWbNgVDbRhb6RACuPfESbhl9wHzAygET2G9eyNDZ+yKQt5csoEGDI0Ls9LjJ9EQroLj4IB1robNo2kiIALDmwADsfP1MpTDr721zcyZOdXcf/NyO1Tv3ptXWjUJY7/1xBinisYhc7Sbly2ynz9/5kVzEllbf/bcy8gC2tU54BqXzDB349KFXTq46HhiJ9fBo6fMc4gf0xN79vWNdrY//8zHQ2dfgsQoVPBtRzy2ykrP2cQZqVZahf0OOirdSnZj/l+tXQc1Y7nl5qa7TzaQWck7B2fmT596wQ4/fvAu92vnz0mRxAi7DgzfkB9PvPSG2QX15lFUqCtjOG8ZI60Y8Rqn4JjHQd0UNA7XZaKR3agsHz5+Kvhzp++uEr3unW1W3cRzmWmuKE9dR+EsqIY6MOR5OzpF+zMcmI4bOoH4imax1JPRlhns6S5UyNo33zFnoZpjncLv5LaOIFy/m3cdMHvTjpkboNQMM/roeM9mQwE3FmFO2KCi08kZHVQ3LVto4zi7af5Pqhd5D/XE9kZUo1T5sQPcJkCJlDNcfjpUoxw9sguxCf3GkAXch/EYeh5mHF2xFnHnmCX6QjcdCo+vfcWuYuaUCeg46Vyn4w8Mi8B9YCdvb4xlDIcWM2HdEqiOed0GO/e5Pqqx165/2676qRc9JWG07Tj/KUPY3IiYguysCbMDx0+YHftKbUxaKjuDxmuhA9PZ4bwRMWfpiL8ew9CDxs6UVSizZSIgAiIw3AnU8dn0/KtWUcjQNLT/gZF+V8OoYmd4ltfe2WEVhHQacvRfd0b/IPT7drYpyV5H38lWr25SH3EWdreOePldTsJ4OdO9OE5XEQ4uQsUeVSPopw3+NKDfeeuyB94qDyIKHA4noY2JNI6cEzATyhkO6WCWRg4B9g+/4vzsmebvEYEOJ4WaVQMh9hN7hakQZBxBmQiIgAj0hgAdXGzsM6ZgDcIy5GXvtUohOndoTN5Ac+qcaAo5O5PvzQ2rnYzhxFQlVkORUxNJDsDZWFZySGdyYpIt79ywR98qPKcEnJXzMYyOQ9xiKVu43LSIA86/Dv/fyclQQaHMdQ5K7hcVSlRH2TLXtbb9C+HvpuZWO1QzusrKW4AhGmwQfJTJO6I4AS/GcKoFNjvkvjrnEp85VP7xeGNZIs4tnSKpAQWhW4Zx6xjygkOE58+d4SbH/KTjgk6VsIQMXJCJKxjOg9dWf4z3hc2e2xK9yklF3VA3l4GZjZFYcZnpkKc14pOKO/KLdk/y3g3WqTiN55p1mmjmwgC0RBo70eZz07NHu+zInetvvFfpvE0IxD1kDD6qC6M5duloJo+eDOuqjzhAD8J5TRVs0I4hlhQdeb3NfEs1bQliGTLjLh2EfjWs2wbXSwf3YcRi7Ym5ciyZ9V2wceVbcNlmlGNU7jZDoRnLOAKHjGKVd9wOze1/T1TAsbap30RABETgWhM4GVG7H4uEsWB9YyCMz1++mKRkH0b8HcXzg8+j9o7OnTV80rEamjgK2eYTPMVgdoJXXucneJ1yU1K8eldu5Pl3rt1zbDZ0IEyZSTB1HQmm/dIo+/LcigNxBMNnHdFrbMPnGLSnA0zA36PtXzUbIKzEuAqN/7eB+NspSHizc8gvK2eukrwIWfho7719lf10hc0CKD/ZwJmErMmpqCQGjb+xst3dcD8OR65Eo7sUQ8i37N4fXI2+i4AIiEBMAhwuydfBw8fsi+XX9xN+Y7LRgbEEjjl2bFAZSKfMDQu8pCCzMUSuJ3YH4gzSGMPqzPly80vEZt2118sgyulUo3D9OXACBmOj8ncmS2Enz63LkLW2h8Gkw5waXJez/Oxck57SdLlhS8UNnw/cfjT1DZel428fwkk4NZtbX/CzBo7Q1xC3kPbsq28Gfx723+kkpKP2BIYbM35cd07b0VnpNrmDi2cZBJAOhw6VWowft3jOtODPod+ZNIEda3QEhlkuHEtMbhKmzgqbP9o0Oko41DRWqBI6N4e6MQwKraIaQ7ojw3jD9rkMQ8dp5zGSgEO6qQwMG35P5yHrOG7IvlsXz0cJ4jqFLcN58jEM9vMff9jO3tNh2uOxPpYRwY5UxlBlPSl4z3IoP5fh72HWAMUGebDu1J2djAw7+9vv/lt3s/bq9ykl4wxf0YwOWsaUPldWaf71F09Fm63TdIZRYNnHzyAT/4zMirwHo03cufb/5v+7GopLzkfHb5hxuiuzXcxCKmRkIiACIjBcCVBR+MTa1+zujy/0Rj587fOfHJDD4fBihml5HOtnjG2W843obA0aHYRJ6ETLS2g3q7MaTDochTdlNJhUDDFelBbeubO7yUuS92Z9ummCqnBtfaZpaE8wNXAWtsFZGG/W1asSbwR8x3vk1Dn7jRW0VGThYw9qGhp0zvg3YxUycPscDEVgz+DJERiXkD3+YcbKLBu+gSRvYbN2mebvjaUzsDvLxdATLsOMobR5U73GNLPw0Zh1j5Y7evTlXnquta+3MPfJqgMimdd6so92B/QmAiIgAjEIMEYK1cmMj0o1C58vrsFYF4lZ5pSCYyKKQxdbNbhaZsmko4WZRrkOllN8sRPEOhuiNERZLlpVNVR+sRq+/u25ffRP8/9NpyOdgnRA0pKgdLP7EFHF+Ofl39xv/nPOVKekC84XL9/tcETGZOzB85BM7DlmJx1eYUYVpxuu2dNzTKcRK9L+ou5KUAAAMwJJREFUGHX+dfP8cgg84wP3x3iNsiIfSyHVX0dkf/avp8tecch1X4fhOnlqmQGc8Qd7Y1aRi07PWB2yLh5nT+8jroshWYLG+5xOSjrGXD2N58s6j7kP+C3MeN3ac9oSWwEbtuxgTqOjNQNxUpkxmlbXzSgR1xHuWAT3lWeS55TXMsvvaPVltxzVLZyPimHrJI9xv7H8lImACIjASCJw8oIXIocxA2muHd/bY6RCnzG5T1JBWHrcnC2vsJ3NHQEFYRKUg6MT203aqHZTkthocvH3xOQ2kwYn4egExAvH79EsEw5F2tgklO1QEs5JbjetqHIdbcswDR3Jpqo9Ma6cheG1zWj0Rvj0//jV0/YI//BjH7AXIoPGpxVccRIyTqH3yjOLoWAbqbEJy6uuKFT8p5zOUVaSGUC9NxasbPE7K6HRjJW5VYgFk5eTbf7isx+3s1HNEMu4X6wss8LrNVljzd31NyYoKUfvRB2GCMbat65LaooIiIAIdCXAcoRquVrE7Nq254CdYePWnZ1mZDZi2ofuv8N+fuRdd9rPMQX5qJ50teWL5tkG6suIfbgVDXgmImhDpGUqDPPQYRLMAuzWwHIxhS+oGhmaYSCMMfLYscIhzjQmiGIMmpTI9+A2mA2TToUGlLVMShLvRnWdN0TGU6B2x4MOPT4TMzM8Z0dwfjoRsyOJLhjfbSAsC85onmd3jvu6Tg7NpaIu1rO1GPWroW4urnGM6kunQ+jo8IKou8RrnX6M8YWOOd6n0ZyEdGQNVDB4Xld8cbg3HYV0/vE8sZPchnGJ4pTm9VuBBC3NuKeHqtFpPplD6nFs4zEsmXbgyImYu8uY3HSMk3GYtaPMJSPGVKUCONY1zeU5JLm+vtHko/7M+50O4IQojlfeazRmf5eJgAiIwEgg8GQkDmxJRFH4l3/0e306rFOIx30RKv3HX3jN/MYqCL1hx8GV0UF4X1Y9HIMN5qO53cco9C8/NTL82H0+FKlKPVXTYs62pZnHqrNMWVvvfCD+9Q+3v8OfgsPtKAZ4f9nrxwzGdIplI7ObjcXnU0ewMs4KFFWFBQg6zWEXjQ1dpa4DvFuDtjqXsc9VfpyTz8UlskPb4MhzFebudiwNcQMz0Ii1vdURjqxkt9heAa9ngHFd2JBlBYoV4wJk1WOAa06juX1xWY3p1KOx0UlzyVY4tFgmAiIgAlebgC2vIiq6sG1Z5RwLOurnovSJuCG31WhI0lwGzgJ0ilDhFRzyaztAWEaikUlFIstFZgvl+vm3Kyftynxv9jd8Z7xZt03fz336k2Wve1ZwBW770faBzxH/yy3Tp43H4UJX+IYfvBu+zOsuGJsnfInup1pHJpxBly558Xy6XyJ8Du4bYy7GiruYnORVvF022Vjzhm/Fm8r6A+sqycgunhwSv9E6wcCI9Y+e1mFibe9q/EbFLfeTr2jmHO2ct19mF0c5gvNs63qRbfLDsoqycs7bXRkYZdFBnezKHA7RptljxGe0csrdZ3bmkDe7Pq4HdVOWz+0EhXI1mnEevqjidNuONm+0fYo2f1+n96Ujva/b0nIiIAIiQAIu1j9De9F62mHNOiufT4ztesGKeRov1zftiiJvyRhGnAyVIOMO5iS2QjnYz2ejb+WjoTCsTWg1+UntprljlGlGN34LhiCPdJOTMOQM/ycUhXxRUXjXjUvNRARwn4Sskc4KUNngi5kVGVtqpCkKdyBDIs1lbGNvLCs3+VAx0FbMn2Ny0tPNWzv3mqoeBI6/77aV5iP3rTHFhflmji8G115kYWTGOQb5//nTL9ieWzpmmbnxH/7sc3Zb7s0FtH761fV20qvIME07cOSkHfbxZ5/5mC1wFiJ2YbSYTXYBvYmACIjAABCgco4dRbbRGNLqaoLK7iKGQzAIQrTGHwMv07736BP28xfPveR9/uNfmbGFBbajyu8odOqWmRPGm2XI5rnnyHFzAYoWDn3jcLZomedddmP2wjJG10DYMcQZo5KR6msanRbE0HYpvMFsnTcIDp0CZxCPiUxsA9suPVTfPMcmz+G1tnZUktlJFm3ILoe18/xynhN4pg6EHTp2ypQhPprrnOvrOpvRqXfg6AmMxPAS+IStZ0oklMi0CSX25yMI5dIXR2FxUYHN4rts/mxkvZ19+d6L+L5sDD02Njj0/0e/9EaPhO3PtZzWAXUwY0Nz+KmLV+ffH95r76D+RXMdpf7f+/L36XPeNeOudHY+MOM0uYV1vtIRyxh6yXC2DlVj2cwysxjK7L/54qftbt77e39iP3m/hBm5tya22Q6VsN8pEuAA7DwoDgtRX2WGd76iGTtz8qEKLcyBIjeKgtAtyzL8alt3jsqrvX2tXwREID4J/PSptfbAXTiUP/ndD/fIUXgEz+oLEG79y6O/MRs274RvAh2OIeX3zNQm80hOnSlIajE3Zgzsc2l1FtfXYpalI9Fce5L5bsVos7VxYEblDOWrQU7CGGfHKQoZdLoJldt4URS63msXkDo5qXPg6tzsbAxByvaGZGDIW7SKPBUBfKVDScjhLMFYSi3IJlwPBWYrPmmJqECxMhqW/c41RMsra+y8rjLFHgaqY5JRcXMNaDvDEHgb1YOe4yGwm9oFERCBPhBgWVWQl2OfCyy7glaJ5AbVtbWGzp1gzJTgvO67K3tbEOcrWrnKeelkYzZPp7Tmcgy5EM0Zyf5U/sY4uhciSRXcNvv6WYmA/BxC7Izbt2Efonbe0v3AWGeMgZYELmiIu4VDPj2VktdTyyymYeYYuU//PFF3AzNx3Xw2dRdrj3HZ+NwPJnvwb2ew/uY5piKPTpswoyOYyk7b2z5A55h1oDqMlGAcoP4Yn9Hctya8nJI12lBal/m7r9ujY43OK45e4D3q8fKg8W9eozz/Q9lZYh3oMe5nsqmKqDHqGr1RFX3l5ZbjueZ23eXVAfWoVSljP8KMoz7o9GpHjKbujLxpzJYcZu1witLoTO6NufKuEU5TdiQzbjjrmmHn1oXJGY3RQbSKyvDkIDzmsOWD+8VygbHLG5piHz+dimmYL9r17l8vr83eGPeTZROfB1SXU0XMMiKauXnd+Yg2n6aLgAiIwNUi4DpV3DMsmqKwi4Iw8owKVoIYg5AZjNNRo0yH4i/JRC8D+3tMjGfYgtiGGYh3yEQorUhmMpITmoTXvPtLcYQs7xSFD99/p3nkgTu6VRTuPHjEfP2ffjjsj56NDNq6tz213l033YAse15acE7/wD232QpZS2uL2X/4mGF6c/Y4B206smgumjHV3LViiVmxeH7wZ6Qvv2h+u24DevY9j38mKva3XL84tGfhF8+8Ypf/y3/+caf1OJUj1QPjoUD072enGa/BF+6bHTqFipxMBERgZBG4Y9UN5pPvu9fGifMrzd1R7sLz4L9/+3umGiqT/VBN98SqkQGWduj4KTgY65BZNidUxTNubIFhZuSjiNFyDlne6uoaTCPK4NqQcpjr4/BTKtA2bN9lvvrtH3DSgFttXR2SAoyyWeZc493f2GYxyO8F2ZlWmV+NfT5fVh51P+jsGYcEVVTiXDdnZuh8uw4ettOpSvcbY8DFigPH9c7C86kcjpbKKM4Cro+xzMZAAe9U9P5tDPbfdPAyDIobmh7cPjv19hw6avYh5to//OhnwZ+v6fdGOLJ27i81Y8YUIDt3mXWYlERixLkdc47Yz374fXbSn3zruzHPjVsu+Llg9jTzgbtuMzMmT7Cv4O8nzlwwW/cegCPRy0Ac/H0ofOfQKqpCqSJkGRA0Zor+1o9+bidToXk1rLm5FZl7K00H4lu6obr+7aTAITepZKypbeg+5pPL0rx65dLQOlplTY1VRG7DKBZXBvq3Fe1vOsSopNyx/5D5zUtv2ID4n/rAu20541dgs0NlztRJdjW/j99p3/jBT+xn8K0ScRZZTjWhfstyzF+G+eediniyVHPvQh3YNXb9v7u/cxE25zrMx8zj0cyVlxeRDdtvXtIb/5TOfzuFZ3FePsrKQlOOuJ8NMc4HHajFKPuiZazuvHZ9EwEREIGBJ/Dz375oV8pOEXbofeVTHw1t95eiHsw6j1MQcuRKWEdKQVKbWQ6F35K0anOHVfwN/D67NU5NYdd2u3kwp9bMS7tk1tZlmOMtIzfM2cgfUO3OrD5FQAREQAREQAREQAREQAREQAREQAREQAREQARCCUhJGIql88THn33J8OUUhYyrMxO91M74na8FyHi8CK+Roij88jf+2R7i9/76K4jpkmdmoSeWWd8YN5D2f/7Hl2ymTaoXqqE+pPKFsYtmT5tkY8Cwt5JDtYN2GgrCnQcOm/VbdxvGGnDG4SteVrmuwze4bZqLz5OBLJq0j7/3XtsTwfPBHolrYeWI2RRmH333XVDVtJiJY4vsML+NO/aaSsRwZCyFWENCwtalaSIgAkOLwLmyMrNt70GolcZ3ilnr9nIC7vsv/c4HzZ7S4+bvjvyHnRzWC+rm56fLwMlYamOhYGOCrDA7d6Ec8ViPY2ippzy0cepajTkBZeFW7NM4KKv5cmaH4UH5M60E6pcFc2wMrYPdKJBKoMymUUlOcwpzfnJY22koGDkc5AxiIjIBBDMd0w4dO414afvMtIkll58V9ofI25J5s+xfm/bsN79+fp3/p05/T8byf/OF37XDB8OU6Jz5g1/6ql0mqCRkAhiqc5gtlMceNMarK4Gq7RSyiJ44dTb4M7in2IzRc/Hcuf/WG4dEKItzUOBVQfVYUlxkVaE2yZcvA+toPGtXLVlg49jxWcjjr4uhKuJBM4YvFZszJ423Q8Br6r1zW4/leG6PI7YhRwkw3IdLlNEFVi8mNCC8yKPPvGRjeX7mI55iMLj4u1bfZCfZoc5Q4X77P35haqCcY4xkp7jyL+OUXnfefINZMH2qufn6ReaWZYv9s3T6+9jpM+aXz79iKqAiHarG+3rDlp1m/NjCTnVNt7/pGLZ7983L7dfulIQc5kpGa25cZsYiNl8ThuWyHGpE/Duq8OrAmOf2DO6Z87iXnZ3H93XvbDPzMRpkCjIEB43l0397//3mLOb79dp19uew88MfqO6j/eEjD4bGjP7VC+vsyJJDJ8/2Skm478gx88y6jWbnoSPmxTfeMSWIE84QNhPGFZkP3XeH3Wbw7Ysok2kvbNhkP7dGMs/bL3hz5dieg8dM0qhEM3f6FNRju9YtZ06daBPkVOHeOFB6zC3e5bMIdeebli5ETO7weJzcHpWttGC8UapoaByqz/uR6kh3vdsfIm/LFsyEOneUeWHjZnPw8HH/T/bv8WPH2DidN8yZbaZPHN/l94GckI6ykyN6NKR5IKlqXSIw8gg89uzL9qCq8SxmneX3MYpgOup9rFdX4Zn/nV/8xry5eUe3YRSmIYvxp/JqTBayGg+W3ZHVCtVipaloazZV7WNMI4YdtyChyUgzKQlH2hnV8YiACIiACIiACIiACIiACIiACIiACIiACIhALwlISdgLYE5ReMuKZeaPP/GwVQ/6FYXMdMkeQ6coPI94Lp/96jd7sYWhNSvVgbQ/+Po/oAdzlPnh3/6pVQiOh5KBMWao+qMthSqjJ3Yc2TA3Qz1CRd2jT73QRRVQAyXiq+9stVmQP48ebnR+X1Zw3LnqeruJA2u9ODyul9L1XJ9EllCqR9y+9WR/Bmqe19DbTlu9YmmnVd60dJH97vb9T//+e2Y3YmgxZlQdFBsyERCB4Uvg5NmLZsPWXSjHjLk5RLnEYMx33Hg9ngmLzLtXr4Jap9m8uW23jcH6Fj5pThl96/Lr7Pe7EOeQxhhg/phadiLeqOCjHUEcWCoGXQBoOxFve6CooVLrLpSXfiWh+33ldfPN//3ql6wK8Zv/+nNTDzXRCazLGbfp4o/917c8ld7CWdPdz50+/9f3/sswltizb7xtlYTux7d27LZZnR95z93hSsK5M22MQavmQwbn0hOnzZvgyG1TOUlVPrlNKik2ty1f4lbb6dMdN5cLs+M4plo8v9grHaZmnzdjiuGLMdWYNW8XlO27wY4q+aL8PDMVyqnli+dZRaE7R2HbGcxpTMzA1/7jJ81zr79lYyQvjagyuR98Hhfm5Zrli+aZ7379yzY+2V/+84+saj0Yx3AJzgHtu//zT+zx8hjdM9X+EHn7/F992/bq26QjkdjB/t97+3c9VGv/9ye/MoVQod2GWMVMNjYdKsYw+/D9nhKMSlbG6Nu0e59VeZ2CWpYjFnJxfzHW3IJZUxGPuMiMhXI2FxlnoxnPM6+1VzftMC9GVGTR5r3W08sRj/Cx514xixGL871rbrW742I28gvrmn/yyQ/b6W40xjPr3rTf3Rvj1VF19rsPv8tMQ+Zoli3F4B40liPMhv3EK+vNc69uuPzzydNnobh81dTc0mhWr1xmPOXqlVEezFDJe2jKhLHm+3/1FcNETf/4H4/a5Z3q+P7bV9nvf/DR99vPaLHw3kadkKNLqhFTrzfW2tqOulQjEp602sXOoh747X971MybPcMsmEGVbCJiAU7stEpXrn7na39sp6/5nT+yn1RTuvokJ7wMVR7ra1/4+MOhSsKViLO9AvdaPmIOFuVkm91QE+7Hy9lEliFQbd+wcK758AN3Rs2PTrXvT1EfDjOXwfMUjqsDCVUmo0wMJgDkcg9A7XzfLSvNvbeuNCeRpXr3gSPmzIUye29Nh9J91uSJNgYr7/EwJWLYtqNNY7ZzmkuyFZyP7R8+p27GsyYfCkzGz6Qamcogqle5nJ9zcHl9FwERiC8Cj0eU6KcuXDTjUCd8/s1NpgztedatY5UVE1NazOyUVnN9Wp2Zgs9rYTdktJnMxFrzSn26OdnSddTKtdingdymlIQDSVPrEgEREAEREAEREAEREAEREAEREAEREAEREIFhSEBKwj6ctDfe3mL46k5RyNgvT3zn78xwVxRWQS1C+32oItkL+4F7VhvG26LKg8oLxgdk3BtnDZFYN8xiyN7Mo4g7eBS90lRAbEAvPi2sd4DZOQ9AZcc4SJ/52jetUuDLv/sRO7+L1UXlAe3k2fP28//8569MVW2tWY7eWmaivAdxelwmPTvDILx979Hf2K2UQM1A+28P3mc/ua/+Xtsp44tNe3ubOYZ9l5LQItKbCAxbAocQE5CvM1CM50FNQuWbX9nlDowZJadCyUNjfCva5xGbqy/289++YMvHDdt22eynwXXsRgZZvk4ja/BFxK9jXEAqXpwx7gtfMyZNMPfdCnUjnlGMPUZjBmSWWZOhrotl5YirypiqTyEz/XmU78FYdZugCuKrGbFXqdC79YbrrIrFrZNlIlXi11FRiBefBewx9ptfNeWf7v7+VaTnmTHVwuzpV9fbWHvXzZ1hlYn+ctg/P0cC8MURAGF27mKF2bxrv41tyH0dCrZj937zZcQBphLvi5/4AGInpkMpVnJ516hsuueW5Zbrw/fcZmP5HTvlqUUL87LtfGGKsssrwB9bsI2K6lqzDRm6mWl7oIznmmrIC7huPvO1b9lz88O/+VO7+mgqQHc9RlMcdrdvVJVyFMMbm3eaHz3+tI3t1t0y1/p31oX2o2wpg7LuS//rn2x27a9//pN2t7z7Z5Std3HCv/3df7fT3X1cgWUYc5D3Pu/nRNTNqAIMmlN0vfLWVquaO41z4jfGKuTrSSgMT6HOcuN1C80nH7rfzuK/Pxl/7n133mKnf/Ihr+7D+Hk0f73QTgi8nUSm6YamRrMZZdYeZDYOqxcGFon5lctTfXcQsQo/91d/b5WT//XNr9nyxtUd3Qrc9fS1z3lc/+6HP0XsyytxKl99a4udNTMz3UzH/RUsxyxTcL3/tlX2RbUrj9sdQ2Jigi2D3PaCn1RD//y3L9nYmFSNxrInX15v1aNf+NjDtiwKzuvUhawH8/XQXbd3msXt28WKalt3ZsZsd/ydZuzBl32Hj9m5WqOUvamRGLD/+8t/0Glt/xt8X9zwjjmBmORVvVSMdlqRvoiACIxIAi+u9+LE9vTgJiU3m9szG83E5PB6YE/X05/55qa2m+KkerOnKcGcNFIS9oellhUBERABERABERABERABERABERABERABERABERiCBKQk7MdJ2bxrj/nU146YG5FR8A8/9F6TMzqrUyY6ZlVkJskW9Jx/DzFbmKns6//0w35s8douysy8tH/91TMmBbGjvvXvj5lkxATKRwZJxgZiTCT2nl6srDF1jciO2NYB5Vz75Vcrsri5XtZYR8JMmS+jd5ud3y8jRiFtYkSl57ICn4z0ejPrIW0dMiDRvvGjn2Gfku3ffGvEfnB97EmllULNeBTZLLfuP2T+5vs/sdP45vaT8/fW3DF988devMTv//Jpu4rC3CwoLxOh1uFxd5gL6MVl1shoPbC93a7mFwERuPYE9kJt9fXv/Ngq9j6N+F/5iE9FFc9A2mubtkMxXWN+9Ju15tjJ0/aZErZ+Vxath2KbCrhlC+fYbKHjigvNokBsQaqBqLqeiMyXngXkfIENUKFE+4v/7/tWxXgKim8XMyswq/363GsbDVVKJ6EoX4H9mAHF3qxAfDDO6JSFYevwT2PsrrVvvGUnfQOqlFhGRTrtt8h8SiUc48XyvPTUGON2C+LnnjlXjuzUR8ycaVOs6rGny1/N+Zjlt6290by+ZZfZjwzVC2ZOM1/5vY/ac8m4fM7IleopvmZNnWAnh8UddPPzk5lyW/C84rOsFNyoJrwaxuum9MQpcwwjDB75f//SbuIf/+yL9nPmFG9f+7vdQ1h/6bFTZu2bm83LeNXj2c5RDkHVan+3czWXL0Od8SmoYjMzMmyWbyqWP4O6ZpgVYlQHLQ/xTGnJbnRHQEVoY8kBwmPI8LwTCr712/eYI+BEJXGYXUDG4xegSj4KNeFZZAOfPrnEfOSBu8JmvTzNxf27PCHwB1WSzOr7rX/7uTmG+pjLRh6Yrc9fqcTkfX8W/P71sadMDuqoj7z77tD1feDe1Xb6emSTvoBYkDsPlCLGYcvleRkvMDU1FQq4C1DpzTFL5s6ysa8vzxD5g3VfvrozxsZ8a+ceU15Zi+P3Yjh2t8zTkViRLMeKkaF64rgx9nrobjn3+2ubt5lXN26x19G4okIzDeewr0rCE4gJSmN26EJca7djnxifsjubgOfMfJRVzAYtJWF3tPS7CIhAdwSKEprNwtQmMzopdt21u/X05/cJye1mXFK7yU9IMkmjskwHos9GQof3Z7VDZlk5CftxKhobmgxf1bUNtsLjr1i41abBmYbBtXiw56E15KYOz08OYaG1o6LdhJcbwtWCv9kQSYFzLolOQgQ2rkcwaZprtNovvXjj+mnNCPZPw8Bd++mchByu5Dc3v39a2N922AUaWVxvVcTpGTZfb6a5RocbqtKIxiyttaXZDs/mcDxWzDl0hw08mQiIwMgh0IxOiCp0hnD4GO91djgMtLW2taL8aDJ1DfWmLpJQKtY22DHCMo4JBOqbm2KWO0lJV0JFxFqnK3svoiHNhi4GCccs3/k85Iv7wMD1rqMm1ja6+6028lyp9g0LDFumpdULYt3Q1AJuve+Y4TBmLsfOLjon69CwHSrGZypffM6U4RzwfNDp1trWtTrnntHBoZbRjoUOQiYp4bGzU9A9f6PN35/p7Cy7hNr0hbJKu5pYDue+bIfrZ2IehiOpqKyyzFzin76s71ot04A6JiuPld1c884x5z6j7i+vH/zY2NhsGDqA9RJ3v4Qt411bbSjf6m2iosqq0WGzdZrmrrtOE31f6CDkNlk2XERZ4upMvln6/SfPP19MwBdrfxh+gZaOsBB8Bc2VY9V1DXA0N2G/w4e2xdpGcJ31OKd0Wrs6Y/D34HeW+Vw/t83z4eriwfmifefzwHP4J1juHf14RrVh+zSySE/ryivaPrBtQDFBt9dntBVougiIgAj4CCSNumRS0S/Tsxqsb8EB/DMRrgn7gntwJFrXWuVIPMqrfExOUThvxjTz55/6SBdFISveVCUEMwxe5d266qt3DsAqVF4RZQqVGGwSb6yIu9/6uxNuPefQm+3Ztesx6OmxuHg8ZWi80VyvgjuWnq5H84mACAx9AmywtcMZxky72xBXi9l550ExN35sMWKk3mBjAE5FTCs28thIimWNaMzRqPBhvMBHn33ZNqT3QxXDBjUdkj0xV9bs2nfY/I/j/wol2SRzz43LrAJl2fw5VglekJsTc1XOMfb486/Z+X7y9Fr7eRBqs3Zk2uzOqeP24YkXXzNr178NVf1ss2LBXMRlnGzmITYjs68yQ23Q6IykE6EODelTyNRZj2PeAJVPLRx1v3jWi91l1VDBBUO+/+dvnrUqoC17D5mSImTURRZpxmOkY4CxIt0+0tFWBrXUCailmD13D+JuUSlD5db0SDzJkNVf00l0srTWtJlNO/eaz/7Pv7eK0PeuuclmOCbrhFEJl+PWRdtRxrHj84oxz+jk/u3rG61TtBqZagdDdcdtnz5/0e7eI1/5a/v5HmQCp917ywqTlZ5uZk2bZFJ9owPsj743dw6Pnz5vnVhUV/Ia3QkF6O6DR72RBP1wivg2dc3+bIBD+DFkGuY9U11bZ6/f96y5xe4PszvHMt5PrDW9jeuktrbePAN17cVKZHqGgu8CYm62IU5yT+w0srn/qux1ZD/PQYzHC1DTFZo1yHqckgKlaohCmOt0zqzDyCpN24VswexI4WiUKhxHNTPf4tjcObQzDeBbPcrMH//6WVOEMtllSmdGZr855x6zGLNc+zTiYV/EfUEnGPff7duTL71mXkA5RjXfHJSnzFo8eVyxyUJZko0svtGMmbiroMg9hzixb6AcY+zHp17ZgNl7Xk9uw37Rvvz338V9bczHHrgbccELMYppoW1vcNQSO3t4P/F8H0UM0srqGqvWJfst+w6aHftKzVwo+Rg7dyDsXxCLm+xOQynObNsP3LYK12W6LVfDFMt83kwEL8awlImACIhAfwkkwTGXntBhUhKuvV8gM/GSycR+NKETrvlS94ry/h77YC0fu8UyWHsxzLfjFIUX8yujKgrZ6OGw05FoXu/81blJcb9Zc4634cDPVSrb2q8Ok+HAQPsoAvFCwN3vbOzylYAOkwtwfqUkp9gGMVVcbp7umLj5GqECZGOaThw6B8vhxOK6e2MsO6mwboWzkR05VXAQ5Oci9AIakont3VdinOqKCiKaS4xAdY5r/Pdkf+jYbMGxVMEhQAdHI/aJ+xBrHeTAl1UcRfafTqzuFITB/aGChq/KmmqohJLh+Gq22w06GbkvdLrRMUblEdVn3BYdiUPVHCM6BajGSsWoBSotuc/23KHy3J25hAaVcGLQCcv18DqjYsmd/+7W0d/fncKUjhlaRUThz/pSTxWQXI7OLutcxnXCofFUybnRAu6+4nzD1epxXDzX5RipwWu1pfXKkNhYx8RaCI+fTn2qiiuRiO481Jt0XPFe7Km10imNFxPElVdVGY6S8fYhej3HcW9t9dTVtVDjsfOD11kNygLvOuv+Ou3pPobNRxVeGoYLUyEby/IxdJZOQjrX6fxyzkO3TBOUl81QJlPR6S/HOhBKJpbxnLG844vLVbNswfXZG3Mcy3CPcL8qsA85ozPt9c7f+I9m/8Z33lN8fpA374UafHIIdncdO73ZJx4D94XPJ+oDLqHBznI12tWQALkN7+cEhOCRiYAIiEB/CYxCacOyZygY98Pbn6GyRwNDZVTRygeilekDs4U4Wks64nJMgmKE2RL/GL2SrBTsP3oclYJ68y+/eNI+0MtROZKJgAiIgAiMTAJsRDPDI+O2FiBOGLOLMvbfKDQ+C7Iz0UhKMGPyEH4CxgYk7TwyJNPKIjHg2JiknUEcLBodbbGcanamkDdbXUFDLhNql9FQezATLl90KI1FhktmxczJzMSSmBP/6RiiA4B2DkM07WdExX3hgqfmpoOiN9Z5HzJMBuKrZXE/oCgpzGE822QoUDLRwPUUhHSQnkFjmOoZOu3olKxFQ5TbdU6f3myf8+bCAcBYtYX5OTgvKSYH+8ChhV4D21gVXQ0cbE0R5yy355wLqRhSl5GeaiaM65r1maMEqNjhPjs+bt9cls/FUPWFGR0SbFIfKD2O8ByeIzZsvu6msaGeDBVRMo6LcensdYf4i7zOxkJBxd8LIorNRjgOaOcqPIdcGRxp7TjnZyPhO1z9xDkbutv2QP7O/aTlR2LrjSnMt98LcCz8icfAe2k0zh1VU4zvy6H9tfik46kS9Sx+cjodIhzi3hvHOuMr52AbabhXS4qL7LaDb86BWYqYej2xaVMn4lrPsAriMHUVHe90jnoOuO4VfXSyjIZziPdMPu5f2sTIvhbleTEJeV0z8y4dSayDVtIZBwch991+IjayHVaOa7YvZQr3ISuyDwW2DEk04xAnjzFOC3O8fXJZjUtPn7H7WAFlKq2mzvs8jXimtO6us7Fji3CfplpFLMutoLHzg2pEDpmmEzXMeF1lYNnJqJvTsqB2CzM6mGnMskwjG+6fM1eO5eGYyZ+xH/mZg7I1F0pCKuTSfSo5ntMa3Nd1uA7LsY8svziE35YZcPTS/Ot324n16a6hIqiiqR7MHp1l44LnsWxH+4PqRzrX2dFBByzvAXYUNTAeJ5TZ2bi+GZ+R6kc3zNq/Pc5/Gs8clrndhbVw+zIO54hWUjzGNtjJgvHJeR0mJibZIf/NcGifgmKYnRiMcRkWmsm/H/pbBERABLojcF9WpflwboPJTWg1U1Jjd9Z0t66+/t58aZRpxWPiL8+NNq80FKCjBKMp+7qyIbicnIRX4aTMgaT/7770aTgFWzDM+IBVcPwQTkKZCIiACIhAfBJgLCaqVejoGB9p2LvYUC4YPFVCV9OcI4aOJAad9xxKXsOev9Gp4EI7nC/3HEkDrShz+8AGdR6cpmxcc9gxG+V00lHtdzLiROiLE6Mn/Oi4oaOURkcdh3m7od49WX4oz0MHEZ1ovM7GwtHGWGBF+Z5Tmk4EGodV09iB6RzVdsIQfON54jVTXFhgjyUXTg46qqhgojODClkq4ujkGUil1BBEEbpLLmwAh//S6IAnL28oeYcpg9Ofjine2wN9L3N7dBbl4f6lY3AsnFc0nh/antKj9nOk3Fv2YCJvrhyzw43heGRHh9/xxmuSqkM73BhOQlpvnYKRTXX7kQdHOp2EDBFBBSHjBrohyt0uPEAzOMewuz95HbIMqoHzluU6nffOETtAm9RqREAE4pjAnZnV5sGcRjMmqdnMTB34WOA9QdtAJ2HHKPPVc9nmtQbv+deT5YbLPHISXoUz5RSFrJQxWy4fjK6H/ipsTqsUAREQAREY4gTYqKTzhsPZqFqiuUYjG/G0wXJyUPXDhry3T1eijtCJ4ALTM1kKzSemsd8H6o2NSmYDTeAnHA3cDofu0WnleDg+A7VNtx5u2zXyOY3OyKHuLHP73t2nUzzReUOF4Sic6yQoemjuGFvQgUkbDom0nGKJDm0aHQ88d3Sw8/rg9cpPKiKv1vViNzxE35xDLvkyHy+UQOvlMsWLU8fdvxp8bBmCc8Iyhcpkmru3qEyjuevOfhlhb8FyzB2eLVNwjVIxzLbA1TQ+T/hcobLWDvnF/XA1znWsY3Dn3JWtNtMz7tN2DH3mvpDBYO9TrP3VbyIgAsObwKK0BnNzRhMchPVmTZZXXx3sI9rTnGhOtqaaf6/MNvuaosemHez9GqjtXWkdDNQatR471OXAoSMiIQIiIAIiIAKWABtIVD7RqDK/lkZn4GVVR2QI6mDvDxuNXuN58Ct3V7vRPtgs/duzAyTpNAPfK5m2e5bwxr+eofK3czAxtqSsKwHXseA+u85xdafYcg2OWtrlMuXqbnJIrf1almMOhHuuuO/X4tM5AC9fh4NfrF+Lw9Y2RUAErhGBFkQAr+5INI3XcHxvLeJ7l7clm7YRlKzEfzrlJPTT0N8iIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAJDjsCZ1mRkEoaC/VK9eSD72vRKHG5OMBsb001ZuzfSYchB6ucOdZ/isJ8b0OIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIi0B8CLXAQVrYlGcYFvFZW044kYe2JUBJeu324mscuJeHVpKt1i4AIiIAIiIAIiIAIiIAIiIAIiIAIiIAI9JtAawfisI66ZI62Zpk36tvMuKRWMyO136vt0QrOtI7CMOMEc7Al3ZyAorERyUtGoklJOBLPqo5JBERABERABERABERABERABERABERABEYQAaaDaqWasCPZlLZkmrOIDThYVt6WaM60pZsL7amGcQmlJBws8tqOCIiACIiACIiACIiACIiACIiACIiACIiACIQQONuWYp6tG2VuTGszc9PaTYq5ZLITbQq3kLn7N6kNikGueVdTotncmGHOtKb0b4VDfGkpCYf4CdLuiYAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIeAQaMez4cHOqOdKaauoQH7DxKmYapnqxDa8TLclmf0satpU4ok+DYhKO6NOrgxMBERABERABERABERABERABERABERCBEUQA0j7mDTkFVd+zNWmmALEJb8zsMGk4xDHJA6MorIOCsA2r2tyQaCoxvPgAHIRV+GwdmNUP2ZMhJ+GQPTXaMREQAREQAREQAREQAREQAREQAREQAREQAT8B+uku4e18W6pZW59kJia3mAnJNSY7oQ1Owlb/rH3+ux5qRSoW32gYbY63ppnDSFbCaSPd5CQc6WdYxycCIiACIiACIiACIiACIiACIiACIiACI4wAk5hUYLhxy6Vk8+vqdJOf2IbkIh0mM+GSmYLQgUmIJji2h8rC8vZRph3rK202pgUqwu1NUA52JJldGNZc055kmq/ikOahdFrkJBxKZ0P7IgIiIAIiIAIiIAIiIAIiIAIiIAIiIAIi0C0BOglb4dyraU+xCUVGJ3Yg83G6KUpqM8mjGkxqQjuchC3droczlLcnW+fghoYs0wDF4Mv1GaYaDsh4MzkJ4+2M63hFQAREQAREQAREQAREQAREQAREQAREYIQRaO4wiB2YbE60JpoyZBtJNu1mR2oHFIXGFEcUhQVJXlDBqjYENYSdbfU+D7RmmFYoCI9gCDOdj014xaPJSRiPZ13HLAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIjiEALhgSfaME4Y9iB5jSTOOqS2dKUbVIw/HhBKsYRw2ameMrC44gxSOOwYtrJ1iQ73Nh+ieM3OQnj+OTr0EVABERABERABERABERABERABERABERgJBLogBqwAY7DpnaD5COeU7ABakNaBeIM0mojyUg4r4xxHGUiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiMIIIcGBxTbuXkbiqPTVyZO5zBB3oAB7KyM/fPICwtCoREAEREAEREAEREAEREAEREAEREAEREAERGIkE5CQciWdVxyQCIiACIiACIiACIiACIiACIiACIiACIiACvSAgJ2EvYGlWERABERABERABERABERABERABERABERABERiJBOQkHIlnVcckAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAr0gICdhL2BpVhEQAREQAREQAREQAREQAREQAREQAREQAREYiQTkJByJZ1XHJAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAK9ICAnYS9gaVYREAEREAEREAEREAEREAEREAEREAEREAERGIkE5CQciWdVxyQCIiACIiACIiACIiACIiACIiACIiACIiACvSAgJ2EvYGlWERABEfj/27FDIgAAAARi/VuTAfs3j2E4CBAgQIAAAQIECBAgQIAAgaKAk7C4qk4ECBAgQIAAAQIECBAgQIAAAQIEDgEn4YElSoAAAQIECBAgQIAAAQIECBAgQKAo4CQsrqoTAQIECBAgQIAAAQIECBAgQIAAgUPASXhgiRIgQIAAAQIECBAgQIAAAQIECBAoCjgJi6vqRIAAAQIECBAgQIAAAQIECBAgQOAQcBIeWKIECBAgQIAAAQIECBAgQIAAAQIEigJOwuKqOhEgQIAAAQIECBAgQIAAAQIECBA4BJyEB5YoAQIECBAgQIAAAQIECBAgQIAAgaKAk7C4qk4ECBAgQIAAAQIECBAgQIAAAQIEDgEn4YElSoAAAQIECBAgQIAAAQIECBAgQKAo4CQsrqoTAQIECBAgQIAAAQIECBAgQIAAgUPASXhgiRIgQIAAAQIECBAgQIAAAQIECBAoCjgJi6vqRIAAAQIECBAgQIAAAQIECBAgQOAQcBIeWKIECBAgQIAAAQIECBAgQIAAAQIEigJOwuKqOhEgQIAAAQIECBAgQIAAAQIECBA4BJyEB5YoAQIECBAgQIAAAQIECBAgQIAAgaKAk7C4qk4ECBAgQIAAAQIECBAgQIAAAQIEDgEn4YElSoAAAQIECBAgQIAAAQIECBAgQKAo4CQsrqoTAQIECBAgQIAAAQIECBAgQIAAgUPASXhgiRIgQIAAAQIECBAgQIAAAQIECBAoCjgJi6vqRIAAAQIECBAgQIAAAQIECBAgQOAQcBIeWKIECBAgQIAAAQIECBAgQIAAAQIEigJOwuKqOhEgQIAAAQIECBAgQIAAAQIECBA4BJyEB5YoAQIECBAgQIAAAQIECBAgQIAAgaKAk7C4qk4ECBAgQIAAAQIECBAgQIAAAQIEDgEn4YElSoAAAQIECBAgQIAAAQIECBAgQKAo4CQsrqoTAQIECBAgQIAAAQIECBAgQIAAgUPASXhgiRIgQIAAAQIECBAgQIAAAQIECBAoCjgJi6vqRIAAAQIECBAgQIAAAQIECBAgQOAQcBIeWKIECBAgQIAAAQIECBAgQIAAAQIEigJOwuKqOhEgQIAAAQIECBAgQIAAAQIECBA4BJyEB5YoAQIECBAgQIAAAQIECBAgQIAAgaKAk7C4qk4ECBAgQIAAAQIECBAgQIAAAQIEDgEn4YElSoAAAQIECBAgQIAAAQIECBAgQKAo4CQsrqoTAQIECBAgQIAAAQIECBAgQIAAgUPASXhgiRIgQIAAAQIECBAgQIAAAQIECBAoCjgJi6vqRIAAAQIECBAgQIAAAQIECBAgQOAQcBIeWKIECBAgQIAAAQIECBAgQIAAAQIEigJOwuKqOhEgQIAAAQIECBAgQIAAAQIECBA4BJyEB5YoAQIECBAgQIAAAQIECBAgQIAAgaKAk7C4qk4ECBAgQIAAAQIECBAgQIAAAQIEDgEn4YElSoAAAQIECBAgQIAAAQIECBAgQKAo4CQsrqoTAQIECBAgQIAAAQIECBAgQIAAgUPASXhgiRIgQIAAAQIECBAgQIAAAQIECBAoCjgJi6vqRIAAAQIECBAgQIAAAQIECBAgQOAQcBIeWKIECBAgQIAAAQIECBAgQIAAAQIEigJOwuKqOhEgQIAAAQIECBAgQIAAAQIECBA4BJyEB5YoAQIECBAgQIAAAQIECBAgQIAAgaLAAHC4kpjguF27AAAAAElFTkSuQmCC" alt="header">
        """

        st.markdown(image_html, unsafe_allow_html=True)

        st.markdown(
            """
            <style>

                div[data-testid="column"]:nth-of-type(2)
                {
                    border:1px solid lightgray;
                    text-align: left;
                    padding: 10px;
                    border-radius: 8px;
                } 

                .payment-method-box {
                    border: 1px solid lightgray;
                    padding: 10px;
                    border-radius: 8px;
                }

            </style>
            """,unsafe_allow_html=True
        )

        with st.container():
            col1, col2, col3 = st.columns([1, 6, 1])
            
            with col2:

                st.markdown("<p style='margin-top:3px; font-size:20px; color:#01394D;'> ✅ &nbsp;&nbsp; Your details</p>", unsafe_allow_html=True)
                st.write()
                st.markdown("<hr style='border: 0.5px solid lightgray; margin-top:8px;'>", unsafe_allow_html=True)  # Add line break

                st.markdown("<p style='margin-top:3px; font-size:20px; margin-top: -5px; margin-bottom:20px;' color:#01394D;> ✅ &nbsp;&nbsp; Your addresses</p>", unsafe_allow_html=True)
                st.write()
                st.markdown("<hr style='border: 0.5px solid lightgray; margin-top:-5px;'>", unsafe_allow_html=True)  # Add line break

                st.markdown("<p style='margin-top:-10px; margin-bottom:-10px; font-size:20px; font-weight: bold; color:#01394D;'> ③ &nbsp;&nbsp; Payment method </p>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 6, 1])
                with col2:
                    st.write("<style>div.row-widget.stRadio > div{flex-direction: column; margin-top: -50px; margin-bottom: 20px;}</style>", unsafe_allow_html=True)
                    st.write("<style>div.row-widget.stRadio > div > label{margin-bottom: 20px; font-weight: bold;}</style>", unsafe_allow_html=True)
                    st.write("<style>div.row-widget.stRadio > div > label > span{font-size: 16px; font-weight: bold; margin-top: -100px;}</style>", unsafe_allow_html=True)
                    
                    payment_option = st.radio(
                        "",
                        ('Credit/Debit Cards', 'Bank Transfer', 'Installments'),
                        format_func=lambda x: x if x != 'Credit/Debit Cards' else 'Credit/Debit Cards 💳'
                    )

                    # Handling payment option selection
                    if payment_option == 'Credit/Debit Cards':
                        pass
                    elif payment_option == 'Bank Transfer':
                        st.write('May affect your delivery date.')
                    elif payment_option == 'Installments':
                        st.markdown("<p style='margin-top:-40px;'> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Available for selected credit cards.</p>", unsafe_allow_html=True)
                        bnpl_option = st.selectbox("BNPL", ["SAB"])

        st.markdown("""
            <style>
                .big-font {
                    font-size:30px !important;
                }
                .coupon-code-container {
                    display: flex;
                    align-items: center;
                }
                .coupon-code {
                    flex: 4; /* Increase width of coupon text box */
                    width: 70%;
                    border-radius: 5px;
                    border: 1px solid lightgray;
                    padding: 10px;
                    background-color: white;
                }
                .apply-btn {
                    flex: 1; /* Decrease width of apply button */
                    width: 30%; /* Adjust button width as needed */
                    border-radius: 5px;
                    padding: 10px;
                    margin-left: 10px;
                    border: none;
                    background-color: #92b0d5;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)

        # Coupon Code
        st.markdown("""
            <div class="coupon-code-container">
                <input class="coupon-code" type="text" placeholder="COUPON CODE" key="coupon">
                <input class="apply-btn" type="button" value="APPLY" style="font-family: Arial; font-size: 13px;">
            </div>
        """, unsafe_allow_html=True)


        notes_dict = {
            'Available Cash': 2363.64
        }
        st.markdown(
            f"""
            <div style='padding: 10px; display: flex;'>
                <div style='flex: 1; color: #01394D; font-family: Arial; font-weight: bold; font-size: 18px; text-align: left; margin-top:50px; margin-bottom:20px;'>
                    <span>Total:</span>
                </div>
                <div style='flex: 1; color: #01394D; font-family: Arial; font-weight: bold; font-size: 18px; text-align: right;  margin-top:50px; margin-bottom:20px;'>
                    <span>SAR {notes_dict.get('Available Cash'):.2f}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("""
        <style>
        .stButton>button {
        display: flex;
        width: 100%;
        border: none;
        #    margin-top: 150px;
        background-color: #01394D;
        color: white;
        padding: 14px 28px;
        font-size: 36px;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
            }
        </style>
        """,unsafe_allow_html=True
        )

    # Continue button
    if st.button('CONTINUE TO SAB'):
        st.write('Continuing to SAB...')
        placeholder = st.empty()
        st.session_state.checkout_step = 1
        st.rerun()


def generate_fake_traffic_data():
    traffic_dates = pd.date_range(start="2023-01-01", end="2023-08-01", freq="MS")
    traffic_data = [{"date": str(date), "traffic": random.uniform(1000, 1500)} for date in traffic_dates]
    return traffic_data

# Call this function to generate fake duration data
def generate_fake_duration_data():
    duration_dates = pd.date_range(start="2023-01-01", end="2023-08-01", freq="MS")
    duration_data = [{"date": str(date), "average_visit_duration": f"{round(random.uniform(0, 30),2)}%"} for date in duration_dates]
    return duration_data


def save_data_to_sheet(url, timestamp, traffic_data, duration_data, sheet):
    traffic_json = json.dumps(traffic_data)
    duration_json = json.dumps(duration_data)
    data = [url, timestamp, traffic_json, duration_json]
    sheet.append_row(data)


def add_website_and_bank_account():
    print(f"\n\nchekcout step tracker: {st.session_state.checkout_step}")

    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 400px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .logo {
                        text-align: left;
                        margin-left:-10px;
                        margin-bottom: 40px;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 30px;
                    }
                    .htext {
                        margin-top:30px;
                        text-align: left;
                        color: #333;
                        margin-left:-10px;
                        margin-bottom: 30px;
                        font-size: 30px;
                    }
                    input[type=text], input[type=password] {
                        width: 100%;
                        padding: 10px;
                        margin: 10px 0;
                        display: inline-block;
                        border: none;
                        border-radius: 7px;
                        box-sizing: border-box;
                        background-color: #f3f3f4;
                        color: lightgray;
                    }
                    .footer {
                        text-align: center;
                        margin-left: 30px;
                        margin-top: 20px;
                        margin-bottom: 10px;
                        color: #a0a0a0;
                    }
                    a {
                        color: #01394D;
                    }
                    a:hover {
                        color: #c53030;
                    }
                    .st-emotion-cache-16idsys p{
                        font-size:16px;
                        margin-left:5px;
                    }
                </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="logo">
                        <img src="data:image/png;base64,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" alt="Logo">
                    </div>
                    <p class="htext" style="font-weight:light;">Additional information</p>
                    <p style="font-weight:light; color:#333; margin-top:-25px; margin-left:-10px; font-size:16px;">We need a few more information about your company</p>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)

    company_url = st.text_input("Company Website: ", placeholder="Eg. https://nymcard.com")
    st.session_state['gsheet_data']['Company_Url'] = company_url

    traffic_data = generate_fake_traffic_data()
    duration_data = generate_fake_duration_data()
    timestamp = str(datetime.now())
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(GDRIVE_CREDS, scope)
    client = gspread.authorize(creds)
    sheet = client.open("streamlit_data").worksheet('similar_web_data')
    save_data_to_sheet(company_url, timestamp, traffic_data, duration_data, sheet)

    scrapes = {}
    sentiments = {}

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

    max_len = max(len(tweet_list), len(ig_post_list), len(google_reviews_list))
    
    tweet_list.extend([''] * (max_len - len(tweet_list)))
    ig_post_list.extend([''] * (max_len - len(ig_post_list)))
    google_reviews_list.extend([''] * (max_len - len(google_reviews_list)))

    scrapes['Twitter'] = '\n'.join(tweet_list)
    scrapes['Instagram'] = '\n'.join(ig_post_list)
    scrapes['Google'] = ''
    st.session_state['gsheet_data']['Social_Check'] = json.dumps(scrapes)

    sentiments = {"Twitter": 0.70, "Instagram": 0.80, "Google": 0.60, "Average": 0.70}
    st.session_state['gsheet_data']['Sentiments'] = json.dumps(sentiments)

    custom_css = """
    <style>
    .st-emotion-cache-1gulkj5{
        background-color: white !important;
        margin-bottom: -70px !important;
        border: 1px solid lightgray;
        margin-top: -60px;
    }

    .st-emotion-cache-16idsys p{
        margin-left:18px;
        font-size: 18px;
    }

    .st-emotion-cache-9ycgxx{
        color:white;
    }

    .st-emotion-cache-1aehpvj{
        color:white;
    }

    .st-emotion-cache-7ym5gk{
        position:absolute;
        display: inline;
        margin-top: 10px;
        margin-left:180px;
        margin-right:50px;
        border: 0.5px solid red;
        border-radius: 100px;
        color:#d3d3d3;
        width:120px;
    }
    </style>
    """

    # Inject custom CSS with components.html to affect Streamlit's default styles
    st.markdown(custom_css, unsafe_allow_html=True)

    st.markdown(
        """
        <style>

            div[data-testid="column"]:nth-of-type(2)
            {
                border:1px solid lightgray;
                text-align: left;
                padding: 20px;
                padding-bottom:50px;
                border-radius: 8px;
            } 

        </style>
        """,unsafe_allow_html=True
    )

    st.markdown("<hr style='border: 0.5px solid lightgray; margin-top:5px; margin-bottom:5px;'>", unsafe_allow_html=True)  # Add line break

    bank_doc_file = st.file_uploader("Upload Bank Statement", type=["pdf"])
    if bank_doc_file:
        print(f"checkout_step: {st.session_state.checkout_step}")
        
        uploaded_pdf_content = bank_doc_file.read()
        file_name = bank_doc_file.name  # Get the file name
        file_id = upload_to_drive(uploaded_pdf_content, file_name)
        pdf_file_url = f"https://drive.google.com/uc?id={file_id}"

        st.session_state['gsheet_data']['BANK_STATEMENT'] = pdf_file_url
        expense_data = {"Month": ["2024-01", "2024-02"], "Revenue": [50000.0, 60000.0], "Expense": [40000.0, 45000.0], "Free Cash Flow": [10000.0, 15000.0]}
        st.session_state['gsheet_data']['Expense_Data'] = json.dumps(expense_data)
        print(f"\n\n4th: {st.session_state['gsheet_data']}\n")
        data = pd.DataFrame(expense_data)
        st.success("Completed ✅")

    st.markdown("""
        <style>
        .stButton>button {
        border: none;
        border-radius: 25px;
        cursor: pointer;
        margin-left:0px;
        display: flex;
        width: 100%;
        border: none;
        margin-top: 320px;
        background-color: #e53e3e;
        color: white;
        padding: 14px 28px;
        font-size: 36px;
        cursor: pointer;
        text-align: center;
            }
        </style>
        """,unsafe_allow_html=True
        )

    if st.button('Continue'):
        st.session_state.checkout_step = 8
        st.rerun()

def nafath_check():
    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 500px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .logo {
                        text-align: left;
                        margin-left:-10px;
                        margin-bottom: 40px;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 30px;
                    }
                    .htext {
                        margin-top:30px;
                        text-align: left;
                        color: #333;
                        margin-left:-10px;
                        margin-bottom: 30px;
                        font-size: 24px;
                    }
                    input[type=text], input[type=password] {
                        width: 100%;
                        padding: 10px;
                        margin: 10px 0;
                        display: inline-block;
                        border: none;
                        border-radius: 7px;
                        box-sizing: border-box;
                        background-color: #f3f3f4;
                        color: lightgray;
                    }
                    .footer {
                        text-align: center;
                        margin-left: 30px;
                        margin-top: 20px;
                        margin-bottom: 10px;
                        color: #a0a0a0;
                    }
                    a {
                        color: #01394D;
                    }
                    a:hover {
                        color: #c53030;
                    }
                    .st-emotion-cache-16idsys p{
                        font-size:16px;
                        margin-left:5px;
                    }
                    .st-emotion-cache-fqsvsg{
                        margin-top:15px;
                    }
                </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="logo">
                        <img src="data:image/png;base64,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" alt="Logo">
                    </div>
                    <p class="htext" style="font-weight:light;">Address and Nafath Verification</p>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)

    ## TODO: nafath code

    company_address = st.text_input("Company Adress: ", placeholder="Eg. Khaled bin waleed street, Jeddah")
    address_dict = {"user_address": "al salam tecom tower, al sufouh, dubai internet city", "google_address": "Al Salam Tecom Tower - Al Sufouh - Dubai Internet City - Dubai - United Arab Emirates"}
    st.session_state['gsheet_data']['Address'] = json.dumps(address_dict)

    custom_css = """
    <style>
    .st-emotion-cache-1gulkj5{
        background-color: white !important;
        margin-bottom: -70px !important;
        border: 1px solid lightgray;
        margin-top: -60px;
    }

    .st-emotion-cache-16idsys p{
        margin-left:15px;
        font-size: 18px;
    }

    .st-emotion-cache-9ycgxx{
        color:white;
    }

    .st-emotion-cache-1aehpvj{
        color:white;
    }

    .st-emotion-cache-7ym5gk{
        position:absolute;
        display: inline;
        margin-top: 10px;
        margin-left:180px;
        margin-right:50px;
        border: 0.5px solid red;
        border-radius: 100px;
        color:#d3d3d3;
        width:120px;
    }
    </style>
    """

    # Inject custom CSS with components.html to affect Streamlit's default styles
    st.markdown(custom_css, unsafe_allow_html=True)

    st.markdown(
        """
        <style>

            div[data-testid="column"]:nth-of-type(2)
            {
                border:1px solid lightgray;
                text-align: left;
                padding: 20px;
                padding-bottom:50px;
                border-radius: 8px;
            } 

        </style>
        """,unsafe_allow_html=True
    )

    st.markdown("<hr style='border: 0.5px solid lightgray; margin-top:5px; margin-bottom:5px;'>", unsafe_allow_html=True)  # Add line break

    id_data_file = st.file_uploader("Upload Iqama ID", type=["pdf"])
    if id_data_file:
        image_id_urls = []

        uploaded_id_content = id_data_file.read()
        file_name = id_data_file.name  # Get the file name
        file_id = upload_to_drive(uploaded_id_content, file_name)
        file_url = f"https://drive.google.com/uc?id={file_id}"
        image_id_urls.append(file_url)
        id_image_combined = ', '.join(image_id_urls)

        id_data = {"Name": "M ZOUHER JADID", "DOB": "1985/10/24", "ID Number": "2325873335"}

        st.session_state['gsheet_data']['ID_Data'] = id_data
        st.session_state['gsheet_data']['ID_Image'] = id_image_combined
    ###################

    st.markdown("""
        <style>
        .stButton>button {
        border: none;
        border-radius: 25px;
        cursor: pointer;
        margin-left:0px;
        display: flex;
        width: 100%;
        border: none;
        margin-top: 350px;
        background-color: #e53e3e;
        color: white;
        padding: 14px 28px;
        font-size: 36px;
        cursor: pointer;
        text-align: center;
            }
        </style>
        """,unsafe_allow_html=True
        )
    
    if st.button('Continue'):
        st.session_state.checkout_step = 9
        st.rerun()


def show_split():
    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 600px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .logo {
                        text-align: left;
                        margin-left:-10px;
                        margin-bottom: 40px;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 30px;
                    }
                    .htext {
                        margin-top:30px;
                        text-align: left;
                        color: #333;
                        margin-left:-10px;
                        margin-bottom: 30px;
                        font-size: 30px;
                    }
                    input[type=text], input[type=password] {
                        width: 100%;
                        padding: 15px;
                        margin: 10px 0;
                        display: inline-block;
                        border: none;
                        border-radius: 7px;
                        box-sizing: border-box;
                        background-color: #f3f3f4;
                        color: lightgray;
                    }
                    .footer {
                        text-align: center;
                        margin-left: 30px;
                        margin-top: 20px;
                        margin-bottom: 10px;
                        color: #a0a0a0;
                    }
                    a {
                        color: #01394D;
                    }
                    a:hover {
                        color: #c53030;
                    }
                    .card-input {
                        margin-bottom: 10px;
                        padding: 10px;
                        font-size: 16px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        display: block;
                        width: 100%;
                        box-sizing: border-box;
                    }
                    .card-details {
                        display: flex;
                        justify-content: space-between;
                    }
                    .card-details div {
                        width: 48%;
                    }
                    </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="logo">
                        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIIAAAAoCAYAAAAyhCJ1AAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAgqADAAQAAAABAAAAKAAAAADc5UDnAAAbMUlEQVR4Ae1cB3xUxdbfu33TC0gJkEAgkIQUIk2aEB5GVNDHEz4RecIHkigCKpHuIwgivSkofiiPZw8IiBQBpUMEQxISUjaFdBKSTdve73fOvTtbkk2yweh73/dz/LF3ypkzZ87535kz506kOH+m/wsaoGiaZuSkKIrNdLLUVCfz+5Pd76CB/fv39zl//vys+vp6bkxMzK5t27apOnsYfmcztOcHKEag/UeADd4ks71sf0Tefv4PO/6+fft8r127+kZpafGC7t17nIyOjuah7Pa8sYgrBSSu3byYOrtym9nfDQgFi/aIshJejxHS/F6qiko/CmTlcJg5MAKZOSYO167cppTWRhPkbDys1a1keBTowtvTxPPvosrZuf9C2JvxVa2Q/i7Vy5Yt619VVTVGKBTSy5cvP7Z58+amjg7U0NDQW6GQx/bu3acyOnrI3sLCQiXyWLp06YDa2uqxPJ7QxOVyvwMQKLdv3z4qKysjAnRk6t69+49AVubqeL8LEOjUVEHaxl1z9AX50znRg7/V5uQmmOsbIwlicYlwttE1XzpohoqlpmBhad6H0GN9S540hysSmgShA4/xGhv96Ozs5wr37n2r/8KF5a4q57fS5ebmTpRKc3eKROKm/v0HXAJ+HQbCgwcPBsG/riaTSaxWq9fGxDz6FvDJvH+/fNTt22kf0bRZAWA4B3XKrKw78365eetl2kzrg4L6Toe6fx8QspOThXe27HlJfSt1A9dkqOvx/LPfiAKCMmr/9UUyrVQGoTXbMigID4k1LTE+ebJtjkYnvGygsVAJ+CZRaOixbs9MWCK7fOtdTa50dv2XOl328qRV4ZuTXFYQGfNhnhbgE7w+DAvO0KFDT7m5uRWZzWaeQCAwd+vWjaxquDQ68IbdgWr5Qrg2rP2e4lqPNqhg4nzNocPzlCm3tnHk8i5gUG4d0A/c9I9f/adOTuD5+d6xFx39XwfBiVWh1qEeeBBaMnOHJ9OP7YPiUUKBUdQ38Mvgf+6d33vZsiqzCd4bo1Goz86dqTh5el/Zp1/3RLo/KjHWecjBZs+erS4ulurOnj0z5Pz5H0MWLVoka4cVUU07ZI7NnQaE4oMHxRnTXorX3sl8z9yk8LWcdmA0f2bEQR/tOuf9+NiFvC5+dwkYGFfSIo/FlqSJqbWfEdIiDfmHBNa8hRDLlJtYJw4L+dxn2LBVfsHBzFJMARDQRTGbaa6hvGJy5b6PduZs2BYIwLUfAln+R6aGBlWsUqncp1Zr/wECtiEzY05UQ4dTp/gIBXv2iJp+vPyKJj19hVmu8MW3t7k0Fq/2xt34xSuaTp/dZpYrBxEiMjPsg/+wTJ6krfnMSDs+MTF0IlgJQvof6frS7NVB8bPJEgoeNjazlJDnGouKn1V+/4M5J798OXRFn4GwQVadnpozT0pK4mo0ml5paWl+Wq3C+jKKxZ7myMjICnD6HN56OPAgDff3BO5vBsKNHTskjcfPzdMVFKynm5ReqFLbxG051K4FDKczZ86Vq3759UNjfUMEayTnunfsbQMIgYl9O6wEGn5Az6/5UdHvBC54qZoTP7sZUxukaJNRpMsvnE4bDKa8JcvWD9y1OR9la9ah04q2kTmcgwcP+pw8efK/ZbLa6dXV1eEmk5EHBmbG8vXVGxsaZCj4CVcHxzMxOgu/NVnR+DCMLl68yJfcynxJW1C4FrYDb4JY68TN1pyVPSo88uuD1zxixy3ld+2SBfsnowWkJNTEIqSMnTFP6gklaecKBWZJeNg3Xk9OXhPz4Zb7LY1q6832gUHB+dKXlE9v+PnS1pKt+7rhGJ2diD4IXyzfvZv5cmFh/obKyoqRfD6XHxTUV+nr54fnYjeQ2xOcwhYvZ1svixMDErWQYV16OuHjUj8OnZwt9Nm5f6465de1HLnCn1jJpnLkYzOdPVc0VMSn+372mhz7GtfDvdC2cBMTOxrefmYkT8ahxCKdoH/wl5KJj60O27jauh3Yj0dWENIH25iTiMkkNFZUxcmOJG/JeXvNgOaGc+ThvAR9uBD5E+DTOYWtFmIAwhs3bkyCY6DE09OrZMSIUbMiIiJjzCbzYULFd/J+k5eF0Ng/zS3DZM6Vbt/JSb4F+pzQtKiCSQvSJj27RJ2Xt4ojV/pYVrYWdDaztmxCMEC6cVenn6P46fJHxroGiDPYeuBsWMPhwZCYH02KJbbMlYj0gj599vV8JWFD7/kz6luOYqnhOSKSAILhAmDQSgtn6esbAiujBs2CHhWt8mnWAAEiz2eeeWpBfUNjSHLy1xeh+Rt7EpyjfRkcPonBaHSHt54jkUguwIngzIQJE7SDI8MVhM4IgbYOpXbh5xq3DrOhMU7wtxf/WyPNf5tWqHyIilGpRMG2oR30YKu25FBRgz/Zm+L++MjlfD+fHGRAejBGYugcc8ybDPWUSKjn9++b7DM0ZnubIEAegB0iG3my1fgLCU4Tppq60ZV7DiQVJiU9AjLYBmUpnP5CRE8ik9U9X/PgwYIHD2pHNicCoDvw8fLyAhyzdTB3EQCD1b/DW91yx7fbGhz44XiOBnRg1FycNssdWhGqt251z/ji6Iuq9PQN4BN0sVoNhiAGdBythdyOzVCyrAxnM+YvUqgvXNxlkjUMRaLm/JAT1uGT5yZS84L7Jfec+dzqPosW3YeqthO4BLiSYGrO11qmaZ4hv+ilWrXK05i4ZgVn24YSJ+TIonkCkaxcHNq4jlbilJWV6cRiiZyiGjlKpWLSBx98sHDu3Lm3MjMzAjQaNdMXDbIHTmG5uVkjeTyamjfvZajiMjqBJvGrr74yfv78OYb6BvlwAFqzERgW7SudIXP8cRkI5W/ukFSc/GmerrhktbkRQGBJRAXEUFhtlcSZmKSj3dMChht5L/49sT4lbae5viEadOu4rhJ6kUDL7RnwdZcnnlwFIKgh1W0+TSgSkcq2tTSX3WwyiejSyunycxfMJYnrVwVuXVOCsrXJm/mG0pICj4gZGWnuCHXSCtuAbsGCBd/J5U2jVCpVl+Lios0qlUJlMBhEhIYDFpHL5Y9kZWUnQ193CC3TcoWcaTcY9L3u3s2GEwVlBhoxAoGRzrqIMApvR17rSA4Zl4BQnpwsqf/quznawsJ34PxvBYGNE45tnW8r74eN2lnOAoYrmXNfW6K8cm2fWVYfjssocsW3Gc3HBcdQNKDfcf+nY1f3W/22ayDAwRgfgdWPdWuxE8JeczASpSstn1Z95geJ2ZcbD2QP7Egdsh5MiQUKn89DhxGmwZYlErW7TqedCNLzYQshQ9DBwcFH4XNyhdGon1NRUT4cPigJdToDRt0EyI6iBJRCoaCUSpUK+Omxjs/jczw82NEUCvwCjXsd1eTh4YnNTe7uHkbMQChaBnUVZrPJIBaLtVjnamoXCMUXL4qrNu9+Q5+dk0jLlX7ImDWO/RC2D0KkjYFFB7csixKvZi9Y8mrD+Z/20owDyb7B6BMIo8MPiObMfKffrFkN9qO3m7eTwxGyrczFbBLqyyum1nx7ipOzesOS0PfWlMF8iDGtw3n26KEFmZk1nc/nj128ePELn3322T0erOnXf7keeb+qOgqIuf36BReGhobpjh8/zoGvkAow8IXbt29fqamp4WZnZ/M///zQbqPRMM/L29sQEREhgzByOTiTIdaB2snA6mNC3cFzGXyUWtmzZ0+U1XzihMvhCFyIWk8gMD913JT5+nvSZWZ0DC2JaIQxNtSRMmkn9RALgyr82tCxpHk07KaPSfea/NylfaYmeSQlhNNBQI/D3nHjkwZ2FAQwNIQzQCT2rIES2eRlVxrmDYN2Uo/yo4NmKCt7pin5KFVxKPk1zsszKpvPYtasWcojR458r5DLo+BzccT161cPFBUVNvF4XLqy8r6fSqkUS9zclAEBPT6HewRWRUycOHEI0M8BT89NwOND7MA0AQ0J6krt2rVrAeZhLOYtbz5mW2UAAkLeDvZtUTu2tQoEXOZuPzVtqbYobwWtVLOnAxTPamWbQhnF2TURhaIFyLcGx2HbLg2NjzcAjxvZCa+/Jr9+a5eg2yO/UGOGrhuYmOgQem2bi62Vy6jGKhUzBYSAbTLNQEC6msw8Y3X1M+Vbt/OkCQnxAz/+2AEMYDAzKH//I4/434c9faFarfKrrCgXA4Zgj6Abu/foURMZEXEoNHTwkRkzZjDLPLLW6VT+BoNuNJdLeZoMBg6sILV9+gReHT123LqZM2e27/wS+Trx2SoQLq1bx/NQagI4epM76owxth0ISJaol2lvIRhpbdHQbgXwo2+Lfer5/v7lbr0D0sLWrm3gJCW1288ZAfuK2IzN0pAZ2ODgTFo47HFphby/ulEZCP0cgIB8AAhaiLAei4xMuWBoooV5ZWUeXl5Cc5cuvXT+/v5qODIq7UGAfYYPH3VNr9dP09JagZ+7G+3t3Q3uDwQ1kUsnSPNHp1aBMCEpyXgncc1OymjqrpHmTaMNRotvyi6xKKi94uzzzkHh+tRwNUpPWBxqvHZ1u6607Al9fmF06uNPUfBx68sBixfrXOdkobQ7vbCyobS2eSCVvfyWXngeoLlukgfuoYNXRsXPu8X55gvS5PCE0wAu49al36HRSWHnzp0aqC510vRvq7JTUUsZorZtKJZMjV0ljoy4QokEEPKyvUX2iiN50krKLTm2X4MgyN26pz9dWPKe/l7xE7ROxzWr1H11hUWbdOk547G9fS6OFOzWwNaxsrEsnMmJddiKxxWur0+NR1zskqgzySco1tiOjP8flVpdEcgcw1euLMzduD0B3Jf1mqxsWBkMfHsFEqtgHanHOpInfFx9Fqxc11dx+dr/GPKkY81GEwtUDAcplF0bf764L23KjFVwFe4oNXSowVWeHC4rpU1WlI4t2XKkBpvAcfPxvO8RO/YNw8JXvgdfoM24L2wPwtzcu+Nra+uH0LTJXa83SgQCno7PF2rhSFc+bty4U3DHsM7iBDqIDfVdCgqkL8BdAwkGoHy6+GWGhYRdBJ5WnwI7wElCBC/BZLj+FgLiWRxC8h6bKJOJo+vdu0dpXNzTV8CJ7dipCvi3CwQUInTV0vy8+YkraJPJXZebF2fWG5h+RLFIgwnLqFgbCJpTIJXzhG96xtw3A5uu/7JHL80fC2ORWVo7QCCrnyY1bU/6mk0UhLoPUzNmtGkgW0c2ZzM6KxeR10qHGajkuruVukdHLY38+wsnAHBteu/79+/s8dVXR9dBbOBZ+JjUFR1I4ALTYaJ+FJ7n4VSAYFoG9eU4hH2qqKgYJpVKdxiNRkan3ZSqHDeh2/NAk2dPBwEoYUND3Xy4zfwU8LZvsuahXV5SUnH86NGjy6ZNm+Z6nAU4tFC2lWuzzMAD20o8xw9bJIqOOgIfe4z2SiRikae1K8Pdta3z3rr3B5iK8vZrc3Imgz/CRMzwEMWazAIuKJtVmkdU2Vlb7xw7M/NOYiJE7lxI8MWfUGHGnifJYzsNryTl61XtETducdSbCe1uBwjey5dvLqitlc0GEDwCwZyS0aNHLXruuWnjxowZsxnKcp1OJykvL5smk8kSLOAgonBOnz4tqqurm4UggLgBYIWi4J5CCESgnoQVwZltcCYoMgWXYR/ExAw9DcfSEz17BlyRiCV1EIjyrqmpfuHQoUN4cbVDydlgThnA6PTA9etL/KY+vVwSFX4E7wU6JWxRyV5Va1FtqUBlSt/dFFX/0+W9cNv5L7TeCDKxdmvuDRCj0U2KXqor13eZpSUzabgT0Rpvaz2rPKaIPCzcmTJBCNiAFvj7ZrlPGPdq5MEDP7riExw+fJhbWFgUpdfrxNDfOHDgoA1PPz31E/gDlJRJk+I2wR+jfNOjR486X18/Q1NTY7BVHksmNTV1UEVF2bPQlzNy5MjLECE0wJdJQeG9oheHDx/ORBqb90HfBelHjBh5ds2aNf915MjR6YsWLZ7cJ7DPAYxgYrhaLm/sg3pt3retsstAQCaorOAl8WX+4x5fJRow4DQl4DNgwBGbj8qULTtZawKgsHfmvB7WeOan97R50ljYclh57OZgNZSFCcMXKk0Kpb86I2vlnR0HnoQNVdzaGEw9c3Ik5mef5MyA/DBiDzecasRDo/4R/fLMkzBP1/0PDoVXyHAYCt7ssVevXu0Bt5DEeBSMjIzaFBY26CUAyEz4u4TNqD9GHvjB1QCiiwnQxw2OmHWBgX23BAYG3kVestravmfPnh1IaO2fZG2DoJUZjK63yKrXGQxMjMUyhosvqY1z+2+TjdaaC3rn7eKipE2LGrw9dNr0rL+aNRo+KpRRqoXKOmNrL8cMgqB4y+4QfX4e+gTjOQbWJ2B4wE97/ZHAJFf2U96++Zknx4gO5KFWHUhmRUDOmAgE2BJ+zeD5+xQIw8OTor/9/AdQpGt+B3SH+IA5Li4uu6mp4QkwqCQn5+7LMlnNSNjPT0GQ6OegoKD8xMQVFwcMGNDiyFtQXDAKaJ8DPXAhmnjSz8/vipeP92fwVu/W6rS+ubk58wAsy5566im7vrB1oW4QLDJZIFx5G/32228YTp892xsc61dgNaHgwktVUFC/dHvQsTNt+/ehgIAsg5NWlJXt2bOyljbr1OlZL3C0OuY0wRiSjNnKeoMgkG7YEgKng490udLxtMl2p40AgOWDJdaAthxhDi1mmmNWqLvqMzLWpm/eoYO4/bfh4eEO3jZSs7d4WM728lGwEnC9vSt9J8e9Gfr8lHMdAYFFCjo6etB+OCkEl5eXP2fQG0SVlZWD8B/4B4vhOloGXEP/fvfu3cmwRdwD4DAgw/lPmTJlWGNjQ1f4WwWTSCS8tXDhQiWcDFJ9fXyK6urrB4DPMf769esjYJwrlrFwJhj6ZhK0TfDwcB8NN7M5dXUyoV5voGBMbUjIwK2JiYknYFWydXMh14qpXOgJJH0WLy7yi4l5Rxw66DtKyG4T2BOVbTMf1thScnIy784Lrw+Qnzn3gS79zuMEBCy9jc5mNsc6rLfxZ/NG8Bk0N26/q3516ezU/akt9lY4PVrUx640TH9YprnenlLx4MFLQz/cfs4Vn8AmiS23efPusokTJ701ZMijGwJ69coCo9bAByitSqXkS6V5wzIyMtZ8883X/7x27Voc6bVu3Tp/uI8wUqvV8dzd3YtjYobdxDaIRKZxuLw7uGbV1taEZ2dnTQJ9CUk/AAFglS3BpZZ6+HO6upqaB3Xwl00y2Cq0sCrxAHwxsFL0xZWG9HPl+dArAmEe9P7a0qa31izlebrz1Klp02i11k4AlNrx1BCZmjOkqSxvhz5XOqY1EBDe+LTM276qZR7MbFIogiAC+b7khy34OfgAaMy2T1q2BuTFIAKQAdtBocfIEYsiXpl9yYG2Jfd2a+CL4n0w2BbY8z8AXv4NsFVIc3OebGqSj0dPHow68vbtW2+CXOeh3VCUn/8oLO3wiZrDgX3eBE5jv9jY2MArV65wBHw+JYDLuBCC5jU0NL5wJyXlYyBjQtsAAgJo+rHHRi1pKi09JejalQuftv1gW5ouleavBGDMvHz5kgSOrW9BvzIcw5X0m4EAE4P50feLd3+0xqTRcLUZWc9iOLq5AeEbKfcezy247uzPGw3SgtH2ICCzcyYwthED2j+RlrQx/aBggnO8JjNzdcaMl+X0RTqZmmAHBoYIfoAJz9e3WDJ8aJL+rdcutxcnIN2cPdEpzM7OnAR3B3oCCEqmT59+Af5ErQn08clXX3317dGjR5ZnZWW9CZdLhBqNzu/mzZsSaDNNnTp1iFaj8USesAWE5OfnfUH4wzR4cMOaeZmqq6v6Nuh0gdDGAgGJcNLwC1tK1fFLlxqZEodTv3Hjxk/Kysqnw/2GIdUPqieCPPgZ+48DAgqCYICHNGv1hje4fL5BnZbxN46ODTphO0yeSnvltcHmvHvbIE7wF3AMGZwQwyINSUwDFJAhyZM2VgdEF47tDC8ggKBTL9X1lK3psmfwBs+/oK+JwospbFCC5nq43fedMmXuoD0br4PctlWDDNKBJ/D3TEvPSJTVyh6D/brIYNDMg+43gK8ZVgiIIRiygMZydmIfcA0tuLyidD7ESinYQpQAknqgAcOT2dIcqBfDStEFl/qiosKF4DTehc/duK6xni7ME6+x2Yt6//79rvA10w3rNGq1EOITzK0me5q28r95RbBnHvHemnLptv2vc0Dzmtu3/4ZtGEWQbtgWZM6/95E2O/sxymhmUIM/7FTQvOycGGNip2YJKTA5aydtVi6wkdLwhqpz83ZnJizWRH685zvm3hCc8rj+/sWSYY8uBRBcsYCXZfyQvwEBfLXJaFLBfUMBfIIOgZjC0vj4eC8fHx85/I8tusE1tLeBtZDL5XE8PL1l8NdNaljC5+q0+r4wG1NERMTmdevWb8Hhw8LC6JycHEYRJ08eH/vZwUM/GiGcX1P7YCzcdRwG18Ju1duO4xSAbOyKFUsb6+rkIvhraXeITs4Gv4GJVQQE9MocO2JEyalTp1yeWacCAUcdmBgvy33//RUco56vLS0Jb8zJf1R+9vxbupzcx2gAAdIQELCGZaqwmkmOJdvKgIa2GtuSxw4sD9sTqSAqwDGrNR6Kk2d3Z/51lg9HJHTndfWr8Bj/eMLgD7dd6AwQ4NhxcX9XJSQkfA0GGAL3ELvl5OROKy0tm+ImkZiVKjUfDM8DMrp//+CiMWPGflglr/LPyro7Bo7/XJFIBKsBfdXZKeeDDzbn9goIeFBSUhKgUWsDTpz4flZwcP9fOfUyAgUK/lxuOfgBC3U6vRguwLiTd8nDzb0qJKT/rn6DBjmEqFHetlKnAwEHC125sqR4y97Xm369uUT25ZH1pqrq3rTRVMGcga1TYQ2L9MSYmMdE3nLMM8CAPnDUg3r8j60jgCFl2xNbcAVlVgaO8uatRfzA3nUesRPmD96z5afOAgHKhgn2+2S4GlYGDtra8vKKUAgpw9uqw83ICGFjdWjooPMRjw7bPXr48IJPP/30Wa1W7Q5bQTnEDq5CNLHg2LFjLCO739jYZ2QpKekfl5SULgDQcCAq2aV7v+7uEIUshbmVo4YgVsFRKeH+IsXBT9oN3l4++ujoqCy4DbXp3Xc3psI8XY6H4NBEn3ZidFqWujh+jkhwN0UgN7M+Qadx7gAjLy6P9uwZaJYO9NbOOHy4Q8pxdRg8Eh84cEAMy7sXGN8TPxB5enoqGhsb4QqqSgVOpQ4BCM6kMDMzUwR+AQVAMKSkpGhhDHvcW4fEr41nzpxh9vnQUG/jiROpmlGjRolra2tbHI+xEwSwaAg+GXfs2IH3KJ3ytDL/M/OnBv7UwJ8aaFMD/wtZgl7V2zg1mAAAAABJRU5ErkJggg==" alt="Logo">
                    </div>
                    <p class="htext" style="font-weight:light;">Select payment plan</p>
                    <p style="font-weight:light; color:#333; margin-top:-25px; margin-left:-10px; font-size:16px;">We accept any Credit/Debit card</p>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)

    with st.expander("Pay in 6 months"):
        html_content = '''
        <html>
        <head>
        <style>
        body {
        font-family: Arial, sans-serif;
        }
        .header {
        background-color: #E5E5E5;
        text-align: center;
        padding: 10px;
        }

        .payment-option {
        border: 1px solid #D22630;
        border-radius: 10px;
        padding: 10px;
        margin: 10px;
        }
        .payment-details {
        color: lightgray;
        margin-left: 0px;
        margin-top:-15px;
        }
        .payment-total {
        font-weight: bold;
        margin-left: 20px;
        }
        .continue-button {
        background-color: #808080;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 5px;
        width: 100%;
        }
        .st-emotion-cache-1clstc5{
            border: 1px solid red;
            border-radius:5px;
        }
        </style>
        </head>
        <body>

        <h6>Pay in 6 months</h6>
        <p class="payment-details">Pay using any debit/credit card</p>
        <!-- Add payment details here -->
        <div class="payment-details">
            <p style="margin-top:15px;">Today: SAR 206.97</p>
            <!-- Repeat for each payment date -->
        </div>
        <div class="payment-total">
            <p>Total (incl. SAR 10/month fee): SAR 2,483.64</p>
        </div>
        </body>
        </html>
        '''

        st.markdown(html_content, unsafe_allow_html=True)


    with st.expander("Pay in 12 months"):
        html_content = '''
        <html>
        <head>
        <style>
        body {
        font-family: Arial, sans-serif;
        }
        .header {
        background-color: #E5E5E5;
        text-align: center;
        padding: 10px;
        }

        .payment-option {
        border: 1px solid #D22630;
        border-radius: 10px;
        padding: 10px;
        margin: 10px;
        }
        .payment-details {
        color: lightgray;
        margin-left: 0px;
        margin-top:-15px;
        }
        .payment-total {
        font-weight: bold;
        margin-left: 20px;
        }
        .continue-button {
        background-color: #808080;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 5px;
        width: 100%;
        }
        .st-emotion-cache-1clstc5{
            border: 1px solid red;
            border-radius:5px;
        }
        </style>
        </head>
        <body>

        <h6>Pay in 12 months</h6>
        <p class="payment-details">Pay using any debit/credit card</p>
        
        </body>
        </html>
        '''

        st.markdown(html_content, unsafe_allow_html=True)

        html = """
            <html>
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f0f2f6;
                        }
                        .container {
                            background-color: #fff;
                            border-radius: 10px;
                            width: 300px;
                            margin: 0px auto;
                            padding: 10px;
                        }
                        .logo {
                            text-align: left;
                            margin-left:-10px;
                            margin-bottom: 40px;
                        }
                        .applicationimage {
                            text-align: center;
                            height: 580px;
                            width: 400px;
                            margin-bottom: 10px;
                        }
                    </style>
                </head>
                <body>
                    <div class="container" style="margin-left:10px;">
                        <div class="applicationimage">
                            <img style="width:370px; height:560px;margin-left:-90px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmcAAAOrCAYAAAAS7yFqAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAACZ6ADAAQAAAABAAADqwAAAACUJOPiAABAAElEQVR4Aey9b9Bd1X7ft7nIQuJKF4QcCQndQRW098YFNR0ZPK074DSJYabjmJvxC0gbOzDNxAPJG0Fn3ICTScGJZwq8SWCayQzEaWN4kYkhmcwAiRsDcaFgJikwLTeFa4guKFINEkhCICPT81nw1f1pae1/z1nPfs7z6Ltmztn77L3Wb6312Xv91nevtfc+F3w5C42DCZiACZiACZiACZjAQhD4xkKUwoUwARMwARMwARMwARNIBCzOfCKYgAmYgAmYgAmYwAIRsDhboIPhopiACZiACZiACZiAxZnPARMwARMwARMwARNYIAIWZwt0MFwUEzABEzABEzABE7A48zlgAiZgAiZgAiZgAgtEwOJsgQ6Gi2ICJmACJmACJmACFmc+B0zABEzABEzABExggQhYnC3QwXBRTMAETMAETMAETMDizOeACZiACZiACZiACSwQAYuzBToYLooJmIAJmIAJmIAJWJz5HDABEzABEzABEzCBBSJgcbZAB8NFMQETMAETMAETMAGLM58DJmACJmACJmACJrBABCzOFuhguCgmYAImYAImYAImYHHmc8AETMAETMAETMAEFoiAxdkCHQwXxQRMwARMwARMwATWLQqC058ca/7gN36zOfHK7zWn3v+g+cPZh3DhtzY3G777neZbf/pnZp8/2ay/YueiFNnlMAETMAETMAETMIHqBC74chaqWx1hECH2w1/5G0mUDUm25Xt/ttn2V/+yRdoQWI5jAiZgAiZgAiaw6gisqDhjpOzw3/1fGkbNvrHpm81lN/9s880/sbfZePWe5scu39688TM3F4Eymrbtr/zl5sd/6b8t7vdGEzABEzABEzABE1itBFZsWvPQ3/l7SZgB7lv/1X/R7PqVe5oLZwKtKyDYNs3E25Fn/kVz8G89OBN1x5vts1E0BxMwARMwARMwARNYKwRWRJxpxAyIO2cjYFt/4XuDeG7/i/9ds+XmP9Osn4m0Q//gf0vi7sJvbfII2iB6jmQCJmACJmACJrAaCEwuzrjHjKlMAmJrqDBjuhNhRtg2S/eNTZuagzM7h//u3/ODAomKv0zABEzABESA22VOvvX95rP/h8+/S5t/7IodzYY//p1m4+yzlIfLsHn62LFk68LNm9MDa8qvbRnTtMVh+1B7XTa8b+0QmFycHf47X91jhtBCZA0Nu37l7rOi/vgv3NKc+Lf/V/PJv34pPVCw53/9+2ft9w8TMAETMIHzk4BmZxBGbWEpD5cd/Fv/c3Pkt/5ZMvnN63+yGdLvIBB//y/8pbZinLM9icfZGwpqPPh2fPb2gyhOmWni7Qff/KmfHCROSX/i//y92dsTDjYStpfM3powJMCe9J/OPtyCRMDGt/7Mn2w2zsowT8D2kd/6p+mtDtjGLnXaNDsmpcCgEJ+xoc3eWDtLiT/pAwHA+f5//d+kcn7nyd9I05NdhdYDAQi5XJyR7vTxE833b/3FtPyJV18YdBXTld/5to8T/L279p+pNleTO/7aPWd+e8UETMAEVhuBeD8zZf+x2euXNEpGH6TXNLGP7Vc++nASLPzuCrH/UjzEGSKtKyBQxogz2RpTNqXRkrL2vQVh21/55dZ7tk/ORhv//axvwE4eKNeuX/+bnfXuSo89HuZbal/zwex+8w9/4x/lxUq/Kdt/NDsmLGM4NBsUYpZtbLj2+/9mbJJq8ScdOfvkX/6rVHDdNzakFjwE0DbCxgMEl86E24f/+KnZO9L+0exE++UhJpctDmKHBxWWGjb88f9k0vvnGJ7nvXIOJmACJrAWCBz5J//0zG0zjEDtnF1s5uIJwcEMDiNgrL935/7m6qee7L24ZwQpDx/P+rTcfh4n/v7xX/rz6TacuC2uI2ooF6NdY8oWbZAOMciS8I3Z2w0u+VNfjXaxTT6f24tK92yn9L/4l9JbFEhP/RA7SsvyBzP7bcK0lP6b1+9r/mjW33z8L38niWP6629s3jS6z47CjHoxssV0cCzb27fcmo5nLtCoy2oKE4uz30lseDpzaPhjs+lLHgBoC5v+xH+WxNmJV15rizLZdsQOQ61LDd98/ycnFWdLLafTmYAJmMAiEtCUI6NlVz7y8DkjKJSZTnvXr/9PqfgSaAgWXnLeFf7gH/5m2i0xRpqjMyG186/9D13JztqXphQ7RtqwzagS4gf7iA4GNbb8uT97lp2uHwhP0hF4mwEjZDFglxkTBhMYTWJ6l9dTKSDs2Ef49myE7NLZfgXsUjZGHxmZK4lapUc87Z4dA/HCBmX5wUz4IT4/nPGkrjFv5VNaIoQ1Yobw3vMP//5ZaWO9KFuccobfptm0Z1+gfl+9CeJY66hin41a+yf9+6bPZnPvBEbDhgTi9T0wsGH2TjRCHKoeYttxTMAETMAE1hYBOmgCIyp9IydbZ8JAganHrsCIFoKCsOXP/dxMcOxL64gY5Zk2VPqKr4jinrUx4ZPf/p0UHVGUCzN2sH3rL/75FIfyxwEFOERhF4UZCWCqshFPs2HJ2OyLkUulL41aIsTYTiDvPH3a0fL14ey9qAQJ71zUUa9df/tvpjgck3hcKDf7+z7kQbnS/YiZqE2GJ/yaVJxRacLGq68aVEWe5uwLGlXTCdEX3/tNwARMwATWHoHYB3xjduN7X+AeW3XWfUJOIzbY/NZsijCOZB35J189INCX35j9CBCFP/r6Znr97loirtTPIiLbQiy/nmQl7tGZuFLIhZm2U38JI41Uap+EIeVH4JQCzHmJPJ/1u35Uz1LcuE1iq0t4M/qpsjHSNiZwryIinLLzMMZKh0mnNcdWVq/OGJtupeLTwL/7v//zc7LnJIn3ohEvDrmekyDbQGNjynSeR61lo88JZVmf87OWnXMMe4MJmIAJzEEg+rZjs3ubTs9GPtRRt5kd6od124ymALGLyEAwfPLb/2omiGYvUQ9Tg235Dd0+VmjK7h99PQDCb6b+2kJkFeOcfOvfpZ/UrS0O9WR6lrprNkw2NBLGf2F3hbH3h0ce3JvdFb4xuweNfkrHrCuu9mFfr/hiKret7oo/xXJScYYiZfrx1H841Hkf2ZiKn3z7Byl6zYYxJv88brzi0T5EVR5K8WIcTi4eB9fjwtpHPblyuXR2VdT3mG+bjXTlMvL/SSkLN3HG6WPsMMTN8q2vn8KlnJzYOD3y/39nN2fGsH12tRSv2uI+rlri06PsYwi8716QaMPrJmAC5y8BfBGigc6WG8MZnRn62og2aggOiYM4GoUAIS/8HH665t8JIi4Vhr66gvgIMp6kJKzf2T4qFadxNcpIPTR12ydOEEiqO2yIj/9WUJnFhiWB8qWb+OcQsqX+VPnGZeyr4vbSup6mRXxzDi1CmFSccQAB9tnb71QTZ384E3oElPxaCTiDH/6PfyM1+rxOOtnlDNoeR6bBxCd2oh0a1e//hd8760bPuD+ukx+CiTR5YNsPZna4ryE2hAu+joiQZOpAV1NsZhi8TZwxdRDtIGAtzHLq/m0CJtBGAGGCKMNv4QPxowREAe/W4l6xDT/x1XqbjXy7pu7wR7HjpiPXjMgnMzFVQ5xRbl0IUw78X8wzL1v+mz52fct0Yoz7/uyGeQUJKQlQtvPesK4QBZJeyht9Nw8DxCcroy3KuHX21OoYXjE/7sHbEg1m6yoHLIcEpjOpO8d3EaYzVeZJxRkNgw79+L99Y/Z/mv+lyjDX8pN//X+k9H3DqHNlMmFihEw+etSWPSNZnIC6Uorx2oRZjHN0wJOlvz97siZeEcX0WtdwsH7HJY+OR3HG8edTcjj5MDRpHUzABExgKAE6fp4g1KsylI4RIT66+Z14+KC+F73Sact/5TMVXHxiQz4NX9w3g3Pwbz/YHGp53xavmoiCAtu6wV31mHeZBOtMmEmIxZEiiSzy6KsH/BQ0lSqbbP+Df/CbsydZv7p/DWGMuMI+x4B4Xz0ROfy/sSNrnpDd3jJljbAdEyiLynnZbDYq1muMneWIO+kDAVLKR5/5F+nFsfNWiOlR/gSdsBZGWHTSRi5cgTB1iABjlIwTPQacDSItBl0JxG00Qh4tZ7oRW33TqqTlyZtcmCWHMUuPHcrTZ4f4fGIoNaD4lJDiroVjqrp4aQImMA0BOlhelfGd2f2/+Dr8SO6n8LX4Tl6Kjr9sC/HdZlv/4rkXi3FQIPfDJZuIL0Z2Sp8ozCRG+kRSKY+2bfhdRhURkwS4tM28xJGqNnv59lh+BA99FcfgP56JZfoLlvzWseCiXmXJbZV+a0qZfBgR5RjGQP26BgpiXK3rtSOUqe0BCMWdejnpyJlOOA7ID3/9oebKB/76XPU9PPvzcwLCY5EU71IrpRNF6TlhOKlj3RC4/IVIFDj5u2p0JSA7iLv4SPU3ZzsQTBr+V7x8mb9RmcaMwFPABtv03httz5fkz/SnAleiNLDoeOJTQsRbK8dUdfbSBExgWgL4Tab48CUEOnNGbvA/x2fvxdT0Fx166WWspNG7zfBV+Kx4rxb7JTRYz0f+2ZYHyvLNn9qXb06/sU/5VDbKxWham4AqGilspMyHZwJUQogL/stn9+LFV4kUknVuiqNspYip78reQ0Y8jgk33NNnEHjSNb94TzsKX7BDLDPNzDHko7Q8mAA/AqIQjn3hK4H+z1K0ridA++ws1/5JxRmV4EoGUcB05B/8499qfvwXvrekuh2aCTNGzTjRFmmeeEmV+TpR3rgRNVGYyTZCixNUJ2Nq1LOTkxM1H4GikURhJhvY5V03uQDTfk7c/Mqk5CSww/Sj7r1Q+rikXHmD4SozPrGT111XSdGO103ABExgqQTwVXy4oCTgg+S38gtc9jNroE4eH6ubxtlXCogfPhIMpTjc2iOxWNrPNvyuLpwpIw81xAvZtnT5dsrMCBMiRoG826Zy42hZ7vuVXkv1PfyOAlX7GVFsKzN8SIM4lmBUur4lI6K8fuP/m42SMZ0a06MFvj17zxn15bjls0y5bb03je2LqCEmndYEAo2Dk41wcDb3jsgaGxB1GjXjCgCbqz1wsucNoq0Rc9Jf+r2z32Gj6cc//OHZQ70bOx47brsxH5Z5WWhQbZzbyhmPyZasvLwdWoHGFPOj4XY5OKXz0gRMwAREgNsw+A/FIdOLpGEWQn4p+d8Pzvad8d1myqNvebzwF099afL9+Nno309l5crjl37TH6RBkK+FGf5Ut7S0+fG4vW9kLO5XOi0pT98fm/Og2FIDgw3f/e1/fqY+DPhQt/909v/aCO9Tsz9pJ6zveahBohUhGcu+1HLVTjf5yBkVoFEwXMtcPyKLJy75/0y9ULatkvzR+Q9//cHZqNtLKQojS/MMzbblsxLb48lO/n0nS7zKIb6uZKLIYXvXU6xdeeQirytu2xUS+Ssg4Lg6VTlZ0jhoTHoaSnE5rg4mYAImMIYAL0DFp+CPdH9zX3pEi/yPbmxXGo3mS9hoe2n5f193Q/JtXHTGGYFS3CHbon/Py9WXnj6AB7nwsWOmMOGmEa34YtpSftofR6fGvFBW/UDJ9pBtlJXjwi06MWBXo2nsbwtxQEAjqW1xV2r75CNnqijql2kyIDM9+f1bfyndh/bxTHidnL1qQ4Gb/tnGKNv3b/3FJMw44Xj/VWm6TulW+zIXa3l92vbnIqotHva6GgjHJYbTxz6JP0evY09/GaLE3DdHGXQFw3acw5CRONnw0gRMwAQgoNc/xA66j0z0j/QrCvFviIbcYqGRrjF5K6/SMvfjpTht2/hfScpBffj/yTEDGJu+/lsqBA42SgHx9yMB9KP75+JAQN9fTul+P/z90MBbDLhXrWtkNPYlXaLrrHhf/yn80HJMFW/FxBkV5OqGx541tIxI+/f3ze5J++/vat74mZvTB9HGNqYyGTlDDfPUx5gTbiqY8+RDY4yCqK+Rx5cUkq+GifOrF139lcoWT9B8f7wiYh922hprl51ol+Md60gD1z0fipc/rq7tXpqACZhAFwG9r4s4XU9gygb+TPcdIRLiVJz+hoi4XSMwshXzrv13TqeyW1WUZ2nJdKaEEwMY6hdKcUvb4q0ubSIo1i+OUOLbxYrXXeSzOMpvrPBVOolC3inXFnQPNeXoErg6vsSLfVKb3ZXYvqLijAoDUI89M5IGrHgFQ6NhG1NdPzGbU86fXlwJaMuV57f+1M+cZZqX+JUEUelVGTAicPUSTzZujNSwfTSOXZ3IcbvWS2KxFB87ucCSjXxJufLRM713SHEX8cZMlc1LEzCBxSWAD9RoCQKFfydpG8HhwSmm/iQgeMeVAtt0wTn0fiTylt/96u+cyqNOyqNvKVt98fL9Kjfbv5x9Ppq90qLvE59ApR7qS/D3uUCLr6tghiMXQLolhX6h9K7N9OTozC6hNEvyw1/5680b3/nP00ciM0Wefal/ZHteLvKjv9Tx5D60tkAZiE/QH9i3xV3J7Styz1mpwhxkVLiUOAeIUPqvylL6tbCNukchhbDipk4eoPix2RMqnFDHZvdUxDjUm6cl1ZhZchLHOJzwpz/5JDku7mXAYf2HcCK3scuf5qRBUAb+OorjxUn+0WxqUg2izU7czpVZSeQRB6eQN/aY1usmYAIm0EWAl7b+YCau8J3Jf/78rcmnaPqMaUym1NQ5Y4tpy3iLTHy32ZhbLJjaZCQO24ikOArVVebSvjhA0fdG/Jj+s6//G5Nt8V8AYpx8nTrGGQu9UYF6cOFNX0K/gZ+P05GlC2l8OAJNAwi8R45t9Euk55gQ0pTr7Cb+MUH9I2WgXIygIa64f50y6piSf1c/Eo/vpp9qvy9tTNmWI+7CiLPlqNxqs8lUIqOHcSSKE1p/QVKqD04nOhbibPurv3zmXTlKg81oV9u7lrExKB4jXflol/YNWdJoaKz5VRFp/Y8AQwg6jgmYQBsBRAC3vfCOsI9m79CiI8eH8smDhATLGHTxiG/VSFzc37bO1KamSREL84izKC6YIrxsdlEb7+lqK0Opnm1x27aTN7cb6f2VElSKDy8EXCyj9rGkP4IdAg3+ua8nPf1cW/poK65zbJk54546bOqjOAi+Ie9viwJ2CFPZn3p5wZezMHWmQ/LTyNm13/83Q6IvdBzm2KPA4qTkTcltAccy5J4JxBwvhS2d5DSod2c3UOpKp5QXjSQ2HH5z8sdAY1cjjdvjOlee8T6EvvqRp15CKDs05vNplFT19tIETGD5COBreL3FV3+NdDw9NMB9uYwU4XMcugmIH7EQR9zDRj8xNMybvi0f7HJ/nUbLOKbfmt3YTxnXSrA4m+BIjhVnFAlRlP8/nIqKKLtsNoTe91BEmw2uMP7YbCqUKxyJYGyXxBnb2+xQju2zKVeWDF8r9Ikz4iHOaGAKXImNmUJQOi9NwARMwARMYK0RsDhbBUc0ihiEz9grPq4u+HsLAvcOIKaWEqKdpZQj5snNunG4nJFEbDqYgAmYgAmYwPlOwPecrYIzYMwwcqk6DPXOawO7tezwIEEUZqWnfkr18DYTMAETMAETOB8IrPirNM4HyK7j2QTO+ZPz8Bj72TH9ywRMwARMwATOPwIWZ+ffMV/RGnP/WnzNB1O0NUb1VrRSztwETMAETMAEKhKwOKsI06b6CehRc8XUSwv120sTMAETMAETON8JWJyd72fAxPWPb7Ama4+aTXwAnJ0JmIAJmMDCE/ADAQt/iNZOAZnS1B8EUyveTeMnNNfO8XVNTMAETMAE6hDwqzTqcLQVEzABEzABEzABE6hCwNOaVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIWZ1Uw2ogJmIAJmIAJmIAJ1CFgcVaHo62YgAmYgAmYgAmYQBUCFmdVMNqICZiACZiACZiACdQhYHFWh6OtmIAJmIAJmIAJmEAVAhZnVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIWZ1Uw2ogJmIAJmIAJmIAJ1CFgcVaHo62YgAmYgAmYgAmYQBUCFmdVMNqICZiACZiACZiACdQhYHFWh6OtmIAJmIAJmIAJmEAVAhZnVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIWZ1Uw2ogJmIAJmIAJmIAJ1CFgcVaHo62YgAmYgAmYgAmYQBUCFmdVMNqICZiACZiACZiACdQhYHFWh6OtmIAJmIAJmIAJmEAVAhZnVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIWZ1Uw2ogJmIAJmIAJmIAJ1CFgcVaHo62YgAmYgAmYgAmYQBUCFmdVMNqICZiACZiACZiACdQhYHFWh6OtmIAJmIAJmIAJmEAVAhZnVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIWZ1Uw2ogJmIAJmIAJmIAJ1CFgcVaHo62YgAmYgAmYgAmYQBUCFmdVMNqICZiACZiACZiACdQhYHFWh6OtmIAJmIAJmIAJmEAVAhZnVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIWZ1Uw2ogJmIAJmIAJmIAJ1CFgcVaHo62YgAmYgAmYgAmYQBUCFmdVMNqICZiACZiACZiACdQhYHFWh6OtmIAJmIAJmIAJmEAVAhZnVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIWZ1Uw2ogJmIAJmIAJmIAJ1CFgcVaHo62YgAmYgAmYgAmYQBUCFmdVMNqICZiACZiACZiACdQhYHFWh6OtmIAJmIAJmIAJmEAVAhZnVTDaiAmYgAmYgAmYgAnUIWBxVoejrZiACZiACZiACZhAFQIXfDkLVSzNaeT06dPN4cOHm2PHjjWnTp1qPv/882TxwgsvbC6++OLm0ksvTZ/169fPmZOTm4AJmIAJmIAJmMDiElhxcYYQe/fdd5MoG4Jp69atzc6dOxuLtCG02uOcPHmy4UPYuHFj+rTH9h4TMAETWF0E8G/vv/9+88EHH6Qlpb/ssstS/3HFFVek9bE1WorfjGm68rMf7qJz/u1bUXHGSBkNh1GzdevWpcayefPmJBQuuuiiZv/+/c2WLVuaTZs2Nbt27Wr27NmTjhCjaQi0bdu2rZojRgN94YUXUt1uuOGGweV+4403EqNrrrmmwaHUCg888EDz0UcfJXOU55Zbbqll2nZMwARMYEUJ4GufffbZMxegpcJcd911zU033TRKpD3xxBPNq6++msxdddVVzV133VUyfda2t99+u3n00UfP2tb1g74NXz+2bCWb5B3FKQIQ25QdodoXSP/OO++kvkLC9tprr+1LlvbT5yk96wRs1OjLsMdxoA9jHbvU6eqrr0755F/EU3+X7+v63WavK02tfetqGRpr5+DBg+mkIR1Tlrt3724QXXk4cuRIw+fAgQPN66+/3uzduzeJNH4j6nbs2JEnWcjfnOA4C06iMeLsueeeS1d9pKslzmgw8UTlJMcR0HAdTMAETGA1E8DP8lHgAh//ScDv0Z8Q8Hv45dtvv32QbyWthBnpSYsvrd2BI6b4jCkb5YmBsiIksdEW8Pl8SoERx8cff/ysfkLxYHnrrbd21rsrPcdmngGBp556Kg10qDxxSdnuvPPOM8db+zhu8ZzQ9r7lww8/3Bdl2faviDjTiBm1YkRs+/btgyp44sSJ5qWXXmpYot45gRF0q2EE7ZlnnhlUxxiJUTNO8tohOhhsc+VBI+aKxsEETMAEViuB2AkzAsWMQC6eEC501MRlHRFy9913916cloTOm2++eY79LnaIki4/i7+nXPRtY8oW8yQdI3UsCRs2bEj9JetsUz1gwAV5Plig9Brt0iib0mo/IihnqzzIP6YnHr/p0xDHmkVqE4fYKYUozKgXdqlDLNtDDz2UjqcEecnOatg2uTjjHjNOPAKjXkOFWYTJCBp29u3bl2wx8raI96BxMtLYaASqc6xH2zonGo1+KUq/zaa2Y1vijGF98qGczz//fKfTUHovTcAETGBRCbzyyiupaIyW3XHHHeeMoLCTTvu2225L8STQhlycIigIiBUCaUg/5pYQZj9KgiYZnH2x78Ybb2weeeSRZF99Ab56aKDfIB2hNDrGaB+CFL9PXGzHWZMorOAU88YuZUNgPfnkk0VRq/SIJ45BrC/lIT39ITwRhjHvrjoi7HQMEN5MKce0sV6MGsYpZ+qg49aVB/V7+umnE5uxwrHL7lL2Tf4qDQ4K05G6sX8phSbNW2+9laY6scUDBYsUaLT3339/c++996YrGF2p9JXxscceS2m4H4wrBBpP7RDLwsnHSU5g+3LkV7v8tmcCJmACbQTk3xAEfSMnccSIjr0rcJGtWQw6egkOfGZf2i67bfuiMFC+bXHz7VxwExAj0Y7iUXbVnfLrYp391CUKuyjM2A9T2SSe8mIfQWKX9dKoJWJKYpa88/SkawsSZhLeUZiRhnox3UrgPIjHhXKzv+/z4osvpn6QequeyeAKfE06csZo14cffpiqKVGw1DozNPzTP/3TqcHw+g1EWumetaXanycdJ63uaxhjB+G63AJJV5bw54S9/vrr04lMOWlYarR5uTnZlZarKepIY9EwNQ2FY8IJXXKKNELiqnGSnqsb6kw6Xcnm+fq3CZiACQwhgE9RyDtubY9L3RjPNjr8riBhQBxuqcFPa2YDv0mnXzNEHzqmT0CQKH4urGL52KfyR/EXhVpbeuqv0SX6hBgPH0+AJ31LKcBKwqePe0w/RHhTNo49DOhzxhwXeMCCMql8Mf+p1ycVZxIsjJotdRpSVwOC/tlnn6X3ox06dOjMKNDUEPP8EBv33XffWZsZRo6N4KydX/9gDj8GTkYETK2A89IJLhFGWXUy07C0Pc+TtGq4xNHQteLRGNjPhxM7P7mpO/twOjTmPL3seGkCJmACSyEQBQ0dMz6oT6TFqa+uPOU38V3Y5ENfxHbywv/15dVlP983VmgqPf2hQtcDZJGV4rPkYplA3driUE8u7qm74qdEsy9YEBBJXSHvH7risi/y6KoXcSkfxyOOnLG9K2BfYpWBgra6d9movW9Scfbxxx+n8nOP2NjA/PXNN998jnjg1Rs8YHD8+PGxJpctPidH3lApf1/IT4h4QvalHbJfJx9xJW5jQ6OxIaL6Tn6EJu8upoEh7gikwz4CnCWNW3mkCF9/0Wh0vwMNPF69xnheNwETMIGxBCSY8J3cGI6P6hIaQ+wjOOSL4ygRAgSfqQvTtgvbIXnkcSRy2C4fm8cp/canamov709i/Chc1FdRDw0gdKXFDn5bdYcN8ZWW/Sqz2LAkUD76BeWZNo78GppWg0FDzDNYQOD4lvqtITZqx5lUnH366aep/GNHzWhgnPilg8K/BxD0jwLph7+KBGhMBBpObHzw1cmJU+gTZzRGRgajDdJwUuMQaYgItNJJzj4++Y2mxQJ7owmYgAmMIIBfkQ/CT2nmQReC+CStDzWr2zmY7oo+jY6ce4MJXbMOQ/MhHr6RKVRNo+KrY559tvDJbdOJMS038ytISEmAsj36dsWLy9gXU2ZCFEPsj09WxrTYpj8fI2ZjfojAKJKjbdZVD5Ur35//pq8izaJMZ6p8k4oz7gsjSFCpEG1Lrnj6hhgl9LifzaGdAFdKOmnVGBUbYcXJL8eAWOsKNIxS41Wj42TvGoXDflfj6srb+0zABEygjQA+iNdi4IN0GwZxmX7jo23Eo3/BF5V8mezjMzWKlYskfKZG6jSKFEWEbMQlgqXttUpMSUZBof4vpp93nfogWNUX4IdVr5h3Xz0iM6WTTcqIuBRrxLD6F44B8fTAW19fo/pG1tglXamMErVK17ekLConojbWqy/tcu+fVJyNrczQ+wHG2j0f4+sE5Oogv7LiJEewEYeGhpBTgy2x6hJWOBQFGmJpFK4rvdJ6aQImYAJLIUAHy0U9HTi+DHHFaEsc2aFTVsdMvDaRoNkGylEa6dHUJvsRBm122E/Av0rMfLWl/I1PxgeXBEg5Rf9WyodoVf74fD05madeSr6yiy36EkRZ/joTmOtVHJSF/qKrr4nlot+QCEZgUvYoplS/mKZvnTJQJvrFReuXJhVnjHIxwsUUJH/PVCPohFiUJzVr1Km2DTkh7HIyx/sNlFc8yXFmXQ0mxlV6LaMYI99S6Epfiu9tJmACJjCWAH6GC1FdjOKPEGn4N3ygxBodNGKkJL40EsN++prcd9KpK7CvT5whAOIFrNKyxD4XtCqbhFSbgIppu9axhy0Jzbb7t7ts5PvU7+bb9Rsu+XvI2McxQTjrNhpEXFdfI3ssOY7UgTQcQz5iCTeVCVHI774Q+0XKsGj90qTiDEGGOANiLXGme82GTpX2HbC1uF+NkrqxrobRVldOfpxM29VT10nclqYtL283ARMwgSkI4Lf46ElCXrzNKyEIiBeEU/RfCDk+BPqsPr+Jb0UIdYkN9vWN0CAadN+cRuNiuVKBBnxRZkaYEDEK5I1vL/nwmEfbhbXsSAjxu2QLxtGe0rGUECKP2DfFOG3rus2JY8c0cEyP6GQ/9UWcIdK6goQ3cfpEdZed5do3qTjjD8x5JxmfpTyxWYJw9OjRtPmSSy4p7fa2GQHd0DoUBg0Pp9TlZIbacjwTMAETmIIAF5V0+IiC0ihYXgbexE8nTjp8HmnjyH/svPO0bb8RC/P6TcQOIkr55+Vqyztux3/zVDxpCYwwIUC6yhZFVhRf0a7W436l05I4kaPSxCXCSWWL24esUw+OL3WUDfJW3cQtlqdkV6KV6d2+uKX0y71tUnHGXzXxh+e8iJaDM+9UZHypbRxeXm5oq8k+J6+uLmjwXFm0BeLy7wQEriR1sufxidd2MutKkzRtcXJ7/m0CJmAC8xLgiUk63KHijPzwcYgzQhQc/JbfRNj03f/Mv8GQHmFQYxQmjjrl5aJsXQH/zCgf6cZMYZInPpv00Y+X8tL+ODo1pg8eW6e8DJS11D9hV8ettF92OE+oJyF/QE5xVno56d83IcZ4L1mtv1zSvPI8L7Vd6QOw3PkjshT6riZpmJrD5wRva0BqmLIblzombIsNN8bxugmYgAnUJqCLQfwW04tDQvRxURBpFA4bfdOQMc6YvLvKp7p0xWnbx1Qm5UCYISr7/H60M8T/I2pKAiiOlnX1EeSn+/3GCDr+3pCHCTQyFsutdY2G8btLdOmfDIinaW7WFylMKs6o+O7du9OIGdORvDx2qUEjcOvWrbMI6ICoRoRQio2nLUm82tAVZR63q3FIDNLohuSX2/ZvEzABE1gKgdgZyw912UHAyJfl/ip23tEnttmLebf5zba0fdslZPrisR9RJJ/PgwRjfXAUomKT5xvrF4Uf4lbiLorbUnqNWsX88nj5bzhQt3hs8jg67pSjS+BKxBEvivLc3kr+nlyc8cSmRlQOHDiQpjnHAkDUaYTm8ssvX/JfQY3Nd7XFj0O3sRF11SM2lrZGQANRI5AtHB1XbGp0NYb2ZdtLEzABE+gjgIiSSMJHPfjgg63Tc4ysMfUnf6UnOsmDbeq8sdfVyatM5K1OnrT4w3mCbI21oXIrHfcb933iKCP1kMDCx+cCjd/y/fQVORv5feof+ao85KX0COLInTj0Ifv370+fWC72xWObl4v8eHeajmfX7TvY1fEZIrzJeyXCpPecqYLbtm1rvvjiiyTMEFk8cYlg0wtlFS9fajpUDwHs2LGj4T42hzKBKK6GnoQ0Nhonzo0PJ3veAGlUNDCujiS0iasTnvR5oyuX0FtNwARMoB4BOmWmvuhX+PDUI/4Ln0XARzECI1/FNkSGRAW/8WUK8WJV29qWxEU0YBuRNCZtbpMpSQVGw4baitOJ8V8AZKu0xHbsH2Cop0URPIg7xCJ9gUbx4BmZyS522E7/QHzuYdboFL81qKIpV6UbsmSAgbJQBspF/0Z+8KYv0jEl/7zPivbj8ZUQjfsXZX1FxBmVp1NnSpKDxQMCfLh3jKc4EWl6NQbCDeg84UkcBBrpGDGzMGs/jWgIGn7mBOw6WXMrnPA6gbGRN0JeLIgTYh/5xEADyuPH/V43ARMwgeUigIi45557kjhQR46Pyv0U+eMX8VVRmLA9juyMuR+JkR2N6JD3UEFFnnmI/ho/i60hU5QST7m9Mb/Jm39Z0MtiJahkA24IuFhG7WMJU13AUx71JYpD+vwFstrXteTYcg8do2vY1Edphj78EAXsEKayP/XygtkfWH85daYxP564lECL29vWeaCA+9b6Rtna0nv70gjgIGgUBP2vJsPDnOi8b4bG2PVum6Xl6lQmYAImsHQC+Cg6cS7w+SAo8FUIsjZxsfTc1l5K8aNmiB/ETC5mu2o9b/o227HvIc5a7H9WXJwJPiKN6Uo+NCKmPQm8rBYhxjvSGCmb9/Ubys/LcQRK4mycBcc2ARMwARMwARMYQmDFpjXzwiHAuBeND+G1115LS90EmH74ywRMwARMwARMwATWOIHJn9Zc4zxdPRMwARMwARMwAROYi4DF2Vz4nNgETMAETMAETMAE6hJYmGnNutWytdoEuBmUmy4dTMAETMAETMAElpeAxdny8l0z1nkSc8xj5Wum4q6ICZiACZiACUxMwNOaEwN3diZgAiZgAiZgAibQRcDirIuO95mACZiACZiACZjAxAQsziYG7uxMwARMwARMwARMoIuAxVkXHe8zARMwARMwARMwgYkJWJxNDNzZmYAJmIAJmIAJmEAXAYuzLjreZwImYAImYAImYAITE7A4mxi4szMBEzABEzABEzCBLgIWZ110vM8ETMAETMAETMAEJiZgcTYxcGdnAiZgAiZgAiZgAl0ELM666HifCZiACZiACZiACUxMwOJsYuDOzgRMwARMwARMwAS6CFicddHxPhMwARMwARMwAROYmIDF2cTAnZ0JmIAJmIAJmIAJdBGwOOui430mYAImYAImYAImMDEBi7OJgTs7EzABEzABEzABE+giYHHWRcf7TMAETMAETMAETGBiAhZnEwN3diZgAiZgAiZgAibQRcDirIuO95mACZiACZiACZjAxAQsziYG7uxMwARMwARMwARMoIuAxVkXHe8zARMwARMwARMwgYkJWJxNDNzZmYAJmIAJmIAJmEAXAYuzLjreZwImYAImYAImYAITE7A4mxi4szMBEzABEzABEzCBLgIWZ110vM8ETMAETMAETMAEJiZgcTYxcGdnAiZgAiZgAiZgAl0ELM666HifCZiACZiACZiACUxMwOJsYuDOzgRMwARMwARMwAS6CFicddHxPhMwARMwARMwAROYmIDF2cTAnZ0JmIAJmIAJmIAJdBGwOOui430mYAImYAImYAImMDEBi7OJgTs7EzABEzABEzABE+giYHHWRcf7TMAETMAETMAETGBiAhZnEwN3diZgAiZgAiZgAibQRcDirIuO95mACZiACZiACZjAxAQsziYG7uxMwARMwARMwARMoIuAxVkXHe8zARMwARMwARMwgYkJWJxN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LzMOFZfSedvaIRCf8PGU5to5rq6JCZiACZjAOAILI87GFdux1woBzf8zWqp7PRBmnnJYK0fY9TABEzABExhLwOJsLDHHr0qAmzkZMVPgvgZPZ4qGlyZgAiZgAucjAYuz8/GoL1CdEWME3WxaesXGAhXXRTEBEzABEzCBZSewMA8E5DXVPWf79u3Ld/m3CZiACZiACZiACaxZAiv2nrM1S9QVMwETMAETMAETMIE5CFiczQHPSU3ABEzABEzABEygNgGLs9pEbc8ETMAETMAETMAE5iBgcTYHPCc1ARMwARMwARMwgdoELM5qE7U9EzABEzABEzABE5iDgMXZHPCc1ARMwARMwARMwARqE7A4q03U9kzABEzABEzABExgDgIWZ3PAc1ITMAETMAETMAETqE3A4qw2UdszARMwARMwW4UfcwAAQABJREFUARMwgTkIWJzNAc9JTcAETMAETMAETKA2AYuz2kRtzwRMwARMwARMwATmIGBxNgc8JzUBEzABEzABEzCB2gQszmoTtT0TMAETMAETMAETmIOAxdkc8JzUBEzABEzABEzABGoTsDirTdT2TMAETMAETMAETGAOAhZnc8BzUhMwARMwARMwAROoTcDirDZR2zMBEzABEzABEzCBOQhYnM0Bz0lNwARMwARMwARMoDYBi7PaRG3PBEzABEzABEzABOYgYHE2BzwnNQETMAETMAETMIHaBCzOahO1PRMwARMwARMwAROYg4DF2RzwnNQETMAETMAETMAEahOwOKtN1PZMwARMwARMwARMYA4CFmdzwHNSEzABEzABEzABE6hNwOKsNlHbMwETMAETMAETMIE5CFiczQHPSU3ABEzABEzABEygNgGLs9pEbc8ETMAETMAETMAE5iBgcTYHPCc1ARMwARMwARMwgdoELM5qE7U9EzABEzABEzABE5iDgMXZHPCc1ARMwARMwARMwARqE7A4q03U9kzABEzABEzABExgDgIWZ3PAc1ITMAETMAETMAETqE3A4qw2UdszARMwARMwARMwgTkIWJzNAc9JTcAETMAETMAETKA2AYuz2kRtzwRMwARMwARMwATmIGBxNgc8JzUBEzABEzABEzCB2gQszmoTtT0TMAETMAETMAETmIOAxdkc8JzUBEzABEzABEzABGoTsDirTdT2TMAETMAETMAETGAOAhZnc8BzUhMwARMwARMwAROoTcDirDZR2zMBEzABEzABEzCBOQhYnM0Bz0lNwARMwARMwARMoDYBi7PaRG3PBEzABEzABEzABOYgcMGXszBH+mpJT58+3Rw+fLg5duxYc+rUqebzzz9Pti+88MLm4osvbi699NL0Wb9+fbU8bcgETMAETMAETMAEFo3AioszhNi7776bRNkQOFu3bm127tzZWKQNoTUszkcffXQm4mWXXXZm3SsmYAImsFoJnDx5snn//febDz74IC2pB/6N/uOKK65I62Prhk0+hI0bN6ZPn42YpivuUHtdNrxv7RBYt5JVYaSMhsOo2bp161Jj2bx5czrhL7roomb//v3Nli1bmk2bNjW7du1q9uzZ03z44YfN0aNHUwPbtm3bShZ/VN400BdeeCHV7YYbbhic9o033kiMrrnmmuRQBiccEfHRRx9tEGg4rvvuu29ESkc1ARMwgcUjgK999tlnzwipUgmvu+665qabbhol0p566qnm1VdfTeauuuqq5q677iqZPmsbAhEfOzRIPI4tW8n+22+/fZY4RQAiTCn7kAtx0r/zzjtn+gfKdu2115ayOmcbfZ7SS9CSZ42+DHscB/ot1rFLna6++upzysEG4sVBiGKkwsY2e4Wo1TetmDg7ePBgOmmoEVOWu3fvbpjCzMORI0caPgcOHGhef/31Zu/evUmk8RtRt2PHjjzJQv7mBMdZcBKNEWfPPfdcuuojHY3KwQRMwARMoJ0AfpaPAhf4+E8CHTT9CYHOHb98++23D/KtpJUwIz1pER+1O3AGLPiMKRvliYGyPvHEE8lG3B7XEX98SgFB+fjjjxcFDSxvvfXWznp3pefY0Afecsstpax7tyGQEd+lQNnuvPPOM8dbcThu8ZzQ9r7lww8/3Bdl2faviDjTiBm1YkRs+/btgyp44sSJ5qWXXmpYot45gRF0q2EE7ZlnnhlUxxiJUTNOcgcTMAETMIF+ArETZpQHAZCLJ4QLHTVxWUeE3H333b1TlIilPLz55pvn2M/jxN+IEkaO2gL+nnLRt40pW7RHOs2GsH3Dhg1nRrvYp3rAgJG0fLBA6TXapVE2pdV+RFDOlvy0P6YnHr/p0xDHmkVqE4fYKYUozKgXdqlDLNtDDz2UjqcEecnOatg2uTjjHjNOPAKjXkOFWYTJCBp29u3bl2wx8raI96BxMtLYaASqc6xH2zonGo1+KUq/zaa3m4AJmMBaJ/DKK6+kKjJadscdd5wzgsJOOu3bbrstxZNAQ7B0iSYia7QGsUIgDenHjAAx+1ESNMng7It9N954Y/PII48k++oLmIIdGug3SEcojY4x2ocgpX8iLrYROAoIOwkrOMW8sUvZEFhPPvlkUdQqPeKJYxDrS3lIT38IT4RhzFtlKC0RdjoGCG+mlGPaWC9GDeOUM3XQcSvZ1jbq9/TTT6f6jxWOslFrOfmrNDgoTEfqxv6lVuStt95KU53Y4oGCRQo02vvvv7+599570xWMrlT6yvjYY4+lNA888EDDFYIaSF867zcBEzABE/hKMMEBQdA3chJHjOjYuwIX2ZrFoKOX4MBH96Xtstu2LwoD5dsWN9/OhT0BMRLtKB5lV90pPwJTgbpEYReFGXFgKpvEU15KL7HL79KoJWJKYpa88/SyU1pKmEl4R2FGfOrFdCuBPjceF8rN/r7Piy++mPpd6q16JoMr8DXpyBmjXdzQT0D5zhtefvnlNPLG6zcQaaV71ubNYynpOWl1X8OY9AjXRRJknOC6EqVB5Y1BdeMqhXD99defdXWiKzgaBCc7jYUGhrOBD+cAV5I0gj5Hqry8NAETMIESAYkK9rX5qphON8azjQ6/K0gYEIdbavDTmtlAkODjaoboD8f0CfhYxc+FVSwf+1T+KP6iUGtLT/01ukT/EOMxukWAJ/1BKcBKwqePe0yvQQ7SRz4xDmXj2MMA4TfmuMADFpRJ5Yu2p16fVJxJsDBqVmMaErHHgwVXXnllc+jQoSqCr8YBYHg8f+qRYeTYCEr5MIcfAyejhE/cPtU6zk6NlZO1zeEpDg0hDh3jKNSgsCVnoPIjRvnQiKi7H3gQGS9NwATGEogdNj6ly2fJdpz60rbSUn4MIYIf5IOvYzt5IQba/GPJXt+2sUJT9j777DOtdvrTyOpMgtkK/phA3driUE8urKm74qdEsy9YEBBJXWGs+Ik8+voJysfxiCNnXWVhX+yfmMptq3ufnZr7JxVnH3/8cSo794jVCu+9914SZ8ePH69lcm47nBx5Q2X+vS/kJ0Q8IfvSLvJ+OS+uSBhOV+NC1PGhITGNO9RRLnJdXTYTMIGVIyDBhO/kxnBEQJfQGFJS/Jd8cRwlQoAgUPBf+DFNFQ6x2RdHIod4fffCRVuIJk3t5f1JjBeFi/oq6qEBhK602MGHq+6wIb7Ssl9lFhuWBMrHRbzyTBtHfg1Nq8GgIeb1qhOO75jRtiG2lxpnUnH26aefpnLWGDVThdVo9I8C2u7l4hCgYSLM7rnnnrMaJY2A40cjV0Mf2vAWp3YuiQmYwKIQYNQDUYbPwbdo5kG3UOBztD60zLq1Ax8WO246ci4qCUzn1RBnlJspVE2jInJinn1lRiS1TSfGtNzMryAhpb6U7X3iLPppCa8ohtgfn6xUXrINqzG8Yn6IwCiSo23WVQ+VK9+f/2ZGhzSLMp2p8k0qzrgvjMDfMdUKvFaDwBSnw+ISyJ+sUUl19clvGlNshIrjpQmYgAkMIYCo4LUYdLi63YJ0uoVC24jHiBoja11ChE5bo1i5SMJXaaRu6MUlgqXttUpMSUZBgW09VTqk7kPiUB8EqwRMHCmKeff54chM6WSTciAuxRoxjD3icRyIBwd+D53ejKyxS7pSGSVqh7AgDmVRORG1sV5DbSxXvEnF2dhKMDxLI4uKfKwNx195AjTOtpM+bqehxN8rX3KXwARMYLURwIcgaujAmb5DXDHaEvsRfI06ZuK1iQREl0JppCdeXCIM2uzIBoJEYkbbSkuEB2KwJEBK8Ydso3z0p8qfETM9OZmnX0q+sostBA9+P3+dCcz1Kg7KggDNRW9eFv1GSEoEIzApe+wvVD/FH7KkDJSJUbOu0bghtmrHmVScMZ3JCBdTkPw9U19AyfJ5/vnnkxKPjUtpgUpYlCc1VS4vf0Sgq6EPuRfvR5a8ZgImYALDCNBxqw8hBZ0wIg2xhmhTf0IHjY8qiS+NxLAf8RHv1cKm+h/W2dcnzhAACJJSwD4jSyqbhFSbgCrZKG3DHrYkNPG5N998c7G+pfSlbVGIlfbDpTRbIuGse7wQcUPFGceSOpCGY8hHLOGmMiEK+d0XJM6JRxmi0OtLO8X+ScUZggxxBsQh4kwAeCkfVyicYBqC1D7+d5NQc6pUtr00ARMwARNYGwTofPnQlxC46OeVEAT6FoRTvJBEyPEh0GdJUKQNhS+EA0KoS2ywr2+EBtGg++Y0GhfLVci6uIkyM8KEiFEgbwRkSYjEPChDV5AQIk7JFoyjvWhLQog8JBjj/q51PUnJsWMaOKZHdLKf+iLOEGldQcKbOH2iusvOcu2bVJwhpHgnGZ+xT2xyAmiomhNOB4W/fyJccskly8VoVdvlRlVOVBpK6cpw3srFRjqvLac3ARMwgaUS4MKdDn+or+OiH99IOvwYafUkOWWInffQMtEvdYmzIXbo6xBRyj8v1xAbiMr435iMMCFAusoWRVafX4/7lU5Lyhc5lsqLcKJeSwnUg76MOsoGeatu4hbLU8pHopXp3b64pfTLvW1SccZfNfFeMl5Ey8FZylQkEBku5Qma3/3d301/gg6kOLy83NBWk31OQJwP3JZDnKlxrCYmLqsJmMDaI8CFKP5uqDiDAB26ZmOi4GCfBgAQNn2v+eHfYEiPMKgxChNHnfJyUbaugE+Of6E0dAqTPOknSK8Rw7Z8tD+OTo3pg8fWKS8HZZUYi/uwq+NW2q+4nCfqu/S0qvYtynLSv29CjG3evDm9zX/ev1xi/vl73/te4ljrpbaLclCWoxxdjUH7xjQulXHI3L7iemkCJmACy0VAox/4M6YXhwT5PuJGQaRROLb3TUPGOGPyJl1bUF3a9ndtZ2aJcjDNh6gcc1Gue7gQOJFNzA9RUxJAcbRM4i2mi+u6329Mn8PfG/IwgUbGoj2tazSM312iS/9kQDxNc7O+SGFScUbFd+/enUbMjh492hw+fHjJLDQCt27dut655SVnsgYSyuHQ0EoNhoamRqi4qnb8rcaofVpyr4aDCZiACaw0gdgZD/FL+D119IiEKC5i5901AqM6x7w1Eqd98y4lZIbYwcfLV/MgQazTkPRRiIpNni7WLwo/+guJuyhuS+k1ahXzy+Plv+FA3eKxyePouFOOLoErEUe82M/l9lby9+TijCc2NRR64MCBNM05FgCiTiM2l19+eZW/ghpbhtUSPzoNTlw1CsqPc9JLFPkd4/JbDY31Ulqu0KI94jmYgAmYwEoQQETJh9GJP/jgg8ULUsrGyBpTf/JfzMQosE2dN/a6OnmlIW918qTVBa/2j13K1th0KrfScftP3yeOMlIP+X18fi7Q+C0BhLDK2WhKl/pHvioPeSk9gjhyJw59yv79+9Mnlot98djm5VJfpuPJ/eltAbs6PkOEd5ud5d4+6T1nqsy2bduaL774IgkzRBav1kCw9f1zAC+xZTqUUTfCjh070h+fy66X5xJQY8NZ0XBZwpqTkysRnaRsyxsKDoIrIxoCJ/0DDzyQGm5My37sqlGcWwJvMQETMIFpCNApM/VFv8KHpx4REJo+i75LJUJkSFSwDR+pMGZkh7j4SvLAJ45Jq/y0jK8YYjRsqK04OxL/BUB2S0tsR5ECQz0tysU74o6+AB+vUTx4Rmayix2262JefYbSa1BFU65KN2RJX0NZKAPlYgSN/ODNSB1LAvnnojHaj8dXQjTuX5T1FRFnVB4xwJQkB4sHBPhw7xhPcSLS9GoMhBvQecKTOAg00jFixgMGDv0EaGw0Fp3A8eQkNVckbVcanOg6+Ykb09JYGDrPr9aI52ACJmACUxNABPA3cfg7deSIitLFIx0z/i0KE8obR3bG3I+EH9WIDnkPFVQlRlFc4LexNWSKUuKpZHPoNvLmXxb0slgJKqWHG/1FLKP2sYQp4g2OlCf2Gewnff4CWbb3BY4t99AxuoZNfZQOwTfk4YcoYIcwlf2plxd8OQtTZxrz471nEmhxe9s6DxRw31rfKFtb+vN5Ow6Kqw3eD0OgAeGY2hpZZEVaTmqEGo2EdCwdTMAETGBRCTCFRSeO3+KDrxvj9xa1XlOVS/zID/GDmMnFbFdZ5k3fZhu79EexL+t6t1qbnUXevuLiTHAQaUxX8qERMe1J4GW1CDHekcZI2VJev6E8vDQBEzABEzABEzCBRSewMOIsB/Xaa6+lTfv27ct3+bcJmIAJmIAJmIAJrFkCkz+tuWZJumImYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgcAFX85CBTtzmzh9+nRz+PDh5tixY82pU6eazz//PNm88MILm4svvri59NJL02f9+vVz52UDJmACJmACJmACJrCoBFZcnCHE3n333STKhkDaunVrs3PnzsYibQitYXE++uijMxEvu+yyM+vzrpw8ebLhs3HjxvSZ157Tm4AJmMBQAvie999/v/nggw/SknT4N/qPK664Iq0PtaV48mn8HurXYhrZKS2H2iul9ba1R2DdSlaJkTIaDqNm69atS41l8+bN6aS/6KKLmv379zdbtmxpNm3a1OzatavZs2dP8+GHHzZHjx5NDWzbtm0rWfxRedNAX3jhhVS3G264YXDaN954IzG65pprkkMZnHBExEcffbRBoOG47rvvvhEpu6M+9dRTzauvvtpcddVVzV133dUd2XtNwARMoBIBfO2zzz6bLg7bTF533XXNTTfdNEqkyadhc6hfQyDiY4cGicexZSvZf/vtt88SpwhAhCllH3IhTvp33nnnTP9A2a699tpSVudso89TetYJ5FmjL8MefQv9FuvYpU5XX331OeVgA/HiIEQxUmFjm71C1OqbVkycHTx4MJ001Igpy927dzdMYebhyJEjDZ8DBw40r7/+erN3794k0viNqNuxY0eeZCF/c4LjLDiJxoiz5557Ll31kY5G5WACJmACJtBOAD/LR4ELfPwngQ6a/oRA545fvv322wf5VtKSRoG0iI/aHTgDFnzGlE1l0pKyPvHEE8mGtuVLxB+fUkBQPv7440VBA8tbb721s95d6Tk29IG33HJLKevebQhkxHcpULY777zzzPFWHI5bPCe0vW/58MMP90VZtv0rIs40YkatGBHbvn37oAqeOHGieemllxqWqHdOYATdahhBe+aZZwbVMUZi1IyT3MEETMAETKCfQOyEGeVBAOTiCeFCR01c1hEhd999d++tF4ilPLz55pvn2M/jxN+IEkaO2gL+nnLRt40pW7RHOs2GsH3Dhg1nRrvYp3rAgJG0fLBA6TXapVE2pdV+RFDOlvy0P6YnHr/p0xDHmkVqE4fYKYUozKgXdqlDLNtDDz2UjqcEecnOatg2uTjjHjNOPAKjXkOFWYTJCBp29u3bl2wx8raI96BxMtLYaASqc6xH2zonGo1+KUq/zaa3m4AJmMBaJ/DKK6+kKjJadscdd5wzgsJOOu3bbrstxZNAQ7B0iSYia7QGsUIgDenHjAAx+1ESNMng7It9N954Y/PII48k++oLmIIdGug3SEcojY4x2ocgpX8iLrYROAoIOwkrOMW8sUvZEFhPPvlkUdQqPeKJYxDrS3lIT38IT4RhzFtlKC0RdjoGCG9ulYlpY70YNYy30lAHHbeSbW2jfk8//XSq/1jhKBu1lpO/SoODwnSkbuxfakXeeuutNNWJLR4oWKRAo73//vube++9N13B6Eqlr4yPPfZYSvPAAw80XCGogfSl834TMAETMIGvBBMcEAR9IydxxIiOvStwka1ZDDp6CQ58dF/aLrtt+6IwUL5tcfPtXNgTECPRjuJRdtWd8iMwFahLFHZRmBEHprJJPOWl9BK7/C6NWiKmJGbJO08vO6WlhJmEdxRmxKdeTLcS6HPjcaHc7O/7vPjii6nfpd6qZzK4Al+TijNGu7ihn4DynTe8/PLLaQSN128g0hYlcNLqvoYxZUK4LpIg4wTnCoRPV7kUZ6gIHcPEcU3ABExgCAGJCuLmHXcpvW6MR8TQ4XcFCQPicEtNFC1R3HTZGLMvCssu35vbRJAofixjHi/ui+Iv1iXGiempv/hqpFL7Gd0iwPP666/X5rOWCCSED58+7jGh+hfSRz4xTizbGOGHDUYRYUGZVlqYUZ5JpzUlWBg1qzENidjjwYIrr7yyOXToUBXBB5R5A8Pj+VOPDCPHRlDKgzn8GCSO4rYp13F2aqycrGqQeRkUh0YzZOg4T+/fJmACJjAvgdhh0zF3+SzlFae+tK20lDBAsOAH+eDr2E5eCKI2/1iy17dtrNCUvc8++0yrnQ85RFZnEsxWdPsNdWuLQz0ZXKHuii8bEkSIpK4wVvxEHn0PxlE+jkccOesqC/uwr9uImMptq3ufnZr7JxVnH3/8cSo794jVCu+9914SZ8ePH69lcm47nBx5Q2X+vS/kJ0Q8IfvSer8JmIAJnO8EJJjwndwYjgjoEhpDeCE45IvjaBICBIGCEOACVVOFQ2z2xZHIIV7fvXDRFqJJU3t5fxLjReGivop6aAChKy12EEiqO2yIr7TsV5nFhiWB8nERrzzTxpFfQ9NqMGiIeb3qhONL+RYhTCrOPv3001TnGqNmgqdGo38U0HYvTcAETMAEzi8CjHogyhAD9A3cckFAFOhmfK0PJaOpO6a7YsdNR869wQSm82qIM8rNFKqmUceKBURS23RirC838ytISKkvZXufOIsCScIriiH2xycrlZdsw2oMr5gfIjCK5GibddVD5cr357/1AMWiTGeqfJOKM90Xxt8x1Qq8VoPAFKeDCZiACZjA+UsAUcFrMehwdbsFNJh+46NtxGNEjZG1LiFCR69RrCjMsIlg0EidRpGiiCBOHhAsba9VYkoyCgps6+b53M5Sf0uwSsBE8Rfz7qtHZKZ0sknZEJdijRjGHvE4BsTTA29Dpzcja+ySrlRGidqhfCiLyomojfUaamO54k0qzsZWQif+2HSObwImYAImcH4SoINlBI0OnOk7xBWjLXFkh05ZHTPx2kQCokuhNNKjqU3iIAza7MgGAkViRttKS4THvNN/uV3Kh2hV/oyYtYm/kvDJ7eW/ZZftCB5EWf46E5jrVRyUhT4+F725Xf1GSEoEMyJK2aOYUv0Uf8gyjpp1jcYNsVU7zqTijOlMRriYguTvmfoCDYzXSnQFPe1R+neBrnTeZwImYAImsHYJ0HEzGqJpPoQBIg2xhmiTWKODRoyUxJdGYtiP+Ij3akFO/Q/r7OsTZwgABEkpYJ+RJZVNQqpNQJVslLZhD1sSmtz/fPPNNxfrW0pf2haFWGk/XPL3kBFPwln3eCHihoozjiN1IA3HkI9Ywk1lQhTyuy9InBOPMkSh15d2iv2TijMEGeIMiEPEGbA42Tmx2gL/u0moOVXalpe3m4AJmIAJrE4C9Cd89CTh888/n144Sm3oYxBOccQIIceHQJ8lQZE2FL4QDgihLrHBvr4RGkSD7pvTaFwsVyHr4ibKzAgTIkaBvOlTS0Ik5kEZuoKEEHFKtmAc7UVbEkLkIcEY93et60lKjh3TwDE9opP91BdxhkjrChLexOkT1V12lmvfpOIMIcU7yfgMfWKTqxkgxpMhwuDvnwiXXHJJ3Oz1rwlwoyonKg2ldGU4L6i24zKvXac3ARMwgTEEGFGhwx/q63gTP76RdPgx0sbXNMTOe2g5EAtd4myIHcQOIkr55+UaYgNRGf8bkxEmBEhX2aLI6vPrcb/SaUn5IsdSeRFO1GspgXrQl1FH2SBv1U3cYnlK+Ui0Mr3bF7eUfrm3TSrO+Ksm3kvGi2g5OEOmImloP/uzP3vmCicCQezt2bMnbYrDyzHO+b7OCYjz4eRbDnGmxnG+c3b9TcAEVpYAF6L4u6HijNLSoeMfCVFw8FujMgibvveh8W8wpEcY1BiFoQ4Kebm0vW2JT45/oTR0CpM86SdIrxHDtjy0P45OjemDx9YpLwdllRiL+7Cr41bar7icJ+q79LSq9i3KctJ/CECMbd68Ob3Nf8xfLnGFo7nlCE7D07Veahttr7X1rsagfWMal/gMmdtXXC9NwARMYLkIaPQDf8b04pAg30fcKIg0Csf2vmnIGGdM3qRrC6pL2/6u7UxlUg6m+RCVYy7K1c8icCKbmB+ipiSA4miZxFtMF9d1v9+YPoe/N+RhAo2MRXta12gYv7tEl/7JgHjSEawvUphUnFHx3bt3pxGzo0ePNocPHx7MIr8a2bt3bxo1W7duXe/c8uBM1mBEORwaWqnB0NDUCBVXGOJvNUbt07LrfkDF8dIETMAElptA7IyH+CX8njp6REIUF7Hz7hqBUZ1i3hqJ0755lxIyQ+zg4+WreZAg1mlI+ihExSZPF+sXhR/9hcRdFLel9Bq1ivnl8fLfcKBu8djkcXTcKUeXwJWII17s53J7K/l7cnHGE5saCj1w4ECa5hwCgAaiBvDd7373jNq9/PLLq/wV1JAyrMY4YkbZOXHVKPiNc9JLFPkd4/JbDY31Ulqu0KI94jmYgAmYwEoQiH0EnfiDDz5YvCClbIysMfUn/6UnOtnHNnXe+MSuTp74BPJWJ09aXfB+tXf8t2yNTalyKx0v0O37xFFG6iG/j8/PBRq/JYAQVjkbDaJQ/8hX5SEvpUcQR+7EoU/Zv39/+sRysU/9E8c2L5f6Mh1PHgxoC9jV8aG+ixomvedMELZt29Z88cUXSZgxLcarNRBsff8c8HM/93MNU5h6CGDHjh0N97E5tBNQY+OEpuGyhDUnJ1ciOknZljcUHARXRjQETnpea0LDjWnZj101ivaSeI8JmIAJLC8BOmWmvuhX+PDUIwJC02fRd6kkiAyJCrbhIxXGjOwQF19JHvjEMWmVn5bx7/4YDRtqK86OxH8BkN3SEttRpMBQT4ty8Y64oy/Ax2sUD56Rmexih+26mFefofS6DUZTrko3ZElfQ1koA+ViBI384M1IHUsC+eeiMdqPx1dCNO5flPUVEWdUHjHAlCQHiwcE+CC8eIoTkaZXYyDcgM4TnsRBmJGOETMLs2GnEY2NxqITOJ6cWOCKpO1KgxNdJz9xY1oaC0Pn+dUa8RxMwARMYGoCiIB77rkn+Tt15IiK0sUjHTP+LQoTyhtHdsbcj4Qf1YgOeQ8VVCVGUVzgt7E1ZIpS4qlkc+g28uZfFvSyWAkqpYcb/UUso/axhCniDY6UJ/YZ7Cd9/gJZtvcFji330DG6hk19lA7BN+ThhyhghzCV/amXF3w5C1NnGvPjvWcSaHF72zoPFHDfWt8oW1v683k7DoqrDd4PQ6AB4ZjaGllkRVpOaoQajYR0LB1MwARMYFEJMIVFJ47f4oOvG+P3FrVeU5VL/MgP8YOYycVsV1nmTd9mG7v0R7Ev63q3WpudRd6+4uJMcBBpPCTAh0bEtCeBl9UixHhtBiNlQ16/IZtemoAJmIAJmIAJmMBqI7Aw4iwH99prr6VN+/bty3f5twmYgAmYgAmYgAmsWQKTP625Zkm6YiZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBgMVZBYg2YQImYAImYAImYAK1CFic1SJpOyZgAiZgAiZgAiZQgYDFWQWINmECJmACJmACJmACtQhYnNUiaTsmYAImYAImYAImUIGAxVkFiDZhAiZgAiZgAiZgArUIWJzVImk7JmACJmACJmACJlCBwAVfzkIFO3ObOH36dHP48OHm2LFjzalTp5rPP/882bzwwgubiy++uLn00kvTZ/369XPnZQMmYAImYAImYAImsKgEVlycIcTefffdJMqGQNq6dWuzc+fOxiJtCK32OCdPnmz4EDZu3Jg+7bG9xwRMwARWFwH82/vvv9988MEHaUnpL7vsstR/XHHFFWl9bI2W4jdjmq787Ie76Jx/+1ZUnDFSRsNh1GzdunWpsWzevDkJhYsuuqjZv39/s2XLlmbTpk3Nrl27mj179qQjxGgaAm3btm2r5ojRQF944YVUtxtuuGFwud94443E6JprrmlwKLXCAw880Hz00UfJHOW55ZZbapm2HRMwARNYUQL42mefffbMBWipMNddd11z0003jRJpTzzxRPPqq68mc1dddVVz1113lUyfte3tt99uHn300bO2df2gb8PXjy1bySZ5R3GKAMQ2ZUeo9gXSv/POO6mvkLC99tpr+5Kl/fR5Ss86ARs1+jLscRzow1jHLnW6+uqrUz75F/HU3+X7un632etKU2vfulqGxto5ePBgOmlIx5Tl7t27G0RXHo4cOdLwOXDgQPP66683e/fuTSKN34i6HTt25EkW8jcnOM6Ck2iMOHvuuefSVR/paokzGkw8UTnJcQQ0XAcTMAETWM0E8LN8FLjAx38S8Hv0JwT8Hn759ttvH+RbSSthRnrS4ktrd+CIKT5jykZ5YqCsCElstAV8Pp9SYMTx8ccfP6ufUDxY3nrrrZ317krPsZlnQOCpp55KAx0qT1xStjvvvPPM8dY+jls8J7S9b/nwww/3RVm2/SsizjRiRq0YEdu+ffugCp44caJ56aWXGpaod05gBN1qGEF75plnBtUxRmLUjJO8dogOBttcedCIuaJxMAETMIHVSiB2woxAMSOQiyeECx01cVlHhNx99929F6clofPmm2+eY7+LHaKky8/i7ykXfduYssU8ScdIHUvChg0bUn/JOttUDxhwQZ4PFii9Rrs0yqa02o8IytkqD/KP6YnHb/o0xLFmkdrEIXZKIQoz6oVd6hDL9tBDD6XjKUFesrMatk0uzrjHjBOPwKjXUGEWYTKChp19+/YlW4y8LeI9aJyMNDYageoc69G2zolGo1+K0m+zqe3YljhjWJ98KOfzzz/f6TSU3ksTMAETWFQCr7zySioao2V33HHHOSMo7KTTvu2221I8CbQhF6cICgJihUAa0o+5JYTZj5KgSQZnX+y78cYbm0ceeSTZV1+Arx4a6DdIRyiNjjHahyDF7xMX23HWJAorOMW8sUvZEFhPPvlkUdQqPeKJYxDrS3lIT38IT4RhzLurjgg7HQOEN1PKMW2sF6OGccqZOui4deVB/Z5++unEZqxw7LK7lH2Tv0qDg8J0pG7sX0qhSfPWW2+lqU5s8UDBIgUa7f3339/ce++96QpGVyp9ZXzsscdS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QAISkEArAoqzViS1IwEJSEACEpCABBoQUJw1gKgJCUhAAhKQgAQk0IqA4qwVSe1IQAISkIAEJCCBBgQUZw0gakICEpCABCQgAQm0IqA4a0VSOxKQgAQkIAEJSKABAcVZA4iakIAEJCABCUhAAq0IKM5akdSOBCQgAQlIQAISaEBAcdYAoiYkIAEJSEACEpBAKwKKs1YktSMBCUhAAhKQgAQaEFCcNYCoCQlIQAISkIAEJNCKgOKsFUntSEACEpCABCQggQYEFGcNIGpCAhKQgAQkIAEJtCKgOGtFUjsSkIAEJCABCUigAYFT/vl7aGBn2yZ+++23xeeff7749ttvF7/88svi559/7myeeuqpi7PPPntx/vnnd5/TTz9922VpQAISkIAEJCABCexUAhsXZwixDz/8sBNlcyBddNFFi8suu2yhSJtD6z9pvvzyy2NfLrzwwmP7Uzs//vjjgg9hbp4pe8ZJQAISWBcBfNfHH3+8+OSTT7ot5eLHGD8uv/zyLfm06hPPOuusBZ9loeaZSjvX3pQN4/YOgY2KM2bK6DjMmu3bt6/rLPv37+8u+DPOOGNx5MiRxQUXXLA499xzF1dcccXi4MGDHXlm0+hgBw4c2DVngg768ssvd227+eabZ9f77bff7hhdd911nUOZnbGXEJYJlH/77bfn6+j26aefXrzxxhtd/GOPPTaazggJSEACO4kAvvaFF144dnM5VLcbbrhhceutt64k0qpPvPrqqxf33nvvkOnjjr333nuLJ5544rhjU18iHlet25BNyq7iFAGIMKXuc264yf/+++8vuLmPsL3++uuHivrDMca85GefgI3tjmXYwR5jE/ViH7u06ZprriH6D4F0dYLiDwlGDozZG0ne9PC+ptZWMPbpp592Fw1ZWLK86qqrFoiufvjqq68WfI4ePbp46623FocOHepEGt8RdZdeemk/y478zgWOs+AiWkWcvfjii91dH/noVC0CjosOsskLr0U7tCEBCUigTwA/yyeBG3z8J4EBmvGEwOCOX77rrrtm+Vby5maV/ORFfLT2o4gpPqvUjfrUQF0RktgYC4g/PkOBGcennnpqUNDA8o477phs91R+zs3cCYKhuj377LPdRMdQHHW75557jp3vpOG81Wsix5dtNzkpsRFxlhkzwDAjdvHFFy9j1MV///33i1dffXXBFvXOBYyg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" alt="ApplicationImage">
                        </div>
                    </div>
                </body>
            </html>
        """

        st.markdown(html, unsafe_allow_html=True)

    st.markdown("""
            <style>
            .stButton>button {
            border: none;
            border-radius: 25px;
            cursor: pointer;
            margin-left:0px;
            display: flex;
            width: 100%;
            border: none;
            margin-top: 120px;
            background-color: #e53e3e;
            color: white;
            padding: 14px 28px;
            font-size: 36px;
            cursor: pointer;
            text-align: center;
                }
            </style>
            """,unsafe_allow_html=True
            )

    if st.button('Continue'):
        st.session_state.checkout_step = 10
        st.rerun()


def add_repayment():
    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 600px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .logo {
                        text-align: left;
                        margin-left:-10px;
                        margin-bottom: 40px;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 30px;
                    }
                    .htext {
                        margin-top:30px;
                        text-align: left;
                        color: #333;
                        margin-left:-10px;
                        margin-bottom: 30px;
                        font-size: 30px;
                    }
                    input[type=text], input[type=password] {
                        width: 100%;
                        padding: 15px;
                        margin: 10px 0;
                        display: inline-block;
                        border: none;
                        border-radius: 7px;
                        box-sizing: border-box;
                        background-color: #f3f3f4;
                        color: lightgray;
                    }
                    .footer {
                        text-align: center;
                        margin-left: 30px;
                        margin-top: 20px;
                        margin-bottom: 10px;
                        color: #a0a0a0;
                    }
                    a {
                        color: #01394D;
                    }
                    a:hover {
                        color: #c53030;
                    }
                    .card-input {
                        margin-bottom: 10px;
                        padding: 10px;
                        font-size: 16px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        display: block;
                        width: 100%;
                        box-sizing: border-box;
                    }
                    .card-details {
                        display: flex;
                        justify-content: space-between;
                    }
                    .card-details div {
                        width: 48%;
                    }
                    </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="logo">
                        <img src="data:image/png;base64,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" alt="Logo">
                    </div>
                    <p class="htext" style="font-weight:light;">Add repayment method</p>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)

    html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .card-form {
                background-color: #ffffff;
                max-width: 450px;
                margin: 10px auto;
                padding: 10px;
                border-radius: 8px;
            }
            .card-form h2 {
                font-size: 18px;
                color: #333;
                margin-bottom: 20px;
            }
            .card-input {
                font-size: 16px;
                display: block;
                width: 100%;
                box-sizing: border-box;
                padding: 15px;
                margin: 10px 0;
                display: inline-block;
                border: none;
                border-radius: 7px;
                box-sizing: border-box;
                background-color: #f3f3f4;
            }
            .card-details {
                display: flex;
                justify-content: space-between;
            }
            .card-details div {
                width: 48%;
            }
        </style>
        </head>
        <body>
            <div class="card-form">
                <p style="font-weight:light; font-size:16px; color:#333; margin-bottom:-5px;">Card Number</p>
                <input type="text" class="card-input" placeholder="0000 0000 0000 0000" />
                <div class="card-details">
                    <div>
                        <p style="font-weight:light; font-size:16px; color:#333; margin-bottom:-5px;">Expiration (MM/YY)</p>
                        <input type="text" class="card-input" placeholder="MM/YY" />
                    </div>
                    <div>
                        <p style="font-weight:light; font-size:16px; color:#333; margin-bottom:-5px;">CVV</p>
                        <input type="text" class="card-input" placeholder="CVV" />
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    components.html(html_content, height=300)

    st.markdown("""
        <style>
        .stButton>button {
        border: none;
        border-radius: 25px;
        cursor: pointer;
        margin-left:0px;
        display: flex;
        width: 100%;
        border: none;
        margin-top: 150px;
        background-color: #e53e3e;
        color: white;
        padding: 14px 28px;
        font-size: 36px;
        cursor: pointer;
        text-align: center;
            }
        </style>
        """,unsafe_allow_html=True
        )
    
    if st.button('Continue'):
        st.session_state.checkout_step = 11
        st.rerun()


def application_submitted():
    creds = ServiceAccountCredentials.from_json_keyfile_dict(GDRIVE_CREDS, SCOPE)
    client = gspread.authorize(creds)
    gsheet = client.open("streamlit_data").worksheet('flow_data')
    # print(st.session_state['gsheet_data'])
    gsheet.append_row(list(st.session_state['gsheet_data'].values()), value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS', table_range="A1")
    st.session_state['gsheet_data'] = {}

    html = """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f2f6;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 10px;
                        width: 300px;
                        margin: 0px auto;
                        padding: 10px;
                    }
                    .logo {
                        text-align: left;
                        margin-left:-10px;
                        margin-bottom: 40px;
                    }
                    .applicationimage {
                        text-align: center;
                        height: 200px;
                        width: 400px;
                        margin-top:100px;
                        margin-bottom: 40px;
                    }
                </style>
            </head>
            <body>
                <div class="container" style="margin-left:10px;">
                    <div class="logo">
                        <img src="data:image/png;base64,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" alt="Logo">
                    </div>
                    <div class="applicationimage">
                        <img style="width:370px; height:310px;margin-left:-40px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAo4AAAIaCAYAAACu+cy1AAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAACjqADAAQAAAABAAACGgAAAADaAAnYAABAAElEQVR4Aey9b5Acx3XgmdUDwAQBUAPrj0WKskq2RdLhs9iwGb5Pkgqx/rDmmeLQd2ufeeFFww5LjlhpCa28EZa0oWkobEkfpAXo9Uas7LOnsRsrr70OAzRt+YvvuildxN1tSEZLCodFSudpyRSptf5gTAAkRGC67r1GF1RIVHVX9b/Kqvq94GNVZr7MfPnLmpmHrKosYxAIQGCpBP72vqb/hXubXT0utSMahwAEIAABCCyZgLfk9mkeArUmoMHi1dB0TWh8ATHY2zBHf/RL/UGtoTB4CEAAAhAoLQECx9JOHY67TsAKGiN3CR4jEhwhAAEIQKB0BAgcSzdlOFwGAilBY+Q6wWNEgiMEIAABCJSKAIFjqaYLZ8tAYErQGA2B4DEiwRECEIAABEpDgMCxNFOFo2UgkDFojIZC8BiR4AgBCEAAAqUgQOBYimnCyTIQyBk0RkMieIxIcIQABCAAAecJEDg6P0U4WAYCMwaN0dAIHiMSHCEAAQhAwGkCBI5OTw/OlYHAnEFjNESCx4gERwhAAAIQcJYAgaOzU4NjZSCwoKAxGirBY0SCIwQgAAEIOEmAwNHJacGpMhBYcNAYDZngMSLBEQIQgAAEnCPQcM4jHIJASQi8HJqN8RdhFumx/7IxrUU2SFsQgAAEIACBRRFgxXFRJGmnlgQ+f0+zLT9Emwsc/Jk3P9NvLbA9moIABCAAAQgsjACB48JQ0lBdCSwweCRorOtFxLghAAEIlIQAgWNJJgo33SawgOCRoNHtKcY7CEAAAhAQAgSOXAYQWBCBOYJHgsYFzQHNQAACEIDAcgkQOC6XL63XjMAMwSNBY82uEYYLAQhAoMwECBzLPHv47iSBHMEjQaOTM4hTEIAABCCQRoDAMY0M+RCYg0CG4JGgcQ6+VIUABCAAgWIIEDgWw51ea0BgQvBI0FiD+WeIEIAABKpIgMCxirPKmJwhkBA8EjQ6Mzs4AgEIQAACEIAABBwjoMHjF+5phqIdx1zDHQhAAAIQgAAEIAAB1whI0Ljhmk/4AwEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhAoloBXbPf0DgEIQGB1BMIwXDdXrqyb3bV1E+6KDtd3jeRlkDXj7RivsTMy9dZ2zNrujrd//yBDVUwgAAEIVIYAgWNlppKBQKDeBEZB4eWr/u7w5abXMOvG8+73jCfBYeiHRtLG+EshFIYSUHo70tfAeGYnHIafN1640wjX+kYCTO/gvv5S+qVRCEAAAgUQIHAsADpdQgACsxMYBYiXrjSH3m5zFByGpil5vpxnWjmcvefZa8ovWgkivYEGlY1Qzht7BwSUs/OkJgQgUBwBAsfi2NMzBCCQgUB48aUgChJNaAKp4meo5r6JrFR6XqMvq6H9xjB8yuxt9Ln17f604SEE6k6AwLHuVwDjh4BjBDRQNA3zNllFDMJwqKuKzq4kLgHdQNrshSZ8am1trUcguQTCNAkBCMxFgMBxLnxUhgAE5iUQvvSSP9zd3fBM4+EaBooT8ckv6OsrkmHjjHdof2+iMYWVJHBx42cDeU53UwbXNNdf5OqHnnn8jnOf6lRywAzKeQIEjs5PEQ5CoHoEolXFYThsyej86o1wCSPSW9uNRk+YPcFq5BL4OtjkpUf+p2PyXGwnxbX+oSc+dSSljGwILI1AY2kt0zAEIACBGAENFncvvXhq9+KlC0Nv2JUAqC3FfsyE00kE5Ja93L6XlVlva7g73B5eerF77dKllq7YTqpGWTkJvLSx4d8IGkPz+DVv32EJFD1ZbTwuKz4DGVXz4tsfbJdzdHhdZgKsOJZ59vAdAo4TkEBn3bx45TFWFpc7UZ7nnfN2wzPeHQfOLbcnWl8VgYsbD56Wl8Ee8zzTOXjuU8fj/V6/fT3sSt6OBJOH42WcQ2DZBFhxXDZh2odAzQhosBi+cHlDV8SGl1+8wMri8i8AXYkcNszZ3UuXt0W3WIVcPvPl9+Ddr32EpnHG7uvQuT+XF6hGq47rL238U98uJw2BZRIgcFwmXdqGQI0IjALGyy9tDiV40SBG3gwOajR8V4bqiyOt+K1sVxzDj9kIhEa+cJQg8sjCjmbvmkZieUIVsiCwEAIEjgvBSCMQqC+B0T6L8dXFem2f4+zEa+Cuz0PqKmQojwuwCunsVKU4Jl8gEmmEjYdtA33+UdYim5K/I7ex+3Y5aQgskwCB4zLp0jYEKkzgxu1oedGF1UWnJ9ofDndP6yokt7GdnqebnLtmhqeNrCrKz1ZLXoLZvB4sGqPPN+6GL+vzjXof+/GbKpGAwAoI8HLMCiDTBQSqQkBvR+9evqxv9uq+cn5VxlXDcXQaa42TbDDu9sy/sPFgywvNVqKXntc7dO4vjiaWkQmBJRIgcFwiXJqGQJUIhC+++JisWrVr9iWXKk1h0lgIIJOoOJR3QV5+2WMap0zoBboBuL4U0/DCxw+e+0tZkUQgsHoCBI6rZ06PECgVAd0rkBXGUk3ZLM4SQM5CjToQqCEBAscaTjpDhkAWAvrSS+gNT8kKhz6Ej9SDAAFkPeaZUUJgZgIEjjOjoyIEqkngesAYbvLCSzXnN8Oo5FZoo+Md2H8ygy0mEIBAzQgQONZswhkuBNII6IsvRvdhNOGJNBvya0VgIP94OLnn4MFOrUbNYCEAgYkECBwn4qEQAvUgwIsv9ZjnWUYpfyT63lrjEd7AnoUedSBQPQIEjtWbU0YEgcwEeI4xM6raGzaMd9pc/e5J7/DhndrDAAAEakyAwLHGk8/Q60uA29L1nfs5R87t6zkBUh0CZSdA4Fj2GcR/COQkcE038B6GW+zHmBMc5nECvH0dp8E5BGpEgMCxRpPNUOtNQFcZw0svboWe2ag3CUa/IAKsPi4IJM1AoEwECBzLNFv4CoEZCeizjENvqJ8u82dsgmoQSCPA6mMaGfIhUEECBI4VnFSGBIGIAM8yRiQ4LpnAYBg2ju89tL+35H5oHgIQKJgAgWPBE0D3EFgWgfCll3z5tnRX2veX1QftQiBOQDYOb7NxeJwI5xCoHgECx+rNKSOCgGFfRi6CogjIHxX2fSwKPv1CYAUEGivogy4gAIEVERi/AHNqOAxP89b0iqDTzU0E9NvmutJ9VZ6rvamABAQgUAkCrDhWYhoZBASM0VvT4e7wrP7hhsdkAleff97sXrwoeumGTqqxduigUVXZd9edpnHw0I30pHp1L+PWdd2vAMZfRQIEjlWcVcZUOwK8Nf29KddgcHjporn02fNmKOdXnvmyHC+al57+yihI1PNFyV4JIvfd9dpRELn3zjuNpm+790fMbffcQ2A5hswXZxZ1tdEOBNwgQODoxjzgBQRmJjB6nlFvTddQNEi88swz5ooEhRogXpZg8epzzztBonHokNk/CiLfZG5/4MgowNSAsqYyaKw1jvK965rOPsOuFAECx0pNJ4OpG4Hw8uXNYWjadRm3BoqXP/fX5kUJEC9/7rwEjF8u1dA1mDz4QNPc/pM/MVqZPCDHGgnBY40mm6FWlwCBY3XnlpFVmIC+BDO8/OIpGWKrwsMcDS0eKOqKYpUkCiQPBW8dBZN627vishMOzfE9dxw4V/FxMjwIVJYAgWNlp5aBVZXA6M3pyy92q/wSjAaLF7ufMRee/MvR84lVnUt7XAfklvb6Qw/WIIj03rN28PZaPl5hzzlpCJSNAIFj2WYMf2tNoMqbetc1WEy7oKseRPLGddrMkw8BtwkQOLo9P3gHgRsEqhg06jOL3/nkH5kXep8p3fOKNyZmBSfrb39QViJ/xlTtmUiCxxVcPHQBgQUTIHBcMFCag8AyCFQtaNTVxW9/8r/K7ehPLwNXZdvU7X5e885frtStbILHyl6uDKyiBAgcKzqxDKs6BKoUNL7Q+7SsMP7xaNuc6sxQMSPRVchXv+NXRtv8FOPB4noleFwcS1qCwLIJEDgumzDtQ2AOAlUIGvV29M6Tn5IVxj92Zo/FOabEuapVCSAJHp27tHAIAokECBwTsZAJgeIJlD1ojJ5f/Jbckl7k11qKnxk3PahCAEnw6Oa1hVcQiBMgcIzT4BwCjhAoe9CoK4z/8Ik/YIWxgOup7AEkwWMBFw1dQiAHAQLHHLAwhcAqCJQ5aNSXXr4pAWPVNupexbwvuo8yB5AEj4u+GmgPAosjQOC4OJa0BIG5CYy/CKOfR/HnbmyFDbz83DfMc+3fJGBcIfMsXUVvYeum4uUTNgkv35zhcR0IEDjWYZYZY2kIDC/pF2HCoCwOR88x6m1pxF0CGkC+rv1+c+CBcn0bWz5P+AifJ3T3usKzehIgcKznvDNqBwmEl148NTThCQddS3RJb0t/ffPDPMeYSMfNzBLevt7ZNeHRfQcP9t0kilcQqB8BAsf6zTkjdpBAePny5jA0bQddu8UlXWX8evu32Lz7FjLlyCjh7etBY61x1Nu/f1AOwngJgWoTIHCs9vwyuhIQCF988bHhMDxdAldHweKz7Q+zvU4ZJmuKj2VafZQ/VH3v6stHvcOHd6YMi2IIQGDJBAgclwyY5iEwicDoDepru+eN561Psiu6TFcZv/Gxx0cbeRftC/0vjkDJVh87awcPHF/c6GkJAhCYhQCB4yzUqAOBBRAoy7Y7PMu4gMl2vIlXPvrz5rW//pjjXhrDNj3OTxEO1oAAgWMNJpkhukmgDG9Q62cCdaURqT4BXX30f/d3nP/2NW9aV/9aZIRuEyBwdHt+8K6iBFx/GYYXYCp64U0Z1tqhg6OVR8f3fdyRl2WO8LLMlMmkGAJLIkDguCSwNAuBNALXLl/e8EJzNq286HzdzHvwjnexzU7RE1Fg/6955y+bV7/zVwr0YHLX8oer3zh44MhkK0ohAIFlEGgso1HahAAEkgnoc40SNJ5KLi0+V59n/P9+sUXQWPxUFOqBbuj+9+/9DaMrzy5KaExT9z110Td8gkDVCbDiWPUZZnxOERheunxe/+g55dTYGZ5ndHFWivXJ9eceh2Hj6N5D+3vFUqJ3CNSLACuO9ZpvRlsgAX2u0dWgUVeYeAmmwIvD0a6vPvf86LEFfXzBRWl4w7O6iu+ib/gEgaoSYMWxqjPLuJwiMN56Z9spp8bOaMCoq40IBNII6MrjD378I+a2e9+UZlJYvme8XuPg7UcLc4COIVAzAqw41mzCGW4xBIa7w24xPU/u9eubv0XQOBkRpUIgWnm8/Nm/do5HaMJg99KLJ5xzDIcgUFECBI4VnViG5Q4BvUUt3vjueGRGLz1o0Ljz5KdccgtfHCagL8oM3vFuR6+ZcJNb1g5fPLhWKQLcqq7UdDIY1wi4eIv6egDwLnPl6S+7hgt/SkLgdSc/YFzb65Fb1iW5eHCz9ARYcSz9FDIAlwm4eIv66+3fImh0+aIpgW8urlZzy7oEFw4uVoIAgWMlppFBuEjAxVvU+gf/YvfTLuLCp5IR0Jeq3Fu1llvWFy6slwwl7kKgVAQIHEs1XThbFgKjW9Shabvkr/6h55lGl2ak3L44+sjD+nDvPjYGL/elhfeOEyBwdHyCcK+cBOQWtb4Q44zoPo1suePMdFTGEQ0ev/be9xnH9nlsXb34UlAZyAwEAo4R4OUYxyYEd8pP4NqlSy15UH/LlZFo0PjNT/y+K+7gRwUJ6D6PP/yHHbN26KATo5M/bHzL2omZwIkqEmDFsYqzypgKJSBBozOrjfrtaYLGQi+HWnQe7fPoymBD+awnezu6Mhv4UTUCBI5Vm1HGUyiB8MUXHxMH/EKdGHeutw+/vvlhF1zBhxoQ0Bdl3PpsJS/K1OCyY4gFECBwLAA6XVaTwOiFmGHoxBcsohcXdCUIgcCqCOhztN/55B+tqrtp/awP9+xz4udxmqOUQ6BMBAgcyzRb+Oo0gfELMb4LTurKD0GjCzNRPx+e/9hvG2c+TeiZx/iiTP2uQUa8XAIEjsvlS+s1ITD+49RyYbj6Mgzb7rgwE/X14evtD7vypvW6azsc1PeqYORVIUDgWJWZZByFEnDlj5M+18jLMIVeCnQuBHS1+7n2b7rCosWqoytTgR9VIEDgWIVZZAyFEnBltVGDxsE73lUoCzqHQETg8mfPO/O8Y7gbOrM9VsSHIwTKSoDAsawzh9/OEHBltVFXGnmu0ZnLAkeEgD7v6MJnCfU71mwKziUJgcUQIHBcDEdaqSkBV1Yb9ZlGnmus6UXo+LD1yzL6ln/RstYIdassBAIQmJMAgeOcAKlebwIurDbqLWp9IQaBgIsEdBXcheduwzDc4FlHF68QfCobAQLHss0Y/jpDwJXVRm5RO3NJ4EgKAd3f0YUteobXdtnXMWWOyIZAVgIEjllJYQcBi4ALq43corYmhaSzBL7x8d8u3jfPOxZeuLBevCN4AIHyEiBwLO/c4XnxBIIiXdDnxrhFXeQM0HceAvqSjANfleFrMnkmDVsIJBAgcEyAQhYEphG4dulSS2z8aXbLLNfbf7xFvUzCtL1oAvoPHX0mt1DRr8mw6ljoFNB5uQkQOJZ7/vC+IAKe8TYL6nrULRt9F0mfvmcloKvk//3jp2etvqh668O939daVGO0A4G6ESBwrNuMM965CYQXLwbSiD93Q3M04MJbqnO4T9UaE3ih+5nCX5TxjHm4xlPA0CEwFwECx7nwUbmOBIZe41iR4778ufPs2VjkBND33AS++bvFbh/FhuBzTyEN1JgAgWONJ5+h5yfgwhY8X9/8rfyOUwMCDhHQzxEWvT1Pw+xuOIQEVyBQGgIEjqWZKhx1gcDu7m5QpB+6/Q4vxBQ5A/S9KAJfb394UU3N1g5b88zGjVq1J0DgWPtLAAB5CBT9Ugzb7+SZLWxdJqD/ACr4M5nru3v3suro8kWCb04SIHB0clpwykUCL1+61BS//KJ8Y7WxKPL0uywCRf9DqGGKfV55WVxpFwLLJEDguEy6tF0pAmvGe6zIARX9R7bIsdN3NQkUveqoL8mwp2M1ry1GtTwCBI7LY0vL1SMQFDUkVhuLIk+/yyZQ8O1qw56Oy55h2q8aAQLHqs0o41kKgaL3btx58i+XMi4ahUDRBIp+w5o9HYu+Aui/bAQIHMs2Y/hbCIEi927Ur8QUvXVJIdDptDYEitzXkdvVtbnMGOiCCBA4LggkzVSeQFDUCPlKTFHk6XdVBHTV8crTX15Vd7f0w+3qW5CQAYFUAgSOqWgogMB1AkXeptbVxqKfAeM6KAeBAz/1gHnDv/+35r7/8y/Mm879F3P3R0+ava+7qxzOi5dFXufcri7NZYKjDhAgcHRgEnDBbQJD4xW219uLn/trt+HgnRME7nr/r5sf+k+/Z+746aOjYPG2H73XHH7k7aMg8vAjDznh4zQnNHDcvXhpmtlSyrldvRSsNFpRAgSOFZ1YhrVAAp73tgW2lqsptuDJhauWxj/w7neaVx7731LHfvdHP2Q0kHRdNGjcefIvCnOTzcALQ0/HJSNA4FiyCcPd1RIYf5taN/5euVz+3Hk+L7hy6uXqUIPG17zr16Y6/ap//uhUGxcMLvY+U5gbnrdW2D8QCxs0HUNgBgIEjjNAo0p9CBT5beqdP/tUfUAz0twEsgaN2vCB//GB3O0XUUFfkinqdrUJh4U9klIEa/qEwKwECBxnJUe9ehAIGw8XNVBdcUQgkEQgT9CYVN/lvO988o+Kcm89vPRyIXcXihow/UJgFgIEjrNQo05tCHheWMgfkhfklp1+jg2BgE3g8M89lOn2dLzey19/Lp50+rzIfzANzbXAaTg4BwEHCBA4OjAJuOAmgZcvXdKg0S/Cu4vdTxfRLX06TkDfmr77Ix/K7eXOn/5Z7jpFVdDb1VefL+YfTWEYBkWNm34hUBYCBI5lmSn8XDkB+eEoZLVRB1rkqsvKQdNhJgL6ZvTdHzmZyTZu9MJfdc2Fs0/Gs5w/L+r5Xs8zvCDj/NWBg0UTIHAsegbo310CBT3fyNvU7l4SRXmmQeMP/cffM2t3HMrlwkt/+7R59n2bueq4YFzgP5zWxzspuIABHyDgJAECRyenBadcICDPN/pF+PECt6mLwO5sn/r1F/0iTN6gUZ9r3P7nv2p2X7jo7NjSHCvy7eoid1JI40E+BFwiQODo0mzgizMEwgsX1sWZQm5VX/5c3xkOOFIsAQ0a9Ysw+3J+OnAUNP5SOYPGiPjF3qej05Ue2c9xpbjprIQECBxLOGm4vAICe/YUEjTqt6m/+/QzKxggXbhOYN6gsUxvUifNxeWCPrfphcNCfvaTGJAHARcJEDi6OCv4VDiBoWkERTjBt6mLoO5en3UPGnVGLnaL+YpMKHcaxncc3Lsw8AgCDhAgcHRgEnDBPQKh8e4vwit9tgupN4GGvACjzzTOenu67CuN0ezrF2SK2pbH7D3gR35whAAEbiZA4HgzD1IQGBEo6sWYl575CjNQcwL69vR+eYs6j+gLMF/7F//KVCVojMZe1Itiu4YvyERzwBECNgECR5sI6doTKOrFGJ5vrP2lZ17/0ZO5g0alpm9P69Y7VZMrz3y5kCF5YTEvxhUyWDqFQE4CBI45gWFeAwIFvRhT1B/JGsxoKYaoQeP6I2/P7evf/8ZmJYNGBXH5s8XsMCCPqvjSPQIBCCQQIHBMgEJWvQnshuF6EQSu8DZ1Edid6PMH3v3OmYLG5z78MbNztjyfE8wLW7/Xrs86rlrkCzKFPOO86nHSHwRmIUDgOAs16lSagOzjVsh2HC+yf2Olr6u0wWnQ+Jp3/VpacWr+f/93nzDfPvOfU8urUlDQP6h83qyuyhXEOBZNgMBx0URpr/QEinqjuqA/kKWfrzIPYJ6g8R9+5z+UeeiZfS/sEQ7erM48RxjWiwCBY73mm9FmINDwhiu/Va2344q4JZcBByZLIkDQmA1sUYEjb1Znmx+s6keAwLF+c86IpxCQFceV36ou6o/jFBQUL4nA4Z97aObb03VZaYzQX3m6mC2qPNNY+T8gozFzhIDLBAgcXZ4dfFs5gfFzTSv/g3Hl6WK2HVk5YDo0d/z0UXP3Rz6Um8SFP33S1C1oVEj6gkwhEg79QvqlUwg4ToDA0fEJwr3VEri6d6+/2h6v9/ZyUX8cixhsjfu8TTb2vvsjJ3MTeOGvuubZ930wd70qVCjqMQ625KnC1cMYlkGAwHEZVGmztAT2FrQVz9Xnv1FaZjiejYAGjfpVmDX5pGAe0Y29n33fZp4qlbO9+txzKx9TwzNvWHmndAiBEhDYUwIfcRECKyOgezjKHm4rl2EBe9UtapB7X3eX+X55Zu+Of3J01KR+9u5bZz5pLv+3zy6qi9K3o4z0+9N5g0ZlqV+F0U8K1lmuyKc4b7v3npUiCI1Z+SMrKx0gnUFgRgIEjjOCo1o1CXiNhl/EyMq6Fc/15/VO3hQQ6cqa5uvzeLrXYN1Fg8Yf+k+/Z/bJMY+MgsZfImhUZrsXCwmc/TzzhS0E6kKAW9V1mWnGmY1A6BWyylDGrXg0INLn9dJW0XRTa91yps4yb9CowSOiL8gU8ygHm4Bz9UHgVgIEjrcyIafGBMIw9Fc9/MLeGp1zoBoUpgWNUdN1Dh4JGqOrYP7j7qVCVhyNue22Qv4hOT8xWoDA8ggQOC6PLS1DIBOBMq426sD0lnQWqWPw2JAXYPSZxllvT7PSePOVNXxh9d+rvtkDUhCAQESAwDEiwRECQqDRWP2blLuXyvlHce1Q9reDNXh81bFHa3ON6dvT+zMG1hEUfQHma//iXxmCxojI945F/Yxcu2b873nBGQQgoAQIHLkOIFAwgbKuOF7N+fzdne//1+bwIw8VTHv53b/+oydzB43qlb49rVvvILcSeLmgZxxv9YQcCECAwJFrAAIFEyjojdG5R61fMskrd3/0Q+bATz2Qt1pp7DVoXH/k7bn9/fvf2CRozE1t+RU8b9dffi/0AIFyESBwLNd84e2SCcjXIngYPiPjC2f/bKa9GvXZv6zPR2Z0xQkzfVlolqDxuQ9/zOwISySdwLCY7XjSHaIEAjUmQOBY48ln6IkEVh44lnnz76/KM3lXvpTv9qq+ia3PAFYpeNSgUZ/jzCu6z+W3z/znvNVqZ1/WxzlqN1EMuBYECBxrMc0M0mUCZb1VrUz1hY6/k02q877QocGjrjzqljVll3mCRt0kHYEABCBQJgIEjmWaLXyFgIMENHjcniF41K1q9IsqZQ4eCRodvCBxCQIQWCoBAsel4qVxCNSDgK441i14PCzf55719jQrjfX4uWCUEKgiAQLHKs4qY4JAAQTmDR6nfYWmgCGldnn9G90fSi1PK9A30Qka0+iQDwEIlIEAgWMZZgkfK00gz0baroOIgke9fZ1HRret5YWZMgSP+lKPfqM7r7zwV13z7Ps+mLca9hCAAAScIkDg6NR04EwdCTQOHazUsDV4/DvZzDpv8KgBmb4w47Koj/pGeN4AVzf2fvZ9my4PzWnf1ir2M+I0bJyDwBQCBI5TAFFcLwKeCQf1GvFyRntFAiXdqiev6Obgd8sm2i6KvsSjgW3eoHG0CjtDIO0ig6J8auT4vOUifVzzvJ1FtkdbEKgCAQLHKswiYyg1gSrdqo5PxOX/9lnzrHwRJa8cli+vuBY8atCob4DrLfU8Muut+zx9YLs8AteGDQLH5eGl5ZISIHAs6cTh9nIIDMPV/6Go8m04/brM8/JllLyiwaNudeOCzBs0avCIzEdg312vna8BakMAAgsjQOC4MJQ0VAkC4fAfVz2OfXdW+4/it+TLKPqFlLyiW90UHTwSNOadtWrZ7/HWWHGs1pQymgUQIHBcAESagAAEJhPQLWjKFjw2xl+3mfX2NCuNk6+JPKV7i1pxXNslcMwzUdjWggCBYy2mmUFmJeB53iCr7aLs9t5156KacrqdeYLHVx17dOVj07en98tb1HlE3yT/mrwURNCYh9p02713FvMz4u3fP5juHRYQqBcBAsd6zTejnUbACwtZYahT8Ki3rvPKne//1+bwIw/lrTaz/evlze68QaN2ti1vT+vWO8hiCVT5OeDFkqI1CCyfAIHj8hnTQ4kIhENTSOBY1HYjRUyNvixz4eyTubu++6MfMrpdz7JFg8Z1eTknr/y9vEFO0JiXWjb7glYcB9m8wwoC9SJA4Fiv+Wa0UwisecXs47j/nh+Z4lm1ip/9jQ8a3a4nr+g+iroJ97JEX8aZJWh8ToLhHXmDHFkOgbU7Vr9JvmdW/9jKcujRKgQWS4DAcbE8aa3sBPbsGRQxhKp9PSYLQ90g/MqX8t3W1c239dnDZQSPGjTqm9x5RV/6+fYMt9/z9lNn+9vuuWflwx+G4cp3WFj5IOkQAjMQIHCcARpVKkzgypVCblXfdu+bKgw1eWj6Isnf/dKv5n6RRINHXXnUrXIWJfMEjfrSD7I8Avp8YxHPOPIVqeXNKS2XmwCBY7nnD+8XTMA7fFgDx5UHj/vvqV/gqFOnweP2DMGjbpGjX3JZRPBI0LjgH6IFN1fYP6q8xmDBQ6E5CFSCAIFjJaaRQSyYwGDB7U1tri5vVSeBiD7Ll3cLm0UEj4d/7qGZb0+z0pg0m4vPu62gf1Q1CnreefEEaRECiyVA4LhYnrRWAQLhMPz8qoeht+IIHvPfto6CR719nVfu+Omj5u6PfChvNXPhT580BI25sc1cobDNv8O9g5mdpiIEKkyAwLHCk8vQZiPgeau/Va2eFnZLbjZMC68VrTzq7es8Mgoe5YWZPMGjvlxz90dO5ulmZPvCX3XNs+/7YO56VJidQGE/F1cvD2b3mpoQqC4BAsfqzi0jm5FAGJr+jFXnqra34t+szgJHg8e/k0208waPGgjqCzNZRG31zew8gaa2q3s0Pvu+zSxdYLNAAkW8US3u74yfd17gSGgKAtUgQOBYjXlkFAskMGwUEzgeeOAnFjiK8jZ1RQI03aonr+jm4HfL5t2TRF+m0QAzb9A4Wg2dIaCd5Atl0wnoamMxb1R7hfzjcToRLCBQPAECx+LnAA8cI7D36tVBES4d+MkjRXTrZJ+6Ofiz8iWWvHJYvviSFjxq0KhvYuut7Twy6y30PH1gm0ygqNvUYThc+XPOyQTIhYB7BAgc3ZsTPCqYwPgW1WDVbtT9BRmb9wX5Eot+njCvaPCoW+zEZd6gUYNHZPUECvvHFFvxrH6y6bE0BAgcSzNVOLpKAmFYzK2qwv5QrhJujr6+JV9k0S+z5BX9AkwUPBI05qXnjv1tBX2Kc1jQz7875PEEAukE9qQXUQKB+hLwvOFTxngbqyZw+wNHzM6Tn1p1t073F219EwWCWZ2NPh946J8cnfn2NCuNWWkv3k63p7rt3tV/alBHsvfQ/t7iR0SLEKgGAVYcqzGPjGLBBMLhcLDgJjM1d0fw1kx2dTPS4HHWlcf98hZ1HtE3ur8mL+cQNOahtnjbA/KPqCLEM8W8HFfEWOkTArMQIHCchRp1Kk9gbXe3V8Qgec4xnboGj3rretmyLW9P69Y7SLEEinpsIyRwLHbi6d15AgSOzk8RDhZBoKgXZHSsh4K3FDHkUvSpL8tcOPvk0nz9e3mTm6BxaXhzNVxc4BjKYyoIBCCQRoDAMY0M+bUnIJ8eLOQPCLerJ196z/7GB41u17NoeU6C0h15kxspnoDepi7qE5xrZh97OBZ/CeCBwwQIHB2eHFwrloBX2EbgRwrZ9LhY2vl61w3Cr3xpcbeT9fnJb6/gNni+UdbXusBV9x3vIIFjfa88Rp6FAIFjFkrY1JJAY23tXFEDP8RLMhPR6wssf/dLv7qQF1g0aIze3J7YKYUrI1DUqrt8brSQuwwrA0tHEFgAAQLHBUCkiWoS8PbvH8jIdooY3fpDDxbRban61OBxe87gkaDRvSnXr8UUdZva87yee0TwCAJuEWAfR7fmo7TefPG+ZhDumodNw2yY0PjjgewYT7a2GJozb/5yv1PGwclzjk94De/Yqn3XZ7z0Devdi5dW3XWp+os+B/jGGT4lSNDo5lSvP/QzhTnWMHt6hXVOxxAoCQFWHEsyUa66ue03179wb/NsODRdCRJPxIJGdXld0oHkb33hnua26Mo31F4At94C2pipiVew6piJWxQ85tl38cKfPsnt6Ux0V29U1G1q2fB/wPONq59veiwfAQLH8s2ZMx7/7X1N/+L3mfMSHGpAuCP7n52UF0qO7r5sDr/5mb63u9cckRXI46FnBlLui5794j3NTTmWRtZ2rxb2nGNxf0BLMz03HI2CR719PU1e+KuuefZ9H5xmRnkBBIp8m9qYsFfAkOkSAqUj4JXOYxx2goAGjVdDWWWU29K6Ye6wYR458qX+IM25z9/TbMvFFgWNj0hgWVhAluZjWv7upcvnpayZVr7M/K/84nHz3aefWWYXlWr7NvlKzA/9x98za3ccShyX7tGoG3xnCTATGyBzqQRed/IDpqjne0MTHt9z8GBnqQOkcQhUgAArjhWYxCKGcHUoQeD1oHEwfNkcnRQ0qn/3P9Nv64rk2NctvcVdhN8z9RkOn5ip3gIq3cFm4LkoXpHA8Csb/2vi29bfOvNJgsZcNFdrrC/EFBU06kjXrhZ3d2G1pOkNAvMRYMVxPn61rD1abRyabR38bsO8cVrQGIckz0PqKmWgQaQGk/EyV8+vXrwYNLxGtwj/9OWYL//s/8xLMjPAP/BTD5h9r7trVPOF/6PLKuMMDFdZZf3tD5rXtT+wyi5v9OUZr9c4ePvRGxmcQAACqQRYcUxFQ0EagatGXni5Lp08QaNW8bzrq47yL5Zj4zacP+w9dKgnTu4U4ai+Wc2ejrOR16/LXJAvwahya3o2hqus9Zp3/PIqu7upr6EZnrkpgwQEIJBKgMAxFQ0FqQSGsu2Oygyb5f74l/o9qalBmF+u29VhYX9Yirx9J/OEQGDpBIp9KUZuU6+t9ZY+SDqAQEUIEDhWZCJXOgxPttkR8dZGb0vn7lpWGwdaaeeA8fVYBhma8FxRfuof1QMP/ERR3dMvBJZO4Pt/8eeX3kdaB3qberzZf5oJ+RCAQIwAgWMMBqcQSCNQ5O1q9enVBd7GS2NCPgQWQUBfirnj6FsX0dRMbXCbeiZsVKoxAQLHGk/+rEOX77l+VevKl2L8WdqQF2NG9dYvz7ZiOUufC6kTFne7mlXHhcwgjThI4DXv/OVCveI2daH46byEBAgcSzhphbusnxFUaYyfdczhkH6aUMzXJXjsv3HQ12cdSyNF3q5WSKw6luZSwdGMBIregofb1BknCjMIxAgQOMZgcJqNwPC7pjOylC/G6NY82Wpdt5LVys3RmWfO5Knngq3ervYK/LoEq44uXAX4sEgCRa82cpt6kbNJW3UhQOBYl5le4DiPyEqhBICPa5PXhuZs1rejR58bvL6H42DomcJeNpkHRRiGT81Tf966rDrOS5D6rhAoerVROOzwpRhXrgb8KBMBAscyzZZDvg6vmrZ+g1puOTcv7TPdaSuPGjSKbVuH4IXmZN79H10ZeuPatdNF+sKqY5H06XuRBIpebZSxlPIfr4ucA9qCwCwEvFkqUQcCSuC83KZuyPeqJRD0JanPK57zGubMeK/GqHxDLrKHZc/HQMrlUJ4vxqi/STK8dKkbGi9IKltF3uXPnjeDd7xrFV3RBwSWQkBXG+/58z9ZSttZG22YvUe8g/v6We2xgwAErhMgcORKmIvAKHgcmrZcSMcmNSQB46DRMMejoHKSretlRX6CMGIzeMe7zeXP/nWU5AiBUhH44f/SMbfd86bCfJbfV/3GwQNHCnOAjiFQYgIEjiWePJdcjwJI8el+uaiaI9/kVrYc+xI0PqUv1OizkaP8Cvxv99Ll8zKM6+MsYDxXn3vePPOz/0sBPdMlBOYjUOQ3qSPPQxMe5/nGiAZHCOQjQOCYjxfWEBgR2L106YQ8rXmqSBz/8Ik/MN/8xO8X6QJ9QyAXgcahQ+ZH/nDL6K3q4sQbrB28/Y3F9U/PECg3AV6OKff84X1BBBpXr3ak60JXUF/56M8X/Ae4IPh0W1oCr3r0nxV+zcofvXOlBYjjEHCAAIGjA5OAC+Uj4B0+vGPC4WhLoqK8Xzt00Lyu/YGiuqdfCOQioKuMr37nr+SqsxTjNa/Qn9uljIlGIbBCAgSOK4RNV9UiMN6ap9BVR92e51CB3/mt1owymmUSeOPv/rtlNp+17Y63f/8gqzF2EIDArQQIHG9lQg4EMhG4vupY3PerIyd11VFXHxEIuEpA92ws9rnG62Qaa42TrjLCLwiUhQCBY1lmCj+dJNDYs3a6aMc0aLyr/W+KdoP+IZBIwJlb1Maw2pg4Q2RCIB8BAsd8vLCGwE0E9LZXOCx+1fGOo28x6w89eJNvJCDgAgFHblEbVhtduBrwoQoECByrMIuMoVACa3vX2oU6MO78tb/+mBO3A11ggQ9uEHDlFrXQYLXRjUsCLypAgMCxApPIEIol4MqqI29ZF3sd0PvNBPTFLSfeoha3WG28eW5IQWAeAgSO89CjLgTGBMarjoW+Ya2u6B9rXXlEIFAkAX2u0aGtolhtLPJioO/KESBwrNyUMqAiCIy2+Ch4X8do3LoxOFv0RDQ4FkHgBz/+EWcem2C1sYgrgD6rTIDAscqzy9hWSsCFfR2jAetqjwvbn0T+cKwPAX2u8bZ73+TEgIdh+Dj7NjoxFThRIQIEjhWaTIZSLAEXviYTEdDnHfVtVvZ3jIhwXAUBXe125blG+Zb8YI8D22Wtgjt9QGCVBAgcV0mbvipP4PqqozdwYaC64vj6j3/UBVfwoQYEdJXRpedrQzM8yWpjDS48hrhyAgSOK0dOh1UmoKuOw3D3uCtj5GUZV2ai2n7oP1L0uUZ3RFYbDx7suOMPnkCgOgQIHKszl4zEEQJ7Dx3qeSbsOeKOcev2oStU8GNRBDRo1MciXHqmdtcMH1nU+GgHAhC4mQCB4808SEFgIQS8tTVddSx8e55oMPrCwvc/+gtRkiMEFkKgcejQaKXRpaBRBtbZd/BgfyEDpBEIQOAWAgSOtyAhAwLzE3Bpe55oNHf++r/ks4QRDI5zE9CgUVcaXXmD+vqAvAHb78w9tTQAgYkECBwn4qEQArMTWDt0qO0Z49TKx+tOfoDgcfYppWaMgP5DxK2g0RheiIlNEKcQWBIBAsclgaVZCCiB3XD4HtdI6Juvrv3Bd40R/kwm4OI/QDzj9XghZvK8UQqBRRAgcFwERdqAQAoBfVFm6MgXZSIXdW9H/3d/h6/LREA45iLgYtAoS4073prnzG4GuYBiDIGSESBwLNmE4W75COy5dq2tmxG75LkGj7p9yvpDD7rkFr44TECfafR/73ecvGZ2vZA9Gx2+dnCtWgTkESwEAhBYNoGXL11qrhnv/LL7maX95z/22+Y7n/yjWapSpyYE3HwR5gb8ztrBA6w23sDBCQSWS4AVx+XypXUIjAjo9iC7JnTueUd1Tl9ycOczcVwwrhHQrXZ+5A+3HH0ulreoXbte8Kf6BAgcqz/HjNARAhI8nnZpY/A4Ft3nkeAxToRzJaAvUbm2uXd8ZniLOk6DcwishgC3qlfDmV4gMCIQvvSSf/U7L5y/8pVn1jXjwE/+hFNkXuh+xjzX/k2ze/GSU37hzOoJHDr6VnN3+/1Gb1O7KMPQnNx76EDbRd/wCQJVJkDgWOXZZWzOEfibH2s2d6+arjg2Chz1NqCu9rn0ksrV55432+94t9EjUk8C7q9Ae4O1g7e/sZ6zw6ghUCwBAsdi+dN7zQh84d7mtmwd4tvDXn/7g+bV7/gVs++u19pFhaR1xfEbH3vc7Dz5qUL6p9NiCOjqovtfGNLnGr2jo68zFYOJXiFQawJrtR49g4fACgl88b5mIEHjiaQurzz9ZXmz+Y/NUAK2fb5vdLucIqXxffvMHXKrUrYRMi9+zsmXwYvEU8m+dfX7h898whx4wK3HJ2zYoWeOr91++/9j55OGAARWQ4DAcTWc6QUC5l2HX7suf/R+bRKKl774N+Zi7zOjwNGFr7sceOCIuSN4q7n0f/+/o6B2ku+UlZfAKx/9efP6j5w0e171SqcHMXqu8eCB/+C0kzgHgYoT4FZ1xSeY4blFQG5Vd2XVMcjila4A6RdeXLh9rc87/sMn/oBb11kmrkQ2emtaX4DRF2FcFy805xqHDjziup/4B4GqEyBwrPoMMz6nCJz3m+uNfUa25THHsjrm0vOP+syjBpC8OJN19ty109Xk17U/YPQfKO6LPNd4YP8Rz/N23PcVDyFQbQIEjtWeX0bnKIHz9zX9Rmi6soriZ3FR/7gffuhnnNhrkdXHLDPmro2uMupb03p7uhzCyzDlmCe8rAsBAse6zDTjdJLAF+5rtsLQbOYJIF3ZvofVRycvqYlO6er1ne/9l87uzXiL86HZaexpHOEN6lvIkAGBwggQOBaGno4hcJ3A+Pb1Cflh3MzKxJXb17ptz7flbfBvfuL3s7qOXQEE9EWr1/76Y7Lh/JECep+9S3mZ7JE9Bw6cm70FakIAAosmQOC4aKK0B4EZCYxuXw9NW34oMz//qKuP3//oLxS+fQ+3r2ec9CVXK99t6e8B0W+762c6v5fDGQQg4AIBAkcXZgEfIBAjUObb1y/IVkK6cTgvz8QmtKBT/fb4qx79Z+W5LR3jxOcEYzA4hYBjBAgcHZsQ3IGAEtBvWj/3kX/bfeHT/5efNQhzafsenn8s7jrWrXX0OcZyvC19KyeCxluZkAMBlwgQOLo0G/gCgRgBDR6vDL7W/eb/fsbP8+k/V55/1KEQQMYmdMmnur2OrjKW7TnGOBaCxjgNziHgJgECRzfnBa8gMCKgweNwN+xefe45f/sd7858C1hXm/Q2pT7/6IIQQC5vFqoQMCodgsblXSO0DIFFEiBwXCRN2oLAEghEwaPcwB6tPObZgFsDyNfKbcvr351egnM5m9QAUt/C1m9zI7MT0JdedF9P3YuxrLek46MnaIzT4BwCbhMgcHR7fvAOAiMC8eBRn3n81if/q/nOJ/8oMx2Xbl+r05c/d97s/Nmn+IRh5hm8bqgBowaLZX3pJWm4BI1JVMiDgLsECBzdnRs8g8BNBOLBoxbMsgWOK9v3RAPTMWgQmWcVNapbl6MGi/vv/ZHSP7+YNF8EjUlUyIOA2wQIHN2eH7yDwE0E7OBRC/M+P6i3Nl35+kx8cNEqpB6zvkker1+1c3128VDw1tEtaQ0eqyYEjVWbUcZTFwIEjnWZacZZGQLhhQvr4d593dCYZnxQumqnt6/1ay5ZRL8m8vqPf9Tsu+u1WcxXalPXILLqwWJ0EYUmPL7n4MFOlOYIAQiUhwCBY3nmCk8hcBOBay9c6ngN76avzMxy+9q15x9vGqQkNIi82P306Fi1l2p0JfGOo28xt8unAF8RvKWUm3Xb8zUxLd+eHprhI3sPHepNtKMQAhBwlgCBo7NTg2MQmE7g6sWL7YbXuOUb1xpgfe2978t8y9fV29c2geHFi+bS5/rmxc/+dSkDSQ0UdVVR91rUFd8y77loz830tDfYlaBRPiPYn26LBQQg4CoBAkdXZwa/IJCRwMuXLp1YM96pJPNZnn90afuepDHF8zSQfOmZr4y294mejXRlVTJ6qeW2e95kvk+CxIMSMO698864+7U594zX99a8R7z9+we1GTQDhUBFCRA4VnRiGVb5CJy/r+nvMUZ18KNf6g/yjECCx+aaaZzVvR7tenr7uuzb99hjmpa+8syXzcvPfUMCymfM1ee/ISuv35BnPy+O8jTYXJToSu3aoYOj1cO1gwdHAeLa+C3ougaJNttwGJ5ZO3TghOd5O3YZaQhAoHwECBzLN2d4XEECX7ynuSkvu7RjQ+vsbZiTeQLIpDeuY+2Nbls///HfHj0vGM+fdK5vX+tn7KomV59/fvQSUfQi0csSXE+TfRIkqkQvExEYTiNmzK4J3yO3pk9Pt8QCAhAoCwECx7LMFH5WlsAX7mu2zNBsJQxwEHrm8fuf7uf6wyvPPZ6W5x4fS2hvlDXL7WsXt+9JGx/5DhDgJRgHJgEXILAcAgSOy+FKqxDITODz9zQ78oN409vRVuWBpN/z5mf656z81OT4uUd9aWY9zUi37/nmJ34/rfiWfH2p4672v7mx4naLARkQEALyPGNPnmc8zvOMXA4QqCYBAsdqziujKhGBDIFjNJpct6+n3brWRqu4fU8Ei+PqCQzD8PG9hw6eWH3P9AgBCKyKAIHjqkjTDwRSCHzxvmYQDk03pfiWbPmhbR982Tz+xkF/55bChIxpt661SlW370nAQdZSCHiDYbh7nP0ZlwKXRiHgFAECR6emA2fqSuAL9zQ35HnGU15o/IwMBiY0J9/85X4ni/21S5dantH9Hm996zpef5bnH3/w4x8ZvVUcb4fz+hCQa/acd/D247w1XZ85Z6T1JkDgWO/5Z/SOEZDb1m35odQXW1KfTYy7LLb9PQ3zSJa3r/XW9e7V3bb9tZl4e3rO7WubCOlEAvICTNgwx/ccOHAusZxMCECgkgQIHCs5rQyqzAR0P8fG0GgAOemFGXuImZ9/zLr6qAHk19sfNpflKy1Zparb92Qdf13sWGWsy0wzTgjcSoDA8VYm5EDACQLn39RsNhrm7DJuX2ddfVQQs9y+ZvseJy6hJTjBs4xLgEqTECgVAQLHUk0XztaRgO7zGIZmM1cAmXH7nklfnLFZ592+546jbzE/8N4TbN9jgyxpWt+Y3nPwQJtnGUs6gbgNgQURIHBcEEiagcAyCYxuX+8a+Wzb6PnHrF1lvn19fd9H3TR88sszszz/+MpHf958/6O/QACZddYcs9N9Ga+ZoX4Bpu+Ya7gDAQgUQIDAsQDodAmBWQloALk2NKek/kbWNuSHvP3jz/RPTrPPc/v68ufOm69v/tboRZpp7Wq5ftOZ29dZSLlk48mXi8L38PKLS3OCLxAongCBY/FzgAcQyE1gptvXGbfvGQWQ18JTnhdODU5nef6R7XtyT/dqK1z/XKDclj54mtvSq0VPbxAoAwECxzLMEj5CIIXAePse/bRgNvFMb69njmfZvifP29f6/KMGkVll/e0Pmle/41e4fZ0V2IrseI5xRaDpBgIlJkDgWOLJw3UIKAGXtu/56nvfb7779DOZJmbt0EHj/+7vsHl4JlpLN+o01hon+b700jnTAQRKT4DAsfRTyAAgcJ3AMrfv0R6yrkDmuX2tzz7e8+d/whQWREBffNkNd0/yqcCCJoBuIVBCAgSOJZw0XIbAJAKzPP+4ttc88mN/08/01mzWADLr9j33/MWfmL133jlpSJQtmIA8u3hud7j7OAHjgsHSHARqQIDAsQaTzBDrR2CW29cNY1r/wzP9M1lpZQkgp23fw4pjVtoLsBu99BKe2bNn7TS3pBfAkyYgUFMCBI41nXiGXQ8Co+17QrNlQhNkGPHgzc/035jB7iaTqxcvBl7otSZ9A/uF3mfMNz72+C3b9/CJwptQLifBW9LL4UqrEKgpAQLHmk48w64Xgay3ryVwnPl3wvf2gWy8LW0jcX3+cefJvzQNeTHmjuAtZv2hB+s1ESscrT6/OBzK117uOHBuhd3SFQQgUHECM/+RqDgXhgeBShKYtH1PaEz//mf6RxYxcL2NLbe+j4XGCxbRHm1kJDBeXRTrHs8vZmSGGQQgkIsAgWMuXBhDoPwEUp5/3Nnda44eyfiCTFYKugo53N2VjcSnf84wa5vYWQQkWJSXXfq8HW1xIQkBCCyFAIHjUrDSKATcJ/DF+5rBcCjPPnpmZ/hd0zky6O8s02v5HnazMZTvbTfSb2Uvs/+qta23okMzfKJx4ECHL7xUbXYZDwTcJUDg6O7c4BkEKktAX6gxxttY87y3yS3yZmUHusiBjVcWCRYXCZW2IACBvAQIHPMSwx4CEFgogdFLNbu7QcPzHg6vr4CuL7SDcjc2kM8APiEvG52Tb0f3WVks92TiPQSqQIDAsQqzyBggUCECuhrZMI3A80JZjazdyzUDeXSgF+6GT63tXeux32KFLmyGAoGKECBwrMhEMgwIVJXAKJD0vKastr1N9qP0K3Nr+8ZLLcPPe6HpEyhW9QpmXBCoFgECx2rNJ6OBQOUJhGG4Ltv9NOXWdnMogeSaZ+4PQ68pK3Uu3+IeeJ7p7w7DrxIkVv4SZYAQqDQBAsdKTy+Dg0B9CEQBpSeBpeetNYcmXNegUgnILW9fDqqLF1k51DfTPRMOQs8byKbb/9jwzCAcDgdre/f2ud28eOS0CAEIFEeAwLE49vQMAQismIAGl+bKlfVr1675UdfyucQb51Fe2jH0woGW7dmzZ3QkKFQaSJEEvnBP86z8w8WYoXlibZ/p/9iC92Itcmz07SYBAkc35wWvIAABCEAAAhMJnPeb6xIsXrCMBpLuiT6xt2H6P/qlvqYRCCyMAIHjwlDSEAQgAAEIQGB1BGS1eY6F0QAAQABJREFUcUN6OysvjI2eodUXx+QZWj/ugfyR74eh6Xlr5okf/1K/Fy/jHAKzECBwnIUadSAAAQhAAAIFE5DAcUtcaIWeec/9T/dPqzvnf6zZbFwzgfxxf1ge7m1K1s0vjel2T7IaKc/h9gkklRiSlwCBY15i2EMAAhCAAAQcIPCFe5vbEhz6XsMcTQsCR58W3TUbYnO/2AaW2503P9M/buWRhMBEAnsmllIIAQhAAAIQgIBzBP72vqZ/dWh8cWwnLWhUp8dlPT0fPxOp36c/pQGnrFR+XvMRCOQh0MhjjC0EIAABCEAAAsUTuGqurx5K8PdUVm+ODPo7ssJ4LrIf7hm9RBMlOUIgEwECx0yYMIIABCAAAQg4RGAozzCKeENzIxDM4t3fvKnZHK02ygs1R9i6JwsybCwCBI4WEJIQgAAEIACBEhAI1MfdtXyrhtca11cq5QWHntZHIJCXAIFjXmLYQwACEIAABAokMFo1lLeldRueIzn3aZSAcbRSKauOmW9xFzhUunaQAIGjg5OCSxCAAAQgAIE0AnOtGl7foif3SmWaL+TXjwCBY/3mnBFDAAIQgECJCdxYNZT9GPMMQ7fmEXtdqeznXanM0w+21SZA4Fjt+WV0EIAABCBQNQLj/RgPvZzvOcXh0ASKosFt6qpdESsdD4HjSnHTGQQgAAEIQGB2AuNVQ3lE0fTfKNvr5GnJ88zbRvZr+d7EztMHttUnwAbg1Z9jRggBCEAAAhUhMNSvwMi9avmvKV+O6UoA+cQe2Y/xx6ZsraObf0u0GSiGg1dMvyI4GEYBBAgcC4BOlxCAAAQgAIGZCDTMIAxNXwNHDQTlGOzKbuDy3eqBRJN9MzRP7JUten7Uett6bd/1oFFsenlXKmfyk0qVJSDXHAIBCEAAAhCAQJkInJdPDq4NTVNWHDckGHybJ58QtPwfSLon+oQ+C3lxn3xm0JiWfGnmPfc/3T8t5wgEZiJA4DgTNipBAAIQgAAE3CEwCiT1M4Sh7NN4/Zb0uuWdPg+57jXM0UnftrbqkITALQQIHG9BQgYEIAABCECg3AT0JZqh7Nkof+SjQFIHpN+qPlzukeF90QQIHIueAfqHAAQgAAEILJGAvhiz5za5rb1r/Dd/ud9ZYlc0DQEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEykHAK4ebeDmBwIaUrVvlA0n3rDySxgQCwY+B6Mu5qi3Kc8PKPCfpHSuP5HWegQWiY6VJVpdAIENTjaQvJ/qzUkfxZdBBbOD6+6KuLGIYcp2eEOv1WI3Tcr4TS3MKAQjMSUB/wMIEvTBnu1Wt3rFYtVMG6lt2yjgQRW4l0JIs+xq81YqcqhJoy8Di879V1YFmGFfLYrGdoQ4mNxNQZvHryb+5mJQLBPa44AQ+zExgI6WmBpSBaE8UgUAeAr5lrP/aV0UgAIHFEvCt5rL8rOnvdtVIstSJbDlCYCEEGgtphUaKInBsQsebE8oogkAaga4UbMd0I82QfAhAYC4Cs/ysnZAe4z+fZ+fygMoQmIEAgeMM0Byp4osfwQRfmlK2PqGcIghAAAIQgAAEIJCLALeqc+Fyylj/5RmXHUnEA0U9b4meFkXyEVCWx60qAytN8jqBnhxsVrCBQB0J9GTQ8Z8F/T2CQKByBAgcyzulD1uun5T0pqgGjJGoDYFjRCP7UX/hd7Kb19pyIKPv1JoAg4fAdQIDOXSun/J/CFSXALeqyzm3gbjtW66fk/QZKy+QdDyQtIpJQgACEIAABCAAgewECByzs3LJ8pjlTE/SA1ENHm05YWeQhgAEIAABCEAAArMQ4Fb1LNSKreNL9y3LhWilsSf5O6LxVUYNMtuiixRtvymqt8L13BcdiH5V9JxoX3RRou23RO8X1XNVbf/zoj3RgaiLEohTbxNtivqi6vdAdEf0KdGeqI5jVvGl4oboG0S1bV9U21bVeeiNVQ4TReuqpskrpMCPFUZ9xLLmPg2khUWz8i2vBlZax9wUja7hqDgPu6jOIo7qz4aoXue+qKZVdkQHok+JnhPNKr5lqO2oZhXfMhxY6azJdTFsiUbj0nrqx0D0CdGeaFbRtlQj0XZU4xJIoimq/aloeZbfFYHYxetJMtfPkdpPk3UxUE2TV0iBHytU31XjeWoTF23Pj2VEdWJZqadad0NUWel5JMqrL9qLMuY8Rv34sXZ25HyRfcSa5hQCELAJtCQjtFR/MCM5LSd2eRAVZjy2xS7ehqYjeUxOLojGy+3z81Lui2aRbTGK1w/GlXRMp0Sn9bUlNr5oFumIUbyvdkol37LTOoFoFgnEqCsa7yftXDk1RfNIIMZZ21d2W6K+aJoEUpDmX1J+y2pI07adZZKaDKSkK2rXT0orqw3RrLIthvF2/HFFva42RaddV1o/T3/j5nMffKmxJRr3Ne1cfdoU1TFME7uN1rQKVrldP7DKo2RbTuK2W+OCPJxb4zrTDmoX76sbqxDIuabj5fb5qZh9dBrIybR622KT5VpoiV28T60Xl0AS8fJp561xZW1nmm1U3h3XmXTwpfCsaFQn7bgtNi3RWSWQiupPWvuab/eh6bi9L2kEAhCYk0BX6sd/sLas9gKrXG1PWzbTkm0xiPehaf1D0LXy4zZJ55tiP022xSBeN5C0L2rnx23sc7Vtik6TjhjE67ZTKviWndYJRKfJphjE2896rvWmySz84/2fSOkgkPy43bTzltWOpu06lsktSR3LVkI9u52kdNIf/1s6kIxtq31f0qp2flIf8bw0btLU3NKUFqYFsHFfovNtqedP6T2yjY6tKfZ2cVQvOga2wTjdlmNko8ctUV90WzSeP+1c51Wvi0nSksJ4O92x8aaVH7exz6M6WjVPPW3nmFaaIC0pU7tIty3bIFYW2Uw6tsb1tZ1JdvGy7rhO2uExKch7zWn/eq3mkU0xjvs17VztVbZF47a+ZiIQgMDsBHypGv+h0vNA1Bb7F4Om80hbjOP9aPq8lRcvn3S+KfUmybYUxuu3JG3nxcvTznWM0365dcQmXr8t6STxJTNup+eB6CTZlEK7Tp70iUmNS9kk/ttSHumkPoOEPjRvUh27rGW1oWnbxjK5JZllLDqfdrtRWutPCzK2rfqBpO28qL1pR627aPGlwbQxqp+Rpvmm5ZMY2PVaYp9H7PpBSuW25Mdtu5LetvLi5ZPOte4kaUlhvL7ab1p58fK0c/1Zm6WezpcvmiYtKYj3uW0ZBlZ53DbpvDWur+0klSfldcd1kg6bOdpJavtYUqMJebP2o/W2LR/9hPbJggAEchDYEtswpvpDliRtyYzb6XkgmlXaYhivr/3E01uSDkSjP1x61HRHNG4XnW9IfppsS0FkZx/1F3Vb1BeNpCknLdGketN+sXekXryPtqSTxJfMuJ2eB6JpsikFtn2S71o/EO2IJtlHPKX4JmlJyrY/L3mBaFIdze+I2nW2Jc8Wrd+Kqfodr7cVK1M7XzQuLUnE7fV8kpySQtt+W/JOiNpj8SWvJarldp0tyZskdp2kcW1IA/5YAzmeFrXrab9d0UWL3Y+mkxhov4FoR1R9iWtb0mkSt9PzVpphSr5dP0ixa0u+bRtPd6W8JeqLqugcB6Id0bhddN6W/DRpSUFkp0d7TruSpzb+WAM5dkTjdZLqaTtt0eh6CORc52Jb1K57WvLSpCUFcXutHxcdeyumtv9bsTK180VV1K/WWM/KMd7H+ViZ2qhtkmxKZryenkfjDuRcfVPxRbWNjqhtr+mm6CRpSWFSva7knxDV+r5oIKrpbdEk+yjPl3IEAhCYg4D9Q7aV0lYg+dEPXnTUXzhZpS2GUb34UX/RBKKTRH8ZxOvoudZbT6m0nWCvdTTfF50kHSlU27h2J1Sw7dsptr7kx9vU80A0SXzJtG23JU9/QU6SthTa9TQvSc5LZtxW02k84/VPW/W0jWl+qe/xvlqSniQtKYzb63matKTAts0yFl/q2Qy0nUA0TbalwO5L05rvi6aJLwUXRO26WXintWnnBwnt+7ZRQtqeT/UzzS/b/1ZCe5Oy7PpBinFb8m1bTatvJ0QniZYn1fVTKrVS7Kf1ZXOL99mVNtMY+lK2bfWpfaVJSwribWvdSWK33ZpkPC5ryzHeRzdDHd+qo/W1b82fJEnzc35SBSnTdrX9uGo7k6QthXH7+Lk/qSJlEIDAZAKBFMd/oPS8OaHKtmWvv/DSfkHazbStulG/LdswJX06oX7aLw/bT+1L83zRLNIVI60T1zQuHcuuLekk8SUz3p6eB6JJsiWZtm0ryTAhr2vV3U6w0Tmz2/cT7JKytK7Oe7x+K8kwlqc+5LHX9uL2ep4mdtua9tOMrXy1s8cy6Y+Y3Zf6lbW/ttiqfVwDSS9K2tJQvO1zGRvOM5/x9vW8lbGPyMyuH0QF1rEtadtW04FoFjkhRnb90ykVWwm2WlfzJ4lys/vQ9PakSuOyQI52XX9cZh9akhG3nda+lsfttf40aYtBvE53WgUpV5t4nW1J+6JZJGl+gpSKLcmP96PnbdEsonNu19W0n6UyNqsl0Fhtd/Q2B4FjVt2+pFXT5IxVsC7plpWXJ9kT407GCm2x27FsH7bSk5KPS+FgkkGs7GTsPDrdiE6WfPSl/ZbVR0fSqlnE9t2XSjpPcWnGE3LeFx1YeWnJHSlQexckECd8yxEd/8DKS0uqnc1L2QSiWeU9YjjIYHw6wcZPyJs1y25LA+IsovN5xjL0rbQLyY440cvoiLIeWLb27zqr+KbkE5Lq3JRza0K5DW7NvunzgAnFo6x+QkEzIc/VrEAcU41Lnp87nZ9evLKcb1rpKGnnd6SgHRVOOaqdzhNSAgIEjiWYJHHRF22JxkWDq0lyLqEwT/BmV7f/YNnl8bT+ArD9CyRvPW404TzJ9zTznhSoxuVt8cQSz4OEtvNw6kl9ZRWXIJ6Q84Go/qKP1OYqRaUQOxgYiNednJ6rvc1rI2MbPbHLel1pHwPRuPjxxILPdQzrGdtsi90bY3o6Y71Vmum1mkfsa1pZNDM20MloN7DsdiTds/KSkmpni/pXFrF/7vrieCen809Y9k0rrclA1BeNy5l4Ysq5cravgylVKC6KAIFjUeTz9RskmPcS8uJZ+gvCtgkkb110FjmXs1KSfZChjZ7YDDLYxU3sX2xBvHCJ53YgviN99XL294jYH49p36o/kHQ7ph05zyq+GDazGi/ZLrDa71npLEnla/O5P0tFsXkqo11kNohOlnDUccRlXRJbon48M+Vc6w5iareVUm1l2f2xb3k67CQYNxPykrJ6SZkZ8tTPOkhgDdL+XWkVJybPWbnrkvatvA0rPZB0z8qbluxMM6DcDQIEjm7MwzQvHrMMepIeWHlJyaQ/lieSDKfk9aV8Z4qNXZxUx7eNEtKfT8ibljVIMPAT8hadZfehY84rPanQielAzucVXxrYED0rui5atKgPvuXELH/AtAn7+rDbtbq5kRzcOCv+5FyCCzpf26IaQAaiLsybuJFbkn7nTGtkRwwGlpFvpZOSWk91FhnMUqlkdZrir2/53LPSWZIDMbI5a9txsf8BZ/+cxm3TzgdSYPeTZkt+gQT2FNg3XWcj4IuZ/UPakzzNnyY9Mdi0jB6WdNvKm5b86jSDlHL9JbAeK4ufx7JvOu3flMqWSKrjS9VBtuozWzWtmrP8srSayJRUjtq3P9Y3jNOar3muic1J/RvM6KRdz8/Yzk5Gu1WY9aSTx0XtfxBq362x6nlPtC/61PjcpTGIS4kyq48Dac2PtajX9DSZta9p7ValfD1hIMckL0jIz5tlt920Guhb6azJHTG0285aF7sVESBwXBHoObqxAz9tqj1WPc8r+gMeiPZEs8ogq6Flp/V8K29acjDNIKFcf9msWpJ+uQ2W7EQg7ev1oHOY1L9kl0b6M3q6s+J6M3Y3tdoJsdCxJP18R5UDOVFVW5We6JnxcSBHF2XW+fnqDIOZta8ZuiplFT/B61ZC3ixZvlVp3UoPrHTWpNbzsxpjVwyBRjHd0msOAkEO26ymG1kNx3au/4Iuwj/7F6WiWpYf2pfedu6KBqJJfUv2TaK+nBQd3JRbTMIvplvne22Lh0dENRjMIoEYbYlui54SzXIdiNlKRa+7Vckq+1rVmMrYj19Gp/F5dgKsOM7ObhU1N6QTfwkdHZM2Tyyh3aKaXC+q4xX060sfGjDqMUn0j+dAtC/6j+Pz3jgth6nf11WbMknV5lrnrSXaFg1E9VGSpqgvOklOSOGGqAaeO5MMV1y2PmN/b5ixHtXyEeiL+SKul0G+brGuEgECR7dnU/+IxGUgiV48I+N5U+xUI1mXk0C0J5pF1H4W8a1KO1Z6UUm7H213WX1FPie1PyunqM2k46Zk+laB9q3PyHVEB6KuSxqrpPxpY7EZD6ZVKEm5jqMzVjmMfl6bctTfAYGoPW7JGl0XJ+TY1sQCJamvrM3PUzfex1fjCc4XRuARaWmwsNauN5TU3qzXwaz1FjwkmptEgMBxEp1iy3zpvmW50JP0cSsvSzIQI121istjkujFMyacv2JC2aQi3yocWOmkpJ+UOSUv6ZdNf0qdeYt3pAHVeN/+vI1a9bW9lpU3kLRrq0yWi7ck1WdbfMmYZY7eZjU0sNJVSSob1c54QIEcW6LHROOiP8enRXfimXOe+3PUf8OMdZtWPR07Mh+BpGvClyYH8zWbWFv7Wo+V3B87z3Pq5zHGthgCjWK6pdcMBIIEmzMJeVmyemJk/xIJJC/+gy7JVGmmlqQXBAlFg4Q8O2sRffXtRpeUHljtzvLLUgP67ZgGsTbj51H2UTnZiRIlOQ4S/AwS8rJk2dfH57NUqoBNT8bQEj0pGpd1SfjxjAWcz9NeMEP/Oqc6jrgM4gnOZyLQT6ilrJchdl+z9KN11pfhHG0ulgCB42J5LrI1XUmIy0ASvXhGznM76NQf0FbGNmb5gbZXRgbSVz9Df7MEXw9b7Wbpx6oyU/Ipq1ZeTr7UD0T1GOlAziPxo5PxcUeOAytvUtKXQtWiRf2258Sesyw+BmK0bhmes9KuJzfEwfg/FLZyOtwW+x2rTtNKa3KQkJc1a5a5idr25UQ1jwSW8UDSfSuPZH4CA6miGpdZ5taXBuLXrJ6vxxuVc/sfcHpN2jZWlVuSwS05ZDhJgMDRyWkZ/eLVH7y4nIknZjg/l1Anzy+REwn107L0F0ZgFfasdFoykALVrBKIoc3qqayV57Szmeq4T+Ro85hlO5C0aiR+dDI+7ljpack88zutrXnLn7AaCCTtW3nTkkm8etMqOVauc+jHNJDzvGJfB4MMDTQz2KiJL9oSnUdaOSs/Ztn3rDTJ2Qkk/dyt52xuU+z9mOr1Z1+D5yTPlhN2xpS0fR1MMae4KAIEjkWRn9yv/qDa0rEzcqZ7Yj+w6gSSXrfy0pL6Q+2nFVr50S+aePaZeGLKedL4k6qo71tWwUDSHStvWcmeNKwaF+WUhakvdi3RuPTiCTkfWGltN0vbWs0XbYu6Ip0ER04l5KVl+VLQsgp7VroMyb7lpC/pwMqblPSlUDUug3hifG73cyzBJikr689eUt0oT9toRokpR7X1LZuTVprk7ATOJVTNM8e+1G9ZbTxupTXZG6ueRzLv34yoHY6OESBwdGxCxu4Ells9SQ+svFmSZxIqnUjIS8pal8yzon5SYSxPfynZbQ4kryeaVQIxnPbLTf3RwMMXjUvSGOPliz4/aTWofm1ZeXYyjaXdVs+qqPWmcdEqgWhXVO3nlea8DYzrD+Roz82G5GUZj45DxxOXgSRsXvFyV893xLGe5ZxexzrGLHLMMhpIWtUW+9ahtj+NtZa37IZmTGf5XaFjaVvtdyQ9sPLqkvRnGOi0Oj1p85zV7glJT7sWtIov2tWTmAzkvBNLx0/tn0e95rS+HzdKOE+6DhLMyIIABNIIbEhBaGkrzThnfiD2dtv6g21LWzJsuyi9LWUtUf2lEJdAEtpWZBc/+pKfJtpe3DZ+fl7KAqui9qt5SfU0b5J0pDDefjvF2LfstE4gmib6RzLerp5vi7ZE45z0fENUy2z7tuTZovYXRG3bTcnzRW0JJKMrGre365+yK1lpeyxa/4RoMFZfjnFpSSLen56niS8Ftj9qvyXaFLVFxx+IbouqXVzVp0li1wkmGSeUdSUv3l87wWbWrEAqxtvW821RzU+TQAq6ona9luQlSSCZtq2mt0S1TNmq+qLKsisat7fTgZQnSVsy4/Xi5zrXp0SbonEJJLElGrfV821RXzRNWlIQr9NNM0zIV9t43a0Em7SseD09b6UYan7cdjvFLsruWvbTfta0ns5VvA893xINxmqzluzRPG/LMalemv2m2Cf9rAaSP0nOSqHdj/bdEl0XjYum9fqI29t9+vEKnEMAAskEkn7w/GTTmXL1hzj+g6rngdVSW9Jxm56k7R9oLd8ea1JZVL8tNpNE24hs9di10lHZtuSrpvWl+b7oJOlIYdSeHtuiSeJLZtxOzwPRNNFfgNuidp0orWWTys+nNSz5Jya025UyVa2fxOW05CfVj/zxpdyWtmSEE7QlZXFpScK2j5fb50GCfVRfx9Ada9qY1FbHNU22xSBqV4/BtApWeVfS8fptq3zeZEcaiLcfnUcMtqQ80u0UWy2fJMopnEHbUuesVS+QdJK0JTPeh6bT/E3Lj+pvSN1J0pLCyFaP3UnGVpnaxutuWeWTkvF6et5KMdb8uO12il2U3bbs43XT+vGn1OlKeZI0JVOvLbsPTUfXnNbdTrFRu7boNFkXg0ltnJfytH70eu2Ial+R+nKOQAACEwj4Uhb9wETHcxPsZylqJ/ShP7BxaUsi6l+PW6JN0bRfPHHb+PkJqTNNtsUgXqcl6baVFy9POtc21L9p0hGDeP12SgXfstM6gegk8aVQfynG289y3pU666KTpC2FWdqK20Tsgwl1fSmzRX2ZNM8tq4Km4/3q+TQJxGBb1K6XJX16WuPjcrv9IGO9yKwrJ3F/2lHBgo7KeZbrJfJJ/dM2JsksfbTHDdrjD1I6UvvIJz22RH3RbdF4/qRzvd5aotOkJQbxdrrTKsTK1TZedytWNu00Xk/PWykVND9uu51iF2Xr/OT5WYvqdeUk3k/8XMvSxJeCbdG4fdbzE2mNJuT7kpe3n67UUR4d0bhPvqQRxwg0HPOn7u4ECQDOJeTNk9VLqHwsIc/O6kvGEdGBXZCQ7kme2p5OKMuS1Raj46ID0WnSEQPtS/0rUgbSufqR1W/1V22Piu6ITpK2FJ4UnWanbfRE4+w1rXWzivahPg2yVpjBrid1tI8zOeoqL61zIkcdl02Vs87T4zmd1HonRZWFnk8SLVe7LH30xrZtOc4rA2lA++2JTpOeGCiHjmjdROfnuOgg58C1Ti9nHTUfiOq8nBHNKj0x1Pk5nbWC2A1E3yh6UnSaKAO1Oyqq50gJCHgl8BEXV0+gLV1uxrrtyPnxWDqQ8w3R+0V9UZW+6FdFz4n2RLPKthj6MWPtpxNLt+T8YdF1UV90R3Qg+pRoR1TTLsqGOBWIvkFUfVc/VT8v2hftieYVXyoEosrDF43a1fa03Y6o9pEkvmS2YgU9OVedJIEU+jED7WcgmtZHzDTzqS+WG6LRHK/Hamp/XxU9J9oTrar4MrBAND6vmqcyEN0RVRZ6zSsLTecVXyo0RQPRV4hGMs/1GLUx6RhI4Ybo/TGjgZwvu99Yd6U4DcRLP+ZpX85VJ4nOpy+6PjbakWNPVI/TxBeDQDR+zUnyxrWm83NOdCA6j/hSeUM06idqqy8nej13RLP4K2YIBCDgMoG2OBfGdGuJzmrgGO+rtcS+aBoCEIAABCAAgTkINOaoS1UIQAACEIAABCAAgRoRIHCs0WQzVAhAAAIQgAAEIDAPAQLHeehRFwIQgAAEIAABCNSIAIFjjSaboUIAAhCAAAQgAIF5CBA4zkOPuhCAAAQgAAEIQKBGBAgcazTZDBUCEIAABCAAAQjMQ4DAcR561IUABCAAAQhAAAI1IkDgWKPJZqgQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQAACEIAABCAAAQhAAAIQgAAEIAABCEAAAhCAAAQgAAEIQGAFBNZy9LEutq8d219ZQb0cXWA6gYDO26+J/lPRQLQnGokvJ1q+E2WMj74ck/Its4Umi+hzoQNwuDGdS/3Zted5VS5H/Wt/eX53rMq/Mvbji9Or/hl1mVN0jeW9xmet5zILfIPAogj444Zm/r3dlAZC0Qui+sOWVbbFUOu1slbAbqEEIv46B6px6UpC8/x4ppxr/raVt+yk9qe+IIsn0JEmi2TbHvffkiOyGAI6n/ozg1wn0JKDMglE80hbjGepl6cPbCFQRgK+OK0/G23Rm6RxU2pyoi/Fj4tq0Lg52fRG6WNy5ov2RDuiyGoJBNKdL3pO9LCoJ4pAAAIQgAAEVkGgLZ20VtERfayOwJ6cXbXF/mHRE6JPiPZE08SXgva48Pj4yGG1BIJxdxrw7yR0fVLyzqSUJZgvNes90rr+owSpHgH9h8tAtCeKLIaA/k5N+pleTOu0AoHFENBFpp5oRxSpCIG8gaP+otJfWF3RU6JHRNNELxgNBDQ4GYgi7hHoOeSSBhdINQn0ZViqyOIIdBbXFC1BAAIQyE4gz63qqNWenOgf+aboCdEkaUmm6kC0LYoUS2BQbPf0DgEIQAACEIBAFQjMEjjquPW24o6orir6onFZl4Tmqxy9fkj9f2SrK5jbY9XzlqgvmiS+ZLZFA9FJ0pTCtqgvGpcNSbRFte94/9pvVona1qOKL7opel5Ux6HHLdFANE3sNlpiqD5ofV80LurnCdGzolquqra66uuL2tKSjLbo20RVtG57fJTDDdmQs/aNVL6Tlpjb/mieLzqLtKRSO6Wijn9TVMe8PVY9b4n6orNIWyq1xhV9OSrLqO3zcr4l6otOk0AM4hwm1W2KbVtUj2nSkoK26CSbE1LeEp1VAqkY91lZPibqi2aRDTGy65+SPD+lso6lLeqLxiWQRFvUF1Vpiaov0TzoueZNk3UxUCaT6rakvC2aV7Td1riSL0cdp/qn+baoH5ui50XVRo9nRVuitqhtW7QlmkXaYtSKGWr/ST5EJtq+licx0TJb1FY1TXwpaItmsVFbW7TPrGzsupoORLdElauqstW0L7pICaSxU6JZ+2mL7SQmUnxD2nLWupHKfhKx60qVyC89b4n6okniS2ZbNBCdJE0pbIv6onEJJNEW1b7j/Wu/WaQtRqoqvmh7rIEckySQTP1ZiY9P58EXnSaBGGyJ6jURr9+SdJqckAJVFV/UnvPHJE/HHUlTTpJsovJZjtq++nBWNPL7vJzrWALRNGlLQWtcqG1sitr1/XH5pIPa6Ji0T62fpW8xm090wKHoWasZdUTz21a+nQwk44Ko2kYOb43PNW9btClqSyAZWt4WnSQtKVS7QDQuHUlovratfei5alc0q7TEUOvo8TFRHYfq1li1LS1XPSWaJC3J1HI9qk1kr+34opH4crItquVpfehcxKUjCa2j9lpPz1W7onHpSELLbVE7tU8SXzLPi2o9tdkaazzPl7y80pUK2qYtvmRoP1qmfWyJnhWN8vSYdJ1I9kTR9rqigeiFsW7JUVXzw3FeWtu+ZWfX1fqbonHxJaH5bdE0UV/Uxp7TyN4fl29FGRmOnXEdX47d8fm2HLUNVT0Px8e08Urx6Lrsjm3VT62rGuVty3lS/Zbkh6KBaFzaktD8DdGt8Xl3fB6fYy1LE18KtkVDUfVJ66l9V1TztkV90Sgtp7lE62tdHZe2H471hBzjckwSUbnab4mqL9ui4fh8XY5xUTutY+fHbfR8Q1TbaItGou2qJokvmVqmdfS4JRr3RfN80bh0JKH2ab60xuWT/NV+tA1fNC7HJKH1tKwruiUa90fz0vqVotHPkdZVVdstUa0ftbkp5y1RLQ9E80hbjKN6p8bn2q72oXp+nKc2m6K2dCVDywK7wEprudptWfnTkk0xiMapvmh91a5oKLotqteHLYFkaHlbdJK0pFDtAtG4tCWh+b5onEFX0llkW4xUtQ31P0qfkPO4+JLoikZ2W3KuGuVty7kySBO1DUW1j7Oimtaj1tN8Pa6L2qL5qtq21lXdGqvmh6LnRbXusXE6bqNlkY2c5hZfakT96HFrrF05aj+h6KZokmiZ2iX5rvlarnpMNE0ek4KoHx3LluhZ0W1RrXtK1B+ft+W4UOlKa9pJMG7Vl6Omt8fptIMvBZFdkGC0IXnahg5M4cQlkITWbYtOkpYUql0gGpeOJDR/S1Tbb4vqxZFHWmKsbXTHx9NytMWXjG1RtdNJsKUlGXYbth++2ERtnJBzW3zJiMqP2YWSbotqH75oknQkU8tt6UrGtp0paX+cr3WS/NkYl2tdeyySNVG0T23XlvOSofktu2Ccp3Oo/eUVbVPr6vG0qO2vL3larmqXSdYN7ml1z4qNtr2pxjHZlvPzsXT8NJCE1lHtiiZJSzK1PBDNKh0x1Drar45nQ9SWlmRomaovmiTbkqntnEgo9CVPy5PqtyRf6wWicWlLQvO1jtYNRG1RvmrTtgsk7YtqPS1Pm4fzYxs9ql1e0fa7onr8/9s7u/NGjjTN7vTO/WDu9q6jLWi0BQpZIK4FlbJAbAuYZUGxLQBkQbEtyJQFZFuAlAXi3O0d9xwyojoUykwkUGSxfvJ9noOI+P4i4ksQRFVraqwRoZb9tLYxEWq1GPS/rxz2UbvjnMwzLhRB7iW1Agbtv4HnqtVg0GfMBrKMfYAmG6oxn8GYWPny0ppdXqRxy2iOvgi1Wgz667wcd5X8t4whG9Po+hrM1+8Y4RS1BJf5lyPJEdshxdmnUpGF+Z5jTjucxoW5oMpnrM9KItQKGPK5tpUzsna/FubU4DQuQqmWhfYduH8LGzhV1uhmkg74jGlHYgI2/e7vvNYVBnPt/djZ2uR3rJXrOo7la7P2Lo1zMQ0xp8p9rd+MJAZst6A/Qi3t9sRx7Fwh+Y3ZQK0Gg7kHiFCrxaD/fRpdP6u2VMsH8IAexHWEOeU486eUa3dVQGTtHi3MqcE5dpZ9stvUAOeoIcnax84x15OyxiW1xrTD6B5TfnMCeJexN0mL3fwAY9pj1F+rw3Cojax3YPzceWKKuWY8Re5p7VIbFtpuSmM1b1kbE+EUmSPtTJI+Yxoo1bDQfuyOtykuMmaZY27IhmK8ZK5vD2PPE/OHLzHOl2pPoHUlwpQiDmO6kYCr5GtHfNkUmIzlN8keGUu1LIw/QIAxbTDaC2Nq7TCY39aOYm2+ucbJqcq5jtYakz4JY85ku2Z8gJjWDvluXWGrpwGDeXXMAZvU2mF4gKZ2FOvI3JgWsvJZzB+Tz2APdV6O3SbfZTak8cAoIa3HhmuM1o2VM7DWbr7nm9Ieh3FjNaZysr1NeeY6n1LAYQ/Gfi6zfSrXs1v/dipgwm78sTttU0xX1YjJ3lb2etlgGNujTXbv5h7nytr12XKtKyb622wYGQM2zzBWQ/sB5qR/LEbbA+wmkn1m1l8SM1VjovSH/wXh3VQA9gjufQ21tM+dy/g2xVy6qHRgbX6o7OXSvLxPWzqea+7F3OA2jbsjhePCOMu8T7HRRVJkdL8W5tTgNC5CqT0L7cfOWebU8waDNQ61Y2SdH4B9KtWwmKsRjvhxf1DLzFruVaploT3AmPYY9dfqMBwqY2BtrM/5mMz/DTbHAgu/OdYvFVho25XGah6S/6KyH1taV8JM4DbFtFXMIdlDZa+XEYN7XBeObLssbHnaMRHvYl6EUhsW2nelccF8T8zSvC7FBsZSBxZyTPln1rNmNUzcP0KploX2XWkcmeeatcvzyDE1BLiPnCrrmxcnEhvs+h3nNPXsrkk6p77nklKBhbW60jgxN8af0VJjNv0RrOtojNTK9wiFo2Fu3rvCNja1N56lrptrNmNJhS3nu1cs7EumLUHmHRYE59imis32WNnzsmHiHo5LtSXQnJsFCfsUG4tY5+a3MKcGp3ERSrUstO9K4xlza3QTeQfsckz5feBzzgpMzG1hTnOfHQ8k2ucpWd+YOBWA3ZjbGf+Y6zLlxTFnYXPvXbHOU+0SsmFk9F7GtJXvItnH6lahH77T1TX+15/qyDPWFh3Agzq+hTnF5PznXFAVY+3n1pL9j+3ZHwvAv08xf52InTpHvvPPE3mleZ8WU3uUsefOTzmPd9pAOHezlHfPKBcQYUwDxh/hZsx5xNbjH2Zi3LvWFkMA7zjAnHqc1vihCBqz6d5ABOv2oOLj679fLtJ0yXvi31n/nk291/4d8bS/67yX8wgBTsk3Z6mO3ed/RgptsQXo4ZhuCLg/FjTjN7ef8OdnO+XPada4g5gNabxJY23PYVdMBtjDMcUUcKyfhv0LNhAgy+erLWZDGvO6Z22ea+NKfcfiDobCqE3942mYfL3HY+62isifZzeVvV7m/Np+ynpJz/pUMN8r19+nic9qTG+SsR9zTthish+7u2E5ZptynnPwPfESihQNsKT+HXHq4ml4fB14/Qu0MKdjPcm152r0M84B32bGP+a6xujZ+zFnsi059zCTf598f65iYloveb9PPpv/rIqes/SAb2EHHmaAOeUPg2EuKPn6NOacBSmLQ4bFkdOB/5p2ffDYnwECjOluzIhtm+xT/jJtSIucU/qea17WjkeK5jerOUvOP1XuHofvrXfQQQ++x6z5MXVJP1shZS7dfyB+m3Ly4A/kG9jAfTLGNFpXWw/fQakfWGRfaV867xcE5phQxG7T3L1jYR+bbpIxjDmf0Zbr/7qgpuceIN9jQcrvQsydUsBhfUeZk3GeYQPOVQ8D/AQtlDI2wB6WyPismCcT40OymzOk+Z7Rn7UL6CHL92GfFjeMntW8HlQA13+HUtruISQYZrXBK+aoLdxBXmubkj9Tccq5wN6fEOO5Sg0setC+gfK8gXWEPQywVHmPuwUJOeavC2JPDRlOTVgYn+93T3w8krNJ/jATZ4x+6zq3FxECTGmYchT2JTFF+FnTQJZn9uzO/wwXMKf7OeeML79H+pmY7LrLk3p8ji+Odc1j600KmDzUSIH/HrF9rOncxpf7nlIjlIknzJfuMVBzc0LdU0NDSnh3QuJznOea/ezBG4gJhkfbDePP0MOnUr7TsHBDz17Lc3ufC9iD+gGM7UH9C36CDWhXEW6cnKlcZy49x/xXEbRJ8ytGWaKcsyT2nJhcf1iYnO+1MPx3YXO5nkO632XML4wva/oetq8Resjy+au3T8PRV+uq3dOw6DXnGOyZevC9eAlKf4T8pfCOuXEX0INyrm6ehg+vG2Zybm/Mvf9QbX6yNG6+ynHvQIjnqpW/uDY4rguna+UzPkV/TsGn3CucssHC2FP2X1jyMSz30Pe9nCtzY6Ks4bl7GCDC56bAgfz5biD3gumjBl59v+Sf/0fjM73Ue82VvZtyvsYXx3wWL3CfF9/A+NJ3/VT9/L88q7uFz+u57rxnPwmwTXzH2CT2jP5ie679KHVUm6MR0wE9Ls/qHfagvNcvj7OnlxsGPzi09xBhA/6COlfm35+bTN6P0C/M/5h9Fm7xGOadXlsDB/j+hEMYX+qahb8ApYesyKSHAU6RZxkWJtTPyfdghAADRFB3T8Pj+8e5790sv2gOiWzLo/aP6U2uc2zcHAt4Jn+gTu5FWXLPwudnL64h6w2TAXo4RfenBH/BsT9y9n7h+cuebMjpYAs9+Pl/BwMYJ2r/+Pp5vXhmz76BPfgzdweeeYCsl/jimGsvGcNU0Gt8cfw1HcZD2aw5heQc5oImfGHC/pxmH/wSBYKO3bWu45tIhcfX+RfPIafuMV/1915r+yGohsfXT//ivnIDKsA7aMD3VQsvrdzjsHCjLXH3Vaxr61zAjxBgCz9Dlv57MKYHe+/6Bs7VhkRrzCkk5/8UQcPEvDB/8uld2jEs3Hlp3MJyH8Lsp7UHOFfW6CHCBlw3EOAtLJV5WUOenDj2xF9BAy34RSifj+mjfuHVGM8qEf4BtczbgqOcKnPCwqSlcVPlluRvUvLYXbT9DP6yj9CnMTDu4VT9mhIC45DmU0NIjn9NBczY851mQl7ENaSq7p/nybRo8HN/C2+hhSn915TjFe3v2dt7/w3uPvE5Bvazb+5/D3MyZlR/GrW+rPEulY8LtrlIMf2C2Drkr7XhBdY/LKgZU0y+94KUx5Acv12QkPt0zgfHgvK/O09ckOB5WgjwMYoktzDVgwHfj3AP+Ust0xfVkKoveX8FYjfwS8oph38mX2QU1T++Pr14pzv4Ltki41id5F40XCyI2qaYvoj1HCqf5Wk1/hoxtxDgJTVQ/B6WnMk7BXgJ+TO3gbigeEuMjOltMl6m0fez97tJ6yXDXQqKC4IbYloIUKpn4b65r5H5L1CqT4sLxpjm+zSWQ87blsaJ+SX2tvLdsQ6wqexjy3zeMd8S25L8fI+pz9mbtFFMo89QvX0aTnr17io+vs6/5HPlHKPv51M+eJfc+0PwM07yWZd8jkb2bSHfk+nj3Du2Lma0mfG9hss7BPDz/w6mFKYcH2n/NeV7jmNa8v3mWI1Zf4P3AVo4Jh/kb3A4EhhSTB2n3b12MKWAwxiJUGrPQnuAc9WQOFW/rrlLsbFyNMnuOKUDDnsVpgKS/ZZx7E7thD2lPf5J2LxaHQb3LpWfm+dxPidz5VhcWcM9H0oD8ybZWsY5LXk/1fnu5Z5zCjiNa6GUedpjaRyZ77AZ14z47I2+a3gPB6jVYjDmIo0N4znak2SdsT3Kep7JGGMDlLLHS579LXF1fpNskbFUy8LYCHPa4zSuVodhSf4uxY3VqGvW6wOGrjYW68jcurvCNjbdHomz9/bXvQIcq3kgRkrlGtqdz2ksP8dfM3mAbRobxlqe1bj3UJ8jx0Ym1umyYWIM2I27qfyXyf6ustfLmOKs4fwUtQSb530CzGmH89geHTHW2qTR9TnK+bnWXI0DTglFkPkPsCts9TRgMEYilGpZaA/wMbJGN1HgFvuSvptfn+WATeYUcJontZbkL4npKGzcUm0JfIDdkYSfZuLM747kh4n8mOxL892rhRdRQ9VTNmhT/DvGKe1wTNX0zTb3hnufcs2PUGrPQnuAc9WQaA05QIAxXWE05nbE2SSf45QucOR8PwjGlPfYjThbbOYHGNMeo/5aHYZDbWTdgvE7mNIVDmPaqYAJe4fdvFLe+dizzj26KRMXzN3LPecUcBrXQqktC+0HCDCmNxhzzJhfWwfW8I47qBUx5BqO9uMc7UnKdd7NFPAMxjnWusSgz/fy1DmuUkyd3yR7ZCzVsrBmhDntcRpXK2LQfoAAY7rCaExmLGbOZu1uLiD5rW+PxhQwWscY51O6xmHMLo2RcUrWk1otBmvMPWd9xjQwpohRf5fGLWMtfQcwznNPKdeY6s2GxFwnVEX0/Qbu8aby5WVgYn6uEZmfopZg67vPLbjnmK4wGuc+c/Kexu3S2DCeq5ZEa/m8ppT3aUcCvI/3CiM+Te/B+hKhVMtCe4CPkft3EwUa7O7hOY/1fUdMKWuaG0tjMQ/MD2CM1NInc1oS01HgWJ1yD+/5AHN3jvjtm3E7qKW9q43VOrCeyjdX3xWMyTN6vnyGdizoOWwNRTxIC0u1J9AcD3gBWwhp3jHqu4YxXWLUf4AG6lwv3IIxEUrtWWgPcK4aEq3RgmeQBvI5IvMdGKMvQK0Gg37HObU4c52GeblHl3z2cAO1WgzmBhjTHqP+WtY91Ma01meO/gbyeS6YZ5/nOVU5t867xDC2n/tegc9aApwia7rnnAJO41qoNXWuSOAOzDtAgCm1OIyTBsbk3fTfjDkX2vbEWSOC9W7hAkKiYdRmzAE2MKY9xhzTMN9CgAjvIfvq/Cb5ImOploU5Eea0x2ncmFqMed+GeXmmXfJdM3ZpznCSDkSbO6eA07gH2EGEkLhkzL6W+ZwiTmuIOXPSPxZj78tnecF6CwGcd/AAe5iSNX4D48b2MO8y+Y2JMKWAwxrG7SBCSFgj+1rmY4oYzR3Lv8LuOb1vPk9kfopagq3dwCHhfAsBLqADY/QHmNMGZ+6dOa4/RnuS896eZQsBnHegbw9jMibnNszrXM95nWIiY6mWhbkBPkYHkt0n7+1YKu9vXAM5LjLvwDPo20CpyCL7GuY574L5FbjnLbwH4yIEyLKmzGlJTEeBY3XqPa4xPIC5EUKiYdSmr4V8h3w3TI/KuXk9NgaMxu1GnPoOkP32TJtcgj6JYEwLL6KGquds0JLnAc0tsWFeYE4tzrHcDnuABqwZodSehfYA56oh0RqOAfbguqbDFmBMDcZcY8xf2ow9QF3fPrWwgTG1GM0JMKY9Rv21OgyH2lis2+Q3t+TYeYoSf5i6p7XG1GA8QLlXnnfYA5wq882dU8BpXAtjihhvwZia99gCzCnizHlhIrBLMc2Ef4l5T5D7qAC5Zt7b0Wd3DVPvJVyP8ufyAGXusfwmxUfGUi0LcyPMaY/TuCk1OA5gTIl38ryqA9enyrrmHlMgYA/l/nlujQtYIvcyrzkSbE2ZUovD+1qrRFsLx/SeAPN2E4Hb5D9M+EtzYLGH8hx57nnyM2I6qoD1FnJOHvNdNvia5I+Mp6gl2HoRAuwh1y/HDnuAJTLW3N2S4AUxLTEHsGbJkt7Z27HcDnuABqwZoVTLQnuAj5H7WyezGynWYDsUMTnW8Rp8vmO6wDiWl98X5kTI9ToNSebJnJbEWPNYnbE9WowPI1gvgtpDjmmYZ2kzbk4Bp3G7iSD9ezCmpsMWEvpa+J3+43er11tEtg5p+4GxT/Njg2+oLYQUeMcoL62GDXbwI+xBBfAsG1A3cP84e74X6wdwjwHu4Ln3oORiRSJDih4YX/o8kT0CKO/dp5HhVRXYfQsb+JzOxXEmFfB8zJkj+dZQn8udI2cJoAa4A8+m/GUywN/gJRUonvvqPp5BXkMbNvUsIW0+MHqW+7T+1ENgQ8+zSRt7FlkqcwOYfw99GhmeVYFq7nXuPv5uaOB76OG5FCkUUrGB8Q7swzF5jy2EFGiefCpFNgpwD30aGf6giCUk67HYFPY4RF7D4+zpXvXdNsk/MFr3c5Hn2kJIB+oZhzTPg3519zQ8+2ugontsUuUbxvs0X4dn7kBDPb+JO65aO7B24HU6ENlWjskPRn9e/YW+au3AS3fAP6QcXnqTtf7agdfqwJ9ea+N137UDawfWDnxkB96R30E4Uuen5PefwFi1duAlO9BQ3L+9efuSm6y11w6sHfjyOtBwZP8Gw3HV2oG1A6/TgYZt/Tm8hQC1/AXul8scU/vX9dqB5+xAoNgh8Zx111prBz6rDvznZ3Wa9TBrB9YOrB1Y3oE9oQGuwF/YPQyg/NIY09gz/gir1g68RAf2FP0OAqj/+zSsr2sH1g6sHfh3By6YdhD/bVpnawfWDrxSBwL7XoN/8+gXyMx75hFWrR14yQ40FPf3wQ4irFo7sHZg7cDagbUDawfWDqwdWDuwdmDtwNqBtQNrB9YOrB1YO7B2YO3A2oG1A2sH1g6sHVg7sHZg7cDagbUDawfWDqwdWDuwdmDtwNqBtQNrB9YOrB1YO7B2YO3A2oG1A2sH1g6sHVg7sHZg7cDagc+xA//7czzUeqavsgP+8yj/J93s/1U3DCfaq/Svbpl7df+F3ixwbu/wpZ7/C237qx87cIJznrt5qv5ceLLOvwbc5+w5X/Xz9XrXqc/Rz/fU68nWDqwdWDtwRgcach7Af7aiVGCh3X/KotYBQx1fx3yN6z2XsidfqnxmPrtV31YHfOanvm9Dytmd2apz9jxzq9E0v8g14Pm7hP/ofIRzdUmijKnB+ACOq9YOvEoH/vQqu66brh34+jvgB3/z9V/zk94wsFsLW1j15XQgcNQWvrbn5n38t0P90ngBagOX4JfIAwQ4RVcE+8Xzp1OS1ti1A5+yA+sXx0/Z7W97r57rv/2GWuAH/5tv6L6f4qqBTfzF6i/sVZ9fB/7Okcb+P/QE7C/13Kb2fOnueKcO/KLoGf4bvoe/wV/gZwiQY5geVSCiPRq1BqwdeOUOrP8vB1/5AXxD2w/cVSIuIF0AABDkSURBVL6DVWsH1g58fR24eYUrvcaeXjN/IfyR+V5DoYF5A3+GCJfQwjFZczgWtPrXDrx2B9a/cXztJ/Bt7f8D1/VP4qvWDqwdWDvwpXYgcvAAPexhSm+T481UQGG/Yh7g+8K2TtcOfJYdWP/G8bN8LB99KP+Eq66fhj+8BiwN3MOxmBti7qDUhoX/U2yEAGqAn2EPY7rAaN5+zPlCtnzOvPc9+wzgOW9AXYL2PYxpg/GUu1rPHAnQguoTzk9VJMEzbFPiwHgD/wTnc/IcY+e/w/4PGGBOOf+CIOdqgLlnbcycAs4mBVwz3qf51BBwNODf4KgfIDhBY/kBe76zZ7b+APZrD6fI/EuwxvWRxIC/gQH2UMo6DZRnH1j3YC8HqGXOJfQJhlFtsV7ADdyNRvzeuCS+ISXAXE1jNnAN6vJp+LDesr6Apc/N9AA+O/PUAHcw9V5t8G3gGko1LLLdMdd0fg938BYGOFXblOD7aU59crrnnCLOFs45j7neLZ9pYP4z7GFMDcYALXiu3Jc75j9CqYbFD5Br3zM37pxzkrZq7cDagc+5A9cc7gE2E4dskn8uZpdiAmOpyOI3MLcD497DAbTdwti+YzZCHz/EzLNOLWt2tXHh+g1x+ZyO1hfrPaS5ZzokG8MftMWi33jvtYP3kG2OAUp1LLLffZ3LJSzVnsAHCNCl+dT+nnFKb3B4Bmvl/B3zXFP7G5iSvpxvzg7ewwEe0hgYaxlrzJgCxpzfjAWM2PJzyGdxtIYEKPUTi4dEx7iDJWcmbFLWcc/NZMSTo2Fwb8dS+fz6DrBLdIzZdsG8VsCgv4U5NTiNc1wi72H89Uzw4UhMrnFT1DBHsi6YuLZ3D2nMMYG1CqBvB2/AWHEtHTzAAbZQS7++WtkecOi35nvYgb6HxCXjqWpIsEaEOW1wuo97TyngOCRyTL3OdscGrOl4lea3jDvwfubqd3T/Wh0G/QGMcS7mlupYaPfsu0S2ab+CVWsH1g58RR2I3MUf7gbG5IeEHwjGRBjTAeNt5QiszdEXoVaLQX9XO2bWAZ85u5GYA7ZTauUSgYk1vePYLwb91rYPU3sYY77+CLWs6x51j3LcVN3snxv3OHNtz3AxEtxg0ycBagUM+jzHFmoFDDl/UztZR/AM5juv1WLI/jq/w2derYBBu/s2cKoiCe7ZwJiuMOq/hQC1LjHoP0B95jq2XOc8xzl1OK0fiiDnuc8XhT1P9Xse8yKUCiy0tzCnBqdxjkvVEei5xhQwWk+/vRyTd6n3PGCTWhFDHZtjQvK5lzFjPY7JN1a7wzdlt6a+a9hAqcBC3wNEeAlFilq/mym+w+c5QxFzYC5jajA+QI6JzGu1GIzZ1Q7WXeGzRoS6Nw028+1brYDBPP0RVq0dWDvwlXTADwI/jLqJ+/iD/z7FjH04bPH5wXAJpczTHkpjNbeeMReVfWoZcBi/Gwk4YOtG7MdMtwRYs5kJDPjskXFje2jTF2BK9seYdiTggM0a52hPknUlwpQiDmPG9snPwZgp5fOPPasDSdYOU8nY8x7WKeV5zC8VWGiz51s4R5Ekz9RArYBBn3s4n5JnNa6dChixb7B57m7El02BiXV32ZDG98neVPZyGVhY/1AamQewZgtzanAa57hULYHmRKjVYNC3T6P3r7XDYEzpO7CWWhGDsQ3UChj0SQtTusZhTKwCOtaHyuZSu/H2f0oRhzHWfm7ZF89l/QbG1GDUf1k5zZMxNRjNkQBTusVhjOco1bHQfoAAY8oxdW6OjUysscuGdVw7sHbg6+iAP/z+Mqp/+LfY/KG/AGP8gKl1icEYY7OM17bLholxg919rb1EgaCpugd8S+vkvXK9JXnXae86Nib7jvGYpu56ILGue6xW9u+ZPMCS/d3D2ACl9izGnm0ZE1mY20CphoX2XWkcmfusjbupfB3rQ2ELaW2vtoX91Gkkwf0aqHWJYcpXx3oOOUXeyfpT598lf2TMCkzMMfeYWgKMjZAVmGhrYU4NTuMclyoQOFX7Pb5biCnmgrGW/bupjAfWUitimDpfSL5jz8MzjNXosI/tqd34CFPa4DBmNxVwpj2QZ/+sfQ1jChgPMLa3dhlTg/EB6t7Xse5rXKgcXbK/q+zl0r3NnZP152rM5a6+L7wDf/rCz78ef7oD/ofbG9hWITGte8ZfQL9xpd6wGOCuMP6Q5v5H6nO6x2nedi7oBX0x1T72H64bdpNi6yEmw8+1Y2TtPhE2I76PNS25Q465qDZrWP+tstXLUBvS+rs0/mPCn833TP4D6r2z33ELHQT4Hu7gJZTfn/2C4j7XDXi2pXqbAi8mEiL2AXrIimmSn1G2j419Mk7VH8v5GNtAsuRnzfSDIrNfoId7iFAqstjATWn8yLn7zclznKN+JinXDDMxp7oaEm5hC77PLmFMu2TM76uxmDlbP+fEl+82FTb3nrxLSVdTydi9199n/KvrK+7Af37Fd/vWr7anAf6J8AJ6yPIXbA9+sDj64RDhBlSALdRfGrSbs4EIx2RcgAE+pULa7G7BplMxf025S+76kGID41S9FHLy0C/IyDHhSKz+LXgn7+c8wpj0qbun4exX63SwSRUi48fWTKX+MLjXkPiDszIYp8xZep6e2Hv4CVooFVkEqH9mrK+W7JFjwmPGp3nxy4P32cB92jKmdZ/WnusHuExrhzdpflPYPnb628cWGMkfRmwvZdpS+B1EuAe/VF3DmPJn7o84h7GABTb3+BjdzSS/xbeFFhr4GfoEw6pvvQPrF8ev9x3gB0sPfshfgtpAhPwLrmduXIQbUPHx9Y//nEPAbr5fBD5nhRMO592llvdU75+GRa85Z1HwwqCxs9WpOea/agfrCD+lsT5fj/0GLqCWsUNtPHFtDd8r9/A92Et/Yd7AAM8t97tbWNQznSN/brxDhB6y3qTJdTak0TOp4fF1/iWfaew5zmee770h1fdHA/nskbnqH1+f/gmjd8y9Sz5jZN4Xa6bftOzPZerAntEvjblXyfxhCMxa2CcYXkVT5/Mwd+DPbAs/gO95UT34RXIPq77RDqxfHL/uB/9PrhcTPeMW1M3T8Pjqh4QfDpfJ5i/BAbTXusfwt9o4szb+U+vUPTczB/zLjK92nbpvnT+29mzn1vWDvk35ftD3MID1HFWECycvIM8+gL+AHH+EDnag7SXkni+pa4rb15+gBxWggR4G+JLUc9h78Offu6nvoAftqn98fXqf7JlvIcBb+NYVaIDv5wg92BPHOb1Pzl8Zm4nATbJn/8C6h0+pgc2atGFk9Ln73nAu/hx8DwOs+sY6sH5x/Lof+A3XewcReriA+zRneJRfLo3ZPC0fY/dpXg53LHK+NT5XDelgYcEBp2L8UM8a8uQVRp/JsV6HdK7/Kc6nrYUBzvlwd88tLNmfsFFZo9y7Z/0P+Aku4RqeUwPFwsKCOc4zniLje4iwAdfO1c9Pw+9ec/0t1uF3nj8ujFHlc3yyvOyrP/8/wCZtExnfprnDHdyDXxr20IDqH1+/3ZfA1Ttw/DtcwxLlPvvF65h2KWDP2Kf5awzuLfmOLXPP7/3/Aqu+sQ786Ru777d23YELy3egHO8eZ/9+6dP0glHU2C/BX59cH/7WMi1HhwZrO+p5eWO+33bBVnEiJteY8pdpDYsWNvDculhQMN+zL2Jznl/UhsJeT6fO/EsKzLXrvHJ9YCG17jEMlbFNtivGAM8pz+x94oKi/hyou6fhpNefiXafJmW9YfSuN2ldDtm2LY0T8xyTc8qwTbkYmef7jLiOmnoirB8TDH/4ktIXPvdyPcC3rI7L27fv4fqERhj/lyMM+CXH+cX0U8k7tXAxs6H+GwiwhVXfWAfWL45f/wP3bxQi+AMurkvdsbgHfyHIAD3UukmGq9pRrQPrHVjrNdSzqfd5AwHmNHWXfFdrzCng3IFx7vnc8m/n5rTBmWPuikDt6tiZ/JumMd0k41R/ck5kEqCHJfI8P4Lns2/PqX0q5rOYU8AZoYcBTpW98R72LkCEbGP6O92xMtZntPmd54+L3Ou+cJmr/vo0jL4GrHHUs8x4Q5j7eB9x3kOpX1gEiLCFn+FbVsPlA7yFHk7RQPAxcr0c5zP5lPK96Ht2Tr8m52YuaPWtHVg78GV2IHLsB7hNox/8td5jOMBvsKudxbpjbq2rwlZO/RCZ26eMzfPAxJq7bCjGA/OuWC+dXhJoTc8y9cF2lWK889ge75PfuCnlmGYk4IBNztGepAcw/x1MaYfDOMdSkcWYvYy5SjHGNaUjzTtGfcaNKWA8gDHOS3Us9E3pGod5F1MBE/aI3Tyf75jcV/+bMSe2AAcwxvm5yufPzz/OFPKs7rebiblKMe1ITJd8YcSnyfeH9aWBc+Qev8EtOK8VMFhfv2OAMR0wSq2IwbwGagUM+na1o1pH1mM1OuyHKtbllL0Otaaxp8g+2K+XkveRMTUYPbPjnFqcxgUo1bHQPqcc82YiKGA/gHU2UOqCRQvb0rjO1w6sHfjyOuCHnD/k/rCPKf9yMyaOBSRbYLSGcTuIEBLWyL6W+VIFAnO9Osd6XW1cuN4TZ11rNOAHWYALsKa+FuyN61obDOYat4MIIdEw+stD3zWMSb+1IwRw/6XaE2jtCNawlucOiYZRmzEH8Ky1sn+HI0IAz3AJHVi3BWsYE6Cs4/oA2R+Zh4Q1sq9lXqvDoH9K7qPfM5R7TsVn+5bJA1jfeYAy37V1jdlBhJC4ZMy+lvnHKJLsHmLNY7omIMc2zPPZL5h3yec4pohxLFe7OfYw12+Yn6NLktxDnI/JffS755QOOKTWFoO578F5gA2oAPp2MKeI07gGSnUsDqUhzafsdag1jT1F5hygXUhD3Cmytoypwej+jnNqcRoXoFTHQvucAs4DGLeDCCHRMGZfy7zWHoN5DaxaO7B24AvuwJ6z+8N8M3GHkPx+IBxTIGAP1qvxl8slnKJAsHV2I0kHbN2IfampJdAaDxXaLkDp6x5nf3wJmPZQ57s+dlf7UObtWC/VnkBzVYAOylrO3f8aNjCmgHEPdZ7rDgKoA+SYoKFQYL6H7C9H83IPmf5OHSv9c4o4reeXiVNkbfMysUoOrPeQ/eV4iz3Cc6ijiLXbhcUa4g5Qnse5z7GFOTU4x3I77FvQby3Hc+R7yHyx3pj2GI/tcSBGxmTvzc/EFBSSbZfWU0NMcU0V0LE+VDaXU/Y69CHF1vapdcBhzil4llN0IFjG1GB0b8c5tTiNC1CqY6H9mAIBOdb4Ep9lA2PaYzS2gVVfaQf+4yu913qtl+9AYIuMu90lnH9uihwopEOV5/SXpB+C/h+RXCb/2LDBaGxIzoHxDu7TemowR9QNHIt/DJx4CdittQHr9GlkmFXAeywvEjMkGP6ggCXX0HmXcP4aumDTDQzgWe6hlv4thOQwTp5L/lKN8BcYYKkigZ5NBvBM97BEkaCQAs2TL0kXHHYDA3j2e1j1eXcgcLwt+NxUDwOsWjuwdmDtwFfVgcht/LA7poaA9U/Hx7q0+usOBAy+b/zyuGrtwNqBtQNrB9YOrB34gjvgn4z9pX44cgfjjDE2wKq1A0s7cEWg75uLpQlr3NqBtQNrB9YOrB1YO/D5duCao/mLfTdxxIC9A2NaWLV2YGkHAoH+d4mHpQlr3NqBtQNrB9YOrB1YO/D5dyB/efQX/HvYJTpGf/E/gDGr1g4s6YDvmwP4vvH9E2DV2oG1A2sH1g6sHVg78BV1IHKXPdyCv/QzO+YRVq0dWNqBSwI78L0TYNXagbUDawe+yQ78f0D1WTqDGgAGAAAAAElFTkSuQmCC" alt="ApplicationImage">
                    </div>
                </div>
            </body>
        </html>
    """

    st.markdown(html, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .stButton>button {
        border: none;
        border-radius: 25px;
        cursor: pointer;
        margin-left:0px;
        display: flex;
        width: 100%;
        border: none;
        margin-top: 150px;
        background-color: #e53e3e;
        color: white;
        padding: 14px 28px;
        font-size: 36px;
        cursor: pointer;
        text-align: center;
            }
        </style>
        """,unsafe_allow_html=True
        )
    
    if st.button('Done'):
        pass
        # st.session_state.checkout_step = 11
        # st.experimental_rerun()


if st.session_state.checkout_step == 0:
    checkout_page()
    # add_website_and_bank_account()

if st.session_state.checkout_step == 1:
    transition_page()

if st.session_state.checkout_step == 20:
    signup_page()

if st.session_state.checkout_step == 2:
    docunent_upload_page()

if st.session_state.checkout_step == 7:
    add_website_and_bank_account()
    
if st.session_state.checkout_step == 8:
    nafath_check()

if st.session_state.checkout_step == 9:
    show_split()

if st.session_state.checkout_step == 10:
    add_repayment()

if st.session_state.checkout_step == 11:
    application_submitted()

