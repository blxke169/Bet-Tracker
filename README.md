# EdgeLab Bet Tracker — No AI Feedback

Based on your previous EdgeLab tracker. Keeps singles, multis, bankroll, sport filters, bet-type ROI, CLV, reasoning, CSV exports and optional data tools. AI feedback, AI reviews and AI provider calls are removed.

## Streamlit deployment
1. Unzip this download.
2. Upload app.py and requirements.txt to your GitHub repository root.
3. In Streamlit Community Cloud select that repository, branch and main file path: app.py.
4. No OpenAI or Groq key is required. Optional sports-data integrations have their own configuration.

If updating your existing app, replace its main Python file with this app.py using the existing main filename. Do not delete betting.db. The previous database schema remains compatible; old AI columns are retained internally for compatibility.

## Use
Log Bet saves singles; Multis records each leg. Sport-specific notes are optional. Results & Notes records outcomes, calculates ordinary win/loss/push P&L and lets you override it for cashouts, each-way or dead-heat settlements. Closing odds remain blank until you know them. Performance breaks down results by sport and bet type.

CLV is the change in implied probability, in percentage points: (1 / closing odds - 1 / odds taken) × 100. ROI uses settled profit divided by settled stake. Data tools and probability-based analysis remain optional; signals depend on your inputs and are not proven predictive estimates.

## Backups
Streamlit Community Cloud local SQLite storage can reset during restarts/redeploys. Keep CSV exports and a copy of betting.db. This package does not include your deployed bet history. For permanent cross-device records, a persistent database is needed.

## Local run
pip install -r requirements.txt
streamlit run app.py

## Clean Finance update
Navigation now runs across the top, with a second row of sport filters. Both rows scroll horizontally on small screens. Filters apply to Dashboard, Today, Performance and History; account bankroll stays global. Includes gentle card hover, selected-tab styling, save confirmations, chart hover/tap details and reduced-motion support.

Verified with Streamlit AppTest: every page loads, single bet logging, settlement and manual notes, sport filters and dashboard quick navigation.
