from flask import Flask, render_template, request, send_file
import os
import zipfile
import sys
from mashup import mash
import requests
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer_name = request.form.get("singer_name")
        number_of_videos = int(request.form.get("number_of_videos"))
        duration_of_each_video = int(request.form.get("duration_of_each_video"))
        email = request.form.get("email")

        #mash(singer_name,number_of_videos,duration_of_each_video)
        # Generate a dummy zip file
        with zipfile.ZipFile("videos.zip", "w") as zip:
            zip.write("out.mp3")

        # Send the zip file as an attachment to the entered email
        send_email(singer_name, email, "videos.zip")

        return "Zip file sent successfully!"

    return render_template("index.html")


def send_email(singer_name, to, zip_file):
    # Replace YOUR_SENDGRID_API_KEY with your SendGrid API key
    api_key = "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"
    headers = {
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json",
    }

    with open(zip_file, "rb") as f:
        file_data = f.read()
        encoded_file_data = base64.b64encode(file_data).decode("utf-8")

    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to,
                    },
                ],
                "subject": "Videos by {}".format(singer_name),
            },
        ],
        "from": {
            "email": "sender_email@example.com",
        },
        "content": [
            {
                "type": "text/plain",
                "value": "Please find the requested videos attached.",
            },
        ],
        "attachments": [
            {
                "content": encoded_file_data,
                "filename": os.path.basename(zip_file),
                "type": "application/zip",
                "disposition": "attachment",
            },
        ],
    }
    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send", headers=headers, json=data
    )
    if response.status_code != 202:
        raise Exception(
            "Failed to send email: {}".format(response.json().get("errors"))
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    api = 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
