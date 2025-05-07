import hashlib
import re
from datetime import datetime
from PIL import Image


def hash_password_(password):
    return hashlib.sha256(password.encode()).hexdigest()
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def string_to_12_digit_number(input_string):
    hash_object = hashlib.sha256(input_string.encode())
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex, 16)
    result = hash_int % (10 ** 12)
    return result

def image_name(product_name, article=None):
    if article:
        return f"{product_name[:50]}_{article}_{string_to_12_digit_number(product_name[:50]+article)}"
    else:
        return f"{product_name[:50]}_{string_to_12_digit_number(product_name[:50])}"


def image_to_16digit_hash(image_path, product_id):
    #product_id - нужен, т.к. для разных продуктов, может быть одна картинка. Тогда у нее будет одно название.
    #И при удалении удалится во всех продуктах
    # Load and normalize image
    with Image.open(image_path) as img:
        img = img.convert("L").resize((64, 64))  # Grayscale and resize

    # Get image bytes
    img_bytes = img.tobytes()

    # Hash using SHA-256
    hash_obj = hashlib.sha256(img_bytes)
    hash_digest = hash_obj.hexdigest()

    # Convert hex to int, then take 16 digits
    numeric_hash = int(hash_digest, 16) % (10**16)
    formatted_hash = f"{numeric_hash:016d}"

    # Format with underscores: 0000_0000_0000_0000
    return "_".join(formatted_hash[i:i+4] for i in range(0, 16, 4))+f"__{product_id}"


if __name__ == '__main__':
    pasw = hash_password_('123')
    print(pasw)

