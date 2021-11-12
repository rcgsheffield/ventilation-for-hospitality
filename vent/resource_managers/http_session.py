import prefect
import requests


@prefect.resource_manager
class HttpSession:
    """
    HTTP session resource manager

    Docs: Managing temporary resources
    https://docs.prefect.io/core/idioms/resource-manager.html
    """

    def __init__(self):
        pass

    def setup(self):
        return requests.Session()

    def cleanup(self, session: requests.Session):
        session.close()
