import xml.etree.ElementTree as ET
from app import run_edirect_command

def extract_pubmed_info(result):
    root = ET.fromstring(result)
    count = root.find('Count').text
    ids = [elem.text for elem in root.findall('.//Id')]
    links = ['https://www.ncbi.nlm.nih.gov/pubmed/{}'.format(id) for id in ids]
    return count, links

def search_pubmed(query):
    result = run_edirect_command(["esearch", "-db", "pubmed", "-query", query])
    count, links = extract_pubmed_info(result)
    return count, links