import random
from decimal import Decimal

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

        nodes = []
        for i in range(count):
            node_type = random.choice(list(NetworkNodeType.values))
            address = Address.objects.create(
                country=fake.country(),
                city=fake.city(),
                street=fake.street_name(),
                house_number=fake.bothify("##?"),
            )
            contact = Contact.objects.create(
                email=fake.email(),
                address=address,
            )
            node = NetworkNode.objects.create(
                name=fake.company(),
                type=node_type,
                contact=contact,
                debt_to_supplier=Decimal("0.00"),
            )
            nodes.append(node)

        saved_count = 0
        for node in nodes:
            if node.type != NetworkNodeType.FACTORY:
                supplier = random.choice(nodes)
                if supplier != node:
                    node.supplier = supplier
                    node.debt_to_supplier = Decimal(random.randint(0, 5000))
                    node.save()
                    saved_count += 1

            sample_products = random.sample(products, k=random.randint(1, 4))
            node.products.add(*sample_products)

        self.stdout.write(self.style.SUCCESS(f"Created {saved_count} network nodes"))
