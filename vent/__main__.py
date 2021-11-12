import vent.settings
import vent.flows.ventilation


def main():
    vent.flows.ventilation.flow.run(
        url=vent.settings.URL,
        workspace_id=vent.settings.WORKSPACE_ID,
        fields=vent.settings.FIELDS,
    )


if __name__ == '__main__':
    main()
