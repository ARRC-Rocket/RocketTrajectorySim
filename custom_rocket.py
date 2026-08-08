from rocketpy import Rocket
from rocketpy.motors import CylindricalTank, Fluid, HybridMotor
from rocketpy.motors.tank import MassFlowRateBasedTank
from rocketpy.sensors import Accelerometer, Barometer, GnssReceiver, Gyroscope

# A hollow grain's mass goes as (outer^2 - inner^2), so an outer radius under
# the inner one is a negative mass. RocketPy 1.13 accepts it in silence: the
# motor carried -0.623 kg of fuel and the flight apogeed at 200 m, not 131 m.
GRAIN_OUTER_RADIUS = 0.0843
GRAIN_INITIAL_INNER_RADIUS = 0.0295


def _check_grain_geometry(outer_radius, inner_radius):
    """A hollow grain needs a positive bore strictly inside the outer wall."""
    if not 0 < inner_radius < outer_radius:
        raise ValueError(
            "grain geometry is impossible: need "
            "0 < grain_initial_inner_radius < grain_outer_radius, got "
            f"inner={inner_radius}, outer={outer_radius}"
        )


def create_custom_rocket():
    """
    Create a custom rocket with a hybrid motor and an oxidizer tank.
    """

    _check_grain_geometry(GRAIN_OUTER_RADIUS, GRAIN_INITIAL_INNER_RADIUS)

    tank_shape = CylindricalTank(0.133, height=0.83)
    oxidizer_tank = MassFlowRateBasedTank(
        name="oxidizer_tank",
        geometry=tank_shape,
        flux_time=(0, 30),
        initial_liquid_mass=13.9,
        initial_gas_mass=2.13,
        liquid_mass_flow_rate_in=0,
        liquid_mass_flow_rate_out=0.425,
        gas_mass_flow_rate_in=0,
        gas_mass_flow_rate_out=0,
        liquid=Fluid(name="HTP", density=1390),
        gas=Fluid(name="N2", density=68),
    )

    hybrid_motor = HybridMotor(
        thrust_source=1080,
        dry_mass=0,
        dry_inertia=(0, 0, 0),
        # 0.15 in the official scenario, not 0.015. Inert while dry_mass is 0,
        # since this is a mass-weighted position, but a 10x error waiting for
        # the day that mass stops being zero.
        center_of_dry_mass_position=0.15,
        burn_time=(0, 30),
        reshape_thrust_curve=False,
        grain_number=1,
        grain_separation=0,
        grain_outer_radius=GRAIN_OUTER_RADIUS,
        grain_initial_inner_radius=GRAIN_INITIAL_INNER_RADIUS,
        grain_initial_height=0.2757,
        grain_density=900,
        nozzle_radius=0.04425,
        throat_radius=0.023,
        interpolation_method="linear",
        nozzle_position=0,
        grains_center_of_mass_position=0.13785,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    # Add tank to motor
    hybrid_motor.add_tank(tank=oxidizer_tank, position=1.4)

    rocket = Rocket(
        radius=0.22,
        mass=70,
        inertia=(26.54, 26.38, 1.6312),
        center_of_mass_without_motor=0,
        power_off_drag=0.25,
        power_on_drag=0.25,
        coordinate_system_orientation="tail_to_nose",
    )

    rocket.add_motor(hybrid_motor, position=-0.8)
    rocket.add_nose(
        length=1,
        kind="vonKarman",
        position=1.5,
    )
    rocket.add_trapezoidal_fins(
        n=4,
        span=0.4,
        root_chord=0.5,
        tip_chord=0.2,
        position=-0.3,
    )

    gyro = Gyroscope(sampling_rate=100)
    accelerometer = Accelerometer(sampling_rate=100)
    gnss = GnssReceiver(sampling_rate=100)
    baro = Barometer(sampling_rate=100)
    rocket.add_sensor(gyro, position=0)
    rocket.add_sensor(accelerometer, position=0)
    rocket.add_sensor(gnss, position=0)
    rocket.add_sensor(baro, position=0)
    # rocket.draw()

    return rocket
