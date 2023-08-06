from .data_structs import ErpRequest, ErpResponse
from .erp_utils import (
    check_erp_compliance,
    fan_eff_uvu_min,
    filters_correction,
    hrs_eff_bonus,
    hrs_thermal_eff_min,
    sfp_int,
    sfp_int_limit,
    sfp_validation,
)


def validate_ahu(r: ErpRequest) -> ErpResponse:
    """Validate the air handling unit per Ecodesign.

    Ecodesign reuirments correcponds to the
    (EU) No 1253/2014 regulation and assess the
    air handling unit weather it is complied with
    the regulation or not.

    The response information should consist of data
    which is prescribed in the regulation. The
    ErpReponse object contains all these data.

    Example:
    >>> from erp_air import (
    >>>     validate_ahu,
    >>>     ErpResponse,
    >>>     ErpRequest
    >>> )

    >>> erp_request = ErpRequest(
    >>>     unit_class="nrvu",
    >>>     unit_type="bvu",
    >>>     has_medium_filter_eta=True,
    >>>     has_fine_filter_sup=True,
    >>>     hrs_type="phex",
    >>>     hrs_thermal_eff_en308=0.827,
    >>>     has_multispeed_drive=True,
    >>>     has_variablespeed_drive=True,
    >>>     airflow_nominal_sup=1,
    >>>     airflow_nominal_eta=1,
    >>>     electric_power_input_effective=155,
    >>>     pressure_drop_int_vent_comps_sup=307,
    >>>     pressure_drop_int_vent_comps_eta=266,
    >>>     pressure_drop_int_non_vent_comps_sup=250,
    >>>     pressure_drop_int_non_vent_comps_eta=250,
    >>>     pressure_drop_ext_sup_nominal=250,
    >>>     pressure_drop_ext_eta_nominal=250,
    >>>     filter_section_area_sup=0.5,
    >>>     filter_section_area_eta=0.5,
    >>>     fan_section_area_sup=0.5,
    >>>     fan_section_area_eta=0.5,
    >>>     fan_eff_static_eu_327_2011_sup=0.35,
    >>>     fan_eff_static_eu_327_2011_eta=0.35,
    >>>     fan_eff_system_static_sup=0.4881,
    >>>     fan_eff_system_static_eta=0.4832,
    >>>     external_leakage_rate=0.004,
    >>>     internal_leakage_rate=0.004,
    >>>     filters_eurovent_compliance=True,
    >>>     filter_energy_class_eurovent_sup="A",
    >>>     filter_energy_class_eurovent_eta="A",
    >>>     recycling_manual_url="url://",
    >>>     has_thermal_bypass_on_hrs=True,
    >>>     has_visual_signaling_on_filters=True,
    >>>     has_alarm_on_filters=True,
    >>>     manufacturer_name="Remak",
    >>>     manufacturer_model="Some model",
    >>> )
    >>> erp_response = ErpResponse(
    >>>     comply=True,
    >>>     sfp_int=1178,
    >>>     sfp_int_lim=1241,
    >>>     hrs_thermal_eff=0.827,
    >>>     hrs_thermal_eff_lim=0.73,
    >>>     hrs_type="phex",
    >>>     has_multispeed_drive=True,
    >>>     has_variablespeed_drive=True,
    >>>     has_hrs=True,
    >>>     has_thermal_bypass_on_hrs=True,
    >>>     fan_eff_uvu=0.4881,
    >>>     fan_eff_uvu_min=None,
    >>>     has_visual_signaling_on_filters=True,
    >>>     has_alarm_on_filters=True,
    >>>     manufacturer_name="Remak",
    >>>     manufacturer_model="Some model",
    >>>     unit_class="NRVU",
    >>>     unit_type="BVU",
    >>>     airflow_nominal_sup=1,
    >>>     airflow_nominal_eta=1,
    >>>     electric_power_input_effective=155,
    >>>     face_velocity_sup=2.0,
    >>>     face_velocity_eta=2.0,
    >>>     pressure_drop_ext_sup_nominal=250,
    >>>     pressure_drop_ext_eta_nominal=250,
    >>>     pressure_drop_int_vent_comps_sup=307,
    >>>     pressure_drop_int_vent_comps_eta=266,
    >>>     pressure_drop_int_non_vent_comps_sup=250,
    >>>     pressure_drop_int_non_vent_comps_eta=250,
    >>>     fan_eff_static_eu_327_2011_sup=0.35,
    >>>     fan_eff_static_eu_327_2011_eta=0.35,
    >>>     external_leakage_rate=0.004,
    >>>     internal_leakage_rate=0.004,
    >>>     filters_en779_compliance=True,
    >>>     filter_energy_class_eurovent_sup="A",
    >>>     filter_energy_class_eurovent_eta="A",
    >>>     recycling_manual_url="url://",
    >>>     warnings=None,
    >>>     errors=None,
    >>> )
    >>> assert attr.asdict(
    >>>     validate_ahu(erp_request)
    >>> ) == attr.asdict(erp_response)
    """
    if r.hrs_type:
        r._hrs_eff_bonus = hrs_eff_bonus(
            r.hrs_type, r.hrs_thermal_eff_en308
        )

    r._sfp_validation = sfp_validation(
        r.unit_type, r.has_fine_filter_sup
    )
    if r._sfp_validation:
        airflow_nominal = (
            r.airflow_nominal_sup
            if r.unit_type == "uvu"
            else (
                r.airflow_nominal_sup
                + r.airflow_nominal_eta
            )
            / 2
        )
        r._sfp_int_lim = sfp_int_limit(
            r.unit_type,
            r.hrs_type,
            airflow_nominal,
            r._hrs_eff_bonus,
            filters_correction(
                r.has_medium_filter_eta,
                r.has_fine_filter_sup,
            ),
            r.has_fine_filter_sup,
        )
        r._sfp_int = (
            (
                sfp_int(
                    r.pressure_drop_int_vent_comps_sup,
                    r.fan_eff_system_static_sup,
                )
                + sfp_int(
                    r.pressure_drop_int_vent_comps_eta,
                    r.fan_eff_system_static_eta,
                )
            )
            if r.unit_type == "bvu"
            else sfp_int(
                r.pressure_drop_int_vent_comps_sup,
                r.fan_eff_system_static_sup,
            )
        )
    else:
        r._fan_eff_sup_min = fan_eff_uvu_min(
            r.electric_power_input_effective
        )
    return ErpResponse(
        comply=check_erp_compliance(
            unit_type=r.unit_type,
            hrs_type=r.hrs_type,
            has_variablespeed_drive=r.has_variablespeed_drive,
            has_multispeed_drive=r.has_multispeed_drive,
            has_fine_filter_sup=r.has_fine_filter_sup,
            sfp_int=r._sfp_int,
            sfp_int_lim=r._sfp_int_lim,
            filters_eurovent_compliance=r.filters_eurovent_compliance,
            fan_eff_uvu=r.fan_eff_system_static_sup,
            fan_eff_uvu_min=r._fan_eff_sup_min,
            hrs_eff_bonus=r._hrs_eff_bonus,
            has_alarm_on_filters=r.has_alarm_on_filters,
            has_visual_signaling_on_filters=r.has_visual_signaling_on_filters,
        ),
        sfp_int=r._sfp_int,
        sfp_int_lim=r._sfp_int_lim,
        hrs_thermal_eff=r.hrs_thermal_eff_en308,
        hrs_thermal_eff_lim=(
            hrs_thermal_eff_min(r.hrs_type)
            if r.hrs_type
            else None
        ),
        hrs_type=r.hrs_type,
        has_multispeed_drive=r.has_multispeed_drive,
        has_variablespeed_drive=r.has_variablespeed_drive,
        has_hrs=True if r.hrs_type else False,
        has_thermal_bypass_on_hrs=r.has_thermal_bypass_on_hrs,
        fan_eff_uvu=r.fan_eff_system_static_sup,
        fan_eff_uvu_min=r._fan_eff_sup_min,
        has_visual_signaling_on_filters=r.has_visual_signaling_on_filters,
        has_alarm_on_filters=r.has_alarm_on_filters,
        manufacturer_name=r.manufacturer_name,
        manufacturer_model=r.manufacturer_model,
        unit_class=r.unit_class.upper(),
        unit_type=r.unit_type.upper(),
        airflow_nominal_sup=r.airflow_nominal_sup,
        airflow_nominal_eta=r.airflow_nominal_eta,
        electric_power_input_effective=r.electric_power_input_effective,
        face_velocity_sup=(
            r.airflow_nominal_sup
            / r.filter_section_area_sup
            if r.has_fine_filter_sup
            else r.airflow_nominal_sup
            / r.fan_section_area_sup
        ),
        face_velocity_eta=(
            (
                r.airflow_nominal_eta
                / r.filter_section_area_eta
                if r.has_medium_filter_eta
                else r.airflow_nominal_eta
                / r.fan_section_area_eta
            )
            if r.unit_type == "bvu"
            else None
        ),
        pressure_drop_ext_sup_nominal=r.pressure_drop_ext_sup_nominal,
        pressure_drop_ext_eta_nominal=r.pressure_drop_ext_eta_nominal,
        pressure_drop_int_vent_comps_sup=r.pressure_drop_int_vent_comps_sup,
        pressure_drop_int_vent_comps_eta=r.pressure_drop_int_vent_comps_eta,
        pressure_drop_int_non_vent_comps_sup=r.pressure_drop_int_non_vent_comps_sup,
        pressure_drop_int_non_vent_comps_eta=r.pressure_drop_int_non_vent_comps_eta,
        fan_eff_static_eu_327_2011_sup=r.fan_eff_static_eu_327_2011_sup,
        fan_eff_static_eu_327_2011_eta=r.fan_eff_static_eu_327_2011_eta,
        external_leakage_rate=r.external_leakage_rate,
        internal_leakage_rate=r.internal_leakage_rate,
        filters_en779_compliance=r.filters_eurovent_compliance,
        filter_energy_class_eurovent_sup=r.filter_energy_class_eurovent_sup,
        filter_energy_class_eurovent_eta=r.filter_energy_class_eurovent_eta,
        recycling_manual_url=r.recycling_manual_url,
    )
