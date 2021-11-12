import prefect


class HttpTask(prefect.Task):
    """
    HTTP request tasks
    """

    def __init__(self, session, *args, **kwargs):
        self.session = session
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        return self.session.request(*args, **kwargs)
