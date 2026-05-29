#  Tic Tac Toe AI using FastAPI, LangGraph, LangSmith & Minimax

This project is an AI-powered Tic Tac Toe game built using Python, FastAPI, LangGraph, and LangSmith.

The application allows a human player to play Tic Tac Toe against an intelligent AI opponent. The AI uses the Minimax algorithm to evaluate all possible future game states and select the optimal move, making it extremely difficult to defeat.

The project demonstrates:

- FastAPI backend development
- LangGraph workflow orchestration
- LangSmith observability and tracing
- AI decision making using Minimax
- Frontend and backend integration
- State management and game logic

---


Traditional Tic Tac Toe implementations often use random move selection.

In this project, the AI:

- Analyzes all possible future game states
- Calculates optimal outcomes
- Chooses the best move every turn
- Never intentionally makes a bad move

Additionally, LangGraph is used to model the game as a workflow rather than writing all logic in a single function.

This demonstrates how AI workflows can be represented as graph-based state machines.

---


```text
┌─────────────────┐
│     Browser     │
│  HTML + JS UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    FastAPI      │
│ REST Endpoints  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LangGraph     │
│ Game Workflow   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Minimax AI   │
│ Best Move Logic │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LangSmith     │
│ AI Tracing      │
└─────────────────┘
```

---


| Technology | Purpose |
|------------|----------|
| Python | Core Programming Language |
| FastAPI | Backend REST API |
| Uvicorn | ASGI Server |
| HTML/CSS/JavaScript | Frontend UI |
| LangGraph | Workflow Orchestration |
| LangSmith | Observability & Tracing |
| Minimax Algorithm | AI Decision Making |
| Jinja2 | HTML Templating |
| Python Dotenv | Environment Variable Management |

---


```text
tic-tac-toe-ai/
│
├── main.py
├── requirements.txt
├── .env
│
├── templates/
│   └── index.html
│
└── README.md
```

---


The AI uses the Minimax algorithm.

The algorithm:

1. Simulates every possible future move
2. Simulates the opponent's response
3. Continues until the game reaches a win, loss, or draw
4. Assigns scores to outcomes

```text
AI Win   = +10
Draw     = 0
Player Win = -10
```

The AI selects the move with the highest score.

Because every possible future board state is evaluated, the AI always chooses the best available move.

---


The game execution is modeled using LangGraph.

Workflow:

```text
validate_board
       │
       ▼
route_after_validation
       │
       ▼
     ai_move
       │
       ▼
      END
```


Checks whether:

- Player already won
- AI already won
- Draw condition reached


If game is still active:

- Calculate best move
- Update board
- Re-check winner


Return final game state to UI.

---


LangSmith is used for:

- AI execution tracing
- Debugging workflows
- Monitoring AI decisions
- Observability

Example:

```python
@traceable(name="find_best_ai_move")
```

This allows every AI move calculation to be visualized inside LangSmith.

---


```bash
git clone https://github.com/YOUR_USERNAME/tic-tac-toe-ai.git
```


```bash
cd tic-tac-toe-ai
```


Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---


```bash
pip install -r requirements.txt
```

---


Create a `.env` file:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=YOUR_API_KEY
LANGSMITH_PROJECT=tic-tac-toe-ai
```

---


```bash
uvicorn main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

---


1. Open browser
2. Navigate to:

```text
http://127.0.0.1:8000
```

3. You play as:

```text
X
```

4. AI plays as:

```text
O
```

5. Click any empty cell
6. AI automatically responds
7. Continue until:
   - Win
   - Loss
   - Draw

---


```http
GET /
```

Returns the game UI.

---


```http
POST /api/play
```

Request:

```json
{
  "board": [
    "X",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
  ]
}
```

Response:

```json
{
  "board": [
    "X",
    "",
    "",
    "",
    "O",
    "",
    "",
    "",
    ""
  ],
  "ai_move": 4,
  "winner": null,
  "message": "Your turn"
}
```

---


```http
POST /api/reset
```

Response:

```json
{
  "board": [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
  ],
  "winner": null,
  "message": "Game reset"
}
```

---


This project demonstrates:

- REST API Development
- FastAPI Framework
- Workflow Orchestration using LangGraph
- AI Decision Making using Minimax
- Frontend & Backend Integration
- LangSmith Observability
- State Management
- Graph-Based Execution Models

---


Potential improvements:

- Multiple Difficulty Levels
- Alpha-Beta Pruning Optimization
- Multiplayer Mode
- OpenAI/LLM Commentary
- Move History
- Game Analytics Dashboard
- Authentication & User Profiles
- Persistent Score Tracking
- Docker Deployment
- Kubernetes Deployment

---


Palguni Aashritha Reddy Solipuram
Backend Engineer | Data Engineer | AI Engineer

Built using FastAPI, LangGraph, LangSmith, and Python.
