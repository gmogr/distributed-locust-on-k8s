from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    # Simulate a user waiting between 1 and 3 seconds between tasks
    wait_time = between(1, 3)

    @task
    def index_page(self):
        self.client.get("/")