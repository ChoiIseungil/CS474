# pip install googletrans==4.0.0-rc1
from googletrans import Translator

translator = Translator()
result = translator.translate('안녕하세요.')
print(result.text)
