import prefect
import requests


class HttpTask(prefect.Task):
    """
    HTTP request tasks

    Docs: Subclassing the Task class
    https://docs.prefect.io/core/advanced_tutorials/task-guide.html#subclassing-the-task-class
    """

    def __init__(self, url: str, session: requests.Session = None,
                 method: str = None, **kwargs):
        self.url = url
        self.method = method or 'GET'
        self.session = session
        super().__init__(**kwargs)

    def run(self) -> requests.Response:
        session = self.session or requests.Session()
        response = session.request(method=self.method, url=self.url)
        self.logger.info(f"HTTP {response.status_code} {response.url}")
        try:
            response.raise_for_status()
        except requests.HTTPError:
            self.logger.error(response.text)
            raise
        return response
