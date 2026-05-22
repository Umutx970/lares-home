import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from store.models import Product, Category


class Command(BaseCommand):
    help = "CSV dosyasından ürünleri içeri aktarır veya günceller"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                category_name = row.get("category", "Genel")
                category, _ = Category.objects.get_or_create(name=category_name)

                sku = row.get("sku") or row.get("barcode")

                product, created = Product.objects.update_or_create(
                    sku=sku,
                    defaults={
                        "category": category,
                        "name": row.get("name", ""),
                        "brand": row.get("brand", ""),
                        "barcode": row.get("barcode", ""),
                        "supplier_name": row.get("supplier_name", ""),
                        "supplier_product_id": row.get("supplier_product_id", ""),
                        "price": Decimal(row.get("price", "0")),
                        "stock": int(row.get("stock", 0)),
                        "description": row.get("description", ""),
                        "external_image_url": row.get("image_url", ""),
                        "is_active": True,
                    },
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Yeni ürün eklendi: {product.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Ürün güncellendi: {product.name}"))