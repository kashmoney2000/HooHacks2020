# Send to single device.
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAAQpo6i_8:APA91bERkpxhdzAD34vzFp35lli7L0hiTpbPCcx7a594fh_DPjiiSFi_p286OibniRXx5b4mdTrDETZT8PucpPksQ_1H7gkVcgmxnw8cs6DjhC-01d22ag-b_BFhT3mWGugeFFKsJDkV")

# OR initialize with proxies


# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "<device registration_id>"
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)