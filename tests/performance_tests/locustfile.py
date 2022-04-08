from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get('/')

    @task
    def publicBoard(self):
        self.client.get('/publicBoard/')

    @task
    def login(self):
        self.client.post("/showSummary/", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get(r'/book/Spring%20Festival/Simply%20Lift/')

    @task
    def purchase(self):
        self.client.post('/purchasePlaces/', data={
            'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '3'
            })
