import json
import re
from string import punctuation
from bs4 import BeautifulSoup
import pymorphy2
import requests

PUNCT = punctuation + '«»–“”—…'
MORPH = pymorphy2.MorphAnalyzer()


def get_words_list(text):
    words_list = [word.strip(PUNCT) for word in text.lower().split()]
    words_list = [word for word in words_list if re.search(r'[а-яёА-ЯЁa-zA-Z]', word)]
    return words_list


def get_freq_dict(words_list):
    freq_dict = {}
    for word in words_list:
        freq_dict[word] = freq_dict.get(word, 0) + 1
    freq_dict = sorted(freq_dict.items(), reverse=True, key=lambda x: x[1])
    return freq_dict


def get_lemmatized_text(words_list):
    lemmatized_text = [MORPH.parse(word)[0].normal_form for word in words_list]
    return lemmatized_text


def get_text_from_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    soup.find('form').decompose()
    text = soup.text
    return text


def get_unique_words(words_list):
    unique_words = list(set(words_list))
    unique_words.sort()
    return unique_words


def main():
    with open('dom.txt', encoding='utf-8-sig') as f:
        text = f.read()
    words_list = get_words_list(text)
    freq_dict = get_freq_dict(words_list)
    with open('freq_dict.csv', 'w', encoding='utf-8') as fw:
        for word, freq in freq_dict:
            fw.write(f'{word},{freq}\n')
    lemmatized_text = get_lemmatized_text(words_list)
    o_lemmas = [word for word in lemmatized_text if word.count('о') == 2]
    with open('o_lemmas.txt', 'w', encoding='utf-8') as fw:
        fw.write('\n'.join(o_lemmas))
    another_text = get_text_from_url('http://lib.ru/POEZIQ/PESSOA/lirika.txt')
    unique_words = get_unique_words(get_words_list(another_text))
    with open('dict.json', 'w') as fw:
        json.dump(unique_words, fw)


if __name__ == '__main__':
    main()
