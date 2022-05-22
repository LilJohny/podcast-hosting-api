from copy import deepcopy

import httpx

from settings import MAILGUN_BASE_URL, MAILGUN_API_KEY


async def send_email(user_email: str, mail_content) -> int:
    mail_content_to = deepcopy(mail_content)
    mail_content_to["data"]["to"] = user_email
    async with httpx.AsyncClient(base_url=MAILGUN_BASE_URL, auth=("api", MAILGUN_API_KEY)) as client:
        request = client.build_request(**mail_content_to)
        response = await client.send(request)
        response.raise_for_status()
    return response.status_code


def prepare_email(receiver_email: str, token: str, mail_content_template: dict) -> dict:
    mail_content = deepcopy(mail_content_template)
    mail_content["data"]["to"] = receiver_email
    mail_content["data"]["text"] += f" Use this token {token} to complete."
    return mail_content
