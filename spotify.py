import requests
from flask import jsonify

class errorGettingToken(Exception):
    pass
class errorSearchingInAPI(Exception):
    pass

def get_access_token():
    client_id = '2e68ba76a1bd413499e685eb62f0764b'
    client_secret = '22a75ae1139a4c08825d4e8785bad17f'
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        raise errorGettingToken('Error getting the token from the spotfy API')
    
def get_list_of_songs(song):
    access_token = get_access_token()
    if not access_token:
        raise errorGettingToken('Error getting the token from the spotfy API')
    search_url = f'https://api.spotify.com/v1/search?q={song}&type=track'
    headers = {
            'Authorization': f'Bearer {access_token}'
        }
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise errorSearchingInAPI('Failed to search for the song in spotify')
    data = response.json()
    tracks = data['tracks']['items']
    result = []
    for track in tracks:
        primary_image = track['album']['images'][0]
        name = track['name']
        artists = [artist['name'] for artist in track['artists']]
        track_id = track['id']
        result.append({
            'image': primary_image,
            'name': name,
            'artists': artists,
            'track_id': track_id
        })
    return jsonify(result)