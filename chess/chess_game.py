import tkinter as tk
from tkinter import messagebox
import chess
import chess.engine
from PIL import Image, ImageTk

from openai import OpenAI

client = OpenAI()

STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag and Drop Chess")
        self.board = chess.Board()
        self.square_size = 96
        self.images = {}
        self.create_widgets()
        self.update_board()
        self.selected_piece = None
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.move_history = []
        print("ChessApp initialized")

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.LEFT)
        
        self.canvas = tk.Canvas(self.frame, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()
        
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.chat_log = tk.Text(self.chat_frame, state=tk.DISABLED)
        self.chat_log.pack(fill=tk.BOTH, expand=True)

        for row in range(8):
            for col in range(8):
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(col*self.square_size, row*self.square_size,
                                             (col+1)*self.square_size, (row+1)*self.square_size,
                                             fill=color, tags=("square",))

        self.canvas.tag_bind("piece", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.drag_motion)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>", self.drag_end)

    def update_board(self):
        self.canvas.delete("piece")
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                image = self.get_piece_image(piece)
                row, col = divmod(square, 8)
                self.canvas.create_image(col*self.square_size + self.square_size//2,
                                        (7-row)*self.square_size + self.square_size//2,
                                        image=image, tags=("piece", chess.square_name(square)))

    def get_piece_image(self, piece):
        piece_name = chess.piece_name(piece.piece_type)
        color = "w" if piece.color == chess.WHITE else "b"
        image_path = f"chess/pieces/{piece_name}_{color}.png"
        if image_path not in self.images:
            image = Image.open(image_path)
            image = image.resize((self.square_size, self.square_size))
            self.images[image_path] = ImageTk.PhotoImage(image)
        return self.images[image_path]

    def drag_start(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.selected_piece = item
        self.drag_data["item"] = item
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        tags = self.canvas.gettags(item)
        if "piece" in tags:
            self.drag_data["start_square"] = tags[tags.index("piece") + 1]
        else:
            self.drag_data["start_square"] = None

    def drag_motion(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.canvas.move(self.selected_piece, delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag_end(self, event):
        item = self.drag_data["item"]
        start_square = self.drag_data["start_square"]
        end_square = self.get_square(event.x, event.y)
        
        if start_square is None:
            return
        
        if start_square == chess.square_name(end_square):
            self.canvas.coords(item, *self.get_piece_coords(chess.parse_square(start_square)))
            return
        
        try:
            move = chess.Move.from_uci(start_square + chess.square_name(end_square))
            if move in self.board.legal_moves:
                piece = self.board.piece_at(chess.parse_square(start_square))
                self.board.push(move)
                self.update_board()
                self.display_feedback(self.get_eval(), break_line=True)
                self.get_feedback(move, piece)
            
                if self.board.is_check():
                    messagebox.showinfo("Check", "Your king is in check!")
                if not self.board.is_game_over():
                    self.engine_move()
            else:
                self.reset_piece_position(item, start_square)
        except ValueError as e:
            self.reset_piece_position(item, start_square)

    def reset_piece_position(self, item, start_square):
        if start_square is not None:
            coords = self.get_piece_coords(start_square)
            if coords:
                self.canvas.coords(item, *coords)

    def get_square(self, x, y):
        col = x // self.square_size
        row = y // self.square_size
        return chess.square(col, 7-row)

    def get_piece_coords(self, square):
        if isinstance(square, str):
            row, col = divmod(chess.parse_square(square), 8)
            x = col * self.square_size + self.square_size // 2
            y = (7-row) * self.square_size + self.square_size // 2
            return x, y
        return None

    def engine_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.01, depth=5))
        self.board.push(result.move)
        self.move_history.append((result.move, self.board.piece_at(result.move.from_square)))
        self.update_board()
        if self.board.is_game_over():
            result = self.board.result()
            messagebox.showinfo("Game Over", f"Result: {result}")
            
    def get_eval(self):
        info = self.engine.analyse(self.board, chess.engine.Limit(time=0.5))
        return info.get("score", chess.engine.Cp(0))

    def get_feedback(self, move, piece):
        self.move_history.append((move, piece))
        #self.display_feedback("Loading feedback...", break_line=False)
        #self.root.after(100, lambda: self.fetch_feedback(move, piece))
            
    def fetch_feedback(self, move, piece):
        prefix = "You're a GM chess player and you're teaching a beginner how to play chess. Be very brief and to the point. The moves go through a computer, so all moves are legal. The beginner plays white and just made a move in the following position: \n"
        
        prompt = f"Analyze the move White {piece}, move: {move} in the following chess position:\n\n{self.board.fen()} \n"
        
        eval = self.get_eval()
        eval_string = f"Eval from the engine: {eval} \n"
        
        suffix = "Reply with Feedback."
        
        messages=[
                {"role": "system", "content": prefix},
                {"role": "system", "content": prompt},
                {"role": "system", "content": eval_string},
                {"role": "system", "content": suffix},
            ]
        
        try:
            completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages
            )
            feedback = completion.choices[0].message.content
            self.root.after(0, lambda: self.display_feedback(f"Move: {move}\n Eval: {eval_string}\n Feedback: {feedback}\n", break_line=True))
        except Exception as e:
            print(e)
            self.root.after(0, lambda: self.display_feedback("Failed to get feedback", break_line=True))

    def display_feedback(self, message, break_line=True):
        self.chat_log.config(state=tk.NORMAL)
        if break_line:
            self.chat_log.insert(tk.END, message)
            self.chat_log.insert(tk.END, "\n")
        else:
            self.chat_log.insert(tk.END, message)
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.yview(tk.END)

    def close(self):
        self.engine.quit()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
