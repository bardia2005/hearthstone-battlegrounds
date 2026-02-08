import pygame
import sys
import asyncio
import threading
from hearthstone.game import Game
from hearthstone.player import Player
from hearthstone.cards_collection import create_starter_deck, mage_hero_power, warrior_hero_power
from hearthstone.gui import GameGUI
from hearthstone.gui.menu import MainMenu
from hearthstone.gui.sound_manager import get_sound_manager


def start_local_game(player1_name: str, player2_name: str, tutorial_mode: bool = False):
    """Start a local game with two players"""
    from hearthstone.gui.loading_screen import get_loading_screen
    from hearthstone.gui.card_art_manager import get_art_manager
    
    # Show loading screen
    loading_screen = get_loading_screen()
    loading_screen.initialize()
    loading_screen.draw(0.0, "Initializing...")
    
    sound_manager = get_sound_manager()
    
    # Load card art with progress updates
    def progress_callback(progress, message):
        loading_screen.draw(progress, message)
    
    # Initialize card art manager with progress callback
    loading_screen.draw(0.1, "Loading card art...")
    art_manager = get_art_manager()
    art_manager.progress_callback = progress_callback
    # Force reload to show progress
    art_manager._load_card_art_from_cards_folder()
    
    loading_screen.draw(1.0, "Starting game...")
    
    # Create players with starter decks and hero powers
    player1 = Player(player1_name, create_starter_deck(), hero_power=mage_hero_power)
    player2 = Player(player2_name, create_starter_deck(), hero_power=warrior_hero_power)
    
    # Create and start game
    game = Game(player1, player2)
    game.start_game()
    
    # Tutorial mode: ensure player has playable cards and extra mana
    if tutorial_mode:
        # Give player extra mana to play cards
        player1.max_mana = 5
        player1.mana = 5
        
        # Ensure player has some low-cost playable cards in hand
        from hearthstone.card import MinionCard
        from hearthstone.spell import SpellCard
        from hearthstone.cards_collection import fireball_effect
        
        # Clear hand and add tutorial-friendly cards
        player1.hand = []
        
        # Add some low-cost minions
        player1.hand.append(MinionCard("River Crocolisk", 2, 2, 3))
        player1.hand.append(MinionCard("Bloodfen Raptor", 2, 3, 2))
        player1.hand.append(MinionCard("Chillwind Yeti", 4, 4, 5))
        player1.hand.append(SpellCard("Fireball", 4, fireball_effect, "Deal 6 damage"))
        player1.hand.append(MinionCard("Boulderfist Ogre", 6, 6, 7))
    
    # Play game start sound
    sound_manager.play('chime')
    
    # Create and run GUI
    gui = GameGUI(game, online_mode=False, tutorial_mode=tutorial_mode)
    gui.run()
    
    # Game ended, return to menu
    pygame.quit()


def start_online_game(username: str, host: str, port: int):
    """Start an online multiplayer game"""
    try:
        import asyncio
        from client.network_client import NetworkClient
        from hearthstone.gui.online_game_gui import OnlineGameGUI
    except ImportError as e:
        print(f"\n❌ Error: Missing required module for online play")
        print(f"   {str(e)}")
        print(f"\n📦 Please install required dependencies:")
        print(f"   pip install websockets")
        print(f"\nOr install all dependencies:")
        print(f"   pip install -r requirements.txt\n")
        input("Press Enter to return to menu...")
        pygame.init()
        return
    
    sound_manager = get_sound_manager()
    
    async def connect_and_play():
        # Create network client
        client = NetworkClient(f"ws://{host}:{port}")
        
        # Try to connect
        connected = await client.connect(username)
        
        if not connected:
            sound_manager.play('error')
            print("Failed to connect to server")
            return
        
        sound_manager.play('chime')
        print(f"Connected as {username}")
        print("Looking for match...")
        
        # Request matchmaking
        await client.find_match()
        
        # Create online GUI
        gui = OnlineGameGUI(client, client.player_id)
        
        # Run the game
        await gui.run_async()
    
    try:
        asyncio.run(connect_and_play())
    except KeyboardInterrupt:
        print("\nDisconnected")
    except Exception as e:
        print(f"Error: {e}")
        sound_manager.play('error')
    
    pygame.quit()


def start_server():
    """Start a dedicated server"""
    try:
        from server.game_server import GameServer
        import asyncio
    except ImportError as e:
        print(f"\n❌ Error: Missing required module for server")
        print(f"   {str(e)}")
        print(f"\n📦 Please install required dependencies:")
        print(f"   pip install websockets")
        print(f"\nOr install all dependencies:")
        print(f"   pip install -r requirements.txt\n")
        input("Press Enter to return to menu...")
        return
    
    sound_manager = get_sound_manager()
    sound_manager.play('chime')
    
    print("\n" + "="*60)
    print("       HEARTHSTONE - DEDICATED SERVER")
    print("="*60)
    print("\nStarting server on 0.0.0.0:8765")
    print("Players can connect using 'localhost:8765'")
    print("Press Ctrl+C to stop\n")
    
    server = GameServer(host="0.0.0.0", port=8765)
    
    # Run server in a separate thread
    def run_server():
        try:
            asyncio.run(server.start())
        except KeyboardInterrupt:
            print("\nServer stopped")
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Show server status window
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Hearthstone Server")
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((30, 25, 20))
        
        # Title
        title = font.render("Server Running", True, (255, 215, 0))
        screen.blit(title, (200, 50))
        
        # Info
        info_lines = [
            "Server Address: 0.0.0.0:8765",
            "Players can connect using:",
            "localhost:8765 (same computer)",
            "or your IP address:8765 (network)",
            "",
            "Close this window to stop server"
        ]
        
        y = 120
        for line in info_lines:
            text = small_font.render(line, True, (200, 200, 200))
            screen.blit(text, (50, y))
            y += 30
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    print("Server stopped")
    sys.exit()


def main():
    """Main entry point with graphical menu"""
    while True:
        # Show menu
        menu = MainMenu()
        result = menu.run()
        
        mode = result.get("mode")
        params = result.get("params", {})
        
        if mode == "tutorial":
            # Start tutorial
            start_local_game("You", "Opponent", tutorial_mode=True)
            pygame.init()
        
        elif mode == "local":
            # Start local game
            player1 = params.get("player1", "Player 1")
            player2 = params.get("player2", "Player 2")
            start_local_game(player1, player2, tutorial_mode=False)
            
            # After game ends, reinitialize pygame and return to menu
            pygame.init()
        
        elif mode == "online":
            # Start online game
            username = params.get("username", "Player")
            host = params.get("host", "localhost")
            port = params.get("port", 8765)
            start_online_game(username, host, port)
            
            # After game ends, return to menu
            pygame.init()
        
        elif mode == "server":
            # Start server
            start_server()
            break  # Exit after server closes
        
        else:
            # No mode selected, exit
            break


if __name__ == "__main__":
    main()
