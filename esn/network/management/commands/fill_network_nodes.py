import random
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from faker import Faker

from contacts.models import Address, Contact
from network.choices import NetworkNodeType
from network.models import NetworkNode
from products.models import Product


class Command(BaseCommand):
    help = "Fill the database with fake NetworkNode objects"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of nodes to generate (default: 10)",
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]

        products = list(Product.objects.all())
        if not products:
            for _ in range(10):
                products.append(
                    Product.objects.create(
                        name=fake.word(),
                        model=fake.bothify("##"),
                        release_date=fake.date_this_decade(),
                    )
                )

        nodes = [
            NetworkNode.objects.create(
                name=fake.company(),
                type=NetworkNodeType.FACTORY,
                email=fake.email(),
                country=fake.country(),
                city=fake.city(),
                street=fake.street_name(),
                house_number=fake.bothify("##"),
                debt_to_supplier=Decimal("0.00"),
            )
        ]
        for _ in range(count - 1):
            node_type = random.choice(list(NetworkNodeType.values))
            node = NetworkNode.objects.create(
                name=fake.company(),
                type=node_type,
                email=fake.email(),
                country=fake.country(),
                city=fake.city(),
                street=fake.street_name(),
                house_number=fake.bothify("##"),
                debt_to_supplier=Decimal("0.00"),
            )
            nodes.append(node)

            for node in nodes:
                if node.type != NetworkNodeType.FACTORY:
                    self_index = NetworkNode.hierarchy.index(node.type)
                    possible_suppliers = [
                        s
                        for s in nodes
                        if NetworkNode.hierarchy.index(s.type) < self_index
                    ]
                    supplier = random.choice(possible_suppliers)
                    try:
                        node.supplier = supplier
                        node.debt_to_supplier = Decimal(random.randint(0, 5000))
                        node.save()
                    except ValidationError:
                        pass

            sample_products = random.sample(products, k=random.randint(1, 4))
            node.products.add(*sample_products)

        self.stdout.write(self.style.SUCCESS(f"Created {len(nodes)} network nodes"))
