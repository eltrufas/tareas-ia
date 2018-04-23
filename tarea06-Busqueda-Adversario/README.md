# Tarea 6: Búsquedas con adversarios

## Objetivos

1. Reforzar los conocimientos de los métodos de búsquedas por
   adversarios, en particular el algoritmo Minimax con poda alpha-beta
   en su versión para dos jugadores por turnos, conocida como
   `negamax`.

2. Desarrollar habilidades para establecer heurísticas de ordenamiento
   de jugadas con el fin de reducr los tiempos de búsqueda.

3. Desarrollar habilidades y conocimientos para establecer medidas de
   estimación de utilidad, al aprender a generar funciones de
   características y establecer pesos entre estos.

4. Desarrollar un juego simple (Othello) con motor de IA desde cero.

Adicionalmente, en los programas se intenta mostrar un punto de vista
más orientado al paradigma funcional en Python, utilizando a las
clases únicamente como contenedores de funciones para un tipo de datos
particulares (el juego).

Si bien se proporcionan las herramientas y ejemplos necesarios para
comprender los rudimentos básicos de programación de interfases en
TCL, de ninguna manera se considera como un conocimiento práctico
adicional que se espera reforzar con la tarea.

## Instrucciones

1. En el archivo `busqueda_adversarios.py` se ofrecen clases para
   juego de tablero por turnos. Revisa el código y procura entender a
   grandes razgos como funciona. El archivo `tictactoe.py` es un
   ejemplo de uso sencillo con el juego del gato. Es importante
   aclarar que este es un ejemplo con fines didácticos y toda posible
   optimización en tiempo o uso dememoria se evitó siempre que eso
   implicara obscurecer el proceso de búsqueda con adversarios, por lo
   que el entorno es bastante ineficiente en estos términos.

2. En el archivo `conecta4.py` se incluye el juego de conecta 4, el
   cual es bastante conocido, y si quieres información de como se
   juega la puedes consultar
   [aqui](http://en.wikipedia.org/wiki/Connect_Four). En el archivo se
   ofrece el juego programado. Dentro del metodo hay dos funciones muy
   malas que impactan mucho en la calidad del juego: `ordena_jugadas`
   y `utilidad_c4`.  Desarrolla tu propias funciones con el fin de
   lograr mejores búsquedas a mayor profundidad (40 puntos).

4. El archivo `othello.py` es un archivo completamente en
   blanco. Desarrolla todo lo necesario para un juego de
   [Othello](http://en.wikipedia.org/wiki/Reversi). Todas las
   decisiones son tuyas. No importa que juegue lento, pero que el
   ordenamiento y las funciones de utilidad hagan que jugar contra el
   motor de IA sea muy dificil de ganar (60 puntos).
