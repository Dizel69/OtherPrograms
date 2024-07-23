from googletrans import Translator

translator = Translator()
while True:
    input_text = input('Введите текст, который нужно перевести: ')
    result = translator.translate(input_text,
                                  src='ru',
                                  dest='en')
    print(result.text)
