import requests

from bs4 import BeautifulSoup

langs = {
    'fr': 'french',
    'en': 'english',
}
dirs = {
    'fr': f'{langs["en"]}-{langs["fr"]}',
    'en': f'{langs["fr"]}-{langs["en"]}',
}

target_lang = input(
    'Type "en" if you want to translate from French into English, or "fr" if '
    'you want to translate from English into French:\n'
)
word = input('Type the word you want to translate:\n')
# target_lang = 'fr'
# word = 'hello'
source_lang = [lg for lg in langs.keys() if lg != target_lang][0]
print(f'You chose "{target_lang}" as a language to translate "{word}".')

url = f'https://context.reverso.net/translation/{dirs[target_lang]}/{word}'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(f'{r.status_code} {r.reason}')

if r.ok:
    soup = BeautifulSoup(r.content, 'html.parser')
    limit = 5
    translations = [t.text for i, t in enumerate(soup.find_all('span', {
        'class': 'display-term'
    })) if i < limit]
    examples = {
        'fr': [],
        'en': [],
    }
    for i, t in enumerate(soup.find_all('div', {'class': 'ltr'})):
        if i > limit * 2:
            break
        if t.text.strip() == '':
            continue

        example = t.text.strip()

        if i % 2:
            examples[target_lang].append(example)
        else:
            examples[source_lang].append(example)

    # print(examples)

    print(f'\n{langs[target_lang].capitalize()} Translations:')
    print(*translations, sep='\n')
    print(f'\n{langs[target_lang].capitalize()} Examples:')
    print(*['\n'.join([
        examples[source_lang][i],
        examples[target_lang][i],
    ]) for i in range(0, len(examples[target_lang]))], sep='\n\n')
