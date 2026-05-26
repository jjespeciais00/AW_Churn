# AW_Churn

AI-powered analytics platform for churn prediction and customer analytics.

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

## Project Structure

```
src/
├── App.tsx           # Root component
├── main.tsx          # React entry point
├── Dashboard.tsx     # Main dashboard
├── AgentBox.tsx      # Agent component
└── style.css         # Global styles
```

## Environment Variables

Create a `.env` file in the root directory:

```
VITE_GRAPHQL_ENDPOINT=
VITE_AGENT_ENDPOINT=
```

## Technologies

- React 18
- TypeScript
- Vite
- CSS3

## License

MIT
