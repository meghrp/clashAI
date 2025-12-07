# ClashAI MVP

AI-powered Clash of Clans player advice application. Get personalized upgrade recommendations, attack strategies, and tips based on your player profile.

## Features

- **Player Data Fetching**: Retrieve and display player information from Clash of Clans API
- **AI-Powered Advice**: Get personalized recommendations using OpenRouter AI
- **Data Persistence**: Store player snapshots and advice responses in SQLite
- **Modern UI**: Clean, responsive Next.js frontend

## Prerequisites

- Python 3.9+ (for backend)
- Bun (for frontend)
- Clash of Clans API key ([Get one here](https://developer.clashofclans.com/))
- OpenRouter API key ([Get one here](https://openrouter.ai/))

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend` directory:
   ```env
   COC_API_KEY=your_clash_of_clans_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

5. Initialize the database (runs automatically on first use, but you can also run):
   ```bash
   python -c "from storage.schema import init_db; init_db()"
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   bun install
   ```

3. Create a `.env.local` file in the `frontend` directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Running the Application

### Backend

Start the FastAPI server:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation (Swagger UI) at `http://localhost:8000/docs`

### Frontend

Start the Next.js development server:
```bash
cd frontend
bun run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Enter a Clash of Clans player tag (e.g., `#YOURTAG`)
3. Click "Fetch Player Data" to retrieve player information
4. Optionally check "Focus on war strategies" for war-focused advice
5. Click "Get AI Advice" to generate personalized recommendations

## API Endpoints

### Player Endpoints

- `GET /api/player/{tag}` - Fetch player data and save snapshot
- `GET /api/player/{tag}/history` - Get player snapshot history

### Advice Endpoints

- `POST /api/advice` - Generate AI advice for a player
  ```json
  {
    "tag": "#YOURTAG",
    "war_focus": false,
    "model": "openai/gpt-4-turbo-preview"  // optional
  }
  ```

## Project Structure

```
.
├── backend/
│   ├── api/              # FastAPI routes
│   │   ├── player.py     # Player endpoints
│   │   └── advice.py     # Advice endpoints
│   ├── models/           # Pydantic models
│   │   ├── player.py     # Player data models
│   │   └── advice.py     # Advice models
│   ├── services/         # Business logic
│   │   ├── coc_client.py      # Clash of Clans API client
│   │   └── advice_generator.py # AI advice generator
│   ├── storage/          # Database layer
│   │   ├── schema.py     # SQLAlchemy models
│   │   └── repository.py # Database operations
│   ├── main.py           # FastAPI app entry point
│   └── requirements.txt  # Python dependencies
│
└── frontend/
    ├── app/              # Next.js app directory
    │   ├── page.tsx      # Main page
    │   ├── layout.tsx    # Root layout
    │   └── globals.css   # Global styles
    ├── components/       # React components
    │   ├── PlayerDisplay.tsx
    │   └── AdviceDisplay.tsx
    ├── lib/              # Utilities
    │   └── api.ts        # API client
    ├── types.ts          # TypeScript types
    └── package.json      # Node dependencies
```

## Database

The application uses SQLite (`clashai.db` in the backend directory) to store:
- Player snapshots (raw JSON from Clash of Clans API)
- AI advice responses (for inspection and debugging)

## Environment Variables

### Backend (.env)
- `COC_API_KEY` - Clash of Clans API key (required)
- `OPENROUTER_API_KEY` - OpenRouter API key (required)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Future Extensibility

The codebase includes TODO comments and extensibility points for:
- Multi-account history tracking
- Clan-wide analysis
- Scheduled player data refreshes
- Advanced filtering and search
- Historical trend analysis

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure you're in the backend directory and virtual environment is activated
- **API key errors**: Verify your `.env` file has correct keys
- **Database errors**: Delete `clashai.db` to reset the database

### Frontend Issues

- **API connection errors**: Verify backend is running and `NEXT_PUBLIC_API_URL` is correct
- **Build errors**: Run `bun install` to ensure dependencies are installed

## License

MIT
