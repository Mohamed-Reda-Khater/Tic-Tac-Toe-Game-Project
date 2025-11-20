import tkinter as tk
import random

# ====== Constants ======
FONT_MARK = ("Consolas", 72, "bold")
FONT_SCORE = ("Consolas", 18, "bold")
FONT_STATUS = ("Consolas", 24, "bold")

COLOR_BG = "#f0f0f0"
COLOR_BTN = "#ffffff"
COLOR_BTN_HOVER = "#e0f7fa"
COLOR_WIN = "#00E5E5"
COLOR_DRAW = "#E53935"
COLOR_X = "#1a237e"
COLOR_O = "#b71c1c"

# ====== TicTacToe Class ======
class TicTacToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe Almdrasa")
        root.geometry("600x650")
        root.configure(bg=COLOR_BG)

        # ====== Game Variables ======
        self.player_score = 0
        self.computer_score = 0
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False

        # ====== Top Frame: Score and Status ======
        top_frame = tk.Frame(root, bg=COLOR_BG, pady=5)
        top_frame.pack(fill="x")

        self.score_label = tk.Label(top_frame, text=self.score_text(), font=FONT_SCORE, bg=COLOR_BG)
        self.score_label.pack()

        self.status_label = tk.Label(root, text="", font=FONT_STATUS, bg=COLOR_BG)
        self.status_label.pack(pady=5)

        # ====== Restart Button ======
        self.restart_btn = tk.Button(root, text="Restart", font=FONT_SCORE, command=self.restart_round,
                                     bg="#4caf50", fg="#ffffff", activebackground="#66bb6a", padx=10, pady=5)
        self.restart_btn.pack(pady=5)

        # ====== Board Frame ======
        self.board_frame = tk.Frame(root, bg=COLOR_BG)
        self.board_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Configure grid weights for responsiveness
        for i in range(3):
            self.board_frame.rowconfigure(i, weight=1)
            self.board_frame.columnconfigure(i, weight=1)

        # Create buttons for grid
        self.buttons = {}
        for r in range(3):
            for c in range(3):
                b = tk.Button(self.board_frame, text="", font=FONT_MARK, bg=COLOR_BTN,
                              fg="#000000", command=lambda rr=r, cc=c: self.player_move(rr, cc))
                b.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
                self.buttons[(r, c)] = b

    # ====== Score Text ======
    def score_text(self):
        return f"You: {self.player_score}   Computer: {self.computer_score}"

    # ====== Player Move ======
    def player_move(self, r, c):
        if self.game_over or self.board[r][c] != "":
            return
        self.place_mark(r, c, "X")
        winner, win_positions = self.check_winner()
        if winner:
            self.handle_win(winner, win_positions)
            return
        if self.is_draw():
            self.handle_draw()
            return
        self.root.after(300, self.computer_move)  # delay computer move

    # ====== Computer Move (Random) ======
    def computer_move(self):
        if self.game_over:
            return
        empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        if not empty:
            return
        r, c = random.choice(empty)
        self.place_mark(r, c, "O")
        winner, win_positions = self.check_winner()
        if winner:
            self.handle_win(winner, win_positions)
            return
        if self.is_draw():
            self.handle_draw()

    # ====== Place Mark on Board ======
    def place_mark(self, r, c, mark):
        self.board[r][c] = mark
        btn = self.buttons[(r, c)]
        btn.config(text=mark, fg=COLOR_X if mark=="X" else COLOR_O, bg=COLOR_BTN_HOVER)

    # ====== Check Winner ======
    def check_winner(self):
        lines = []
        for i in range(3):
            lines.append(((i,0),(i,1),(i,2)))  # rows
            lines.append(((0,i),(1,i),(2,i)))  # columns
        lines.append(((0,0),(1,1),(2,2)))      # diagonal
        lines.append(((0,2),(1,1),(2,0)))      # diagonal
        for line in lines:
            a,b1,c1 = line
            v1 = self.board[a[0]][a[1]]
            v2 = self.board[b1[0]][b1[1]]
            v3 = self.board[c1[0]][c1[1]]
            if v1 != "" and v1 == v2 == v3:
                return v1, line
        return None, None

    # ====== Handle Win ======
    def handle_win(self, winner, win_positions):
        self.game_over = True
        if winner == "X":
            self.player_score += 1
            self.status_label.config(text="You Win!", fg=COLOR_X)
        else:
            self.computer_score += 1
            self.status_label.config(text="Computer Wins!", fg=COLOR_O)
        for pos in win_positions:
            self.buttons[pos].config(bg=COLOR_WIN)
        self.score_label.config(text=self.score_text())

    # ====== Check Draw ======
    def is_draw(self):
        return all(self.board[r][c] != "" for r in range(3) for c in range(3))

    # ====== Handle Draw ======
    def handle_draw(self):
        self.game_over = True
        self.status_label.config(text="It's a Draw!", fg=COLOR_DRAW)
        for btn in self.buttons.values():
            btn.config(bg=COLOR_DRAW)
        self.score_label.config(text=self.score_text())

    # ====== Restart Round ======
    def restart_round(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.status_label.config(text="")
        for btn in self.buttons.values():
            btn.config(text="", bg=COLOR_BTN, fg="#000000")

# ====== Run the Game ======
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
