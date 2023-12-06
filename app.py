import os
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords           
import zipfile                              # for dealing with zip file
import re                                   # regular expressions module  

# Extract the documents data from 'archive.zip'
def extract_documents_data(zip_path):
    extract_path = 'C:\\Users\\yasee\\Downloads\\extracted_data'

    # Create the extraction folder if it doesn't exist
    os.makedirs(extract_path, exist_ok=True)

    # Extract 'archive.zip' folder
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Read and print the content of each text file
    documents = []
    for filename in os.listdir(extract_path):
        if filename.endswith(".sgm"):
            file_path = os.path.join(extract_path, filename)
            with open(file_path, 'r') as file:
                documents.append(file.read())
                
    return documents

# Extract the articles from each document, then return them as a list
def extract_articles(content):
    # Find the index of all occurrences of <REUTERS and </REUTERS> tags
    reuters_start_indices = [i.start() for i in re.finditer(r'<REUTERS', content)]
    reuters_end_indices = [i.start() for i in re.finditer(r'</REUTERS>', content)]
    print(reuters_end_indices)

    # Extract sections between <REUTERS and </REUTERS> 
    articles = []
    for start_index, end_index in zip(reuters_start_indices, reuters_end_indices):
        article = content[start_index:end_index + len('</REUTERS>')]
        articles.append(article)

    return articles


# Your zip file path
zip_file_path = r'C:\\Users\\yasee\Downloads\\archive (1).zip'
extract_documents_data(zip_file_path)
