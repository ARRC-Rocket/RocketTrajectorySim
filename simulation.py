import base64
import os

import matplotlib.pyplot as plt
from rocketpy import Environment, Flight

from custom_rocket import create_custom_rocket

plt.style.use("seaborn-v0_8-colorblind")

output_path = os.path.join(os.path.dirname(__file__), "_output/")


def _encode_image(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f'<img src="data:image/png;base64,{encoded}">'


def main():
    """Create and run a simulation then pack to report"""

    # Create environment
    env = Environment(
        gravity=9.78825,  # 大劉南/Q037/一等水準點 內政部103年公告二等重力點測量成果(計劃年度：2014) 全國衛星追蹤站暨基本控制點查詢系統
        date=(2026, 8, 1, 7),  # 15:00 local time
        latitude=22.17492027,  # 國家科學及技術委員會短期科研探空火箭發射場域
        longitude=120.8926564,
        elevation=31.9331,
        datum="WGS84",
        timezone="UTC",
        max_expected_height=10000,
    )
    env.set_atmospheric_model(type="Windy", file="ECMWF")
    env_plot_path = output_path + "env.png"
    env.plots.info(filename=env_plot_path)

    # Create rocket from script
    custom_rocket = create_custom_rocket()

    # Simulate a flight
    test_flight = Flight(
        rocket=custom_rocket,
        environment=env,
        inclination=85,
        heading=90,
        rail_length=12,
    )
    flight_plot_path = output_path + "trajectory_3d.png"
    test_flight.plots.trajectory_3d(filename=flight_plot_path)

    # Create report
    html_report = f"""
    <html>
        <body>
            <h1>Environment</h1>
            {_encode_image(env_plot_path)}
            <h1>Flight 3D</h1>
            {_encode_image(flight_plot_path)}
        </body>
    </html>
    """

    with open(output_path + "report.html", "w", encoding="utf+8") as f:
        f.write(html_report)


if __name__ == "__main__":
    main()
