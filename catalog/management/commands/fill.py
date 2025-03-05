from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        products = [
            {'name': 'Кепка', 'category': Category(pk=1), 'price': 400},
            {'name': 'Мерседес Бенз', 'category': Category(pk=2), 'price': 5000000},
            {'name': 'Спортивная сумка', 'category': Category(pk=1), 'price': 1000},
        ]

        products_for_create = []
        for product_item in products:
            products_for_create.append(
                Product(**product_item)
            )

        Product.objects.bulk_create(products_for_create)
