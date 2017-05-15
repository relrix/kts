import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import requests

def draw_album_art(song , confidence):
    plt.figure("Album art")

    artist_name , song_name = song.split("__")
    artist_name = artist_name.replace("-" , "+")
    song_name = song_name.replace("-" , "+")

    r = requests.get('http://itunes.apple.com/search?term=%s&trackName=%s&media=music&limit=1' % (artist_name, song_name))
    data = r.json()
    resource_uri = data['results'][0]['artworkUrl100']
    resource_uri = resource_uri.replace("100x100bb.jpg","500x500bb.jpg")

    response = requests.get(resource_uri)
    img = Image.open(BytesIO(response.content))
    plt.axis('off')
    plt.title(song_name.replace("+" , " "))
    plt.imshow(img)
    plt.pause(10)


def draw_404(confidence):
    plt.figure("404")
    plt.axis('off')
    plt.title("404 - Sorry cannot locate the song")
    image= Image.open("404.png")
    plt.imshow(image)
    plt.pause(10)


