# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['erp_air']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.1,<19.0']

setup_kwargs = {
    'name': 'erp-air',
    'version': '0.0.4b0',
    'description': 'Evaluate Air Handling Unit per Ecodesign.',
    'long_description': '# INTRO\n\nStarting from 2018 all ventialtion units should\ncomply with the requirements of the \nCOMMISSION REGULATION (EU) No 1253/2014 of 7 July 2014\nimplementing Directive 2009/125/EC of the European \nParliament and of the Council with regard\nto ecodesign requirements for ventilation units.\n\nThis package solves only non-residential ventilation\nunits.\n\nThese requirements sometimes being refered as `ErP` or\n`Ecodesign`.\n\nIt is importnat to introduce some notations in order\nto understand the code better:\n\n\n**nrvu** - non-residential ventialtion unit\n\n**sfp** - specific fan power\n\n**int** - internal (do not confuse with integer:))\n\n**ext** - external\n\n**hrs** - heat recover system, i.e. rotory wheel,\n    plate heat exchanger o run-around-coil\n\n**rac** - run-around coil heat recovery\n\n**rw** - rotory wheel heat recovery\n\n**phex** - plate heat exchnager heat recovery\n\n**uvu** - unidirectional ventialtion unit\n\n**bvu** - bidirectional ventialtion unit\n\n**eff** - efficiency\n\n**sup** - suply side of the air handling unit\n\n**eta** - extract side of the air handling unit\n\n\nMore expanded list of notation can be found\nin the Article 2 and Annex I.2 of the \n[regulation](_resources/CELEX_32014R1253_EN_TXT.pdf)\n\n\n# INSTALATION\nThere are two ways:\n1. pip install erp-air\n2. pull the docker image from \n[project registry](https://gitlab.com/remak-dva/erp-air/container_registry)\n\n# USAGE\n```python\nimport attr\n\nfrom erp_air import (\n    validate_ahu,\n    ErpResponse,\n    ErpRequest\n)\n\nerp_request = ErpRequest(\n    unit_class="nrvu",\n    unit_type="bvu",\n    has_medium_filter_eta=True,\n    has_fine_filter_sup=True,\n    hrs_type="phex",\n    hrs_thermal_eff_en308=0.827,\n    has_multispeed_drive=True,\n    has_variablespeed_drive=True,\n    airflow_nominal_sup=1,\n    airflow_nominal_eta=1,\n    electric_power_input_effective=155,\n    pressure_drop_int_vent_comps_sup=307,\n    pressure_drop_int_vent_comps_eta=266,\n    pressure_drop_int_non_vent_comps_sup=250,\n    pressure_drop_int_non_vent_comps_eta=250,\n    pressure_drop_ext_sup_nominal=250,\n    pressure_drop_ext_eta_nominal=250,\n    filter_section_area_sup=0.5,\n    filter_section_area_eta=0.5,\n    fan_section_area_sup=0.5,\n    fan_section_area_eta=0.5,\n    fan_eff_static_eu_327_2011_sup=0.35,\n    fan_eff_static_eu_327_2011_eta=0.35,\n    fan_eff_system_static_sup=0.4881,\n    fan_eff_system_static_eta=0.4832,\n    external_leakage_rate=0.004,\n    internal_leakage_rate=0.004,\n    filters_eurovent_compliance=True,\n    filter_energy_class_eurovent_sup="A",\n    filter_energy_class_eurovent_eta="A",\n    recycling_manual_url="url://",\n    has_thermal_bypass_on_hrs=True,\n    has_visual_signaling_on_filters=True,\n    has_alarm_on_filters=True,\n    manufacturer_name="Remak",\n    manufacturer_model="Some model",\n)\nerp_response = ErpResponse(\n    comply=True,\n    sfp_int=1178,\n    sfp_int_lim=1241,\n    hrs_thermal_eff=0.827,\n    hrs_thermal_eff_lim=0.73,\n    hrs_type="phex",\n    has_multispeed_drive=True,\n    has_variablespeed_drive=True,\n    has_hrs=True,\n    has_thermal_bypass_on_hrs=True,\n    fan_eff_uvu=0.4881,\n    fan_eff_uvu_min=None,\n    has_visual_signaling_on_filters=True,\n    has_alarm_on_filters=True,\n    manufacturer_name="Remak",\n    manufacturer_model="Some model",\n    unit_class="NRVU",\n    unit_type="BVU",\n    airflow_nominal_sup=1,\n    airflow_nominal_eta=1,\n    electric_power_input_effective=155,\n    face_velocity_sup=2.0,\n    face_velocity_eta=2.0,\n    pressure_drop_ext_sup_nominal=250,\n    pressure_drop_ext_eta_nominal=250,\n    pressure_drop_int_vent_comps_sup=307,\n    pressure_drop_int_vent_comps_eta=266,\n    pressure_drop_int_non_vent_comps_sup=250,\n    pressure_drop_int_non_vent_comps_eta=250,\n    fan_eff_static_eu_327_2011_sup=0.35,\n    fan_eff_static_eu_327_2011_eta=0.35,\n    external_leakage_rate=0.004,\n    internal_leakage_rate=0.004,\n    filters_en779_compliance=True,\n    filter_energy_class_eurovent_sup="A",\n    filter_energy_class_eurovent_eta="A",\n    recycling_manual_url="url://",\n    warnings=None,\n    errors=None,\n)\nassert attr.asdict(\n    validate_ahu(erp_request)\n) == attr.asdict(erp_response)\n```\n',
    'author': 'Artem Zhukov',
    'author_email': 'zhukovgreen@ya.ru',
    'url': 'https://gitlab.com/remak-dva/erp-air',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
