from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from authentication import get_auth_creds
from tqdm import tqdm


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

if __name__ == "__main__":
    creds = get_auth_creds(SCOPES)
    
    mail_data = []
    try:
        # find docs for service here:
        # https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/index.html
        service = build("gmail", "v1", credentials=creds)

        api_result = service.users().messages().list(userId="me").execute()
        messages = api_result["messages"]
        result_size_estimate = api_result["resultSizeEstimate"]
        for idx, message_meta in enumerate(tqdm(messages, total=result_size_estimate)):
            message_dict = {}
            message_id = message_meta["id"]
            message = (
                service.users().messages().get(userId="me", id=message_id).execute()
            )
            payload = message["payload"]
            headers = payload["headers"]
            for header in headers:
                key = header["name"]
                if key in ["Delivered-To", "Cc", "From", "Date", "Subject"]:
                    value = header["value"]
                    message_dict[key] = value
            message_dict["Snippet"] = message["snippet"]
            mail_data.append(message_dict)

    except HttpError as error:
        print(f"An error occurred: {error}")

    # once everything is collected, store it to the project id; directly via DB or via API?
    print(mail_data)
