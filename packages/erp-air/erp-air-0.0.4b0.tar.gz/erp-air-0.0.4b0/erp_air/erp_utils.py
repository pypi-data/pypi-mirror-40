"""Different supplement utils for ErP validation."""
import math


def filters_correction(
    has_medium_filter_eta: bool,
    has_fine_filter_sup: bool,
) -> int:
    """Calculate the filters correction factor.

    In accordance with ANEX IX.2 of the regualation.

    :raises KeyError: in case of wrong type inputs
    """
    answers_mtx = {
        (True, True): 0,
        (True, False): 190,
        (False, False): 340,
        (False, True): 150,
    }
    return answers_mtx[
        (has_medium_filter_eta, has_fine_filter_sup)
    ]


def hrs_thermal_eff_min(hrs_type: str) -> float:
    """Calculates minimum thermal efficiency of hrs.

    :param hrs_type: should be in "rac", "phex" or
        "rw".
    :raises ValueError: if the hrs_type is not from
        available choice
    """
    if hrs_type not in ("rw", "phex", "rac"):
        raise ValueError()
    return 0.68 if hrs_type == "rac" else 0.73


def hrs_eff_bonus(
    hrs_type: str, hrs_thermal_eff_en308: float
) -> float:
    """Calculates the efficiency bonus of the hrs.

    In accordance with ANEX III.2.2 of the regulation.

    :param hrs_type: should be in "rac", "phex" or
        "rw".
    :param hrs_thermal_eff_en308: thermal (sensible,
        dry) efficincy of the heat exchanger at
        balanced airflow in accordance with EN308 std.
    :raises TypeError: if inputs of a wrong type
        available choice
    """
    if hrs_type not in ("rw", "phex", "rac"):
        raise TypeError()

    if not isinstance(hrs_thermal_eff_en308, float):
        raise TypeError()

    return (
        hrs_thermal_eff_en308
        - hrs_thermal_eff_min(hrs_type)
    ) * 3000


def sfp_int_limit(
    unit_type: str,
    hrs_type: str,
    nominal_airflow: float,
    hrs_eff_bonus: float,
    filters_correction: int,
    has_fine_filter: bool = False,
) -> int:
    """Calc unit internal specific fan power limit.

    :param unit_type: may be `bvu` - biderectional
        ventilation unit or `uvu` - unidirectional
        ventilation unit
    :param hrs_type: should be in "rac", "phex" or
        "rw"
    :param nominal_airflow: the declared design flow
        rate of an NRVU at standard air conditions
        20 °C and 101 325 Pa, whereby the unit is
        installed complete (for example, including
        filters) and according to the manufacturer
        instructions. When sup and eta airflows are
        different - takes as a mean of them.
    :param hrs_eff_bonus: efficiency bonus of the heat
        recovery system. This is a correction factor
        taking account of the fact that more efficient
        heat recovery causes more pressure drops
        requiring more specific fan power
    :param filters_correction: is a correction value
        to be applied if a unit deviates from the
        reference configuration of a BVU
    :param has_fine_filter: does the unit has the fine
        filter
    :raises ValueError: if unit is not intended for
        sfp validation (i.e. uvu without filter).
    :raises KeyError: if unit_type or hrs_type or
        has_fine_filter is not from possible choice
    """
    if unit_type == "uvu" and not has_fine_filter:
        raise ValueError()

    coeff_mtx = {
        ("bvu", "rac", True): (
            1600,
            -300,
            filters_correction,
            hrs_eff_bonus,
        ),
        ("bvu", "rac", False): (
            1300,
            0,
            filters_correction,
            hrs_eff_bonus,
        ),
        ("bvu", "rw", True): (
            1100,
            -300,
            filters_correction,
            hrs_eff_bonus,
        ),
        ("bvu", "rw", False): (
            800,
            0,
            filters_correction,
            hrs_eff_bonus,
        ),
        ("bvu", "phex", True): (
            1100,
            -300,
            filters_correction,
            hrs_eff_bonus,
        ),
        ("bvu", "phex", False): (
            800,
            0,
            filters_correction,
            hrs_eff_bonus,
        ),
        # fmt: off
        ("uvu", None, False): (
            230,
            0,
            0,
            0
        ),
        ("uvu", None, True): (
            230,
            0,
            0,
            0
        ),
    }
    # fmt: on

    try:
        x1, x2, F, E = coeff_mtx[
            (unit_type, hrs_type, nominal_airflow < 2)
        ]
    except KeyError as err:
        raise KeyError(
            err,
            "Impossible combination for "
            "unit_type, hrs_type, nominal_airflow < 2",
        )
    return x1 + E + x2 * nominal_airflow / 2 - F


