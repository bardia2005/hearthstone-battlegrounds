"""
Network client for connecting to Hearthstone game server
"""

import asyncio
import json
import logging
from typing import Optional, Callable, Dict, Any
import websockets
from websockets.client import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkClient:
    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.player_id: Optional[str] = None
        self.username: Optional[str] = None
        self.connected = False
        self.running = False
        
        # Callbacks for different message types
        self.callbacks: Dict[str, Callable] = {}
    
    def on(self, event_type: str, callback: Callable):
        """Register a callback for an event type"""
        self.callbacks[event_type] = callback
    
    async def connect(self, username: str = "Player"):
        """Connect to the game server"""
        try:
            logger.info(f"Connecting to {self.server_url}")
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            self.running = True
            
            # Wait for connection confirmation
            message = await self.websocket.recv()
            data = json.loads(message)
            
            if data.get("type") == "connected":
                self.player_id = data.get("player_id")
                logger.info(f"Connected with player_id: {self.player_id}")
                
                # Register username
                await self.register(username)
                
                # Start listening for messages
                asyncio.create_task(self.listen())
                
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            self.connected = False
            return False
    
    async def register(self, username: str):
        """Register username with server"""
        self.username = username
        await self.send({
            "type": "register",
            "username": username
        })
    
    async def listen(self):
        """Listen for messages from server"""
        try:
            async for message in self.websocket:
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed")
            self.connected = False
            self.running = False
            if "disconnected" in self.callbacks:
                self.callbacks["disconnected"]()
        except Exception as e:
            logger.error(f"Listen error: {e}")
            self.connected = False
            self.running = False
    
    async def handle_message(self, message: str):
        """Handle incoming message from server"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            logger.info(f"Received: {msg_type}")
            
            # Call registered callback if exists
            if msg_type in self.callbacks:
                callback = self.callbacks[msg_type]
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
        
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def send(self, data: Dict[str, Any]):
        """Send message to server"""
        if not self.connected or not self.websocket:
            logger.warning("Not connected to server")
            return False
        
        try:
            await self.websocket.send(json.dumps(data))
            return True
        except Exception as e:
            logger.error(f"Send error: {e}")
            return False
    
    async def find_match(self):
        """Request matchmaking"""
        await self.send({"type": "find_match"})
    
    async def cancel_matchmaking(self):
        """Cancel matchmaking"""
        await self.send({"type": "cancel_matchmaking"})
    
    async def play_card(self, card_index: int, target: Optional[Dict] = None):
        """Play a card"""
        await self.send({
            "type": "play_card",
            "card_index": card_index,
            "target": target
        })
    
    async def attack(self, attacker_index: int, target: Dict):
        """Attack with a minion"""
        await self.send({
            "type": "attack",
            "attacker_index": attacker_index,
            "target": target
        })
    
    async def use_hero_power(self, target: Optional[Dict] = None):
        """Use hero power"""
        await self.send({
            "type": "hero_power",
            "target": target
        })
    
    async def end_turn(self):
        """End current turn"""
        await self.send({"type": "end_turn"})
    
    async def concede(self):
        """Concede the game"""
        await self.send({"type": "concede"})
    
    async def ping(self):
        """Send ping to server"""
        await self.send({"type": "ping"})
    
    async def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.websocket:
            await self.websocket.close()
        self.connected = False
        logger.info("Disconnected from server")
