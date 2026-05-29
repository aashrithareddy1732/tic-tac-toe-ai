from typing import List, Optional, TypedDict
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langsmith import traceable

load_dotenv()

app = FastAPI(title="Tic Tac Toe AI with FastAPI, LangGraph, LangSmith")
templates = Jinja2Templates(directory="templates")


class GameRequest(BaseModel):
    board: List[str]


class GameState(TypedDict):
    board: List[str]
    winner: Optional[str]
    ai_move: Optional[int]


WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def check_winner(board: List[str]) -> Optional[str]:
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "DRAW"

    return None


def minimax(board: List[str], is_ai_turn: bool) -> int:
    winner = check_winner(board)

    if winner == "O":
        return 10
    if winner == "X":
        return -10
    if winner == "DRAW":
        return 0

    if is_ai_turn:
        best_score = -999
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best_score = max(best_score, score)
        return best_score

    best_score = 999
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            score = minimax(board, True)
            board[i] = ""
            best_score = min(best_score, score)

    return best_score


@traceable(name="find_best_ai_move")
def find_best_move(board: List[str]) -> Optional[int]:
    best_score = -999
    best_move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


def validate_board_node(state: GameState) -> GameState:
    state["winner"] = check_winner(state["board"])
    return state


def ai_move_node(state: GameState) -> GameState:
    if state["winner"]:
        return state

    move = find_best_move(state["board"])

    if move is not None:
        state["board"][move] = "O"
        state["ai_move"] = move

    state["winner"] = check_winner(state["board"])
    return state


def route_after_validation(state: GameState):
    if state["winner"]:
        return END
    return "ai_move"


graph_builder = StateGraph(GameState)
graph_builder.add_node("validate_board", validate_board_node)
graph_builder.add_node("ai_move", ai_move_node)

graph_builder.set_entry_point("validate_board")
graph_builder.add_conditional_edges("validate_board", route_after_validation)
graph_builder.add_edge("ai_move", END)

game_graph = graph_builder.compile()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/api/play")
def play_game(request: GameRequest):
    if len(request.board) != 9:
        return {"error": "Board must contain exactly 9 cells"}

    if any(cell not in ["X", "O", ""] for cell in request.board):
        return {"error": "Board values must be X, O, or empty string"}

    initial_state: GameState = {
        "board": request.board,
        "winner": None,
        "ai_move": None
    }

    result = game_graph.invoke(initial_state)

    return {
        "board": result["board"],
        "ai_move": result["ai_move"],
        "winner": result["winner"],
        "message": get_message(result["winner"])
    }


@app.post("/api/reset")
def reset_game():
    return {
        "board": ["", "", "", "", "", "", "", "", ""],
        "winner": None,
        "message": "Game reset"
    }


def get_message(winner: Optional[str]) -> str:
    if winner == "X":
        return "You won!"
    if winner == "O":
        return "AI won!"
    if winner == "DRAW":
        return "Game draw!"
    return "Your turn"