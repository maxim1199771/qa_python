import collection
import pytest

from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

@pytest.fixture
def collection():
    collection = BooksCollector()
    return collection

'''Для корректного отображения аргументов в параметризированном тесте'''
def pytest_make_parametrize_id(val):
    return repr(val)

@pytest.fixture
def collection_five_books(collection):
    collect = collection
    books = ['Властелин колец', 'Король лев', 'Чужой', 'Сон в летнюю ночь', 'Молчание ягнят']
    genre = ['Фантастика', 'Мультфильмы', 'Ужасы', 'Комедии', 'Детективы']
    for i in range(5):
        collect.add_new_book(books[i])

    for i in range(5):
        collect.set_book_genre(books[i], genre[i])

    return collect


class TestBooksCollector:
    '''Проверка добавления трех книг в словарь books_genre'''

    def test_add_new_book_adding_three_books_success(self, collection):
        books = ['Ромео и Джульетта', 'Мастер и Маргарита', 'Король Лев']
        for book in books:
            collection.add_new_book(book)
        assert len(collection.get_books_genre()) == 3

    '''Проверка установления жанра по умолчанию в добавленной книге'''

    def test_add_new_book_check_genre_success(self, collection):
        first_book = 'Ромео и Джульетта'
        collection.add_new_book(first_book)
        assert collection.get_book_genre(first_book) == ''

    '''Негативная проверка добавления книг с именем 0 и больше 40 символов'''

    @pytest.mark.parametrize('book',
                             ['', 'МастерМастерМастерМастерМастерМастерМастер']
                             )
    def test_add_new_book_add_incorrect_name_not_added(self, book, collection):
        collection.add_new_book(book)
        assert len(collection.get_books_genre()) == 0

    '''Негативная проверка повторного добавления одинаковых книг'''

    def test_add_new_book_add_double_books_not_added(self, collection):
        books = ['Война и мир', 'Война и мир']
        for book in books:
            collection.add_new_book(book)
        assert len(collection.get_books_genre()) == 1

    '''Проверка добавления жанра из списка genre книге из списка books_genre'''

    def test_set_book_genre_added(self, collection):
        first_book = 'Властелин колец'
        genre = 'Фантастика'
        collection.add_new_book(first_book)
        collection.set_book_genre(first_book, genre)
        assert collection.get_book_genre(first_book) == genre

    '''Проверка изменения жанра из списка genre книге из списка books_genre'''

    def test_set_book_genre_changed(self, collection):
        first_book = 'Властелин колец'
        genre = 'Фантастика'
        other_genre = 'Детективы'
        collection.add_new_book(first_book)
        collection.set_book_genre(first_book, genre)
        collection.set_book_genre(first_book, other_genre)
        assert collection.get_book_genre(first_book) == other_genre

    '''Негативная проверка добавления жанра не из списка genre книге из списка books_genre'''

    def test_set_book_genre_missing_genre_not_added(self, collection):
        first_book = 'Властелин колец'
        missing_genre = 'Приключения'
        collection.add_new_book(first_book)
        collection.set_book_genre(first_book, missing_genre)
        assert collection.get_book_genre(first_book) == ''

    '''Проверка вывода книги определенного жанра'''

    def test_get_books_with_specific_genre_success(self, collection_five_books):
        assert collection_five_books.get_books_with_specific_genre('Ужасы') == ['Чужой']

    '''Негативная проверка вывода отсутствующей книги определенного жанра'''

    def test_get_books_with_specific_genre_missing_book(self, collection_five_books):
        assert len(collection_five_books.get_books_with_specific_genre('Приключения')) == 0

    '''Проверка вывода списка книг с жанром для детей'''

    def test_get_books_for_children_success(self, collection_five_books):
        children_books = collection_five_books.get_books_for_children()
        assert len(children_books) == 3 and children_books == ['Властелин колец', 'Король лев', 'Сон в летнюю ночь']

    '''Проверка добавления книги из списка books_genre в избранное'''

    def test_add_book_in_favorites_add_one_book_added(self, collection):
        first_book = 'Хоббит'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        favorites = collection.get_list_of_favorites_books()
        assert len(favorites) == 1 and favorites[0] == first_book

    '''Негативная проверка добавления книги не из списка books_genre в избранное'''

    def test_add_book_in_favorites_add_missing_book_not_added(self, collection):
        first_book = 'Властелин колец'
        collection.add_book_in_favorites(first_book)
        assert len(collection.get_list_of_favorites_books()) == 0

    '''Негативная проверка повторного добавления книги в избранное'''

    def test_add_book_in_favorites_add_double_books_not_added(self, collection):
        first_book = 'Властелин колец'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        collection.add_book_in_favorites(first_book)
        favorites = collection.get_list_of_favorites_books()
        assert len(favorites) == 1 and favorites[0] == first_book

    '''Проверка удаления книги из списка избранное'''

    def test_delete_book_from_favorites_book_deleted(self, collection):
        first_book = 'Властелин колец'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        collection.delete_book_from_favorites(first_book)
        assert len(collection.get_list_of_favorites_books()) == 0

    '''Негативная проверка удаления не добавленной книги в favorites'''

    def test_delete_book_from_favorites_missing_book_not_deleted(self, collection):
        first_book = 'Хоббит'
        second_book = 'Властелин колец'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        collection.delete_book_from_favorites(second_book)
        favorites = collection.get_list_of_favorites_books()
        assert len(favorites) == 1 and favorites[0] == first_book