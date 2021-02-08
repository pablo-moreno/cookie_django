import requests
from django.core.files.temp import NamedTemporaryFile


def get_and_save_user_picture(url: str, user):
    response = requests.get(url)

    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        user.picture.save(f"{user.id}.jpg", File(img_temp))
        user.save()
