from copy import deepcopy

import httpx

from settings import MAILGUN_BASE_URL, MAILGUN_API_KEY


async def send_email(mail_content) -> int:
    async with httpx.AsyncClient(base_url=MAILGUN_BASE_URL, auth=("api", MAILGUN_API_KEY)) as client:
        request = client.build_request(**mail_content)
        response = await client.send(request)
        response.raise_for_status()
    return response.status_code


def prepare_email(receiver_email: str, token: str, mail_content_template: dict) -> dict:
    mail_content = deepcopy(mail_content_template)
    mail_content["data"]["to"] = receiver_email
    mail_content["data"]["text"] += f"Use following token to complete: \n\n {token}"
    return mail_content
