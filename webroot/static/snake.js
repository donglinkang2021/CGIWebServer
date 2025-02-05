const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const box = 20;
let snake = [];
snake[0] = { x: 10 * box, y: 10 * box };

let direction = "RIGHT";
let food = {
    x: Math.floor(Math.random() * 20) * box,
    y: Math.floor(Math.random() * 20) * box
};

let gameStarted = false;
let gameInterval;

document.getElementById("startButton").addEventListener("click", startGame);
document.getElementById("restartButton").addEventListener("click", restartGame);

function startGame() {
    gameStarted = true;
    document.getElementById("startButton").style.display = "none";
    document.getElementById("restartButton").style.display = "none";
    clearInterval(gameInterval);
    gameInterval = setInterval(draw, 100);
}

function restartGame() {
    snake = [];
    snake[0] = { x: 10 * box, y: 10 * box };
    direction = "RIGHT";
    food = {
        x: Math.floor(Math.random() * 20) * box,
        y: Math.floor(Math.random() * 20) * box
    };
    document.getElementById("restartButton").style.display = "none";
    startGame();
}

document.addEventListener("keydown", directionControl);

function directionControl(event) {
    if (!gameStarted) return;
    if ((event.keyCode == 37 || event.keyCode == 65) && direction != "RIGHT") {
        direction = "LEFT";
    } else if ((event.keyCode == 38 || event.keyCode == 87) && direction != "DOWN") {
        direction = "UP";
    } else if ((event.keyCode == 39 || event.keyCode == 68) && direction != "LEFT") {
        direction = "RIGHT";
    } else if ((event.keyCode == 40 || event.keyCode == 83) && direction != "UP") {
        direction = "DOWN";
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw snake
    for (let i = 0; i < snake.length; i++) {
        ctx.fillStyle = i == 0 ? "#228B22" : "#32CD32";
        ctx.fillRect(snake[i].x, snake[i].y, box, box);
        ctx.strokeStyle = "#006400";
        ctx.strokeRect(snake[i].x, snake[i].y, box, box);
    }

    // Draw food
    ctx.fillStyle = "#FF4500";
    ctx.fillRect(food.x, food.y, box, box);

    let snakeX = snake[0].x;
    let snakeY = snake[0].y;

    if (direction == "LEFT") snakeX -= box;
    if (direction == "UP") snakeY -= box;
    if (direction == "RIGHT") snakeX += box;
    if (direction == "DOWN") snakeY += box;

    if (snakeX == food.x && snakeY == food.y) {
        food = {
            x: Math.floor(Math.random() * 20) * box,
            y: Math.floor(Math.random() * 20) * box
        };
    } else {
        snake.pop();
    }

    let newHead = {
        x: snakeX,
        y: snakeY
    };

    if (
        snakeX < 0 || snakeY < 0 ||
        snakeX >= canvas.width || snakeY >= canvas.height ||
        collision(newHead, snake)
    ) {
        clearInterval(gameInterval);
        gameStarted = false;
        document.getElementById("restartButton").style.display = "block";
    }

    snake.unshift(newHead);
}

function collision(head, array) {
    for (let i = 0; i < array.length; i++) {
        if (head.x == array[i].x && head.y == array[i].y) {
            return true;
        }
    }
    return false;
}
