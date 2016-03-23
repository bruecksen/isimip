from isi_mip.climatemodels.models import ImpactModel, Water, Region, Sector, Biomes, ReferencePaper, \
    SocioEconomicInputVariables, InputData
import pyexcel as pe
import pyexcel.ext.xlsx
import crossrefpy


class XLSImport:
    def __init__(self, filename):
        self.filename = filename
        self.book = pe.get_book(file_name=self.filename)

    def run(self):
        sheet1 = self.book['General']
        for zeile in sheet1.to_array()[5:13]:
            self.run_general(zeile)

    def run_general(self, zeile):
        SpecificSector = Sector.get(zeile[0])
        general = ImpactModel.objects.filter(name=zeile[2])
        if general:
            sector = SpecificSector.objects.get(impact_model__in=general)
            general = sector.impact_model
        else:
            general = ImpactModel.objects.create(name=zeile[2], sector='Water (global)')
            sector = general.fk_sector

        general.region.add(Region.objects.get_or_create(name=zeile[1])[0])
        general.version = zeile[6]

        try:
            ref = crossrefpy.query(zeile[7])
            doi = ref.DOI
            title = ref.title[0]
        except crossrefpy.ReferenceException:
            doi = None
            title = zeile[7]
        general.main_reference_paper = ReferencePaper.objects.get_or_create(name=title, doi=doi)[0]
        for paper in zeile[8].split('\n\n'):
            try:
                ref = crossrefpy.query(paper)
                doi = ref.DOI
                title = ref.title[0]
            except crossrefpy.ReferenceException:
                doi = None
                title = zeile[7]
            addpaper = ReferencePaper.objects.get_or_create(name=title, doi=doi)[0]
            general.additional_papers.add(addpaper)

        general.resolution = zeile[10]
        general.temporal_resolution_climate = zeile[11]
        general.temporal_resolution_co2 = zeile[12]
        general.temporal_resolution_land = zeile[13]
        general.temporal_resolution_soil = zeile[14]

        for vari in zeile[15].split(','):
            x = SocioEconomicInputVariables.objects.get_or_create(name=vari)[0]
            general.socioeconomic_input_variables.add(x)
        for vari in zeile[17].split(','):
            x = InputData.objects.get_or_create(data_set=vari)[0]
            general.climate_data_sets.add(x)

        general.soil_dataset = zeile[16]

        general.exceptions_to_protocol = zeile[18]
        general.spin_up = True if 'spin' in zeile[19].lower().strip() else None
        general.spin_up_design = zeile[20]

        general.natural_vegetation_partition = zeile[21]
        general.management = zeile[22]
        general.anything_else = zeile[23]
        general.extreme_events = zeile[24]
        general.comments = zeile[25]

        general.save()
        self.general = general
        self.sector = sector
        methodToCall = getattr(self, str(sector).lower())
        methodToCall()

    def water(self):
        # water = Water.objects.get()
        water = self.sector
        sheet = self.book['Water']
        for _line in sheet:
            if _line[0] == self.general.name:
                line1 = _line
                break
        try:
            water.technological_progress = line1[1]
        except:
            print(self.general)
        water.soil = line1[2]
        water.water_use = line1[3]
        water.water_sectors = line1[4]
        water.routing = line1[5]
        water.land_use = line1[6]
        water.dams_reservoirs = line1[7]
        if line1[8].strip():
            water.calibration = True if line1[8].lower().strip() == 'yes' else False
        water.calibration_years = line1[9]
        water.calibration_dataset = line1[10]
        water.calibration_catchments = line1[11]
        if line1[12].strip():
            water.vegetation = True if line1[12].lower().strip() == 'yes' else False
        water.vegetation_presentation = line1[13]
        water.methods_evapotraspiration = line1[14]
        water.methods_snowmelt = line1[15]

        water.save()
