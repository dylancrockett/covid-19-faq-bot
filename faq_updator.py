from bs4 import BeautifulSoup
import requests
import json
import os


def get_faq():
    url = "https://www.cdc.gov/coronavirus/2019-ncov/faq.html"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # parse out each FAQ section
    faq_sections = soup.find_all("div", class_="accordion indicator-plus accordion-white mb-3")

    # store faq questions and responses
    faq_dict = {}

    for faq_section in faq_sections:
        # parse out each question in the FAQ section
        faq_questions = faq_section.find_all("div", class_="card")

        for faq_question in faq_questions:
            # parse out the question and the answer
            question = faq_question.find("span")
            response = faq_question.find("div", class_="card-body")

            # save the faq question and response if they exist
            if question is not None and response is not None:
                faq_dict[question.text] = response.text

    # remove the old faq
    os.remove("faq.json")

    # save the new faq
    with open('faq.json', 'w') as fp:
        json.dump(faq_dict, fp, indent=4)

    # return the faq
    return faq_dict
