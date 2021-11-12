import vent.tasks.http_task


class GraphqlHttpTask(vent.tasks.http_task.HttpTask):
    """
    GraphQL HTTP Request task
    """

    def __init__(self, query: str, *args, **kwargs):
        self.query = query
        super().__init__(*args, **kwargs)

    @property
    def json(self) -> dict:
        return dict(query=self.query)

    def run(self):
        self.request_kwargs.update(dict(json=self.json))
        return super().run()
