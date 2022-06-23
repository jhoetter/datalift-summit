from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

creds = None

def get_auth_creds(scopes):
    global creds
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            auth_with_google_and_store_creds(scopes)
    return creds


def auth_with_google_and_store_creds(scopes):
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json",
        scopes=scopes,
    )

    # port must be the port from "redirect_uris" in "client_secrets.json"
    flow.run_local_server(port=24184, prompt="consent", authorization_prompt_message="")

    global creds
    creds = flow.credentials
