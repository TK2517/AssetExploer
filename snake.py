"""Simple Snake game implemented with tkinter.

Run:
    python snake.py
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass


CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
INITIAL_SPEED_MS = 120


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class SnakeGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("贪吃蛇")

        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="#111",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)

        self.status = tk.Label(root, text="按方向键开始", font=("Arial", 12))
        self.status.pack(pady=(0, 10))

        self.reset()

        self.root.bind("<Up>", lambda _: self.change_direction(Point(0, -1)))
        self.root.bind("<Down>", lambda _: self.change_direction(Point(0, 1)))
        self.root.bind("<Left>", lambda _: self.change_direction(Point(-1, 0)))
        self.root.bind("<Right>", lambda _: self.change_direction(Point(1, 0)))
        self.root.bind("<space>", lambda _: self.restart())

    def reset(self) -> None:
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.snake = [Point(cx, cy), Point(cx - 1, cy), Point(cx - 2, cy)]
        self.direction = Point(1, 0)
        self.pending_direction = self.direction
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.running = False
        self.speed_ms = INITIAL_SPEED_MS
        self.render()
        self.status.config(text="按方向键开始，空格重开")

    def spawn_food(self) -> Point:
        snake_set = set(self.snake)
        while True:
            p = Point(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if p not in snake_set:
                return p

    def change_direction(self, d: Point) -> None:
        if self.game_over:
            return
        if d.x == -self.direction.x and d.y == -self.direction.y:
            return
        self.pending_direction = d
        if not self.running:
            self.running = True
            self.tick()

    def tick(self) -> None:
        if self.game_over or not self.running:
            return

        self.direction = self.pending_direction
        head = self.snake[0]
        new_head = Point(head.x + self.direction.x, head.y + self.direction.y)

        # Check wall collision
        if not (0 <= new_head.x < GRID_WIDTH and 0 <= new_head.y < GRID_HEIGHT):
            self.end_game()
            return

        # Check self collision
        will_grow = new_head == self.food
        body_to_check = self.snake if will_grow else self.snake[:-1]
        if new_head in body_to_check:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if will_grow:
            self.score += 1
            self.food = self.spawn_food()
            if self.speed_ms > 70:
                self.speed_ms -= 2
        else:
            self.snake.pop()

        self.render()
        self.status.config(text=f"分数：{self.score} 速度：{1000 // self.speed_ms}")
        self.root.after(self.speed_ms, self.tick)

    def end_game(self) -> None:
        self.game_over = True
        self.running = False
        self.render()
        self.status.config(text=f"游戏结束！分数：{self.score}，按空格重开")

    def restart(self) -> None:
        self.reset()

    def draw_cell(self, p: Point, color: str) -> None:
        x1, y1 = p.x * CELL_SIZE, p.y * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222")

    def render(self) -> None:
        self.canvas.delete("all")

        # Grid
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(x, 0, x, GRID_HEIGHT * CELL_SIZE, fill="#1a1a1a")
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(0, y, GRID_WIDTH * CELL_SIZE, y, fill="#1a1a1a")

        # Food
        self.draw_cell(self.food, "#f44336")

        # Snake
        for i, p in enumerate(self.snake):
            self.draw_cell(p, "#7CFC00" if i == 0 else "#32CD32")


def main() -> None:
    root = tk.Tk()
    SnakeGame(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
