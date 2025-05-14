import os, sys, json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy

rootDir = os.getcwd()
assetDir = os.path.join(rootDir, "assets")
backgDir = os.path.join(assetDir, "backgrounds")
coverDir = os.path.join(assetDir, "covers")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MO2 Linux Wizard")
        self.setMaximumSize(850, 850)
        self.setMinimumSize(self.maximumSize())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: rgba(17, 17, 27, 0.2); color: #cdd6f4;")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        
        self.addTopBar(mainLayout)
        self.addCards(mainLayout)
        self.addBottomBar(mainLayout)
        
    def addTopBar(self, layout):
        titleLabel = QLabel("Mod Organizer 2 - Linux Wizard", self)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLabel.setStyleSheet("font-size: 20px; color: #cdd6f4; background-color: #181825;")
        titleLabel.setMinimumHeight(50)
        layout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignTop)
    
    def addCards(self, layout):
        gridLayout = QGridLayout()
        gridLayout.setContentsMargins(10, 10, 10, 10)
        gridLayout.setSpacing(15)
        
        try:
            with open(rootDir + "/info/games.json", "r") as file:
                gameData = json.load(file)
        except FileNotFoundError:
            print("Error: /info/games.json not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from /info/games.json.")
            return {}
        
        i = 0
        for game_key, game_info in gameData.items():
            name = game_info.get('name')
            image = game_info.get('image')
            
            card = QWidget(self)
            card.setStyleSheet("background-color: #181825; border-radius: 10px; border: 2px solid #11111b;")
            card.setMinimumSize(125, 225)
            card.setMaximumSize(card.minimumSize())
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
            cardLayout = QVBoxLayout(card)
            cardLayout.setContentsMargins(0, 0, 0, 0)
            cardLayout.setSpacing(10)
            cardLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            
            imageLabel = QLabel(card)
            imageLabel.setStyleSheet("border: none; margin-bottom: 0px;")
            pixmap = QPixmap(os.path.join(coverDir, image))
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(card.width(), card.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

                rounded_pixmap = QPixmap(scaled_pixmap.size())
                rounded_pixmap.fill(Qt.GlobalColor.transparent)

                painter = QPainter(rounded_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                path = QPainterPath()
                path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 10, 10)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, scaled_pixmap)
                painter.end()

                imageLabel.setPixmap(rounded_pixmap)
                print(f"{name}: Image loaded successfully")
            else:
                imageLabel.setText("Image not found")
                imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                print(f"{name}: Image not found")
            imageLabel.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            cardLayout.addWidget(imageLabel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            
            titleLabel = QLabel(name, card)
            if len(name) > 16:
                fontSize = "font-size: 10px;"
            else:
                fontSize = "font-size: 12px;"
            titleLabel.setStyleSheet("font-weight: bold; color: #cdd6f4; text-align: center; border: none; margin-bottom: 0px; line-height: 0.2; " + fontSize)
            cardLayout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

            try:
                gridLayout.addWidget(card, i // 5, i % 5)
                print(f"Added card at row {i // 5}, column {i % 5}")
            except Exception as e:
                print(f"Error adding card: {e} at row {i // 5}, column {i % 5}")
            i += 1

        cardLayoutWidget = QWidget(self)
        cardLayoutWidget.setObjectName("cardLayoutWidget")
        cardLayoutWidget.setStyleSheet("QWidget#cardLayoutWidget { background-color: transparent; }")
        cardLayoutWidget.setLayout(gridLayout)
        cardLayoutWidget.update()
        layout.addWidget(cardLayoutWidget)
        
    def addBottomBar(self, layout):
        bottomBar = QWidget(self)
        bottomBarLayout = QGridLayout(bottomBar)
        bottomBarLayout.setContentsMargins(0, 0, 0, 0)
        bottomBarLayout.setSpacing(0)

        buttonStyle = """
            font-size: 14px; 
            color: #181825; 
            background-color: #89dceb; 
            padding: 4px 12px; 
            border-radius: 10px;
            margin: 10px;
            min-width: 90px;
            min-height: 25px;
        """

        prevButton = QLabel("◀ Previous", self)
        prevButton.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prevButton.setStyleSheet(buttonStyle)

        stepLabel = QLabel("Step 1 of 4: Choose your Game", self)
        stepLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stepLabel.setStyleSheet("""
            font-size: 14px; 
            color: #cdd6f4; 
            background-color: transparent;
            margin: 10px;
        """)
        stepLabel.setMinimumHeight(50)

        nextButton = QLabel("Next ▶", self)
        nextButton.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nextButton.setStyleSheet(buttonStyle)

        bottomBar.setStyleSheet("background-color: #181825;")
        bottomBarLayout.addWidget(prevButton, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        bottomBarLayout.addWidget(stepLabel, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        bottomBarLayout.addWidget(nextButton, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(bottomBar, alignment=Qt.AlignmentFlag.AlignBottom)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec())