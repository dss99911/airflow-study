from airflow.operators.email import EmailOperator


# section/key [smtp/smtp_user] not found in config
# smtp configuration required
def make_email_operator(email: str, email_info):
    return EmailOperator(
        task_id='send_email', to=email, subject=email_info['subject'], html_content=email_info['body']
    )
