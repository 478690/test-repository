@echo off
echo Starting local test server for Cloudflare AI Chat App...
echo.
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
cd ai-chat-app\public
python -m http.server 8000