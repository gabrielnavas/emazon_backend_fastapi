import random
from faker import Faker

from modules.books import models as models_book
from modules.stores import models as models_store
from modules.users import models as models_users


def init_dev_data():
    fake = Faker()

    type_cover1 = models_book.TypeCover.create(type_name='capa dura')
    type_cover2 = models_book.TypeCover.create(type_name='capa mole')

    language1 = models_book.Language.create(code='pt-br', name='portuguese')
    language2 = models_book.Language.create(code='us', name='american')

    category1 = models_book.Category.create(name='action')
    category2 = models_book.Category.create(name='classics')
    category3 = models_book.Category.create(name='horror')

    author1 = models_book.Author.create(name='Tiago Juras')
    author2 = models_book.Author.create(name='Flina pescoço')

    publishing_company1 = models_book.PublishingCompany.create(
        name='Matilda LTDA')
    publishing_company2 = models_book.PublishingCompany.create(
        name='Juca LTDA')

    for i in range(3):
        profile = fake.profile()
        models_users.User.create(
            full_name=profile['name'],
            email=profile['mail'],
            password='123456'
        )

    store1 = models_store.Store.create(
        fantasy_name='fantasia nome 1',
        cpf='86596861015',
        cnpj='88496388000104',
        salesman=models_users.User.get(id=random.choice([1, 2, 3]))
    )

    store2 = models_store.Store.create(
        fantasy_name='fantasia nome 2',
        cpf='04378612011',
        cnpj='92201668000115',
        salesman=models_users.User.get(id=random.choice([1, 2, 3]))
    )

    store3 = models_store.Store.create(
        fantasy_name='fantasia nome 3',
        cpf='72363467051',
        cnpj='67543056000163',
        salesman=models_users.User.get(id=random.choice([1, 2, 3]))
    )

    for i in range(50):
        models_book.Book.create(
            title=fake.name(),
            description=fake.text()[:60],
            price=55.22,
            discount=0.65,
            pages_amount=152,
            heigh=0.30,
            width=0.15,
            thickness=0.03,
            author=models_book.Author.get(id=random.choice([1, 2])),
            type_cover=models_book.TypeCover.get(id=random.choice([1, 2])),
            language=models_book.Language.get(id=random.choice([1, 2])),
            category=models_book.Category.get(id=random.choice([1, 2])),
            publishing_company=models_book.PublishingCompany.get(
                id=random.choice([1, 2])),
            store=models_book.Store.get(
                id=random.choice([1, 2, 3]))
        )
