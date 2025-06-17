import re
import json
import requests

del_keys = [
    'mohseniGrading',
    'behbudiGrading',
    'thaqalaynSanad',
    'thaqalaynMatn',
    'majlisiGrading',
    'translator',
    'author'
]


def save_json(path: str, load: dict | list):
    with open(f'./static/hadith/{path}', 'w') as f:
        json.dump(load, f, indent=2, ensure_ascii=False)


def sort_dict(load: dict) -> dict:
    return dict(sorted(load.items(), key=lambda item: int(item[0])))


def remove_author_dates(book):
    book['author'] = re.sub(r"\(d\. \d+ AH\)", "", book['author'])


def restructure_book(book: dict | list) -> dict:
    bk = {}
    for hadith in book:
        category = hadith['category'] if hadith['category'] != 'Content' else 'Book'
        category_id = hadith['categoryId']
        chapter = hadith['chapter']
        chapter_id = str(hadith['chapterInCategoryId'])
        if category_id not in bk:
            bk[category_id] = {
                'category': category,
                'chapters': {}
            }
        if chapter_id not in bk[category_id]['chapters']:
            bk[category_id]['chapters'][chapter_id] = {
                'chapter': chapter,
                'hadiths': []
            }
        bk[category_id]['chapters'][chapter_id]['hadiths'].append(
            {
                'arabicText': hadith['arabicText'],
                'englishText': hadith['englishText'],
                'frenchText': hadith['frenchText'],
                'thaqalaynURL': hadith['URL'],
            }
        )
    for category in bk:
        bk[category]['chapters'] = sort_dict(bk[category]['chapters'])
    return sort_dict(bk)


def sync_books():
    print('Getting all books...')
    all_books = 'https://www.thaqalayn-api.net/api/v2/allbooks'
    books: list[dict] = requests.get(all_books).json()

    print('Saving book list to books.json')
    save_json('books.json', books)

    print('Iterating books:')
    for book in books:
        book_id: str = book['bookId']
        print(f'\tFetching {book_id}')
        whole_book: dict | list = requests.get(f'https://www.thaqalayn-api.net/api/v2/{book_id}').json()

        print('\t\tRestructuring book')
        final_book = restructure_book(whole_book)

        print('\t\tSaving book')
        save_json(f'books/{book_id}.json', final_book)


if __name__ == '__main__':
    sync_books()
