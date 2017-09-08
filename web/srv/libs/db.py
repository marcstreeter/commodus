from tornado.gen import convert_yielded


class Query:
    def __init__(self, session, sql, params):
        self.session = session
        self.sql = sql
        self.params = params

    async def __aenter__(self):
        self.results = await convert_yielded(
            self.session.query(
                sql=self.sql,
                parameters=self.params
            )
        )

        return self.results

    async def __aexit__(self, exc_type, exc, tb):
        await self.results.free()