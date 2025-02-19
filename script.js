const API_URL = "http://127.0.0.1:5000"; // Адрес Flask-сервера
let gameId = "game123"; // Идентификатор игры
let board;

function startGame() {
  fetch(`${API_URL}/start_game`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.fen) {
        board.position(data.fen); // Устанавливаем начальную позицию
      }
    })
    .catch((err) => console.error("Ошибка старта игры:", err));
}

// Инициализация шахматной доски
board = Chessboard("board", {
  draggable: true,
  position: "start",
  onDrop: (source, target) => {
    const move = `${source}${target}`;

    fetch(`${API_URL}/make_move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ game_id: gameId, move }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.fen) {
          board.position(data.fen); // Обновляем позицию доски
        } else {
          alert(data.error); // Показываем ошибку, если ход недопустим
          return "snapback";
        }
      })
      .catch((err) => console.error("Ошибка хода:", err));
  },
});