def sfp_validation(
    unit_type: str, has_fine_filter_sup: bool
) -> bool:
    """Check if sf validation is required.

    :param unit_type: may be `bvu` - biderectional
        ventilation unit or `uvu` - unidirectional
        ventilation unit
    :param has_fine_filter: does the unit has the fine
        filter
    :raises KeyError: if inputs are outside of
        possible choices
    """
    answers_mtx = {
        ("bvu", True): True,
        ("bvu", False): True,
        ("uvu", True): True,
        ("uvu", False): False,
    }
    return answers_mtx[
        (unit_type, has_fine_filter_sup)
    ]


def fan_eff_uvu_min(uvu_fan_power_input_nominal):
    """Calculate the min of fan system eff.

    Calculates the minimum margin of the fan system
    total efficiency. This margin is used in erp
    validation of the unidirectional ventilation unit
    without the fine filter.

    :param uvu_fan_power_input_nominal: means the
        effective electric power input of the fan
        drives, including any motor control equipment,
        at the nominal external pressure and the
        nominal airflow
    """
    return round(
        (
            (
                6.2
                * math.log(
                    uvu_fan_power_input_nominal / 1000
                )
                + 42
            )
            / 100
            if uvu_fan_power_input_nominal <= 30000
            else 0.631
        ),
        3,
    )


def check_erp_compliance(
    unit_type: str,
    hrs_type: str,
    has_variablespeed_drive: bool,
    has_multispeed_drive: bool,
    has_fine_filter_sup: bool = False,
    sfp_int: int = None,
    sfp_int_lim: int = None,
    filters_eurovent_compliance: bool = None,
    fan_eff_uvu: float = None,
    fan_eff_uvu_min: float = None,
    hrs_eff_bonus: float = None,
    has_visual_signaling_on_filters: bool = None,
    has_alarm_on_filters: bool = None,
) -> bool:
    """Validate air handling unit compliance with ErP.

    :param unit_type: may be `bvu` - biderectional
        ventilation unit or `uvu` - unidirectional
        ventilation unit
    :param hrs_type: should be in "rac", "phex" or
        "rw"
    :param has_variablespeed_drive: means an
        electronic controller, integrated or
        functioning as one system or as a separate
        delivery with the motor and the fan, which
        continuously adapts the electrical power
        supplied to the motor in order to control
        the flow rate
    :param has_multispeed_drive: means a fan motor
        that can be operated at three or more fixed
        speeds plus zero
    :param has_fine_filter: does the unit has the fine
        filter
    :param sfp_int: internal specific fan power of
        ventilation components
    :param sfp_int_lim: maximum internal specific fan
        power of ventilation components
    :param filters_eurovent_compliance: bool = None,
    :param fan_eff_uvu: means the static efficiency
        including motor and drive efficiency of the
        individual fan(s) in the ventilation unit
        (reference configuration) determined at
        nominal air flow and nominal external pressure
        drop
    :param fan_eff_uvu_min: min margin of the
        fan_eff_uvu
    :param hrs_eff_bonus: is a correction factor
        taking account of the fact that more efficient
        heat recovery causes more pressure drops
        requiring more specific fan power
    :param has_visual_signaling_on_filters: if a
        filter unit is part of the configuration the
        product shall be equipped with a visual
        signalling or an alarm in the control system
        which shall be activated if the filter
        pressure drop exceeds the maximum allowable
        final pressure drop
    :param has_alarm_on_filters: the same as above
    """
    energy_check = False
    if sfp_int_lim and not fan_eff_uvu_min:
        energy_check = sfp_int <= sfp_int_lim
    elif fan_eff_uvu_min and not sfp_int_lim:
        energy_check = fan_eff_uvu >= fan_eff_uvu_min
    else:
        raise ValueError()

    fan_control_check = False
    if (
        has_multispeed_drive
        or has_variablespeed_drive
    ):
        fan_control_check = True

    hrs_check = True
    if unit_type == "bvu":
        if not hrs_type:
            raise ValueError()
        hrs_check = hrs_type and hrs_eff_bonus >= 0

    filters_check = True
    if has_fine_filter_sup:
        if not sfp_int_lim:
            raise ValueError()
        if not all(
            [
                isinstance(attrib, bool)
                for attrib in [
                    has_alarm_on_filters,
                    has_visual_signaling_on_filters,
                    filters_eurovent_compliance,
                ]
            ]
        ):
            raise ValueError()
        filters_check = (
            filters_eurovent_compliance
            and (
                has_visual_signaling_on_filters
                or has_alarm_on_filters
            )
        )

    return (
        energy_check
        and fan_control_check
        and hrs_check
        and filters_check
    )


def sfp_int(
    pressure_drop_int_vent_comps: int,
    fan_eff_system_static: float,
) -> int:
    """Calculate unit specific fan power for ref config.

    It is the ratio between the internal pressure drop
    of ventilation components and the fan efficiency,
    determined for the reference configuration

    :param pressure_drop_int_vent_comps: static pressure
        drop of the ventialtion componenets of the ahu
    :param fan_eff_system_static: static efficiency
        of the fan system incl. control unit determined
        at reference air handling unit configuration
    """
    return int(
        pressure_drop_int_vent_comps
        / fan_eff_system_static
    )
