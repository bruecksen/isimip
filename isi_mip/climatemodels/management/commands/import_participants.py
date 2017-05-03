import csv

from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from isi_mip.climatemodels.models import ImpactModel, BaseImpactModel, Sector
from isi_mip.contrib.models import Country, UserProfile


SECTOR_MAPPING = {
    'Agriculture': ('Agriculture',),
    'Agro-Economic': ('Agro-Economic Modelling',),
    'Biodiversity': ('Biodiversity',),
    'Biomes/Forestry': ('Biomes', 'Forests'),
    'Computable General Equilibrium': ('Computable General Equilibrium Modelling',),
    'Energy supply and demand': ('Energy',),
    'Forests': ('Forests',),
    'Health': ('Health',),
    'Infrastructure': ('Coastal Infrastructure',),
    'Permafrost': ('Permafrost',),
    'Marine ecosystems & Fisheries': ('Marine Ecosystems and Fisheries (global)', 'Marine Ecosystems and Fisheries (regional)'),
    'Water (global)': ('Water (global)',),
    'Water (regional)': ('Water (regional)',),
    'All': (),
}


class Command(BaseCommand):
    help = 'Import Participants file'

    def handle(self, *args, **options):
        path = 'data/participants.csv'
        UserModel = get_user_model()
        user_found_counter = 0
        user_not_found_counter = 0
        model_not_found_counter = 0
        user_created_counter = 0
        sector_not_found_counter = 0
        with open(path, newline='', encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            # skip header
            next(reader)
            for row in reader:
                mapped_sectors = None
                name = row[0]
                institute = row[1]
                country = row[2]
                role = row[3]
                email = row[4]
                models = row[5]
                sectors = row[6]
                comment = row[7]
                if email:
                    user = None
                    try:
                        user = UserModel.objects.get(email__iexact=email)
                        user_found_counter = user_found_counter + 1
                        # print('User found: (%s)' % ', '.join(row))
                    except:
                        print('User not found: (%s)' % ', '.join(row))
                        user_not_found_counter = user_not_found_counter + 1
                    if sectors:
                        mapped_sectors = [item for sector in sectors.split(',') for item in SECTOR_MAPPING.get(sector.strip(), ())]
                        mapped_sectors = Sector.objects.filter(name__in=mapped_sectors)
                        if not mapped_sectors.exists():
                            print('Sector not found: %s' % sectors)
                            sector_not_found_counter = sector_not_found_counter + 1
                    if not user:
                        # create inactive user
                        name = name.split(' ')
                        user = UserModel.objects.create(
                            first_name = name[0],
                            last_name = len(name) > 1 and ' '.join(name[1:]) or '',
                            email = email.lower(),
                            username = email.lower(),
                            is_active = False,
                            is_staff = False,
                            is_superuser = False,
                        )
                    user_created_counter = user_created_counter + 1
                    if not hasattr(user, 'userprofile'):
                        UserProfile.objects.create(user=user)
                    if not user.userprofile.institute:
                        user.userprofile.institute = institute
                    if not user.userprofile.country:
                        user.userprofile.country, created = Country.objects.get_or_create(name=country)
                    user.userprofile.comment = comment
                    if models:
                        for model in models.split(','):
                            try:
                                model = model.strip()
                                base_model = BaseImpactModel.objects.get(name__iexact=model)
                                user.userprofile.involved.add(*list(base_model.impact_model.all()))
                            except:
                                print('Model not found: %s' % model)
                                model_not_found_counter = model_not_found_counter + 1
                    if mapped_sectors and not models:
                        user.userprofile.sector.set(mapped_sectors)
                    elif mapped_sectors and models:
                        cleaned_sectors = []
                        for sector in mapped_sectors:
                            for im in user.userprofile.involved.all():
                                if im.base_model.sector == sector:
                                    continue
                                else:
                                    cleaned_sectors.append(sector)
                        user.userprofile.sector.set(cleaned_sectors)
                    user.save()
                    user.userprofile.save()

        print('User found: %s' % user_found_counter)
        print('User not found: %s' % user_not_found_counter)
        print('Sector not found: %s' % sector_not_found_counter)
        print('Model not found: %s' % model_not_found_counter)
        print('User created counter: %s' % user_created_counter)

