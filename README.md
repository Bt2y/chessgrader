# Inteligencia Artificial: Ajedrez

Implementar la inteligencia de un jugador de ajedrez.

## Requerimientos

### python-chess

Deben descargar e instalar la biblioteca `python-chess`:

+ ftp://lara.matcom.uh.cu/clases/IA/proyecto0
+ [Github](https://github.com/niklasf/python-chess)

Esta biblioteca contiene la lógica del juego de ajedrez. Pueden (y deben) ver la interfaz que ofrece en [github](https://github.com/niklasf/python-chess)

#### Instalar python-chess

    cd /path/to/python-chess
    python setup.py install

Nota: Cada vez que se use `python` en esta ayuda se refiere a `python3`. No se a probado su correcto funcionamiento en `python2`.

### chessgrader

Pueden descargar el evaluador que vamos a estar usando para la competencia (y dar las notas al final) en http://lara.matcom.uh.cu:8000/MarX/chessgrader. El evaluador puede sufrir cambios sin embargo contiene esencialmente lo necesario para realizar un juego de ajedrez entre dos agentes.

Nota: No se ha implementado ninguna interfaz visual para jugar contra una IA. Coming soon...

Nota: Si encuentran un error comuníquenmelo en el [chat](http://chat.matcom.uh.cu/direct/MarX).

## Especificaciones

La lógica del juego está totalmente implementada en la biblioteca de `python-chess`. Esta es una biblioteca open-source en github, probada por la comunidad. Si ustedes encuentran un error pueden comentarlo en el ["issue tracker"](https://github.com/niklasf/python-chess/issues) de la biblioteca.

Para interactuar con el juego estaremos usando la interfaz que ofrece python-chess. Pueden ver la documentación de la misma en [readthedocs](https://python-chess.readthedocs.io/en/latest/). Exploren a fondo todas las funcionalidades que ofrece la misma dado que provee varias funciones útiles para el diseño de estrategias.

Un breve resumen de como funciona la biblioteca a continuación:

```python
>>> import chess

>>> board = chess.Board()

>>> board.legal_moves
<LegalMoveGenerator at ... (Nh3, Nf3, Nc3, Na3, h3, g3, f3, e3, d3, c3, ...)>
>>> chess.Move.from_uci("a8a1") in board.legal_moves
False

>>> board.push_san("e4")
Move.from_uci('e2e4')
>>> board.push_san("e5")
Move.from_uci('e7e5')
>>> board.push_san("Qh5")
Move.from_uci('d1h5')
>>> board.push_san("Nc6")
Move.from_uci('b8c6')
>>> board.push_san("Bc4")
Move.from_uci('f1c4')
>>> board.push_san("Nf6")
Move.from_uci('g8f6')
>>> board.push_san("Qxf7")
Move.from_uci('h5f7')

>>> board.is_checkmate()
True

>>> board
Board('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
```
Este ejemplo fue extraído de la [documentación oficial](https://python-chess.readthedocs.io/en/latest/).

Nota: Hay varias formas de denotar una jugada en ajedrez. Los convenios más empleados/estandarizados están implementados en python-chess. Ver más adelante como un jugador debe interactuar con el juego para seleccionar la jugada.

### Implementando un jugador

Un jugador debe ser un módulo en el directorio `chessgrader/players`. Como referencia ver en la implementación actual de `chessgrader` el jugador `random`.

    chessgrader/
        players/                # En este directorio deben estar los módulos de los jugadores
            random/             # Jugador aleatorio (Ver para más detalles)
            template/           # Plantilla para crear un nuevo jugador
                __init__.py     # __init__.py denota que template es un módulo. Puede permanecer vacío
                player.py       # Fichero que contiene la clase `Player`
        core/                   # Lógica del evaluador (no debería ser necesario cambiar nada :)
        README.md
        run.py                  # Punto de entrada para ejecutar el evaluador
        requirements.txt

#### player.py

En el fichero player es importante que este definido las variables AUTHOR (Una lista con el nombre de los autores), NAME (el nombre de la estrategia) y la clase `Player`. Se recomienda que para empezar a programar un nuevo agente creen una copia del fichero `template` y hagan todos los cambios pertinentes.

Es importante que la clase Player cumpla la siguiente interfaz:

```python
class Player:
    def __init__(self, color):
        self.color = color

    def play(self, board: chess.Board, result, local_timeout, global_timeout):
        # Lógica para determinar la jugada a realizar
        # ...
        # `move` es un objeto de tipo `chess.Move`
        move = select_best_move_ever(board)
        # Es importante no devolver la jugada sino guardarla como string en `result.value`
        result.value = str(move)
```

La función `__init__` será ejecutada el comienzo de un partido.

La función `play` será ejecutada cada vez que el agente deba ejecutar una acción.
`board` contiene la información del tablero actual.

Importante: Para determinar la jugada se debe crear un objeto de tipo `chess.Move` y se debe asignar como string en `result.value`

Para más detalles acerca de cada parámetro ver `/chessgrader/players/random/player.py`.

##### Seleccionando jugada

Cada vez que sea invocada la funcion `player.play` (para determinar la próxima jugada a realizar) es importante que esta no tome más tiempo del establecido. El jugador cuenta con un bono de `local_timeout` segundos por jugada más `global_timeout` segundos que puede utilizar a lo largo del juego. `local_timeout` se reinicia cada vez que se invoca la función mientras que `global_timeout` se va consumiendo. Note que funciona como ETECSA: Primero se consume el bono y luego el tiempo total.

Si el tiempo dado es consumido totalmente la ejecución es detenida y se toma como jugada el valor que este almacenado en `result.value`.

## Ejecutar `chessgrader`

Lista de todos los jugadores "registrados":

    python run.py list

Para ejecutar un partido entre dos jugadores "registrados"

    python run.py --verbose 2 match random random

Para ejecutar un torneo entre todos los jugadores:

    python run.py --verbose 2 tourney

Ayuda sobre otros parámetros configurables:

    python run.py --help

## Contacto

+ [Canal de IA 2018](http://chat.matcom.uh.cu/channel/ia-18)
+ [Marcelo @ chat.matcom](http://chat.matcom.uh.cu/direct/MarX)
