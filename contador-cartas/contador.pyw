import sys
from random import choice
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap, QIntValidator, QIcon
from PyQt5.Qt import QTimer
from PyQt5.QtCore import Qt


# (path de la carta, representacion :int:)
cartas = [("sprite/A.png", -1), ("sprite/2.png", 1), ("sprite/3.png", 1),
          ("sprite/4.png", 1), ("sprite/5.png", 1), ("sprite/6.png", 1),
          ("sprite/7.png", 0), ("sprite/8.png", 0), ("sprite/9.png", 0),
          ("sprite/10.png", -1), ("sprite/J.png", -1), ("sprite/Q.png", -1),
          ("sprite/K.png", -1)]


class VentanaInicio(QWidget):
    """
    Objeto que configura la primera
    interfaz grafica de la ventana.
    """

    def __init__(self):
        """Inicio de la ventana principal"""
        super().__init__()
        # Instancias de UI
        # Boton
        self.boton_iniciar = QPushButton("\t\tIniciar\t\t", self)
        boton_iniciar_font = self.boton_iniciar.font()
        boton_iniciar_font.setBold(True)
        boton_iniciar_font.setPointSize(30)
        self.boton_iniciar.setFont(boton_iniciar_font)
        self.boton_iniciar.setStyleSheet(
            "QPushButton{color: grey; background: white;"
            "border: 5px solid grey; border-radius: 8px}"
            "QPushButton:pressed{color: #fcf7e3; background-color: grey}")
        self.boton_iniciar.setEnabled(False)
        # Titulo
        self.titulo = QLabel("Contador de Cartas", self)
        self.titulo.setStyleSheet("color:Brown;font: bold 40pt 'Arial';"
                                  "background: transparent")
        self.titulo.setAlignment(Qt.AlignHCenter)
        # Icono
        self.icono = QLabel(self)
        self.icono.setPixmap(QPixmap('sprite/icono.png'))
        self.icono.setAlignment(Qt.AlignCenter)
        self.icono.setStyleSheet("background: transparent")
        # Parametros
        self.tiempo = QLineEdit(self)
        self.tiempo.setValidator(QIntValidator())
        self.tiempo.setStyleSheet("color:black;font: bold 20pt 'Arial';"
                                  "background: white")
        self.tiempo.setAlignment(Qt.AlignHCenter)
        self.tiempo_et = QLabel("segundos por carta\n↓", self)
        self.tiempo_et.setStyleSheet("color:Brown;font: bold 20pt 'Arial';"
                                     "background: transparent")
        self.tiempo_et.setAlignment(Qt.AlignHCenter)
        self.tiempo.textChanged.connect(self.activar_boton)
        self.alineamiento()

    def alineamiento(self):
        """
        Funcion que alinea los iconos
        """
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.boton_iniciar)
        hbox1.addStretch(1)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.tiempo)
        hbox2.addStretch(1)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.titulo)
        vbox1.addStretch(1)
        vbox1.addWidget(self.icono)
        vbox1.addStretch(1)
        vbox1.addWidget(self.tiempo_et)
        vbox1.addLayout(hbox2)
        vbox1.addStretch(1)
        vbox1.addLayout(hbox1)
        vbox1.addStretch(2)
        self.setLayout(vbox1)

    def activar_boton(self):
        """
        Activa boton si hay texto
        """
        # Si hay un numero activamos el boton, si no desactivamos el boton
        if self.tiempo.text():
            self.boton_iniciar.setStyleSheet(
                "QPushButton{color: brown; background: grey;"
                "border: 5px solid brown; border-radius: 8px}"
                "QPushButton:pressed{color: #fcf7e3; background-color: brown}")
            self.boton_iniciar.setEnabled(True)
        else:
            self.boton_iniciar.setStyleSheet(
                "QPushButton{color: grey; background: white;border: "
                "5px solid grey; border-radius: 8px}"
                "QPushButton:pressed{color: #fcf7e3; background-color: grey}")
            self.boton_iniciar.setEnabled(False)


