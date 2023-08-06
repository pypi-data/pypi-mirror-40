"""Data structures which used in the package.

Attrs data classes to be used as a data structure.
They also to be used as inputs and outputs validators
for request-response objects.
"""
import attr

from .custom_validators import (
    int_or_float,
    int_or_float_or_none,
    from_zero_to_one_or_none,
)


@attr.s
class ErpResponse:
    """Erp response object.

    Some useful notation:
    sfp - specific fan power
    int - internal (do not confuse with integer:))
    ext - external
    hrs - heat recover system, i.e. rotory wheel,
        plate heat exchanger o run-around-coil
    uvu - unidirectional ventialtion unit
    bvu - bidirectional ventialtion unit
    eff - efficiency
    sup - suply side of the air handling unit
    eta - extract side of the air handling unit
    """

    comply = attr.ib()
    sfp_int = attr.ib()
    sfp_int_lim = attr.ib()
    hrs_thermal_eff = attr.ib()
    hrs_thermal_eff_lim = attr.ib()
    hrs_type = attr.ib()
    has_multispeed_drive = attr.ib()
    has_variablespeed_drive = attr.ib()
    has_hrs = attr.ib()
    has_thermal_bypass_on_hrs = attr.ib()
    fan_eff_uvu = attr.ib()
    fan_eff_uvu_min = attr.ib()
    has_visual_signaling_on_filters = attr.ib()
    has_alarm_on_filters = attr.ib()
    manufacturer_name = attr.ib()
    manufacturer_model = attr.ib()
    unit_class = attr.ib()
    unit_type = attr.ib()
    airflow_nominal_sup = attr.ib()
    airflow_nominal_eta = attr.ib()
    electric_power_input_effective = attr.ib()
    face_velocity_sup = attr.ib()
    face_velocity_eta = attr.ib()
    pressure_drop_ext_sup_nominal = attr.ib()
    pressure_drop_ext_eta_nominal = attr.ib()
    pressure_drop_int_vent_comps_sup = attr.ib()
    pressure_drop_int_vent_comps_eta = attr.ib()
    pressure_drop_int_non_vent_comps_sup = attr.ib()
    pressure_drop_int_non_vent_comps_eta = attr.ib()
    fan_eff_static_eu_327_2011_sup = attr.ib()
    fan_eff_static_eu_327_2011_eta = attr.ib()
    external_leakage_rate = attr.ib()
    internal_leakage_rate = attr.ib()
    filters_en779_compliance = attr.ib()
    filter_energy_class_eurovent_sup = attr.ib()
    filter_energy_class_eurovent_eta = attr.ib()
    recycling_manual_url = attr.ib()
    warnings = attr.ib(default=None)
    errors = attr.ib(default=None)


@attr.s
class ErpRequest:
    """Erp request object.

    Some useful notation:
    nrvu - non-residential ventialtion unit
    sfp - specific fan power
    int - internal (do not confuse with integer:))
    ext - external
    hrs - heat recover system, i.e. rotory wheel,
        plate heat exchanger o run-around-coil
    rac - run-around coil heat recovery
    rw - rotory wheel heat recovery
    phex - plate heat exchnager heat recovery
    uvu - unidirectional ventialtion unit
    bvu - bidirectional ventialtion unit
    eff - efficiency
    sup - suply side of the air handling unit
    eta - extract side of the air handling unit
    """

    unit_class = attr.ib(
        validator=attr.validators.in_(["nrvu"])
    )
    unit_type = attr.ib(
        validator=attr.validators.in_(["bvu", "uvu"])
    )
    has_medium_filter_eta = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    has_fine_filter_sup = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    hrs_type = attr.ib(
        validator=attr.validators.in_(
            ["rac", "rw", "phex", None]
        )
    )
    hrs_thermal_eff_en308 = attr.ib(
        validator=from_zero_to_one_or_none
    )
    has_multispeed_drive = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    has_variablespeed_drive = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    has_visual_signaling_on_filters = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    has_alarm_on_filters = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    manufacturer_name = attr.ib(
        validator=attr.validators.instance_of(str)
    )
    manufacturer_model = attr.ib(
        validator=attr.validators.instance_of(str)
    )
    airflow_nominal_sup = attr.ib(
        validator=int_or_float
    )
    airflow_nominal_eta = attr.ib(
        validator=int_or_float_or_none
    )
    electric_power_input_effective = attr.ib(
        validator=int_or_float
    )
    pressure_drop_int_vent_comps_sup = attr.ib(
        validator=int_or_float
    )
    pressure_drop_int_vent_comps_eta = attr.ib(
        validator=int_or_float_or_none
    )
    pressure_drop_int_non_vent_comps_sup = attr.ib(
        validator=int_or_float
    )
    pressure_drop_int_non_vent_comps_eta = attr.ib(
        validator=int_or_float_or_none
    )
    pressure_drop_ext_sup_nominal = attr.ib(
        validator=int_or_float
    )
    pressure_drop_ext_eta_nominal = attr.ib(
        validator=int_or_float_or_none
    )
    filter_section_area_sup = attr.ib(
        validator=int_or_float
    )
    filter_section_area_eta = attr.ib(
        validator=int_or_float_or_none
    )
    fan_section_area_sup = attr.ib(
        validator=int_or_float
    )
    fan_section_area_eta = attr.ib(
        validator=int_or_float_or_none
    )
    fan_eff_static_eu_327_2011_sup = attr.ib(
        validator=int_or_float
    )
    fan_eff_static_eu_327_2011_eta = attr.ib(
        validator=int_or_float_or_none
    )
    fan_eff_system_static_sup = attr.ib(
        validator=int_or_float
    )
    fan_eff_system_static_eta = attr.ib(
        validator=int_or_float_or_none
    )
    external_leakage_rate = attr.ib(
        validator=int_or_float
    )
    internal_leakage_rate = attr.ib(
        validator=int_or_float
    )
    filters_eurovent_compliance = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    filter_energy_class_eurovent_sup = attr.ib(
        validator=attr.validators.in_(list("ABCDEFG"))
    )
    filter_energy_class_eurovent_eta = attr.ib(
        validator=attr.validators.in_(
            list("ABCDEFG") + [None]
        )
    )
    recycling_manual_url = attr.ib(
        validator=attr.validators.instance_of(str)
    )
    has_thermal_bypass_on_hrs = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    has_visual_signaling_on_filters = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    has_alarm_on_filters = attr.ib(
        validator=attr.validators.instance_of(bool)
    )
    manufacturer_name = attr.ib(
        validator=attr.validators.instance_of(str)
    )
    manufacturer_model = attr.ib(
        validator=attr.validators.instance_of(str)
    )

    _hrs_eff_bonus = attr.ib(default=None)
    _sfp_int_lim = attr.ib(default=None)
    _sfp_int = attr.ib(default=None)
    _fan_eff_sup_min = attr.ib(default=None)
    _sfp_validation = attr.ib(default=None)
