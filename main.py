from flask import Flask, request, jsonify
from pypdf import PdfReader
import urllib.request

app = Flask(__name__)


def download_file(url, filename=None):
    """
    Downloads a file from the specified URL and saves it locally.

    Args:
        url: The URL of the file to download.
        filename: The filename to save the downloaded file as. If not specified,
            the filename will be extracted from the URL.
    """
    if filename is None:
        filename = url.split("/")[-1]  # Extract filename from URL

    with urllib.request.urlopen(url) as response:
        with open(filename, "wb") as file:
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                file.write(chunk)

    return filename


@app.route("/read_text", methods=["GET"])
def download_from_url():
    """
    Accepts a URL as a query parameter and calls the download_file function.
    """
    url = request.args.get('url')
    if not url:
        return "Missing URL parameter!", 400

    try:
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
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0')
