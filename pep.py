import smtplib, ssl

port = 465  # For SSL
p = "fyhh euxi mwoo ugru"
smtp_server = "smtp.gmail.com"
sender_email = "ximyb5@gmail.com"  # Enter your address
receiver_email = "ximyb5@hotmail.com"  # Enter receiver address
password = "fyhh euxi mwoo ugru"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)