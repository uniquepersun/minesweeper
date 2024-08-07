import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox
import random

class Minesweeper(QMainWindow):
    def __init__(self, rows=10, cols=10, mines=10):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = []

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        self.create_grid()
        self.place_mines()

        self.setWindowTitle('minesweeper')
        self.show()

    def create_grid(self):
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                button = QPushButton('')
                button.setFixedSize(30, 30)
                button.clicked.connect(self.cell_clicked)
                self.grid_layout.addWidget(button, row, col)
                row_cells.append(button)
            self.grid.append(row_cells)

    def place_mines(self):
        for _ in range(self.mines):
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                if not hasattr(self.grid[row][col], 'mine'):
                    self.grid[row][col].mine = True
                    break

    def cell_clicked(self):
        button = self.sender()
        row, col = self.get_cell_position(button)
        if hasattr(button, 'mine'):
            self.reveal_mines()
            QMessageBox.critical(self, 'losed', 'you clicked a mine!')
            self.reset_game()
        else:
            self.reveal_cell(row, col)
            if self.check_win():
                QMessageBox.information(self, 'yoo!', 'You won!')
                self.reset_game()

    def get_cell_position(self, button):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == button:
                    return row, col
        return None

    def reveal_mines(self):
        for row in self.grid:
            for button in row:
                if hasattr(button, 'mine'):
                    button.setText('M')
                    button.setStyleSheet('background-color: red')

    def reveal_cell(self, row, col):
        button = self.grid[row][col]
        button.setEnabled(False)
        button.setStyleSheet('background-color: lightgrey')

    def check_win(self):
        for row in self.grid:
            for button in row:
                if not hasattr(button, 'mine') and button.isEnabled():
                    return False
        return True

    def reset_game(self):
        for row in self.grid:
            for button in row:
                button.setEnabled(True)
                button.setText('')
                button.setStyleSheet('')
                if hasattr(button, 'mine'):
                    del button.mine
        self.place_mines()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Minesweeper()
    sys.exit(app.exec_())
