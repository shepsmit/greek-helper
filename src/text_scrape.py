
from backend.text_scraper import TextScraper

book_list_nt = {
"Matthew":28,
"Mark":16,
"Luke":24,
"John":21,
"Acts":28,
"Romans":16,
"1 Corinthians":16,
"2 Corinthians":13,
"Galatians":6,
"Ephesians":6,
"Philippians":4,
"Colossians":4,
"1 Thessalonians":5,
"2 Thessalonians":3,
"1 Timothy":6,
"2 Timothy":4,
"Titus":3,
"Philemon":1,
"Hebrews":13,
"James":5,
"1 Peter":5,
"2 Peter":3,
"1 John":5,
"2 John":1,
"3 John":1,
"Jude":1,
"Revelation":22,
}

t = TextScraper()

for book in book_list_nt.keys():
    b_name = book.lower().replace(" ","-")
    for i in range(book_list_nt[book],book_list_nt[book]+1):
        # print(f"{b_name} {i}")
        t.new_chapter(b_name,i)


