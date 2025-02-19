from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import logging
import os

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 10000))  # Используем порт, который задаёт Render

logging.basicConfig(filename='/tmp/server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

games = {}

@app.route('/')
def home():
    return jsonify({"message": "Chess server is running!"})

@app.route('/api/start_game', methods=['POST'])
def start_game():
    game_id = request.json.get('game_id')
    if not game_id:
        return jsonify({'error': 'Game ID is required'}), 400

    games[game_id] = chess.Board()
    logging.info(f"Game {game_id} started")
    return jsonify({'message': 'Game started', 'fen': games[game_id].fen()}), 200

@app.route('/api/make_move', methods=['POST'])
def make_move():
    game_id = request.json.get('game_id')
    move = request.json.get('move')

    if not game_id or not move:
        return jsonify({'error': 'Game ID and move are required'}), 400

    board = games.get(game_id)
    if not board:
        return jsonify({'error': 'Game not found'}), 404

    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move not in board.legal_moves:
            return jsonify({'error': 'Illegal move'}), 400

        board.push(chess_move)
        logging.info(f"Move {move} made in game {game_id}")
        return jsonify({'message': 'Move accepted', 'fen': board.fen()}), 200
    except Exception as e:
        logging.error(f"Error in game {game_id}: {str(e)}")
        return jsonify({'error': 'Invalid move'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
