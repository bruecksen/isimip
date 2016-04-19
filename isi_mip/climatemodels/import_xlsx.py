import pyexcel as pe
# noinspection PyUnresolvedReferences
import pyexcel.ext.xlsx

from isi_mip.sciencepaper import crossrefpy
from isi_mip.climatemodels.models import ImpactModel, Region, Sector, ReferencePaper, \
    SocioEconomicInputVariables, SECTOR_MAPPING, ContactPerson, ClimateVariable, SpatialAggregation, Water, \
    Agriculture, Energy, MarineEcosystems, Biomes, BiomesForests


class XLSImport:
    def __init__(self, filename):
        self.filename = filename
        self.book = pe.get_book(file_name=self.filename)

    def run(self):
        sheet1 = self.book['General']
        sheet_array = sheet1.to_array()
        zeilen = [6, 7, 21, 24, 35, 36, 49, 59, 72, 77,
                  95, 102, 107, 115, 124, 128, 134, 136, 137]
        for zeile in zeilen:
            self.run_general(sheet_array[zeile-1])
        # for zeile in sheet_array:
        #     self.run_general(zeile)

    def run_general(self, zeile):
        print(zeile[2]+": ",end='')
        try:
            general = ImpactModel.objects.get(name=zeile[2])
        except:
            sectordings = Sector.get(zeile[0] + ' ' + zeile[1])
            name = list(SECTOR_MAPPING.keys())[list(SECTOR_MAPPING.values()).index(sectordings)]
            general = ImpactModel.objects.create(name=zeile[2], sector=name)
        print(general)
        # return

        cpers = ContactPerson.objects.get_or_create(
            institute=zeile[4],name=zeile[5],email=zeile[6], impact_model=general)

        general.region.add(Region.objects.get_or_create(name=zeile[1])[0])
        general.version = zeile[7]

        try:
            ref = crossrefpy.query(zeile[8])
            doi = ref.DOI
            title = ref.title[0]
        except crossrefpy.ReferenceException:
            doi = None
            title = zeile[8]
        general.main_reference_paper = ReferencePaper.objects.get_or_create(doi=doi,
                                                                            defaults={'title':title})[0]

        for paper in zeile[9].split('\n\n'):
            try:
                ref = crossrefpy.query(paper)
                doi = ref.DOI
                title = ref.title[0]
            except crossrefpy.ReferenceException:
                doi = None
                title = paper
            addpaper = ReferencePaper.objects.get_or_create(doi=doi, defaults={'title':title})[0]
            general.other_references.add(addpaper)

        general.spatial_aggregation = SpatialAggregation.objects.get_or_create(name=zeile[11])[0]
        general.resolution = zeile[12]
        general.temporal_resolution_climate = zeile[13]
        general.temporal_resolution_co2 = zeile[14]
        general.temporal_resolution_land = zeile[15]
        general.temporal_resolution_soil = zeile[16]

        for vari in zeile[17].split(','):
            x = ClimateVariable.objects.get_or_create(name=vari.strip())[0]
            general.climate_variables.add(x)

        for vari in zeile[18].split(','):
            x = SocioEconomicInputVariables.objects.get_or_create(name=vari.strip())[0]
            general.socioeconomic_input_variables.add(x)

        general.soil_dataset = zeile[20]
        general.additional_input_data_sets = zeile[21]

        general.exceptions_to_protocol = zeile[22]
        if 'spin' in zeile[23].lower().strip() or 'yes' in zeile[23].lower().strip():
            general.spin_up = True
        else:
            general.spin_up = False
        general.spin_up_design = zeile[24]

        general.natural_vegetation_partition = zeile[25]
        general.natural_vegetation_dynamics = zeile[26]
        general.management = zeile[28]
        general.anything_else = zeile[29]
        general.extreme_events = zeile[30]
        general.comments = zeile[31]

        general.save()
        self.general = general
        methodToCall = getattr(self, str(general.fk_sector).lower())
        methodToCall()

    def waterglobal(self):
        return self.water()

    def waterregional(self):
        return self.water()

    def water(self):
        # water = Water.objects.get()
        water = self.general.fk_sector
        sheet = self.book['Water']
        for _line in sheet:
            if _line[0] == self.general.name:
                line1 = _line
                break
        try:
            line1[1]
        except:
            print("Problem adding specific stuff for", self.general)
            return

        assert isinstance(water, Water)
        water.technological_progress = line1[1]
        water.soil = line1[2]
        water.water_use = line1[3]
        water.water_sectors = line1[4]
        water.routing = line1[5]
        water.routing_data = line1[6]
        water.land_use = line1[7]
        water.dams_reservoirs = line1[8]
        if line1[9].strip():
            water.calibration = True if line1[9].lower().strip() == 'yes' else False
        water.calibration_years = line1[10]
        water.calibration_dataset = line1[11]
        water.calibration_catchments = line1[12]
        if line1[13].strip():
            water.vegetation = True if line1[13].lower().strip() == 'yes' else False
        water.vegetation_presentation = line1[14]
        water.methods_evapotraspiration = line1[15]
        water.methods_snowmelt = line1[16]

        water.save()

    def agriculture(self):
        agri = self.general.fk_sector
        sheet = self.book['Agriculture']
        for _line in sheet:
            if _line[0] == self.general.name:
                line1 = _line
                break
        try:
            line1[1]
        except:
            print("Problem adding specific stuff for", self.general)
            return
        assert isinstance(agri, Agriculture)

        agri.crops = line1[1]
        agri.land_coverage = line1[2]
        agri.planting_date_decision = line1[3]
        agri.planting_density = line1[4]
        agri.crop_cultivars = line1[5]
        agri.fertilizer_application = line1[6]
        agri.irrigation = line1[7]
        agri.crop_residue = line1[8]
        agri.initial_soil_water = line1[9]
        agri.initial_soil_nitrate_and_ammonia = line1[10]
        agri.initial_soil_C_and_OM = line1[11]
        agri.initial_crop_residue = line1[12]
        agri.lead_area_development = line1[13]
        agri.light_interception = line1[14]
        agri.light_utilization = line1[15]
        agri.yield_formation = line1[16]
        agri.crop_phenology = line1[17]
        agri.root_distribution_over_depth = line1[18]
        agri.stresses_involved = line1[19]
        agri.type_of_water_stress = line1[20]
        agri.type_of_heat_stress = line1[21]
        agri.water_dynamics = line1[22]
        agri.evapo_transpiration = line1[23]
        agri.soil_CN_modeling = line1[24]
        agri.co2_effects = line1[25]
        agri.parameters_number_and_description = line1[26]
        agri.calibrated_values = line1[27]
        agri.output_variable_and_dataset = line1[28]
        agri.spatial_scale_of_calibration_validation = line1[29]
        agri.temporal_scale_of_calibration_validation = line1[30]
        agri.criteria_for_evaluation = line1[31]
        agri.save()

    def energy(self):
        energy = self.general.fk_sector
        sheet = self.book['Energy']
        if self.general.name == 'GCAM-IIM':
            self.general.name = 'GCAM-IMM'
        for _line in sheet:
            if _line[0] == self.general.name:
                line1 = _line
                break
        try:
            line1[1]
        except:
            print("Problem adding specific stuff for", self.general)
            return
        assert isinstance(energy, Energy)
        energy.model_type = line1[6]
        energy.temporal_extent = line1[7]
        energy.temporal_resolution = line1[8]
        energy.data_format_for_input = line1[25]
        energy.impact_types_energy_demand = line1[1]
        energy.impact_types_temperature_effects_on_thermal_power = line1[2]
        energy.impact_types_weather_effects_on_renewables = line1[3]
        energy.impact_types_water_scarcity_impacts = line1[4]
        energy.impact_types_other = line1[5]
        energy.output_energy_demand = line1[11]
        energy.output_energy_supply = line1[12]
        energy.output_water_scarcity = line1[13]
        energy.output_economics = line1[14]
        energy.output_other = line1[15]
        energy.variables_not_directly_from_GCMs = line1[27]
        energy.response_function_of_energy_demand_to_HDD_CDD = line1[28]
        energy.factor_definition_and_calculation = line1[29]
        energy.biomass_types = line1[30]
        energy.maximum_potential_assumption = line1[31]
        energy.bioenergy_supply_costs = line1[32]
        # energy.socioeconomic_input = line1[]
        energy.save()

    def permafrost(self):
        pass

    def marineecosystemsregional(self):
        self.marineecosystemsglobal()
    def marineecosystemsglobal(self):
        mari = self.general.fk_sector
        sheet = self.book['Fisheries']
        for _line in sheet:
            if _line[1].strip() == self.general.name:
                line1 = _line
                break
        try:
            line1[1]
        except:
            print("Problem adding specific stuff for", self.general)
            return
        assert isinstance(mari, MarineEcosystems)
        mari.defining_features = line1[3]
        mari.spatial_scale = line1[4]
        mari.spatial_resolution = line1[5]
        mari.temporal_scale = line1[6]
        mari.temporal_resolution = line1[7]
        mari.taxonomic_scope = line1[8]
        mari.vertical_resolution = line1[9]
        mari.spatial_dispersal_included = line1[10]
        mari.fishbase_used_for_mass_length_conversion = line1[11]
        mari.save()

    def biomes(self):
        self.forests()
    def forests(self):
        fore = self.general.fk_sector
        sheet = self.book['BiomesForestry']
        for _line in sheet:
            if _line[0].strip() == self.general.name:
                line1 = _line
                break
        try:
            line1[1]
        except:
            print("Problem adding specific stuff for", self.general)
            return
        assert isinstance(fore, BiomesForests)
        fore.output = line1[1]
        fore.output_per_pft = line1[2]
        fore.considerations = line1[3]
        fore.dynamic_vegetation = line1[4]
        fore.nitrogen_limitation = line1[5]
        fore.co2_effects = line1[6]
        fore.light_interception = line1[7]
        fore.light_utilization = line1[8]
        fore.phenology = line1[9]
        fore.water_stress = line1[10]
        fore.heat_stress = line1[11]
        fore.evapotranspiration_approach = line1[12]
        fore.rooting_depth_differences = line1[13]
        fore.root_distribution = line1[14]
        fore.permafrost = line1[15]
        fore.closed_energy_balance = line1[16]
        fore.soil_moisture_surface_temperature_coupling = line1[17]
        fore.latent_heat = line1[18]
        fore.sensible_heat = line1[19]
        fore.mortality_age = line1[20]
        fore.mortality_fire = line1[21]
        fore.mortality_drought = line1[22]
        fore.mortality_insects = line1[23]
        fore.mortality_storm = line1[24]
        fore.mortality_stochastic_random_disturbance = line1[25]
        fore.mortality_other = line1[26]
        fore.mortality_remarks = line1[27]
        fore.nbp_fire = line1[28]
        fore.nbp_landuse_change = line1[29]
        fore.nbp_harvest = line1[30]
        fore.nbp_other = line1[31]
        fore.nbp_comments = line1[32]
        fore.list_of_pfts = line1[33]
        fore.pfts_comments = line1[34]
        fore.save()

    def health(self):
        pass
    def biodiversity(self):
        pass
    def coastalinfrastructure(self):
        pass
    def agroeconomicmodelling(self):
        pass
    def computablegeneralequilibriummodelling(self):
        pass