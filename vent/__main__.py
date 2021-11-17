"""
Execute data pipeline
"""

import vent.settings
import vent.flows.ventilation


def main():
    # Run ventilation-for-hospitality workflow
    vent.flows.ventilation.flow.run(
        parameters=dict(
            url=vent.settings.URL,
            workspace_id=vent.settings.WORKSPACE_ID,
            fields=vent.settings.FIELDS,
        )
    )


if __name__ == '__main__':
    main()
