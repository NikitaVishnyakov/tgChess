from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import logging

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с других доменов

# Логирование
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Храним текущие партии
games = {}

@app.route('/start_game', methods=['POST'])
def start_game():
    game_id = request.json.get('game_id')
    if not game_id:
        return jsonify({'error': 'Game ID is required'}), 400

    games[game_id] = chess.Board()
    logging.info(f"Game {game_id} started")
    return jsonify({'message': 'Game started', 'fen': games[game_id].fen()}), 200

@app.route('/make_move', methods=['POST'])
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
    app.run(debug=True, port=5000)
