from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import pandas as pd


## Conexión con la API de Spotipy
client_credentials_manager = SpotifyClientCredentials(client_id='15e289f759254566a052182bc1faf21f', client_secret='deac0fe27ea643db9356bb39f9cb60a6')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


## Configurar la aplicación Flask
app = Flask(__name__)

#### Ruta principal ###
@app.route('/')
def index():
    return render_template('inicio.html')

#### Función para volver a la página de inicio ###
@app.route('/home')
def home():
    return render_template('inicio.html')


##### Ruta y función para encontrar el cantante que queramos ###
@app.route('/encontrar', methods=['POST','GET'])
def encontrar():
    if request.method == 'GET':
        return render_template('buscador.html')
    elif request.method == 'POST':
        ## Obtener el cantante que ha sido ingresado en el formulario
        artista = request.form['artista']
        ## Se busca en Spotify el artista
        resultado = sp.search(q=artista, type='artist')
        ##
        if len(resultado['artists']['items']) > 0:
            ## Coge el primer elemento y obtiene el id del cantante con la clave "id"
            artista_id = resultado['artists']['items'][0]['id']
            ## Devuelve las canciones encontradas y obtenemos las tres canciones más escuchadas del artista en Estados Unidos
            topTracks = sp.artist_top_tracks(artista_id, country='US')
            ## Almacenamos las canciones en una lista
            canciones = []
            for track in topTracks['tracks'][:3]:
                canciones.append(track['name'])
            return render_template('resultado.html', resultadoHtml=f'Las tres canciones más populares de {artista} son: {canciones}')
        else:
            return render_template('error.html', mensaje='Cantante no encontrado.')



##### Gráficos con Matplotlib ####
### 10 GÉNEROS MUSICALES MÁS ESCUCHADOS DESDE 2010 HASTA 2019
@app.route('/graficos')
def crearGraficosTopGeneros():
    # Se cargan los datos en un dataframe
    data = pd.read_csv("top10s.csv", encoding="ISO-8859-1")

    # Contar las veces que aparece cada género musical
    contarGeneros = data["top genre"].value_counts()

    # Seleccionar los 5 géneros más escuchados
    topGeneros = contarGeneros[:5]

    # Graficar los resultados
    plt.figure()
    plt.pie(topGeneros.values, labels=topGeneros.index, autopct='%1.1f%%')
    plt.title(f"Géneros más escuchados desde 2010 hasta 2019")
    plt.savefig(fname="static/graficoTopGeneros.png", format='png')
    plt.close()
    return render_template('graficos.html')


### Géneros más escuchados desde 2010 hasta 2019 ###
@app.route('/graficos')
def crearGraficos():
    # Cargar datos en un dataframe
    data = pd.read_csv("top10s.csv", encoding="ISO-8859-1")

    # Contar el número de canciones por género y por año
    for any in range(2010, 2020):
        # Filtrar los datos para cada año
        anyActual = data[data["year"] == any]

        # Contar total de canciones por género para cada año
        generoTotal = anyActual["top genre"].value_counts()

        # Seleccionar los 5 géneros más escuchados para el año actual
        topGeneros = generoTotal[:5]

        # Graficar los resultados para el año actual
        plt.figure()
        plt.pie(topGeneros.values, labels=topGeneros.index, autopct='%1.1f%%')
        plt.title(f"Géneros más Escuchados ({any})")
        ### Se crea una cadena formateada donde por cada año diferente, se crea un grafico diferente, ejemplo: ("gráfico2010", "gráfico2011", etc)
        plt.savefig(fname=f"static/grafico{any}.png", format='png')
        plt.close()
    return render_template('graficos.html')


### CANTANTES CON MÁS CANCIONES DE 2010-2019
@app.route('/graficos')
def crearGraficosTopCantantes():
    # Cargamos los datos en un dataframe
    data = pd.read_csv("top10s.csv", encoding="ISO-8859-1")

    # Contar el número de canciones por artista
    contarArtista = data["artist"].value_counts()

    # Seleccionar los 10 primeros cantantes con más canciones
    artistasTop = contarArtista[:10]

    # Graficar los resultados
    plt.figure(figsize=(10,6)) # tamaño de la figura
    plt.bar(artistasTop.index, artistasTop.values)
    plt.xticks(rotation="vertical", fontsize=8) # rotación y tamaño de los ticks
    plt.xlabel("Artistas")
    plt.ylabel("Número de canciones")
    plt.title("Top 10 artistas más populares en Spotify (2010-2019)")
    plt.tight_layout() # ajuste automático de los ticks
    plt.savefig(fname="static/graficoTopCantantes.png", format='png')
    plt.close()
    return render_template('graficos.html')
  

### CANTANTES CON MÁS CANCIONES POR AÑOS 2010-2019
@app.route('/graficos')
def crearGraficosTopCantantesPorAny():
    ### Leer archivo CSV con pandas y luego pasarlo en un dataframe
    df = pd.read_csv("top10s.csv", encoding="ISO-8859-1")

    ### Bucle for para iterar cada año desde el 2010 hasta 2019, para poder obtener la cantidad 
    ### de canciones por artista de cada año.
    for any in range(2010, 2020):
        # Obtener los datos para el año actual
        anyActual = df[df["year"] == any]
        
        ### .value_counts() sirve para contar el nº de veces que aparece un cantante en la columna "artist" 
        ### Contar la cantidad de canciones por artista para el año actual
        totalCantantes = anyActual["artist"].value_counts()
        
        # Seleccionar los 10 primeros artistas con más canciones de cada año
        CantantesTop = totalCantantes[:10]
        
        # Graficar los resultados para cada año
        plt.figure(figsize=(10,6)) # tamaño de la figura
        plt.bar(CantantesTop.index, CantantesTop.values)
        ### xticks rotation sirve para rotar los nombres de los cantantes para que se puedan leer correctamente
        plt.xticks(rotation="vertical", fontsize=8) # rotación y tamaño de los ticks
        plt.xlabel("Artistas")
        plt.ylabel("Número de canciones")
        plt.title(f"Top 10 cantantes más populares en Spotify ({any})")
        plt.tight_layout() # ajuste automático de los ticks
        ### Se crea una cadena formateada donde por cada año diferente, se crea un gráfico diferente ("grafico2010", "grafico2011", etc)
        plt.savefig(fname=f"static/graficoTopCantantes{any}.png", format='png')
        plt.close()
    return render_template('graficos.html')


# Nueva ruta para encontrar artistas por canción
@app.route('/encontrarCancion', methods=['POST','GET'])
def encontrarCancion():
    if request.method == 'GET':
        return render_template('buscarcancion.html')
    elif request.method == 'POST':
        ## Obtener el título de la canción ingresada en el formulario
        cancion = request.form['cancion']
        ## Busca canciones en Spotify que coincidan con la canción del formulario
        resultados = sp.search(q=cancion, type='track')
        ## Almacenar los artistas una sola vez para obtener cuales están asociados con la canción que se ha buscado
        artistas = set()
        ## Itera sobre cada canción de "resultados" que se ha buscado en Spotify
        for item in resultados['tracks']['items']:
            ## Itera sobre cada artista que está asociado con la canción
            for artista in item['artists']:
                ## Se añade el artista en el conjunto "artistas"
                artistas.add(artista['name'])
        ## se comprueba que existan artistas
        if len(artistas) > 0:
            return render_template('resultadocancion.html', cancionHtml=f'Los siguientes artistas tienen la canción "{cancion}": {", ".join(artistas)}')
        else:
            return render_template('errorcancion.html', mensaje='Canción no encontrada.')
 

## Ejecución de la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)

