# INTRO

Starting from 2018 all ventialtion units should
comply with the requirements of the 
COMMISSION REGULATION (EU) No 1253/2014 of 7 July 2014
implementing Directive 2009/125/EC of the European 
Parliament and of the Council with regard
to ecodesign requirements for ventilation units.

This package solves only non-residential ventilation
units.

These requirements sometimes being refered as `ErP` or
`Ecodesign`.

It is importnat to introduce some notations in order
to understand the code better:


**nrvu** - non-residential ventialtion unit

**sfp** - specific fan power

**int** - internal (do not confuse with integer:))

**ext** - external

**hrs** - heat recover system, i.e. rotory wheel,
    plate heat exchanger o run-around-coil

**rac** - run-around coil heat recovery

**rw** - rotory wheel heat recovery

**phex** - plate heat exchnager heat recovery

**uvu** - unidirectional ventialtion unit

**bvu** - bidirectional ventialtion unit

**eff** - efficiency

**sup** - suply side of the air handling unit

**eta** - extract side of the air handling unit


More expanded list of notation can be found
in the Article 2 and Annex I.2 of the 
[regulation](_resources/CELEX_32014R1253_EN_TXT.pdf)


# INSTALATION
There are two ways:
1. pip install erp-air
2. pull the docker image from 
[project registry](https://gitlab.com/remak-dva/erp-air/container_registry)

# USAGE
```python
import attr

from erp_air import (
    validate_ahu,
    ErpResponse,
    ErpRequest
)

erp_request = ErpRequest(
    unit_class="nrvu",
    unit_type="bvu",
    has_medium_filter_eta=True,
    has_fine_filter_sup=True,
    hrs_type="phex",
    hrs_thermal_eff_en308=0.827,
    has_multispeed_drive=True,
    has_variablespeed_drive=True,
    airflow_nominal_sup=1,
    airflow_nominal_eta=1,
    electric_power_input_effective=155,
    pressure_drop_int_vent_comps_sup=307,
    pressure_drop_int_vent_comps_eta=266,
    pressure_drop_int_non_vent_comps_sup=250,
    pressure_drop_int_non_vent_comps_eta=250,
    pressure_drop_ext_sup_nominal=250,
    pressure_drop_ext_eta_nominal=250,
    filter_section_area_sup=0.5,
    filter_section_area_eta=0.5,
    fan_section_area_sup=0.5,
    fan_section_area_eta=0.5,
    fan_eff_static_eu_327_2011_sup=0.35,
    fan_eff_static_eu_327_2011_eta=0.35,
    fan_eff_system_static_sup=0.4881,
    fan_eff_system_static_eta=0.4832,
    external_leakage_rate=0.004,
    internal_leakage_rate=0.004,
    filters_eurovent_compliance=True,
    filter_energy_class_eurovent_sup="A",
    filter_energy_class_eurovent_eta="A",
    recycling_manual_url="url://",
    has_thermal_bypass_on_hrs=True,
    has_visual_signaling_on_filters=True,
    has_alarm_on_filters=True,
    manufacturer_name="Remak",
    manufacturer_model="Some model",
)
erp_response = ErpResponse(
    comply=True,
    sfp_int=1178,
    sfp_int_lim=1241,
    hrs_thermal_eff=0.827,
    hrs_thermal_eff_lim=0.73,
    hrs_type="phex",
    has_multispeed_drive=True,
    has_variablespeed_drive=True,
    has_hrs=True,
    has_thermal_bypass_on_hrs=True,
    fan_eff_uvu=0.4881,
    fan_eff_uvu_min=None,
    has_visual_signaling_on_filters=True,
    has_alarm_on_filters=True,
    manufacturer_name="Remak",
    manufacturer_model="Some model",
    unit_class="NRVU",
    unit_type="BVU",
    airflow_nominal_sup=1,
    airflow_nominal_eta=1,
    electric_power_input_effective=155,
    face_velocity_sup=2.0,
    face_velocity_eta=2.0,
    pressure_drop_ext_sup_nominal=250,
    pressure_drop_ext_eta_nominal=250,
    pressure_drop_int_vent_comps_sup=307,
    pressure_drop_int_vent_comps_eta=266,
    pressure_drop_int_non_vent_comps_sup=250,
    pressure_drop_int_non_vent_comps_eta=250,
    fan_eff_static_eu_327_2011_sup=0.35,
    fan_eff_static_eu_327_2011_eta=0.35,
    external_leakage_rate=0.004,
    internal_leakage_rate=0.004,
    filters_en779_compliance=True,
    filter_energy_class_eurovent_sup="A",
    filter_energy_class_eurovent_eta="A",
    recycling_manual_url="url://",
    warnings=None,
    errors=None,
)
assert attr.asdict(
    validate_ahu(erp_request)
) == attr.asdict(erp_response)
```
