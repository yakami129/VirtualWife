from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate(
    source_language='en',
    target_language='de',
    timeout=10
)
result = translator.translate('This is an example.')

print(result) 
# Output: Dies ist ein Beispiel.