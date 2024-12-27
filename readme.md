# Evil Rat Bot

A Discord bot written in Python featuring a fantasy rat innkeeper named Sławek who provides dice rolling functionality, scheduling features, and AI-powered character interactions.

## Features

### Dice Rolling System
- Standard dice rolling with `.roll` or `.r`
  - Supports standard D&D dice notation (e.g., `1d20`, `2d6+3`)
  - Advantage/disadvantage rolls with `adv`/`dis` keywords
- Multiple rolls with `.multiroll` or `.rr`
  - Roll the same dice multiple times
- Iterative rolls with `.iterroll` or `.rrr`
  - Roll against DC with success tracking
- Custom critical success/failure messages
- Markdown-formatted output

### Scheduling System
- Weekly game scheduling automation
- Reaction-based availability tracking
- Custom emoji support
- Automatic day/time aggregation
- Threshold-based availability indicators

### AI Character Interaction (Sławek the Rat)
- Interactive fantasy rat innkeeper character
- Context-aware responses based on channel categories
- Character memory system
- Custom response strategies per user
- Natural language processing using GPT-4

## Prerequisites

- Python 3.10+
- Discord Bot Token
- OpenAI API Key

## Environment Variables

Create a `.env` file with:
```env
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API=your_openai_api_key
SCHEDULE_CHANNEL=your_schedule_channel_id
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Butterski/evil-rat-bot.git
cd evil-rat-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
   - Copy `cogs/askRat/channelconfig_template.json` to `channelconfig.json`
   - Copy `cogs/askRat/charinfos_template.json` to `charinfos.json`
   - Update both files with your server's configuration

## Running the Bot

### Using Shell Script
```bash
chmod +x run.sh
./run.sh
```

### Using Docker
```bash
docker build -t evil-rat-bot .
docker run -d evil-rat-bot
```

## Configuration Files

### Channel Configuration
```json
{
    "categories": [category_id_1, category_id_2],
    "channels": [channel_id_1, channel_id_2]
}
```

### Character Information
```json
{
    "user_nickname": {
        "info": "General information about the user",
        "character": "User's character description",
        "response_strategy": "How the bot should respond to this user"
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Uses the [d20](https://github.com/avrae/d20) rolling system
- Powered by OpenAI's GPT-4
- Built with discord.py