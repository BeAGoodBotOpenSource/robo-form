import io

from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS
from PyPDF2 import PdfReader

from config import debug_status, whitelist_origins
from debug import debug_only
from gpt_utils import get_form_inputs, sanitize_html_form

app = Flask(__name__)
CORS(app, origins=whitelist_origins)

# The following functions are defined to avoid errors in this file, but when working on them,
# you should start on a new .py file and implement each function in there. Feel free to implement
# internal helper functions within those files. Then import them in this file, and call them in
# autofill().


# def sanitize_html(html_input):
#     # Remove leading/trailing white space and control characters
#     soup = BeautifulSoup(html_input.strip(), "lxml")
#     inputs = []

#     for input_field in soup.find_all(["input", "textarea"]):
#         field_type = input_field.get("type")

#         # Check if the input field is of type 'text' or a 'textarea'
#         if field_type == "text" or input_field.name == "textarea":
#             field_id = input_field.get("id")  # Get the id of the input field
#             name = input_field.get("name")
#             class_name = input_field.get("class")
#             label = input_field.find_previous("label")
#             placeholder = input_field.get("placeholder")

#             inputs.append(
#                 {
#                     "id": field_id,  # Add the id to the dictionary
#                     "name": name,
#                     "type": field_type,
#                     "class": class_name,
#                     "label": str(label),
#                     "placeholder": placeholder,
#                 }
#             )

#     return inputs


def sanitize_cv(cv_text):
    # Remove leading/trailing white space and control characters
    sanitized_cv = cv_text.strip()
    print(sanitized_cv)
    return sanitized_cv


def call_claude(clean_html, clean_cv):
    pass


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(io.BytesIO(pdf_file.read()))

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text


# Just for testing connection with backend; debugging purpose only
@app.route("/test", methods=["GET"])
@debug_only
def hello():
    return "Hello!"


@app.route("/autofill", methods=["POST"])
def autofill():
    # Get the PDF and HTML from the request
    pdf_file = request.files.get("pdf")
    html_text = request.form.get("html")

    pdf_text = extract_text_from_pdf(pdf_file)

    bs_obj = BeautifulSoup(html_text.strip(), "lxml")
    clean_html = sanitize_html_form(str(bs_obj))
    clean_pdf_text = sanitize_cv(pdf_text)

    # # Call ChatGPT (Needs testing)
    # form_fields = get_form_fields_gpt(clean_html, clean_pdf_text)
    # autofilled_dict = autofill_gpt(form_fields, clean_pdf_text, clean_html)
    # result_dict = gpt_filled_dic(autofilled_dict)

    result_dict = get_form_inputs(clean_html, clean_pdf_text)

    # For now, return an empty dictionary
    return result_dict, 200


if __name__ == "__main__":
    app.run(debug=debug_status, port=4000)  # toggled for prod
