forgot_password_mail_template = {
    "url": "/messages",
    "method": "POST",
    "data": {
        "from": "Hermes <hermes@amphora.digital>",
        "subject": "You forgot your Amphora password",
        "text": "Someone initiated forgot Amphora password procedure. "
    }
}

verify_user_mail_template = {
    "url": "/messages",
    "method": "POST",
    "data": {
        "from": "Hermes <hermes@amphora.digital>",
        "subject": "You forgot your Amphora password",
        "text": "Thank you for registering on amphora.digital platform. "
                "You account is already now, but you need to verify it via token. "
    }
}
