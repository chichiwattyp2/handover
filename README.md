# WhatsApp Chat Analyzer 💬

An AI-powered web application that analyzes WhatsApp conversations to provide intelligent insights including summaries, sentiment analysis, and actionable items extraction.

![WhatsApp Chat Analyzer](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Claude AI](https://img.shields.io/badge/Claude-AI-purple.svg)

## ✨ Features

- **📊 Conversation Summary**: Get concise, AI-generated summaries of your WhatsApp chats
- **😊 Sentiment Analysis**: Understand the overall mood and individual participant sentiments
- **✅ Action Items Extraction**: Automatically identify tasks, commitments, and deadlines
- **🏷️ Topic Detection**: Discover main topics discussed in the conversation
- **💡 Conversation Insights**: Get details about tone, engagement level, and key points
- **🎨 Modern UI**: Clean, responsive interface that works on all devices
- **🔒 Privacy First**: All processing happens on your server - no data stored

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd handover
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env and add your Anthropic API key
   # ANTHROPIC_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**

   Navigate to `http://localhost:5000`

## 📖 How to Use

### Exporting WhatsApp Chat

1. Open WhatsApp on your phone
2. Go to the chat you want to analyze
3. Tap the three dots (⋮) or the chat name at the top
4. Select **More** → **Export chat**
5. Choose **Without Media** (to keep file size small)
6. Save the `.txt` file to your computer

### Supported Chat Formats

The analyzer automatically detects and parses multiple WhatsApp export formats:

- ✅ **YYYY/MM/DD, HH:MM** - `2025/02/20, 14:25` (Most common international format)
- ✅ **M/D/YY, HH:MM AM/PM** - `11/10/24, 9:15 AM` (US format)
- ✅ **DD/MM/YY, HH:MM** - `20/02/25, 14:25` (European format)
- ✅ **[Bracketed formats]** - `[11/10/24, 9:15:45 AM]`
- ✅ **Multi-line messages** - Automatically concatenated
- ✅ **System notifications** - Identified and filtered

### Analyzing the Chat

1. Open the WhatsApp Chat Analyzer in your browser
2. Click **Choose File** and select your exported WhatsApp chat `.txt` file
3. Click **Analyze Chat**
4. Wait a few seconds while the AI processes your conversation
5. Review the comprehensive analysis!

## 🎯 What You'll Get

### 1. Conversation Overview
- List of participants
- Total message count
- Date range of the conversation

### 2. Conversation Summary
A concise 2-3 paragraph summary of the main topics and key points discussed.

### 3. Sentiment Analysis
- Overall sentiment (Positive/Negative/Neutral/Mixed)
- Confidence score
- Individual sentiment for each participant
- Explanation of the sentiment assessment

### 4. Key Topics
A list of main topics identified in the conversation.

### 5. Action Items
Extracted tasks and commitments including:
- What needs to be done
- Who is responsible
- Deadline (if mentioned)
- Priority level
- Context from the conversation

### 6. Conversation Insights
- Tone (formal/informal/casual/professional)
- Engagement level (high/medium/low)
- Key points and takeaways

## 🏗️ Project Structure

```
handover/
├── app.py                  # Flask backend application
├── whatsapp_parser.py      # WhatsApp chat parsing logic
├── ai_analyzer.py          # AI analysis using Claude API
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── sample_chat.txt       # Sample WhatsApp chat for testing
├── templates/
│   └── index.html        # Main web interface
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend JavaScript
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Required: Your Anthropic API key
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Flask secret key (auto-generated if not provided)
FLASK_SECRET_KEY=your_secret_key_here
```

### Customization

You can customize the analysis by modifying `ai_analyzer.py`:

- **Model**: Change the Claude model (default: `claude-sonnet-4-20250514`)
- **Temperature**: Adjust creativity vs consistency (default: `0.3`)
- **Max Tokens**: Control response length (default: `4000`)

## 🧪 Testing

A sample WhatsApp chat is included in `sample_chat.txt`. You can use this to test the application without exporting your own chat.

To test:
1. Start the application
2. Upload `sample_chat.txt`
3. Review the analysis results

## 🛠️ API Endpoints

### `POST /analyze`
Analyzes a WhatsApp chat file.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `chat_file` (text file)

**Response:**
```json
{
  "success": true,
  "metadata": {
    "participants": ["Sarah", "Mike", "Alex"],
    "message_count": 45,
    "date_range": {
      "start": "2024-11-10T09:15:00",
      "end": "2024-11-10T11:28:00"
    }
  },
  "analysis": {
    "summary": "...",
    "overall_sentiment": {...},
    "participant_sentiments": [...],
    "key_topics": [...],
    "actionables": [...],
    "conversation_insights": {...}
  }
}
```

### `POST /quick-parse`
Parses a WhatsApp chat file without AI analysis (faster).

### `GET /health`
Health check endpoint.

## 🔒 Privacy & Security

- **No Data Storage**: Files are processed in memory and not saved
- **Secure Processing**: All data stays on your server
- **API Security**: Your Anthropic API key is stored locally in `.env`
- **XSS Protection**: All user inputs are sanitized
- **File Size Limit**: 16MB maximum to prevent abuse

## ⚠️ Troubleshooting

### Common Issues

**"ANTHROPIC_API_KEY is required"**
- Make sure you've created a `.env` file
- Verify your API key is correctly set
- Restart the Flask application after adding the key

**"Failed to parse WhatsApp chat"**
- Ensure the file is a genuine WhatsApp export
- Check that the file is in `.txt` format
- Try exporting the chat again

**"File too large"**
- WhatsApp chats with media can be very large
- Always export "Without Media"
- For very long chats, consider splitting them

**Analysis takes too long**
- Large conversations take more time to analyze
- Check your internet connection (API calls require network)
- Very long chats (1000+ messages) may take 10-30 seconds

## 🚀 Deployment

### Production Considerations

When deploying to production:

1. **Use a production WSGI server** (not Flask's development server)
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

2. **Set secure environment variables**
   - Use strong, random secret keys
   - Never commit `.env` to version control

3. **Enable HTTPS**
   - Use a reverse proxy like Nginx
   - Obtain SSL certificates (Let's Encrypt)

4. **Rate Limiting**
   - Implement rate limiting to prevent abuse
   - Consider using Flask-Limiter

5. **Monitoring**
   - Set up logging
   - Monitor API usage and costs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Anthropic** for providing the Claude AI API
- **Flask** for the excellent web framework
- **WhatsApp** for making chat exports possible

## 📧 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments for detailed explanations
3. Open an issue on GitHub

---

**Made with ❤️ using Claude AI and Python**
