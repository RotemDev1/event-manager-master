import time
from django.core.mail import send_mail



def sendResetPasswordEmail(email):
    milliseconds = int(round(time.time() * 1000 + 24 *
                             60 * 60 * 1000))  # next 24 hours
    key = generateKey(email, milliseconds)
    link = f'http://localhost:8000/reset/password?email={email}&key={key}&u={milliseconds}'
    send_mail(
        subject='Reset Password',
        message='You received this email because you clicked reset password.\n' +
        'Copy the following link to address in browser:\n{link}\n' +
        'The link will be available for next 24 hours' +
        'If you did not request a reset password, please ignore this email',
        recipient_list=[email],
        html_message='You received this email because you clicked reset password.<br/>' +
        'Please click the following link to reset the password:<br/>' +
        f'<a href={link}>Click here</a><br/>' +
        f'If you don\'t see the link, copy it to address:<br/>{link}<br/>' +
        'The link will be available for next 24 hours' +
        'If you did not request a reset password, please ignore this email',
        fail_silently=False,
        from_email=''
    )


def generateKey(email, t):
    t = int(t)
    at = email.index('@')
    key = email[0:at]
    key2 = email[(at + 1):]
    temp = t
    passkey = ''
    for i , _ in enumerate(key):
        passkey += chr((ord(key[i]) + 17) % 26 + 65)
        passkey += chr(((ord(key[i]) + (temp % 10)) % 26) + 65)
        temp = temp // 2
    temp = t
    for i , _ in enumerate(key2):
        passkey += chr((ord(key2[i]) + 13) % 26 + 65)
        passkey += chr(((ord(key2[i]) + (temp // 5) % 10) % 26) + 65)
        temp = temp // 2
    return passkey


def timeIsValid(t):
    t = int(t)
    start = int(round(time.time() * 1000))
    end = int(round(time.time() * 1000 + 24 *
                    60 * 60 * 1000))
    return t >= start and t <= end
