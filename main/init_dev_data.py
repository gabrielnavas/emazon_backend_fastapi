import random
from faker import Faker

from modules.books import models


def init_dev_data():
    fake = Faker()

    # type_cover1 = models.TypeCover.create(type_name='capa dura')
    # type_cover2 = models.TypeCover.create(type_name='capa mole')

    # language1 = models.Language.create(code='pt-br', name='portuguese')
    # language2 = models.Language.create(code='us', name='american')

    # category1 = models.Category.create(name='action')
    # category2 = models.Category.create(name='classics')
    # category3 = models.Category.create(name='horror')

    # author1 = models.Author.create(name='Tiago Juras')
    # author2 = models.Author.create(name='Flina pescoço')

    # publishing_company1 = models.PublishingCompany.create(name='Matilda LTDA')
    # publishing_company2 = models.PublishingCompany.create(name='Juca LTDA')

    for i in range(50):
        models.Book.create(
            title=fake.name(),
            description=fake.text()[:60],
            price=55.22,
            discount=0.65,
            pages_amount=152,
            heigh=0.30,
            width=0.15,
            thickness=0.03,
            author=models.Author.get(id=random.choice([1, 2])),
            type_cover=models.TypeCover.get(id=random.choice([1, 2])),
            language=models.Language.get(id=random.choice([1, 2])),
            category=models.Category.get(id=random.choice([1, 2])),
            publishing_company=models.PublishingCompany.get(
                id=random.choice([1, 2])),
        )
