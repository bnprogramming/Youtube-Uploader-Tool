import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


def get_authenticated_service():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)

    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)


youtube = get_authenticated_service()


def upload_video(youtube, file, title, description, tags, category_id, privacy_status):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=file
    )

    response = insert_request.execute()
    print("Video ID: %s" % response["id"])


# پارامترها
file = ["Anamis-79.mp4", "amis-80.mp4", "Anamis-81.mp4", "amis-82.mp4", "Anamis-83.mp4", "amis-84.mp4", ]
title = "عنوان ویدیو"
description = "توضیحات ویدیو"
tags = ["برچسب۱", "برچسب۲"]
category_id = "22"  # ۲۲ برای بخش "People & Blogs"
privacy_status = "public"  # وضعیت ویدیو (public, private, unlisted)

for video in file:
    upload_video(youtube, video, title, description, tags, category_id, privacy_status)

