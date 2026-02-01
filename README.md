# Solslay Auto Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

Automated bot for Solslay game that handles faucet claims, quest completion, jackpot betting, and boss battles.

## 🌐 Official Website

**Join Solslay:** [https://solslay.com/invite/QEM6Q2](https://solslay.com/invite/QEM6Q2)

## ✨ Features

- 🔄 **Auto Faucet**: Automatically claims faucet rewards when available
- 📋 **Quest Completion**: Completes social quests automatically
- 🎰 **Jackpot Betting**: Places bets in SPL Jackpot rounds
- ⚔️ **Boss Battle**: Attacks boss automatically with configurable multiplier
- 🔐 **Multi-Account Support**: Handle multiple accounts simultaneously
- 🌐 **Proxy Support**: Optional proxy support for enhanced privacy
- ⏰ **Auto Loop**: Continuous operation with customizable cycle delays
- 📊 **Detailed Logging**: Color-coded logs with timestamps

## 📋 Requirements

- Python 3.8 or higher
- Internet connection
- Solana wallet private keys

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/febriyan9346/Solslay-Auto-Bot.git
cd Solslay-Auto-Bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your accounts

Create an `accounts.txt` file and add your Solana wallet private keys (one per line):

```
your_private_key_1
your_private_key_2
your_private_key_3
```

**⚠️ IMPORTANT**: Never share your private keys with anyone!

### 4. (Optional) Configure proxies

If you want to use proxies, create a `proxy.txt` file with your proxy addresses (one per line):

```
ip:port:username:password
ip:port:username:password
```

Or without authentication:

```
ip:port
ip:port
```

## 💻 Usage

### Run the bot

```bash
python bot.py
```

### Select mode

When the bot starts, you'll be prompted to choose:
1. Run with proxy
2. Run without proxy

Enter `1` or `2` to select your preferred mode.

### Bot will automatically:
- ✅ Login to all accounts
- ✅ Claim faucet rewards
- ✅ Complete available quests
- ✅ Place jackpot bets
- ✅ Attack boss
- ✅ Repeat the cycle every hour (default)

## ⚙️ Configuration

You can modify the bot settings by editing the `__init__` method in `bot.py`:

```python
self.enable_faucet = True          # Enable/disable faucet claiming
self.enable_quest = True           # Enable/disable quest completion
self.enable_bet = True             # Enable/disable jackpot betting
self.enable_boss = True            # Enable/disable boss battles
self.bet_amount = 50               # Amount to bet in jackpot
self.boss_multiplier = 10          # Boss attack multiplier
self.boss_attack_count = 2         # Number of boss attacks per cycle
self.loop_delay = 3600             # Delay between cycles (seconds)
```

## 📁 File Structure

```
Solslay-Auto-Bot/
├── bot.py                  # Main bot script
├── accounts.txt           # Your wallet private keys (not included)
├── proxy.txt              # Your proxy list (optional, not included)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore file
```

## 🛡️ Security Notice

- **NEVER** commit your `accounts.txt` or `proxy.txt` files to GitHub
- Keep your private keys secure and confidential
- Use at your own risk
- This bot is for educational purposes only

## 🔧 Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: accounts.txt`
- **Solution**: Create an `accounts.txt` file with your private keys

**Issue**: Login failed
- **Solution**: Check if your private keys are valid and properly formatted

**Issue**: Proxy connection errors
- **Solution**: Verify your proxy credentials and format

**Issue**: Module not found errors
- **Solution**: Run `pip install -r requirements.txt` again

## 📝 Changelog

### Version 1.0.0
- Initial release
- Basic faucet, quest, betting, and boss battle functionality
- Multi-account support
- Proxy support
- Auto-loop functionality

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This bot is provided as-is for educational purposes only. Use at your own risk. The author is not responsible for any damages, losses, or issues that may arise from using this bot. Always comply with Solslay's Terms of Service.

## 👨‍💻 Author

**FEBRIYAN**

---

## 💰 Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|----------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

Your support helps maintain and improve this project. Thank you! 🙏
