import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from library.models import Book, Category, Genre

def populate_database():
    print("شروع پروسه اضافه کردن داده‌های اولیه...")

    cat_fiction, _ = Category.objects.get_or_create(name="ادبیات داستانی")
    cat_nonfiction, _ = Category.objects.get_or_create(name="غیرداستانی")
    cat_science, _ = Category.objects.get_or_create(name="علمی و آموزشی")
    cat_children, _ = Category.objects.get_or_create(name="کودک و نوجوان")
    print("دسته‌بندی‌ها ساخته یا بارگذاری شدند.")

    genre_fantasy, _ = Genre.objects.get_or_create(name="فانتزی")
    genre_adventure, _ = Genre.objects.get_or_create(name="ماجراجویی")
    genre_scifi, _ = Genre.objects.get_or_create(name="علمی-تخیلی")
    genre_dystopian, _ = Genre.objects.get_or_create(name="دیستوپیایی")
    genre_history, _ = Genre.objects.get_or_create(name="تاریخ")
    genre_science, _ = Genre.objects.get_or_create(name="علم")
    genre_philosophy, _ = Genre.objects.get_or_create(name="فلسفی")
    print("ژانرها ساخته یا بارگذاری شدند.")

    books_data = [
        {
            "title": "ارباب حلقه‌ها: یاران حلقه", "author": "جی. آر. آر. تالکین", "year": 1954,
            "price": 550000.00, "category": cat_fiction, "genres": [genre_fantasy, genre_adventure]
        },
        {
            "title": "1984", "author": "جورج اورول", "year": 1949,
            "price": 320000.00, "category": cat_fiction, "genres": [genre_scifi, genre_dystopian]
        },
        {
            "title": "انسان خردمند: تاریخ مختصر بشر", "author": "یووال نوح هراری", "year": 2011,
            "price": 480000.00, "category": cat_nonfiction, "genres": [genre_history, genre_science]
        },
        {
            "title": "شازده کوچولو", "author": "آنتوان دو سنت-اگزوپری", "year": 1943,
            "price": 180000.00, "category": cat_children, "genres": [genre_fantasy, genre_philosophy]
        },
        {
            "title": "تاریخچه مختصر زمان", "author": "استیون هاوکینگ", "year": 1988,
            "price": 410000.00, "category": cat_science, "genres": [genre_science]
        },
    ]

    for book_info in books_data:
        genres = book_info.pop('genres')
        book, created = Book.objects.get_or_create(
            title=book_info['title'],
            author=book_info['author'],
            defaults={
                'publication_year': book_info['year'],
                'price': book_info['price'],
                'category': book_info['category']
            }
        )
        if created:
            book.genres.set(genres)
            print(f"کتاب '{book.title}' با موفقیت اضافه شد.")
        else:
            print(f"کتاب '{book.title}' از قبل وجود داشت.")

    print("عملیات با موفقیت به پایان رسید! ✨")

if __name__ == '__main__':
    populate_database()