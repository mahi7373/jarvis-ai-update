# 🤖 Jarvis AI Assistant

Complete AI assistant with dual brain, voice capabilities, and video processing.

## Features
- **Dual Brain**: Offline + Online AI modes
- **Voice I/O**: Speech recognition + Text-to-speech
- **Memory**: JSON-based conversation storage
- **Video Tasks**: Create videos and YouTube Shorts
- **AWS Lambda**: Auto deployment ready

## Quick Start
```bash
pip install -r requirements.txt
python main.py
```

## Commands
- `switch to offline/online` - Change brain mode
- `create video` - Generate video from text
- `create short` - Generate YouTube Short
- `voice mode` - Use voice input

## AWS Lambda Deployment
```bash
python deploy_lambda.py
```

## API Usage
```json
POST /jarvis
{
  "query": "Hello Jarvis",
  "brain_mode": "offline"
}
```