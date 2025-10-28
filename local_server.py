"""
Simple local server for testing the German translator agent.
Generates LiveKit tokens and serves the test frontend.
"""

import os
import time
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import jwt
from dotenv import load_dotenv

load_dotenv()

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")

class LocalTestHandler(SimpleHTTPRequestHandler):
    """Custom handler that serves files and generates tokens."""

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests for token generation."""
        if self.path == '/get-token':
            try:
                # Generate unique room and participant names
                room_name = f"test-{int(time.time())}-{os.urandom(3).hex()}"
                participant_name = f"user-{os.urandom(3).hex()}"

                # Create LiveKit access token
                token = self.create_token(room_name, participant_name)

                # Send response
                response = {
                    "token": token,
                    "url": LIVEKIT_URL,
                    "roomName": room_name
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

                print(f"✅ Generated token for room: {room_name}")

            except Exception as e:
                print(f"❌ Error generating token: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def create_token(self, room_name, identity):
        """Create a LiveKit access token."""
        if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
            raise Exception("Missing LiveKit credentials in .env file")

        now = int(time.time())
        payload = {
            "video": {
                "room": room_name,
                "roomJoin": True,
                "canPublish": True,
                "canSubscribe": True
            },
            "iat": now,
            "nbf": now,
            "exp": now + 3600,  # Token valid for 1 hour
            "iss": LIVEKIT_API_KEY,
            "sub": identity,
            "jti": identity
        }

        token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")
        return token

    def log_message(self, format, *args):
        """Custom log format."""
        if self.path == '/get-token':
            return  # Don't log token requests twice
        print(f"📄 {self.path}")


def run_server(port=8000):
    """Run the local test server."""
    print("\n" + "="*60)
    print("🚀 German Translator - Local Test Server")
    print("="*60)
    print(f"\n✅ Server running at: http://localhost:{port}")
    print(f"✅ LiveKit URL: {LIVEKIT_URL}")
    print(f"✅ API Key: {LIVEKIT_API_KEY[:20]}...")
    print("\n📖 Instructions:")
    print(f"   1. Open: http://localhost:{port}/test-simple.html")
    print("   2. Click 'Start Conversation'")
    print("   3. Allow microphone access")
    print("   4. Speak in German!")
    print("\n⚠️  Make sure agent is running in another terminal:")
    print("   python agent.py dev")
    print("\n" + "="*60 + "\n")

    server = HTTPServer(('', port), LocalTestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")


if __name__ == "__main__":
    run_server()
