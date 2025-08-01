import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class YouTubeUploader:
    def __init__(self, client_secrets_file="client_secret.json"):
        self.client_secrets_file = client_secrets_file
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.youtube = self.authenticate()

    def authenticate(self):
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes)
        credentials = flow.run_local_server(port=0)
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
        return youtube

    def upload_video(self, video_file, title, description, tags=[]):
        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22"  # People & Blogs
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=video_file
        )
        response = request.execute()
        return response
