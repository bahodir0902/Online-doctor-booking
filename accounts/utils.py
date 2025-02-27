import random
import uuid

def generate_random_code():
    code = str(random.randint(1000, 9999))
    return code

def generate_unique_username():
    # Generate a random unique identifier and trim it if needed
    return uuid.uuid4().hex[:30]