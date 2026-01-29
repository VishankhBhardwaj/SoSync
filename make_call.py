import os
from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)



def _get_client_and_config():

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_from = os.getenv("TWILIO_PHONE_NUMBER")
        target_number = os.getenv("SOS_TARGET_NUMBER")

        if not account_sid or not auth_token:
                raise RuntimeError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in the environment")
        if not twilio_from or not target_number:
               raise RuntimeError("TWILIO_PHONE_NUMBER and SOS_TARGET_NUMBER must be set in the environment")
            

        client = Client(account_sid, auth_token)
        return client,twilio_from,target_number
def call_sos(message: str):
    client,twilio_from,target_number = _get_client_and_config()
    twiml = f"""
    <Response>
        <Say voice="alice">
            {message}
        </Say>
    </Response>
    """
    call = client.calls.create(
        from_=twilio_from,
        to=target_number,
        twiml = twiml
    )  
    print("📞 SOS Call initiated:", call.sid)

if __name__ == "__main__":
    call_sos()