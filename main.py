from flask import Flask, request, jsonify
import requests
from pypdf import PdfReader


def download_file(url, filename=None):
    """
    Downloads a file from the specified URL and saves it locally.

    Args:
        url: The URL of the file to download.
        filename: The filename to save the downloaded file as. If not specified,
            the filename will be extracted from the URL.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for unsuccessful downloads

    if filename is None:
        filename = url.split("/")[-1]  # Extract filename from URL

    with open(filename, "wb") as file:
        for chunk in response.iter_content(1024):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)

    return filename


app = Flask(__name__)


@app.route("/read_text", methods=["POST"])
def download_from_url():
    """
    Accepts a URL as POST data and calls the download_file function.
    """
    data = request.get_json()
    url = data['url']
    if not url:
        return "Missing URL in request body!", 400

    downloaded_file = download_file(url)
    print(f"Downloaded file: {downloaded_file}")
    reader = PdfReader(downloaded_file)
    print(len(reader.pages))
    page = reader.pages[0]
    text = page.extract_text()
    result = ""
    for char in text:   
        if char.isalnum() or char.isspace():
            result += char
    response = {'body': result.replace("\n", "")}
    return jsonify(response)


if __name__ == "__main__":
    app.run()
