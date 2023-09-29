from django.core.management.base import BaseCommand

from core.utils import cyrillic_slug_maker
from products.models import Category, Product


class Command(BaseCommand):
    help = "Download data from tsv file to db"

    def handle(self, *args, **options):
        self.import_products()

    def import_products(self, file="./data/test_prod_data.tsv"):
        with open(file, encoding="utf-8") as f:
            data = f.readlines()
        for item in data:
            datalist = item.split(sep="	")
            if Category.objects.filter(name=datalist[4].strip()[:30]).exists():
                category = Category.objects.get(name=datalist[4].strip()[:30])
            else:
                category = Category.objects.create(
                    name=datalist[4].strip()[:30],
                    description=datalist[4].strip()[:255],
                    slug=cyrillic_slug_maker(datalist[4].strip()[:30]),
                )
            Product.objects.get_or_create(
                name=datalist[0][:30],
                description=datalist[1][:255],
                brand=datalist[2][:30],
                price_per_unit=datalist[3],
                category=category,
            )
