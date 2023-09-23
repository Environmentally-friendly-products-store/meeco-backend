from django.core.management.base import BaseCommand
from products.models import Product, Category
from core.utils import cyrillic_slugmaker


class Command(BaseCommand):
    help = 'Download data from folder to db'

    def handle(self, *args, **options):
        self.import_products()

    def import_products(self, file='./data/test_prod_data.csv'):
        with open(file, 'r') as f:
            data = f.readlines()
        for item in data:
            datalist = item.split(sep=',')
            if Category.objects.filter(
                name=datalist[4].strip()
            ).exists():
                category = Category.objects.get(
                    name=datalist[4].strip()
                )
            else:
                category = Category.objects.create(
                    name=datalist[4].strip(),
                    description=datalist[4].strip(),
                    slug=cyrrilic_slugmaker(datalist[4].strip())
                )
            Product.objects.get_or_create(
                name=datalist[0],
                description=datalist[1],
                brand=datalist[2],
                price_per_unit=datalist[3],
                category=category.id,
            )
