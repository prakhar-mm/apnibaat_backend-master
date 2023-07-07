import json
from googletrans import Translator

def translate_json(input_json):
    languages = {
        'Hindi': 'hi',
        'Malayalam': 'ml',
        'Kannada': 'kn',
        'Marathi': 'mr',
        'Tamil': 'ta',
        'Telugu': 'te'
    }

    translator = Translator(service_urls=['translate.google.com'])

    for language, code in languages.items():
        translated_json = input_json.copy()
        translated_json['title'] = translator.translate(input_json['title'], dest=code).text
        translated_json['content'] = translator.translate(input_json['content'], dest=code).text

        output_file = f"translated_{language.lower()}.json"
        with open(output_file, 'w') as f:
            json.dump(translated_json, f, indent=4)
        print(f"Translated JSON for {language} saved as {output_file}")

# Example usage with the provided input JSON
input_json = {
    "title": "How to do a startup",
    "summary": "...",
    # Rest of the fields
}

translate_json(input_json)
