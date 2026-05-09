from faker.proxy import Faker

from models.auth.requests import RegisterRequest, LoginRequest

faker = Faker()

def generate_register() -> RegisterRequest:
    return RegisterRequest(email=faker.email(), password=faker.password(), username=faker.user_name(), name=faker.name(), last_name=faker.last_name())