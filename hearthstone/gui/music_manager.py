"""
Music Manager - Handles background music for menu and gameplay
Generates procedural fantasy-themed music or loads custom tracks
"""

import pygame
import os
import random
import numpy as np
from typing import Optional
import math


class MusicManager:
    """Manages background music with support for custom tracks and procedural generation"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.music_directory = "assets/music"
        self.current_track = None
        self.volume = 0.25  # Default volume (25%)
        self.is_playing = False
        
        # Create music directory if it doesn't exist
        os.makedirs(self.music_directory, exist_ok=True)
        
        # Track categories
        self.menu_tracks = []
        self.game_tracks = []
        
        # Load any existing music files
        self._load_music_files()
        
        # Procedural music generation
        self.sample_rate = 22050
        self.procedural_menu_sound = None
        self.procedural_game_sound = None
    
    def _load_music_files(self):
        """Load music files from the assets directory"""
        if not os.path.exists(self.music_directory):
            return
        
        for filename in os.listdir(self.music_directory):
            if filename.endswith(('.mp3', '.ogg', '.wav')):
                filepath = os.path.join(self.music_directory, filename)
                
                # Categorize by filename
                if 'menu' in filename.lower() or 'tavern' in filename.lower():
                    self.menu_tracks.append(filepath)
                elif 'game' in filename.lower() or 'battle' in filename.lower():
                    self.game_tracks.append(filepath)
                else:
                    # Default to game tracks
                    self.game_tracks.append(filepath)
    
    def _generate_tone(self, frequency, duration, volume=0.3):
        """Generate a simple tone"""
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Generate sine wave with envelope
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Apply ADSR envelope
        attack = int(samples * 0.1)
        decay = int(samples * 0.2)
        sustain_level = 0.7
        release = int(samples * 0.3)
        
        envelope = np.ones(samples)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
        envelope[-release:] = np.linspace(sustain_level, 0, release)
        
        wave = wave * envelope * volume
        
        # Convert to stereo
        stereo = np.column_stack((wave, wave))
        return (stereo * 32767).astype(np.int16)
    
    def _generate_chord(self, frequencies, duration, volume=0.2):
        """Generate a chord from multiple frequencies"""
        samples = int(self.sample_rate * duration)
        chord = np.zeros(samples)
        
        for freq in frequencies:
            t = np.linspace(0, duration, samples, False)
            chord += np.sin(2 * np.pi * freq * t)
        
        chord = chord / len(frequencies)  # Normalize
        
        # Apply envelope
        attack = int(samples * 0.15)
        release = int(samples * 0.3)
        envelope = np.ones(samples)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[-release:] = np.linspace(1, 0, release)
        
        chord = chord * envelope * volume
        
        # Convert to stereo
        stereo = np.column_stack((chord, chord))
        return (stereo * 32767).astype(np.int16)
    
    def _generate_menu_music(self):
        """Generate peaceful tavern-style music"""
        print("🎵 Generating peaceful tavern music...")
        
        # Peaceful chord progression in C major (I-IV-V-I)
        # Using lower octave for warm tavern feel
        C_major = [261.63, 329.63, 392.00]  # C-E-G
        F_major = [349.23, 440.00, 523.25]  # F-A-C
        G_major = [392.00, 493.88, 587.33]  # G-B-D
        
        duration = 2.0  # Each chord lasts 2 seconds
        
        # Generate chord progression
        chord1 = self._generate_chord(C_major, duration, 0.15)
        chord2 = self._generate_chord(F_major, duration, 0.15)
        chord3 = self._generate_chord(G_major, duration, 0.15)
        chord4 = self._generate_chord(C_major, duration, 0.15)
        
        # Combine chords
        music = np.concatenate([chord1, chord2, chord3, chord4])
        
        # Create pygame Sound
        sound = pygame.sndarray.make_sound(music)
        return sound
    
    def _generate_game_music(self):
        """Generate epic battle-style music"""
        print("🎵 Generating epic battle music...")
        
        # Dramatic chord progression in A minor (i-iv-V-i)
        # Using power chords for epic feel
        A_minor = [220.00, 261.63, 329.63]  # A-C-E
        D_minor = [293.66, 349.23, 440.00]  # D-F-A
        E_major = [329.63, 415.30, 493.88]  # E-G#-B
        
        duration = 1.5  # Faster tempo for battle
        
        # Generate chord progression
        chord1 = self._generate_chord(A_minor, duration, 0.2)
        chord2 = self._generate_chord(D_minor, duration, 0.2)
        chord3 = self._generate_chord(E_major, duration, 0.2)
        chord4 = self._generate_chord(A_minor, duration, 0.2)
        
        # Add some rhythmic elements
        beat_duration = 0.3
        beat = self._generate_tone(110, beat_duration, 0.15)  # Low A for drums
        
        # Combine chords with beats
        music = np.concatenate([chord1, beat, chord2, beat, chord3, beat, chord4, beat])
        
        # Create pygame Sound
        sound = pygame.sndarray.make_sound(music)
        return sound
    
    def play_menu_music(self):
        """Play menu/tavern music"""
        if self.menu_tracks:
            track = random.choice(self.menu_tracks)
            self._play_track(track, loops=-1)
        else:
            # Generate procedural music
            try:
                if self.procedural_menu_sound is None:
                    self.procedural_menu_sound = self._generate_menu_music()
                
                # Play on a channel with looping
                channel = pygame.mixer.find_channel()
                if channel:
                    channel.play(self.procedural_menu_sound, loops=-1)
                    channel.set_volume(self.volume)
                    self.is_playing = True
                    print("🎵 Playing procedural tavern music")
            except Exception as e:
                print(f"⚠️ Could not generate music: {e}")
                print("   Add custom tracks to assets/music/ for better music!")
    
    def play_game_music(self):
        """Play gameplay/battle music"""
        if self.game_tracks:
            track = random.choice(self.game_tracks)
            self._play_track(track, loops=-1)
        else:
            # Generate procedural music
            try:
                if self.procedural_game_sound is None:
                    self.procedural_game_sound = self._generate_game_music()
                
                # Play on a channel with looping
                channel = pygame.mixer.find_channel()
                if channel:
                    channel.play(self.procedural_game_sound, loops=-1)
                    channel.set_volume(self.volume)
                    self.is_playing = True
                    print("🎵 Playing procedural battle music")
            except Exception as e:
                print(f"⚠️ Could not generate music: {e}")
                print("   Add custom tracks to assets/music/ for better music!")
    
    def _play_track(self, filepath: str, loops: int = 0):
        """Play a music track"""
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops=loops)
            self.current_track = filepath
            self.is_playing = True
            print(f"🎵 Now playing: {os.path.basename(filepath)}")
        except Exception as e:
            print(f"⚠️ Could not play music: {e}")
    
    def stop(self):
        """Stop music playback"""
        pygame.mixer.music.stop()
        pygame.mixer.stop()  # Stop all channels
        self.is_playing = False
        self.current_track = None
    
    def pause(self):
        """Pause music playback"""
        pygame.mixer.music.pause()
        self.is_playing = False
    
    def unpause(self):
        """Resume music playback"""
        pygame.mixer.music.unpause()
        self.is_playing = True
    
    def set_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def fade_out(self, milliseconds: int = 1000):
        """Fade out current music"""
        pygame.mixer.music.fadeout(milliseconds)
        pygame.mixer.fadeout(milliseconds)  # Fade all channels
        self.is_playing = False
    
    def crossfade_to_game(self):
        """Crossfade from menu to game music"""
        self.stop()
        pygame.time.wait(100)
        self.play_game_music()
    
    def crossfade_to_menu(self):
        """Crossfade from game to menu music"""
        self.stop()
        pygame.time.wait(100)
        self.play_menu_music()


# Global instance
_music_manager = None

def get_music_manager() -> MusicManager:
    """Get the global music manager instance"""
    global _music_manager
    if _music_manager is None:
        _music_manager = MusicManager()
    return _music_manager
