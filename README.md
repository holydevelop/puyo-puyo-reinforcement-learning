# Puyo Puyo para aprendizaje por refuerzo
Estudiantes de la Universidad Andres Bello realizan un proyecto para el ramo de Desarrollo de Inteligencia Artificial en el cual se eligio un tema el cual fue Aprendizaje por Refuerzo, realizando la investagcion se utilizo de referencia el juego Puyo Puyo para poder intentar que el modelo aprenda mediante tecnicas de reinforcement learning.

# Referencia
El codigo de **puyo puyo on python** no es de nuestra propiedad y utilizamos de referencia el codigo del usuario nicked4 , se realizo modificaciones para la utilizacion del juego como entorno para un aprendizaje por refuerzo y asi poder entrenar nuestro modelo.

GitHub utilizado para este proyecto: https://github.com/nicked4/puyopuyo_on_python

# Explicacion archivos de referencia

Una explicacion de los archivos que vienen del github clonado y nombrado anteriormente, para entender los archivos tenemos los siguiente:
1) puyo_class.py el cual contiene todo lo principal del juego, este se analizo para entender que variables tenia disponible y es la clase padre de otros archivos.
2) puyo_AIplay.py es el cual intentaremos modificar para que juegue nuestro agente y tambien aprenda , todo se desarrollara en este entorno para posteriormente si es posible lograr que juegue directamente en RetroArch que es un emulador que tendra el juego Kirby's Avalanche.
3) DeepTrainLearning es un archivo donde se añadira el modelo y se integrara todo el algoritmo de aprendizaje para asi tener el codigo mas ordenado, ademas las modificaciones se iran realizando en el respectivo archivo.