# RocketTrajectorySim

This repositry hosts a rocket trajectory simulation server that runs a simulation on pipeline.

## Tutorial

- Offline:

    ```shell
    git clone https://github.com/ARRC-Rocket/RocketTrajectorySim
    cd RocketTrajectorySim
    python -m pip install uv
    # Update the parameters in `custom_rocket.py`
    uv run python simulation.py
    # view _output/report.html
    ```

- Online:
  - Update the parameters in custom_rocket.py
  - Send a PR to RocketTrajectorySim
  - View the artifact in the PR comment once the GitHub action is complete
