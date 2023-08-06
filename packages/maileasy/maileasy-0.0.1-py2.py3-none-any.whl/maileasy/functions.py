import json
import smtplib
import warnings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gnupg


def pgp_encrypt(pgp_key, text, gpgbinary="gpg", **kwargs):
    """Encrypts text with a PGP public key

    Args:
        pgp_key (str, path-like): Path to ASCII PGP key file
        text (str): Text to encrypt
        gpgbinary (str, path-like): path to GPG binary (default: "gpg")
    kwargs:
        kwargs to pass to gnupg.GPG.encrypt

    Returns:
        encrypted (txt): PGP-encrypted text
    """
    if "DOCTYPE" in text:
        warnings.warn("html text will not be rendered after decryption")
    gpg = gnupg.GPG(gpgbinary=gpgbinary)
    gpg.encoding = "utf-8"

    with open(pgp_key) as f:
        key = gpg.import_keys(f.read())

    if len(key.fingerprints) == 0:
        raise ValueError(key.problem_reason)

    encrypted = gpg.encrypt(text, key.fingerprints,
                            always_trust=True, **kwargs)

    return str(encrypted)


def send(subject, body, fromaddr, config="maileasy_config.json", is_html=False, toaddr=None):
    """Sends email using the specified arguments

    Args:
        subject (str) : email subject
        body (str) : email body
        fromaddr (str, list) : "From" address(es)
        config (str, path-like): path to .json file with account information
        is_html (bool) : Whether body is in HTML format (default: False)
        toaddr (str) : "To" address (default: fromaddr)
    """
    # get credentials
    with open(config) as f:
        accounts = json.load(f)
    account = accounts[fromaddr]
    username = account["username"]
    pw = account["pw"]
    smtp = account["smtp"]
    port = account["port"]

    # configuration
    server = smtplib.SMTP(smtp, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, pw)

    # set email fields

    toaddr = fromaddr if toaddr is None else toaddr
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
    text = msg.as_string()

    # Send email
    server.sendmail(fromaddr, toaddr, text)
