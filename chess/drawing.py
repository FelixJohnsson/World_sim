from PIL import Image

# Load the image
image_path = "./chess/pieces.png"
img = Image.open(image_path)

# Define piece names and their order in the image
piece_names = ["rook_b", "bishop_b", "queen_b", "king_b", "knight_b", "pawn_b", "rook_w", "bishop_w", "queen_w", "king_w", "knight_w", "pawn_w"]
piece_width = img.width // 6  # There are 6 pieces in each row
piece_height = img.height // 2  # There are 2 rows

# Extract and save each piece
for row in range(2):
    for col in range(6):
        left = col * piece_width
        upper = row * piece_height
        right = left + piece_width
        lower = upper + piece_height
        piece = img.crop((left, upper, right, lower))
        piece_name = piece_names[row * 6 + col]
        piece.save(f"chess/pieces/{piece_name}.png")

print("Pieces extracted and saved successfully.")
