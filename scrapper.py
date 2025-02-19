import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
import csv

# Configure your Spotify API credentials
client_id = 'd55729f1be1b463983bbec9c61dc951d'
client_secret = 'b7feadc83dd246d4910c9caa7c27af6c'

#  Authenticate the client with your credentials
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)


def get_artist_data(artist_name, depth, current_depth=0, checked_artists=set(), unchecked_artists=set(), nodos={}, aristas={}):

    # Even though the maximum depth level has been reached, it is mandatory to process leaf nodes in order to store its information!!

    # Search for artist name
    result = sp.search(q='artist:' + artist_name, type='artist')
    items = result['artists']['items']
    if not items:
        return

    # Get only the first result
    artist = items[0]
    artist_id = artist['id']
    artist_name = artist['name']
    print(f'Procesando: {artist_name}...')
    if artist_id in checked_artists:  # Artist already visited, skip processing
        return
    checked_artists.add(artist_name )
    nodos[artist_id]=artist_name

    # Artist data
    artist_data = {
        'id': artist_id,
        'label': artist['name'],
        'followers': artist['followers']['total'],
        'genres': ', '.join(artist['genres']),
        'popularity': artist['popularity'],
        'image_url': artist['images'][0]['url'] if artist['images'] else None
    }

    # write node data as CSV format
    with open('nodes.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=artist_data.keys())
        if current_depth == 0:  # write header only once
            writer.writeheader()
        writer.writerow(artist_data)

    # If reached maximum depth, stop the recursive process
    if current_depth > depth:
        return


    ######################################################## PRÁCTICA 1
    # Obtengo los albumes del artista indicado
    results = sp.artist_albums(artist_id, album_type='album')
    albums = results['items']
    time.sleep(1)
    for album in albums:                                            # BUCLE: Para cada album del artista
        album_aux = sp.album(album['uri'])                          #        obtengo mediante su URI (identificador) toda la información del album
        time.sleep(0.1)
        tracks = album_aux['tracks']['items']                       #        para ese album obtengo su listado de canciones
        for track in tracks:                                        #   BUCLE: Para cada canción del listado
            for artist in track['artists']:                         #       BUCLE: Para cada artista del listado de artistas de cada canción
                if 'name' in artist:                                #              miro si existe la propiedad nombre
                    if artist['name'] not in unchecked_artists:     #              compruebo que no haya comprobado ese artista anteriormente
                        if artist['name'] not in checked_artists:    
                            #print('\t' + artist['name'])            #              (DEPURACIÓN)lo imprimo por pantalla
                            unchecked_artists.add(artist['name'])   #              lo añado al set de artistas ya comprobados
                            aristas[artist_id] = artist['id']
    #print(f'\nHECHO. Artistas visitados + ({artist_name}): {len(checked_artists)} {checked_artists}')
    #print(f'HECHO. Artistas no visitados {len(unchecked_artists)}   {unchecked_artists}')
    print(nodos)
    print(aristas)
    if len(nodos) < 3000:
        get_artist_data(unchecked_artists.pop(), depth=depth, checked_artists=checked_artists, unchecked_artists=unchecked_artists, nodos=nodos, aristas=aristas)   

    ########################################################

# Start the search process
artist_name = "Lola Indigo"  # Change this to your favorite artist
depth = 2  # Be careful with Spotify API Limits!!

checked_artists = set()    # Creo el set de artistas ya comprobados
unchecked_artists = set()  # Creo el set de artistas descubiertos pero no comprobados

fichero_nodos = "nodos.csv"
fichero_aristas = "aristas.csv"

nodos = {}
aristas = {}
get_artist_data(artist_name, depth=depth, checked_artists=checked_artists, unchecked_artists=unchecked_artists, nodos=nodos, aristas=aristas)

with open(fichero_nodos,'w') as f:
    w = csv.writer(f)
    w.writerows(nodos.items())

with open(fichero_aristas,'w') as f:
    w = csv.writer(f)
    w.writerows(aristas.items())


