import tkinter as tk
import random

FONT_BIG = ("Consolas", 36, "bold")
FONT_SCORE = ("Consolas", 18)
FONT_STATUS = ("Consolas", 40, "bold")

class TicTacToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe Almdrasa")

        self.player_score = 0
        self.computer_score = 0

        top_frame = tk.Frame(root, pady=10)
        top_frame.pack()

        self.score_label = tk.Label(top_frame, text=self.score_text(), font=FONT_SCORE)
        self.score_label.pack()

        self.status_label = tk.Label(root, text="", font=FONT_STATUS)
        self.status_label.pack(pady=(5,10))

        self.restart_btn = tk.Button(root, text="restart", command=self.restart_round)
        self.restart_btn.pack()

        self.board_frame = tk.Frame(root, padx=10, pady=10)
        self.board_frame.pack()

        self.default_bg = root.cget("bg")
        self.buttons = {}
        self.reset_board_state()

        
        for r in range(3):
            for c in range(3):
                b = tk.Button(self.board_frame, text="", width=6, height=3,
                              font=FONT_BIG, command=lambda rr=r, cc=c: self.player_move(rr, cc))
                b.grid(row=r, column=c, ipadx=10, ipady=10, sticky="nsew", padx=1, pady=1)
                self.buttons[(r, c)] = b

    def score_text(self):
        return f"You: {self.player_score}   Computer: {self.computer_score}"

    def reset_board_state(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = "X" 

    def player_move(self, r, c):
        if self.game_over:
            return
        if self.board[r][c] != "":
            return
        self.place_mark(r, c, "X")
        winner, win_positions = self.check_winner()
        if winner:
            self.handle_win(winner, win_positions)
            return
        if self.is_draw():
            self.handle_draw()
            return
        
        self.root.after(200, self.computer_move)

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
            return

    def place_mark(self, r, c, mark):
        self.board[r][c] = mark
        btn = self.buttons[(r, c)]
        btn.config(text=mark)

    def check_winner(self):
        b = self.board
        lines = []
        
        for r in range(3):
            lines.append(((r,0),(r,1),(r,2)))

        for c in range(3):
            lines.append(((0,c),(1,c),(2,c)))

        lines.append(((0,0),(1,1),(2,2)))
        lines.append(((0,2),(1,1),(2,0)))

        for line in lines:
            a,b1,c1 = line
            v1 = self.board[a[0]][a[1]]
            v2 = self.board[b1[0]][b1[1]]
            v3 = self.board[c1[0]][c1[1]]
            if v1 != "" and v1 == v2 == v3:
                return v1, line
        return None, None

    def handle_win(self, winner, win_positions):
        self.game_over = True
        if winner == "X":
            self.player_score += 1
            self.status_label.config(text="X wins!")
        else:
            self.computer_score += 1
            self.status_label.config(text="O wins!")
        for pos in win_positions:
            self.buttons[pos].config(bg="#00E5E5")  
        self.score_label.config(text=self.score_text())

    def is_draw(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    return False
        return True

    def handle_draw(self):
        self.game_over = True
        self.status_label.config(text="Tie, No Winner!")
        
        for btn in self.buttons.values():
            btn.config(bg="#E53935")
        self.score_label.config(text=self.score_text())

    def restart_round(self):
        self.reset_board_state()

        self.status_label.config(text="")
        for pos, btn in self.buttons.items():
            btn.config(text="", bg="SystemButtonFace")


root = tk.Tk()
app = TicTacToe(root)
root.mainloop()
