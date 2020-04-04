from sqlalchemy import and_, func
from models import create_all_tables, delete_all_tables
from models import User, Post, Tag, Category
from settings.database import Session


def create_base_data():
    """Added base data to database"""
    session = Session()

    user = User(username='test user')
    user2 = User(username='test user2')
    session.add(user)
    session.add(user2)

    tag1 = Tag(name='web')
    tag2 = Tag(name='python')
    tag3 = Tag(name='framework')
    tag4 = Tag(name='css')
    tag5 = Tag(name='html')
    session.add(tag1)
    session.add(tag2)
    session.add(tag3)
    session.flush(session)

    post1 = Post(
        published_by=user.id,
        title='Перестаньте использовать !important. Помогаем разобраться с каскадом CSS',
        text='Когда CSS-правило не работает, многие разработчики хотят добавить !important и забыть о проблеме.'
             'Рассказываем, почему так делать не стоит и как правильно работать с CSS.',
        is_published=False)
    post2 = Post(
        published_by=user2.id,
        title='Mastering Django: Core: The Complete Guide to Django 1.8 LTS 1st Edition',
        text='Mastering Django: Core is a completely revised and updated version of the original Django Book,'
             'written by Adrian Holovaty and Jacob Kaplan-Moss - the creators of Django. The main goal of'
             'this book is to make you a Django expert. By reading this book, you\'ll learn the skills'
             'needed to develop powerful websites quickly, with code that is clean and easy to maintain.'
             'This book is also a programmer\'s manual that provides complete coverage of the current'
             'Long Term Support (LTS) version of Django. For developers creating applications for'
             'commercial and business',
        is_published=False)
    post3 = Post(
        published_by=user2.id,
        title='Django или Ruby on Rails: какой фреймворк выбрать?',
        text='Вопрос выбора фреймворка часто встаёт перед стартаперами или программистами. Первые хотят, чтобы проект'
             'был основан на наиболее подходящем, трендовом фреймворке. Вторые хотят развивать свои навыки и'
             'применять знания в реальных проектах. Обе цели могут быть достигнуты путём ознакомления'
             'с веб-фреймворком. Мы перевели для вас материал о правильном выборе из этих двух альтернатив.',
        is_published=True)
    session.add(post1)
    session.add(post2)
    session.add(post3)

    category1 = Category(name="Web")
    category2 = Category(name="Books")
    session.add(category1)
    session.add(category2)

    post1.tags.append(tag1)
    post1.tags.append(tag4)
    post1.tags.append(tag5)
    post1.categories.append(category1)

    post2.tags.append(tag2)
    post2.tags.append(tag3)
    post2.categories.append(category2)

    post3.tags.append(tag2)
    post3.tags.append(tag3)
    post3.categories.append(category2)

    session.commit()
    session.close()


def get_published_post_for_category():
    """Print all posts for category"""
    session = Session()

    q_cat = session.query(Category).join(Category.posts)\
        .filter(and_(Post.is_published == 0, Post.title.contains('CSS')))
    categories = q_cat.all()
    for category in categories:
        print(f"Категория \"{category.name}\" содержит опубликованные посты:")
        for post in category.posts:
            print(post.title)

    session.close()


def get_post_with_several_tags():
    """Print all tags for post"""
    session = Session()

    q_post = session.query(Post).outerjoin(Post.tags).group_by(Post).having(func.count(Post.id) >= 3)
    posts = q_post.all()
    for post in posts:
        print(f"Пост \"{post.title}\" содержит тэги:")
        for tag in post.tags:
            print(tag.name)

    session.close()


def main():
    """Crated database, added base date and executed queries"""
    delete_all_tables()
    create_all_tables()
    create_base_data()

    print('Поиск категории с опубликованным постом, содержащим CSS в заголовке')
    get_published_post_for_category()
    print()

    print('Поиск поста с 3 и более тегами')
    get_post_with_several_tags()


if __name__ == '__main__':
    main()
