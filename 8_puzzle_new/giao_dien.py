import tkinter as tk
from tkinter import messagebox
import random
from queue import PriorityQueue
import heapq


class NPuzzleGame:
    def __init__(self, root, n=3):
        self.root = root
        self.n = n
        self.tiles = [[None for _ in range(n)] for _ in range(n)]
        self.empty_tile = (n-1, n-1)  # Initial position of the empty tile
        self.initialize_tiles()
        self.set_goal_state()
        self.moves = 0

    def check_win(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.tiles[i][j]["text"]:
                    if int(self.tiles[i][j]["text"]) != self.goal_state[i][j]:
                        return False
                else:
                    if self.goal_state[i][j] != 0:
                        return False
        return True

    def show_win_message(self):
        messagebox.showinfo("Congratulations!", f"You solved the puzzle in {self.moves} moves!")
        self.shuffle_tiles()  # Sau khi giải quyết, trò chơi sẽ được trộn lại

    def set_initial_state(self):
        initial_state = [[1, 2, 3], [0, 8, 7], [6, 4, 5]]  # Trạng thái xuất phát
        for i in range(self.n):
            for j in range(self.n):
                number = initial_state[i][j]
                if number != 0:
                    self.tiles[i][j].config(text=str(number))
                else:
                    self.tiles[i][j].config(text="")
                    self.empty_tile = (i, j)

    def set_goal_state(self):
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Trạng thái đích

    def initialize_tiles(self):
        for i in range(self.n):
            for j in range(self.n):
                tile_label = tk.Label(self.root, text="", font=("Helvetica", 16, "bold"), width=4, height=2, relief="ridge", bd=2)
                tile_label.grid(row=i, column=j)
                tile_label.bind("<Button-1>", lambda event, i=i, j=j: self.tile_click(i, j))
                self.tiles[i][j] = tile_label

    def shuffle_tiles(self):
        numbers = list(range(1, self.n**2))
        random.shuffle(numbers)
        for i in range(self.n):
            for j in range(self.n):
                if (i, j) != self.empty_tile:
                    number = numbers.pop()
                    self.tiles[i][j].config(text=str(number))
        self.moves = 0
        self.update_moves_label()

    def tile_click(self, i, j):
        if self.can_move(i, j):
            self.swap_tiles(i, j)
            self.moves += 1
            self.update_moves_label()  # Cập nhật số nước đi trước khi kiểm tra trạng thái chiến thắng
            if self.check_win():
                self.show_win_message()
                self.moves = 0  # Đặt lại số bước đi khi bắt đầu một trò chơi mới
                self.update_moves_label()  # Cập nhật số nước đi sau khi hiển thị thông báo

    def can_move(self, i, j):
        x, y = self.empty_tile
        return (i == x and abs(j - y) == 1) or (j == y and abs(i - x) == 1)

    def swap_tiles(self, i, j):
        x, y = self.empty_tile
        self.tiles[x][y].config(text=self.tiles[i][j]["text"])
        self.tiles[i][j].config(text="")
        self.empty_tile = (i, j)
        self.update_moves_label()

    def update_moves_label(self):
        moves_label.config(text=f"Moves: {self.moves}")

    def get_current_state(self):
        state = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                if self.tiles[i][j]["text"]:
                    row.append(int(self.tiles[i][j]["text"]))
                else:
                    row.append(0)
            state.append(tuple(row))
        return tuple(state)

    def get_possible_moves(self):
        empty_tile_row, empty_tile_col = self.empty_tile
        possible_moves = []

        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = empty_tile_row + i, empty_tile_col + j
            if 0 <= new_row < self.n and 0 <= new_col < self.n:
                new_state = [list(row) for row in self.get_current_state()]
                new_state[empty_tile_row][empty_tile_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_tile_row][empty_tile_col]
                possible_moves.append(tuple(map(tuple, new_state)))

        return possible_moves

    def update_gui_with_solution(self, solution):
        for i in range(self.n):
            for j in range(self.n):
                number = solution[i][j]
                if number != 0:
                    self.tiles[i][j].config(text=str(number))
                else:
                    self.tiles[i][j].config(text="")
                    self.empty_tile = (i, j)
        self.moves = 0
        self.update_moves_label()



root = tk.Tk()
root.title("N-Puzzle Game")
game = NPuzzleGame(root)

# Nút "New Puzzle"
new_puzzle_button = tk.Button(root, text="Reset", command=game.shuffle_tiles)
new_puzzle_button.grid(row=game.n, columnspan=game.n)  # Đặt nút "New Puzzle" dưới cùng

# Nút "Trạng Thái Xuất Phát"
initial_state_button = tk.Button(root, text="Trạng Thái Xuất Phát", command=game.set_initial_state)
initial_state_button.grid(row=game.n + 1, columnspan=game.n)  # Đặt nút "Trạng Thái Xuất Phát" dưới cùng


# Label để hiển thị số bước đi
moves_label = tk.Label(root, text="Moves: 0", font=("Helvetica", 12, "bold"))
moves_label.grid(row=game.n + 3, columnspan=game.n)

root.mainloop()

