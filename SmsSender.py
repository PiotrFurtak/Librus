from twilio.rest import Client
from TomorrowInfo import output
account_sid = input("account_sid: ")
auth_token = input("auth_token: ")
client = Client(account_sid, auth_token)

message = client.messages.create(
    body=output,
    from_=input("from: "),
    to=input("to: "),
)

print(message.body)
input()