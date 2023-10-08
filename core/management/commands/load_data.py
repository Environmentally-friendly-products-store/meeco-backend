from datetime import date

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from core.utils import cyrillic_slug_maker
from events.models import Event
from products.models import Brand, Category, ImageSet, Product


class Command(BaseCommand):
    help = "Download data from tsv file to db"

    def add_arguments(self, parser):
        parser.add_argument(
            "filepath",
            action="store",
            nargs="?",
            type=str,
            default="./data/test_prod_data.tsv",
        )
        parser.add_argument(
            "-p",
            "--product",
            action="store_true",
            default=False,
            help="Выбор модели продуктов без изображения",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            default=False,
            help="Выбор модели продуктов с изображениями",
        )
        parser.add_argument(
            "-i",
            "--image",
            action="store_true",
            default=False,
            help="Выбор модели изображений",
        )
        parser.add_argument(
            "-с",
            "--category",
            action="store_true",
            default=False,
            help="Выбор модели категории",
        )
        parser.add_argument(
            "-b",
            "--brand",
            action="store_true",
            default=False,
            help="Выбор модели бренда",
        )
        parser.add_argument(
            "-e",
            "--event",
            action="store_true",
            default=False,
            help="Выбор модели события",
        )

    def handle(self, *args, **options):
        filepath = options["filepath"]
        if options["product"]:
            self.import_products(file=filepath)
        elif options["all"]:
            self.import_all(file=filepath)
        elif options["image"]:
            self.import_images(file=filepath)
        elif options["category"]:
            self.import_categories(file=filepath)
        elif options["brand"]:
            self.import_brands(file=filepath)
        elif options["event"]:
            self.import_events(file=filepath)
        else:
            self.stdout.write(self.style.ERROR("Cannot find argument"))
        self.stdout.write(self.style.SUCCESS("Finished"))

    def get_or_create_category(self, name, description=None, slug=None):
        if description is None:
            description = name
        if slug is None:
            slug = cyrillic_slug_maker(name)
        if Category.objects.filter(name=name).exists():
            category = Category.objects.get(name=name)
        else:
            category = Category.objects.create(
                name=name,
                description=description,
                slug=slug,
            )
        return category

    def get_or_create_brand(
        self, name, description=None, slug=None, country="Eastasia"
    ):
        if description is None:
            description = name
        if slug is None:
            slug = cyrillic_slug_maker(name)
        if Brand.objects.filter(name=name).exists():
            brand = Brand.objects.get(name=name)
        else:
            brand = Brand.objects.create(
                name=name, description=description, slug=slug, country=country
            )
        return brand

    def create_event(
        self,
        name,
        description=None,
        slug=None,
        discount=0,
        image=None,
        date_start="1970-1-1",
        date_end="2077-1-1",
    ):
        if description is None:
            description = name
        if slug is None:
            slug = cyrillic_slug_maker(name)
        if Event.objects.filter(name=name).exists():
            event = Event.objects.get(name=name)
        else:
            event = Event.objects.create(
                name=name,
                description=description,
                slug=slug,
                discount=discount,
                image=image,
                date_start=date.fromisoformat(date_start),
                date_end=date.fromisoformat(date_end),
            )
        return event

    def get_event(self, name):
        if Event.objects.filter(name=name).exists():
            return Event.objects.get(name=name)
        return None

    def import_products(self, file):
        with open(file, encoding="utf-8") as f:
            data = f.readlines()
        for item in data[1:]:
            datalist = item.split(sep="	")
            category = self.get_or_create_category(name=datalist[2].strip()[:30])
            brand = self.get_or_create_brand(name=datalist[3][:30])
            event = self.get_event(name=datalist[3][:30])
            Product.objects.get_or_create(
                name=datalist[0][:30],
                description=datalist[1][:255],
                brand=brand,
                event=event,
                price_per_unit=datalist[5],
                category=category,
            )

    def import_all(self, file):
        with open(file, encoding="utf-8") as f:
            data = f.readlines()
        for item in data[1:]:
            datalist = item.split(sep="	")
            category = self.get_or_create_category(name=datalist[2].strip()[:30])
            brand = self.get_or_create_brand(name=datalist[3][:30])
            event = self.get_event(name=datalist[4][:30])
            product, created = Product.objects.get_or_create(
                name=datalist[0][:30],
                description=datalist[1][:255],
                brand=brand,
                event=event,
                price_per_unit=datalist[5],
                category=category,
            )
            ImageSet.objects.get_or_create(
                product=product,
                image=datalist[6],
                big_image=datalist[7],
                preview_image=datalist[8],
                image_thumbnail=datalist[9],
            )

    def import_images(self, file):
        with open(file, encoding="utf-8") as f:
            data = f.readlines()
        for item in data[1:]:
            datalist = item.split(sep="	")
            product = get_object_or_404(Product, name=datalist[0])
            ImageSet.objects.get_or_create(
                product=product,
                image=datalist[1],
                big_image=datalist[2],
                preview_image=datalist[3],
                image_thumbnail=datalist[4],
            )

    def import_categories(self, file):
        with open(file, encoding="utf-8") as f:
            data = f.readlines()
        for item in data[1:]:
            datalist = item.split(sep="	")
            self.get_or_create_category(
                name=datalist[0][:30],
                description=datalist[1][:255],
                slug=datalist[0][:30],
            )

    def import_brands(self, file):
        with open(file, encoding="utf-8") as f:
            data = f.readlines()
        for item in data[1:]:
            datalist = item.split(sep="	")
            self.get_or_create_brand(
                name=datalist[0][:30],
                description=datalist[1][:255],
                slug=datalist[0][:30],
                country=datalist[0][:50],
            )

    def import_events(self, file):
        with open(file, encoding="utf-8") as f:
            data = f.readlines()
        for item in data[1:]:
            datalist = item.split(sep="	")
            self.create_event(
                name=datalist[0][:30],
                description=datalist[1][:255],
                slug=datalist[0][:30],
                discount=int(datalist[3][:30]),
                image=datalist[4],
                date_start=datalist[5],
                date_end=datalist[6],
            )
