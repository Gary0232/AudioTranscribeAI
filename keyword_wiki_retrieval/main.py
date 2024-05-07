import keyword_wiki_retrieval
from keyword_wiki_retrieval.keyword import retrieve_information_from_text

# query = "Wine"
text_file_path = "./text/exampleDoc"
with open(text_file_path, 'r') as file:
    query = file.read()

retrieve_information_from_text(query)