class Contador(QWidget):
    """
    Contador de cartas en si
    """

    def __init__(self, tiempo):
        """Inicio de la ventana que muestra las cartas"""
        super().__init__()
        # Temporizador/Contador
        self._tiempo = (int(tiempo) * 1000) / 25
        self.contador = 0
        self.suma_total = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)
        # Imagen de carta
        self.carta = QLabel(self)
        self.carta.setPixmap(QPixmap(choice(cartas)[0]))
        self.carta.setStyleSheet("background: transparent")
        self.carta.setAlignment(Qt.AlignCenter)
        self.carta.hide()
        # etiqueta del total
        self.total_etiqueta = QLabel("", self)
        self.total_etiqueta.setStyleSheet(
            "color:Brown;font: bold 40pt'Arial'; background: transparent")
        self.total_etiqueta.setAlignment(Qt.AlignCenter)
        # Contador
        self.total_etiqueta = QLabel(f"{self.contador}", self)
        self.total_etiqueta.setStyleSheet(
            "color:Brown;font: bold 40pt'Arial'; background: transparent")
        self.total_etiqueta.setAlignment(Qt.AlignCenter)
        # Pausa
        self.pausa = False
        self.boton_pausa = QPushButton("\t\tPausar\t\t", self)
        boton_pausa_font = self.boton_pausa.font()
        boton_pausa_font.setBold(True)
        boton_pausa_font.setPointSize(30)
        self.boton_pausa.setFont(boton_pausa_font)
        self.boton_pausa.setStyleSheet(
            "QPushButton{color: brown; background: grey;"
            "border: 5px solid brown; border-radius: 8px}"
            "QPushButton:pressed{color: #fcf7e3; background-color: brown}")
        self.boton_pausa.clicked.connect(self.pausar)
        # Atras para reajustar parametros
        self.boton_atras = QPushButton("\t\tAtras\t\t", self)
        boton_atras_font = self.boton_atras.font()
        boton_atras_font.setBold(True)
        boton_atras_font.setPointSize(25)
        self.boton_atras.setFont(boton_atras_font)
        self.boton_atras.setStyleSheet(
            "QPushButton{color: brown; background: grey;"
            "border: 5px solid brown; border-radius: 8px}"
            "QPushButton:pressed{color: #fcf7e3; background-color: brown}")
        # Alineamos
        self.alineamiento()
        self._timer.start(25)

    def alineamiento(self):
        """Alineacion del programa"""
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton_pausa)
        hbox.addStretch(1)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(2)
        hbox2.addWidget(self.boton_atras)
        hbox2.addStretch(2)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.carta)
        vbox.addStretch(1)
        vbox.addWidget(self.total_etiqueta)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addStretch(2)
        self.setLayout(vbox)

    def pausar(self):
        """Cambia el parametro para que se pause"""
        if not self.pausa:
            self.boton_pausa.setText("\t\tReanudar\t\t")
            self.pausa = True
        else:
            self.boton_pausa.setText("\t\tPausar\t\t")
            self.pausa = False

    def _update(self):
        """Funcion que se llama cada 25 milisegundos"""
        # Si pausa == True pausamos.
        if self.pausa:
            self.total_etiqueta.setText(f"Total: {self.suma_total}")
            self.contador = 0
        # Cada self._tiempo segundos + medio segundo retornamos el contador a 0
        if self.contador == self._tiempo + 20:
            self.contador = 0
        # Cambiamos la carta y se lo sumamos al total.
        if not self.pausa and self.contador == 0:
            carta = choice(cartas)
            self.suma_total += carta[1]
            self.carta.setPixmap(QPixmap(carta[0]))
            self.carta.show()
        # Agregamos el petqueño lapso de tiempo con una carta por detras.
        # Principalmente para demostrar un cambio en caso de que la siguiente
        # sea igual.
        if self.contador == self._tiempo:
            self.carta.setPixmap(QPixmap("sprite/atras.png"))
        # Si no estamos en pausa le agregamos al contador 1.
        if not self.pausa:
            self.total_etiqueta.setText("")
            self.contador += 1


class MiVentana(QMainWindow):
    """
    Objeto que maneja la ventana principal
    """

    def __init__(self):
        """Inicia el programa"""
        super().__init__()
        # Dimensiones y titulo de la ventana
        self.setFixedSize(1000, 900)
        self.setWindowTitle('Contador 1.0')
        # Imagen de fondo e icono
        self.setWindowIcon(QIcon('sprite/icono.png'))
        self.setStyleSheet("background-image: url(sprite/fondo.png);"
                           "background-attachment: fixed")
        self.inicio()

    def inicio(self):
        """Inicia la ventana principal"""
        self.ventana_inicio = VentanaInicio()
        self.setCentralWidget(self.ventana_inicio)
        self.ventana_inicio.boton_iniciar.clicked.connect(self.contador)
        self.show()

    def contador(self):
        """Inicia la zona del contador"""
        self.ventana_contador = Contador(self.ventana_inicio.tiempo.text())
        self.setCentralWidget(self.ventana_contador)
        self.ventana_contador.boton_atras.clicked.connect(self.atras)
        self.show()

    def atras(self):
        """Conecta el boton de retroceder con la ventana principal"""
        self.ventana_contador._timer.stop()
        self.inicio()


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())
