# Bazaar — PSX Terminal

A professional stock technical-analysis application designed for the Pakistan Stock Exchange (PSX).

## Architecture

```
bazaar/
├── frontend/          # React + TypeScript + Tailwind CSS
│   ├── src/
│   │   ├── components/    # React components (TopBar, Watchlist, Chart, SignalsPanel)
│   │   ├── pages/         # Page-level views
│   │   ├── hooks/         # Custom React hooks
│   │   ├── utils/         # Indicator calculations, formatters
│   │   ├── services/      # API service layer
│   │   ├── store/         # Zustand state management
│   │   ├── types/         # TypeScript type definitions
│   │   └── styles/        # Global styles, Tailwind config
│   └── public/            # Static assets
├── backend/           # Python + FastAPI
│   └── app/
│       ├── api/         # Route handlers (market data, config)
│       ├── core/        # Config, security, database
│       ├── models/      # SQLAlchemy ORM models
│       ├── schemas/     # Pydantic schemas
│       ├── services/    # Business logic
│       ├── data/        # Data fetching & processing
│       └── tests/       # Unit tests
├── database/          # PostgreSQL migrations
├── docs/              # Documentation
└── charts/            # Chart component library
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript 5, Tailwind CSS 3 |
| State | Zustand |
| Charts | SVG (TradingView Lightweight Charts planned) |
| Backend | Python 3.10+, FastAPI |
| Data | Pandas, NumPy |
| Database | PostgreSQL + SQLAlchemy 2.0 |
| Auth | JWT, Passlib (bcrypt) |
| Build | Vite |

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The app runs at `http://localhost:3000`.

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Edit with your credentials
python -m app.main
```
The API runs at `http://localhost:8000`.

### Database Setup
```bash
createdb bazaar
# Or use PostgreSQL tools to create the database
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/market/symbols` | List all PSX symbols |
| GET | `/api/market/ohlcv/{symbol}` | Get OHLCV data for a symbol |
| GET | `/api/market/ohlcv/{symbol}/summary` | Get summary & indicators |
| GET | `/api/market/health` | Health check |
| GET | `/api/config/` | Get API configuration |
| POST | `/api/config/` | Set API configuration |
| GET | `/api/config/env-check` | Check environment variables |

## Modules Roadmap

### Phase 1: Foundation
- [x] Market Data Module
- [x] Chart Module (Price, Volume, RSI, MACD)
- [x] UI Dashboard (from demo.html)
- [x] Watchlist with sparklines
- [x] Timeframe Selection (1M, 3M, 6M, 1Y)

### Phase 2: Indicators & Signals
- [ ] Indicator Module (SMA, EMA, RSI, MACD, Bollinger Bands)
- [ ] Signal Module (Trend, Momentum, Key Levels)
- [ ] Settings Module (API configuration)

### Phase 3: Strategy & Analysis
- [ ] Strategy Module
- [ ] AI Analysis Module
- [ ] Signal Module
- [ ] Backtesting Module
- [ ] Risk Management Module

### Phase 4: Advanced
- [ ] WebSocket real-time data
- [ ] Paper trading simulator
- [ ] Alert system
- [ ] Drawing tools on charts
- [ ] Portfolio tracker
- [ ] News/sentiment feed
- [ ] Custom indicator builder

## Project Structure - Data Flow

```
Frontend (React) → WebSocket/HTTP → Backend (FastAPI) → Data Service → PSX API
     ↓                                                        ↓
  State (Zustand)                                      PostgreSQL
     ↓
  UI Components → Chart SVG, Signals Panel, Watchlist
```

## Key Principles

1. **Never hardcode API keys** - Use environment variables
2. **Modular architecture** - Each module is independent and extensible
3. **Normalized OHLCV model** - `timestamp, open, high, low, close, volume, symbol`
4. **Error handling** - Invalid symbols, API failures, rate limits
5. **Loading & empty states** - All data views have states
6. **Logging** - Comprehensive logging at all layers
7. **Unit tests** - Test coverage for all critical functions

## Where to Put Your PSX API

The PSX market data provider integration goes in:
- `backend/app/data/market_feed.py` - Connect to the PSX API
- `backend/app/services/data_pipeline.py` - Process and normalize incoming data
- Set `PSX_API_KEY`, `PSX_API_URL`, `PSX_API_SECRET` in your `.env` file

The backend has a clean API layer so your PSX data provider can be swapped later.

## License

MIT
