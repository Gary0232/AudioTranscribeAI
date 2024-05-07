import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from keyword_wiki_retrieval.wiki_retrieval import get_wikipedia_info
from keyword_wiki_retrieval.dictionary_retrieval import get_local_definition

# Set the custom NLTK data path
nltk_data_path = 'nltk_data'  # Relative path to your custom 'nltk_data' directory
nltk.data.path.append(nltk_data_path)

# Download necessary NLTK resources to your specified directory
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)
nltk.download('punkt', download_dir=nltk_data_path)


# Assuming 'get_wikipedia_info' is defined as you provided

# Function to read text, extract nouns, and retrieve definitions
def retrieve_information_from_text(text):

    # Tokenize and tag part of speech
    tokens = word_tokenize(text.lower())
    tagged_tokens = pos_tag(tokens)

    # Extract nouns
    nouns = [word for word, tag in tagged_tokens if
             tag.startswith('NN') and word.lower() not in stopwords.words('english')]

    # Retrieve information for each noun
    for noun in nouns:
        print(f"----------------------------Retrieving Wiki information for: {noun}------------------------------")
        # Online retrieval (Wikipedia)
        title, url, summary, images_url = get_wikipedia_info(noun)
        if url:
            print(f"Wikipedia Title: {title}")
            print(f"Wikipedia URL: {url}")
            print(f"Wikipedia Summary: {summary}")
            print(f"Wikipedia Images URL: {images_url}")
        else:
            print("No Wikipedia page found.")
        print(f"----------------------------Retrieving dictionary information for:------------------------------"
              f" {noun}---------------")
        meaning = get_local_definition(noun)
        print(f"Meaning: {meaning}")

