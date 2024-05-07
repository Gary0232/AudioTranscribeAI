from PyDictionary import PyDictionary
dictionary = PyDictionary()
def get_local_definition(noun):
    try:
        meaning = dictionary.meaning(noun)
        if meaning:
            # Extracting the first definition of the first meaning type
            first_meaning_type = next(iter(meaning.values()))
            return first_meaning_type[0]
        else:
            return 'No definition found.'
    except Exception as e:
        return f'Error retrieving definition: {str(e)}'