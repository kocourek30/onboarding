import csv
from django.core.management.base import BaseCommand, CommandError
from provozy.models import Provoz

class Command(BaseCommand):
    help = "Import provozů z CSV, každý řádek vytvoří nový Provoz"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Cesta k branches_full.csv")

    def handle(self, *args, **options):
        path = options["csv_path"]
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")
                count_created = 0
                for row in reader:
                    Provoz.objects.create(
                        cislo_provozu=int(row["cislo_provozu"]),
                        nazev=row.get("nazev", "").strip(),
                        ulice=row.get("ulice", "").strip(),
                        mesto=row.get("mesto", "").strip(),
                        kraj=row.get("kraj", "").strip(),
                        psc=row.get("psc", "").strip(),
                        manazer=row.get("manazer", "").strip(),
                        email=row.get("email", "").strip(),
                    )
                    count_created += 1
            self.stdout.write(self.style.SUCCESS(
                f"Hotovo: vytvořeno {count_created} provozů."
            ))
        except FileNotFoundError:
            raise CommandError(f"Soubor {path} nenalezen")
