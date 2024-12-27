# FantasyRatBot

A Discord bot written in Python that serves as an interactive fantasy rat innkeeper named Sławek. The bot provides dice rolling functionality, scheduling features, and AI-powered character interactions.

## Technologies Used

- **Python 3.10**
- **discord.py** - Core Discord bot functionality
- **OpenAI API** - Powers the AI character interactions
- **d20** - Handles dice rolling mechanics (same system used by Avrae)
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipeline

## Features

- **Dice Rolling System**
  - Standard dice rolling with `.roll` or `.r`
  - Multiple rolls with `.multiroll` or `.rr`
  - Iterative rolls with `.iterroll` or `.rrr`
  - Special critical success/failure messages
  - Support for advantage/disadvantage

- **Scheduling System**
  - Automated weekly game scheduling
  - Reaction-based availability tracking
  - Custom emote support

- **AI Character Interaction**
  - Interactive fantasy rat innkeeper character
  - Contextual responses based on channel categories
  - Character memory system

## Prerequisites

- Python 3.10 or higher
- Discord Bot Token
- OpenAI API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FantasyRatBot.git
cd FantasyRatBot
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```env
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API=your_openai_api_key
SCHEDULE_CHANNEL=your_schedule_channel_id
```

## Configuration Files Setup

### askRat Configuration

1. Create `charinfos.json` in the `cogs/askRat/` directory using the template:
```json
{
  "user_nickname": {
    "info": "General information about the user",
    "character": "User's character description",
    "response_strategy": "How the bot should respond to this user"
  }
}
```

2. Create `channelconfig.json` in the `cogs/askRat/` directory using the template:
```json
{
  "categories": [category_id_1, category_id_2],
  "channels": [channel_id_1, channel_id_2]
}
```

## Running the Bot

### Using Shell Script
```bash
chmod +x run.sh  # Make script executable (Unix-like systems only)
./run.sh
```

### Using Docker

1. Build the Docker image:
```bash
docker build -t fantasyratbot .
```

2. Run the container:
```bash
docker run -d fantasyratbot
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request


## Acknowledgments

- Based on the [Avrae](https://github.com/avrae/avrae) bot
- Uses the [d20](https://github.com/avrae/d20) rolling system