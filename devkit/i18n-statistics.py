import matplotlib.pyplot as plt
import pathlib


lproj_base = pathlib.Path('res')

available_languages = [
    'en',
    'es',
    'fr',
    'ko',
    'vi',
    'zh-Hans',
    'zh-Hant-HK',
    'zh-Hant-TW',
]

def get_lproj_path(lang) -> pathlib.Path:
    return lproj_base / f'{lang}.lproj'

def get_lproj_strings_paths(lang) -> [pathlib.Path]:
    return [
        get_lproj_path(lang) / 'Localizable.strings',
        get_lproj_path(lang) / 'InfoPlist.strings',
    ]

def get_lproj_strings_count(lang) -> tuple[int, int]:
    all_lines = []
    for strings_path in get_lproj_strings_paths(lang):
        if strings_path.exists():
            with open(strings_path, 'r') as f:
                all_lines.extend(f.readlines())
    todo_count = 0
    for line in all_lines:
        if line.find('/* TODO */') != -1 or line.find('/* Translated with ') != -1:
            todo_count += 1
    return int((len(all_lines) + 1) / 3), todo_count

if __name__ == '__main__':
    x_labels = available_languages
    y_values = []
    for lang in available_languages:
        total, todo = get_lproj_strings_count(lang)
        percent = (total - todo) / total
        y_values.append((lang, percent, total - todo, total))
        print(f'{lang}: {total - todo}/{total} translated, {percent * 100:.2f}%')
    y_values.sort(key=lambda x: 1.0 - x[1])
    y_values.reverse()
    plt.figure().set_figwidth(15)
    plt.barh([x[0] for x in y_values], [x[2] for x in y_values])
    plt.xlabel('Strings Translated')
    plt.ylabel('Language')
    plt.title('Translation Progress')
    plt.savefig(lproj_base / 'stats.png')