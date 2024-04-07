from django import template

register = template.Library()

CENSOR_WORD = [
    'спорт', 'отзывов'
]

punctuation = '?!.,:;'

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

@register.filter()
def censeroid(value):
    try:
        set_text = value.split() #список слов до преобразовани, для вставки в итоговый текст
        str = '' #Строка которая будет выводить итоговый текст
        text = value.lower() #преобразование в нижний регистр всех слов
        clean_text = "".join(char for char in text if char not in punctuation)
        text = clean_text.split() #строка в список слов
        ind = 0 #переменная для перемещения по set_text
        for word in text:
            if word in CENSOR_WORD:
                cen_word = '' # отдельная строка для нецензурных слов, чтобы записать их через ***
                for i in range(0, len(word)):
                    if i == 0: #вставить первую букву слова с учетом регистра если была большая
                        cen_word += set_text[text.index(word)][0]
                    elif len(word) < len(set_text[text.index(word)]) and i == (len(word)-1): #вставить символы, которые находятся после звездочек
                        cen_word += set_text[text.index(word)][len(word)::] #это могут быть знаки препинания, но попадают и остальные буквы например спорт - *****ивный
                    else:
                        cen_word += '*' #втсавляем звезду вместо буквы
                str += cen_word + ' '#добаляем в строку зацензуренное слово
                ind += 1
            else:
                str = str + set_text[ind] + " " #собираем всю строку
                ind += 1
        return str #и возвращаем ее
    except AttributeError:
        return value #возвращаем если введена не строка, а int
