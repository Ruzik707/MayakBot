import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path


def find_poems_key(obj):
    """Рекурсивно ищет ключ 'poems' в глубоком JSON-словаре"""
    if isinstance(obj, dict):
        if 'poems' in obj:
            return obj['poems']
        for value in obj.values():
            result = find_poems_key(value)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_poems_key(item)
            if result is not None:
                return result
    return None


def process_poem_to_chunks(poem):
    title = poem.get('title', 'Без названия')
    name_id = poem.get('name', 'unknown')

    tags = [tag.get('title') for tag in poem.get('tags', []) if 'title' in tag]

    full_text = poem.get('text', '')

    stanzas = [s.strip() for s in full_text.split('\n\n') if s.strip()]

    chunks = []
    for i, stanza in enumerate(stanzas):
        chunk = {
            "chunk_id": f"{name_id}_{i}",
            "text": stanza,
            "metadata": {
                "title": title,
                "tags": tags,
                "chunk_index": i,
                "total_chunks": len(stanzas)
            }
        }
        chunks.append(chunk)

    return chunks


def write_in_json(filename, chunks):
    with open(filename, 'a', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

def pars_all_page_and_all_poems(pages, filename='mayakovsky-corpus.jsonl'):
    data_dir = Path(__file__).parent.parent.parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    filepath = data_dir / filename

    if filepath.exists():
        filepath.unlink()

    total_chunks_saved = 0

    for page in range(1, pages + 1):
        url = f"https://www.culture.ru/literature/poems/author-vladimir-mayakovskii?page={page}"
        print(f'Парсинг страницы {page}')

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        next_data_script = soup.find('script', id='__NEXT_DATA__')

        if next_data_script:
            data = json.loads(next_data_script.string)
            poems_list = find_poems_key(data)

            if poems_list:
                chunks = []
                for poem in poems_list:
                    chunks.extend(process_poem_to_chunks(poem))

                write_in_json(filepath, chunks)
                total_chunks_saved += len(chunks)
                print(f'Найдено {len(poems_list)} произведений. Добавлено {len(chunks)} чанков.')
        else:
            print(f'Ошибка в __NEXT_DATA__')

    print(f'Готово! Сохранено {total_chunks_saved} чанков')
    print(f'Файл сохранен по пути {filepath}')


def main():
    pars_all_page_and_all_poems(26)

if __name__ == '__main__':
    main()