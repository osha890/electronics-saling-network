from django.db import models


class NetworkNodeType(models.TextChoices):
    FACTORY = "FACTORY", "Factory"
    DISTRIBUTOR = "DISTRIBUTOR", "Distributor"
    DEALER_CENTER = "DEALER_CENTER", "Dealer Center"
    RETAIL_CHAIN = "RETAIL_CHAIN", "Retail Chain"
    ENTREPRENEUR = "ENTREPRENEUR", "Entrepreneur"
