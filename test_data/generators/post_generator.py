from faker import Faker

from models.posts.requests import CreatePostRequest

faker = Faker('ru_RU')

def generate_post() -> CreatePostRequest:
    return CreatePostRequest(content=faker.text(max_nb_chars=70))

