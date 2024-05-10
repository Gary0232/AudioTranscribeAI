from PyDictionary import PyDictionary
dictionary = PyDictionary()

def get_local_definition(noun):
    try:
        meaning = dictionary.meaning(noun)
        if meaning:
            all_definitions = []
            for pos, definitions in meaning.items():
                for definition in definitions:
                    all_definitions.append(f"{pos}: {definition}")
            return "\n".join(all_definitions)
        else:
            return 'No definitions found.'
    except Exception as e:
        return f'Error retrieving definitions: {str(e)}'

if __name__ == '__main__':
    # Example usage
    keyword = "Wine"
    all_meanings = get_all_definitions(keyword)
    print(f"All meanings of '{keyword}':\n{all_meanings}")
