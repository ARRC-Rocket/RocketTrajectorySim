import matplotlib.pyplot as plt

from rocketpy import Environment, Flight

from custom_rocket import create_custom_rocket

plt.style.use("seaborn-v0_8-colorblind")


def main():
    """Run a simulation"""
    env = Environment(
        gravity=9.80665,
        date=(2023, 10, 13, 14),
        latitude=39.388692,
        longitude=-8.287814,
        elevation=130,
        datum="WGS84",
        timezone="Portugal",
    )

    env.set_atmospheric_model(type="Windy", file="ECMWF")
    env.max_expected_height = 4000
    env.info()

    custom_rocket = create_custom_rocket()

    test_flight = Flight(
        rocket=custom_rocket,
        environment=env,
        inclination=85,
        heading=90,
        rail_length=12,
    )
    test_flight.plots.trajectory_3d()


if __name__ == "__main__":
    main()
