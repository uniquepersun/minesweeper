import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox
import random
from PyQt5.QtCore import Qt

class MineButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_flagged = False

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.toggle_flag()
        else:
            super().mousePressEvent(event)

    def toggle_flag(self):
        if not self.isEnabled():
            return
        self.is_flagged = not self.is_flagged
        self.setText('F' if self.is_flagged else '')
        self.setStyleSheet('background-color: orange' if self.is_flagged else '')

class Minesweeper(QMainWindow):
    def __init__(self, rows=10, cols=10, mines=10):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = []
        self.revealed = []

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
                button = MineButton('')
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
        if button.is_flagged:
            return
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
        if (row, col) in self.revealed:
            return
        self.revealed.append((row, col))
        button.setEnabled(False)
        button.setStyleSheet('background-color: lightgreen')
        surrounding_mines = self.count_surrounding_mines(row, col)
        if surrounding_mines > 0:
            button.setText(str(surrounding_mines))
        else:
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if r == row and c == col:
                        continue
                    self.reveal_cell(r, c)

    def count_surrounding_mines(self, row, col):
        count = 0
        for r in range(max(0, row-1), min(self.rows, row+2)):
            for c in range(max(0, col-1), min(self.cols, col+2)):
                if r == row and c == col:
                    continue
                if hasattr(self.grid[r][c], 'mine'):
                    count += 1
        return count
                    
    def check_win(self):
        for row in self.grid:
            for button in row:
                if not hasattr(button, 'mine') and button.isEnabled():
                    return False
        return True

    def reset_game(self):
        self.revealed = []
        for row in self.grid:
            for button in row:
                button.setEnabled(True)
                button.setText('')
                button.setStyleSheet('')
                button.is_flagged = False
                if hasattr(button, 'mine'):
                    del button.mine
        self.place_mines()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Minesweeper()
    sys.exit(app.exec_())
