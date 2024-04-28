import logging

import httpx
import nh3
import openai
from PyPDF2 import PdfReader

import config

ALLOWED_TAGS = {
    "a",
    "div",
    "h1",
    "h2",
    "h3",
    "strong",
    "em",
    "p",
    "ul",
    "ol",
    "li",
    "br",
    "sub",
    "sup",
    "hr",
    "input",
    "label",
    "table",
    "textarea",
    "tr",
    "td",
    "th",
}
ALLOWED_ATTRIBUTES = {
    "a": {"href", "name", "target", "title", "id"},
    "input": {"type", "id", "name"},
    "label": {"for"},
    "div": {"type", "role", "class", "id"},
    "textarea": {"type", "role", "class", "id"},
}


def get_form_fields_gpt(clean_html, clean_pdf_text):
    logging.info(f"Clean_html: {clean_html}")
    logging.info(f"clean_pdf_text: {clean_pdf_text}")
    query_1 = (
        f"Given this html code: {clean_html} and cleaned PDF text: {clean_pdf_text}"
        ", return the form fields in a list of comma separated values"
    )

    logging.info("Starting GPT API call via model")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=[{"role": "user", "content": query_1}]
    )
    form_fields = response.choices[0].message["content"]

    logging.info("Result of first query. form_fields:")
    logging.info(form_fields)
    return form_fields


def autofill_gpt(form_fields, clean_pdf_text, clean_html):
    query_1 = (
        f"Given these html form fields: {form_fields} and cleaned PDF text: {clean_pdf_text}"
        ", return a dictionary with the id as key and generated value from clean pdf text"
    )

    logging.info("Starting GPT API call 2 via model")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=[{"role": "user", "content": query_1}]
    )
    autofilled_dict = response.choices[0].message["content"]

    logging.info("Result of 2nd query. autofilled_dict:")
    print(autofilled_dict)
    return autofilled_dict


def gpt_filled_dic(gpt_response_with_text):
    query_1 = f"Given this combination of text and a dictionary: {gpt_response_with_text}. results in json code only."

    logging.info("Starting GPT API call 3 via model")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=[{"role": "user", "content": query_1}]
    )
    cleaned_dict = response.choices[0].message["content"]

    logging.info("Result of 3rd query. cleaned_dict:")
    print(cleaned_dict)
    return cleaned_dict


def sanitize_html_form(html_string):
    return nh3.clean(html_string, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)


def get_form_inputs(clean_html, clean_pdf_text):
    logging.debug("Preparing to compare pdf with html form.")

    with open("templates/prompt_fill_form.md", "r") as f:
        query = f.read()

    query = query.format(clean_html=clean_html, clean_pdf_text=clean_pdf_text)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.5,
        messages=[{"role": "user", "content": query}],
    )
    response_text = response.choices[0].message["content"]
    # logging.debug("response: %s", response_text)

    if logging.DEBUG >= logging.root.level:
        print(response_text)
    return response_text


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    with open("tests/test.pdf", "rb") as f:
        pdf_file = PdfReader(f)

        pdf_text = ""
        for page in pdf_file.pages:
            pdf_text += page.extract_text()

    r = httpx.get("https://forms.gle/bVtB77EK6YezTtH46", follow_redirects=True)
    r.raise_for_status()
    html_text = r.text

    clean_html = nh3.clean(html_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    inputs = get_form_inputs(clean_html, pdf_text)

    pass
