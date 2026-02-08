"""
Sound manager for Hearthstone
Generates simple sound effects using pygame.mixer
"""

import pygame
import numpy as np
from typing import Dict, Optional


class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.enabled = True
        self.volume = 0.5
        
        # Generate sounds
        self.generate_sounds()
    
    def generate_sounds(self):
        """Generate simple sound effects"""
        sample_rate = 22050
        
        # Button click sound (short beep)
        self.sounds['button_click'] = self.generate_beep(440, 0.1, sample_rate)
        
        # Button hover sound (soft tick)
        self.sounds['button_hover'] = self.generate_beep(880, 0.05, sample_rate, volume=0.3)
        
        # Card play sound (whoosh)
        self.sounds['card_play'] = self.generate_whoosh(0.3, sample_rate)
        
        # Card draw sound (swish)
        self.sounds['card_draw'] = self.generate_whoosh(0.2, sample_rate, pitch=1.5)
        
        # Attack sound (hit)
        self.sounds['attack'] = self.generate_hit(0.2, sample_rate)
        
        # Error sound (buzz)
        self.sounds['error'] = self.generate_buzz(0.3, sample_rate)
        
        # End turn sound (chime)
        self.sounds['end_turn'] = self.generate_chime(0.4, sample_rate)
        
        # Victory sound (fanfare)
        self.sounds['victory'] = self.generate_fanfare(1.0, sample_rate)
        
        # Defeat sound (sad)
        self.sounds['defeat'] = self.generate_sad_tone(1.0, sample_rate)
        
        # Menu open sound
        self.sounds['menu_open'] = self.generate_beep(660, 0.15, sample_rate)
        
        # Menu close sound
        self.sounds['menu_close'] = self.generate_beep(440, 0.15, sample_rate)
    
    def generate_beep(self, frequency: float, duration: float, sample_rate: int, volume: float = 0.5) -> pygame.mixer.Sound:
        """Generate a simple beep tone"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        # Generate sine wave
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Apply envelope (fade in/out)
        envelope = np.ones(n_samples)
        fade_samples = int(0.01 * sample_rate)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        wave = wave * envelope * volume
        
        # Convert to 16-bit integers
        wave = (wave * 32767).astype(np.int16)
        
        # Create stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.mixer.Sound(stereo_wave)
    
    def generate_whoosh(self, duration: float, sample_rate: int, pitch: float = 1.0) -> pygame.mixer.Sound:
        """Generate a whoosh sound (frequency sweep)"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        # Frequency sweep from high to low
        start_freq = 1000 * pitch
        end_freq = 200 * pitch
        freq = np.linspace(start_freq, end_freq, n_samples)
        
        # Generate wave with changing frequency
        phase = np.cumsum(2 * np.pi * freq / sample_rate)
        wave = np.sin(phase)
        
        # Apply envelope
        envelope = np.exp(-3 * t / duration)
        wave = wave * envelope * 0.4
        
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.mixer.Sound(stereo_wave)
    
    def generate_hit(self, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a hit/impact sound"""
        n_samples = int(duration * sample_rate)
        
        # White noise
        wave = np.random.uniform(-1, 1, n_samples)
        
        # Apply sharp decay envelope
        t = np.linspace(0, duration, n_samples, False)
        envelope = np.exp(-10 * t / duration)
        wave = wave * envelope * 0.5
        
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.mixer.Sound(stereo_wave)
    
    def generate_buzz(self, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a buzz/error sound"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        # Low frequency buzz
        wave = np.sin(2 * np.pi * 120 * t) + 0.5 * np.sin(2 * np.pi * 180 * t)
        
        # Pulsing envelope
        envelope = (1 + np.sin(2 * np.pi * 8 * t)) / 2
        wave = wave * envelope * 0.3
        
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.mixer.Sound(stereo_wave)
    
    def generate_chime(self, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a pleasant chime sound"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        # Multiple harmonics
        wave = (np.sin(2 * np.pi * 523 * t) +  # C
                0.5 * np.sin(2 * np.pi * 659 * t) +  # E
                0.3 * np.sin(2 * np.pi * 784 * t))  # G
        
        # Decay envelope
        envelope = np.exp(-2 * t / duration)
        wave = wave * envelope * 0.3
        
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.mixer.Sound(stereo_wave)
    
    def generate_fanfare(self, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a victory fanfare"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        # Ascending notes
        freq1 = 523  # C
        freq2 = 659  # E
        freq3 = 784  # G
        
        wave = np.zeros(n_samples)
        third = n_samples // 3
        
        wave[:third] = np.sin(2 * np.pi * freq1 * t[:third])
        wave[third:2*third] = np.sin(2 * np.pi * freq2 * t[third:2*third])
        wave[2*third:] = np.sin(2 * np.pi * freq3 * t[2*third:])
        
        # Envelope
        envelope = np.ones(n_samples)
        fade = int(0.05 * sample_rate)
        envelope[-fade:] = np.linspace(1, 0, fade)
        
        wave = wave * envelope * 0.4
        
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.mixer.Sound(stereo_wave)
    
    def generate_sad_tone(self, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a sad/defeat sound"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        # Descending notes
        freq1 = 523  # C
        freq2 = 466  # Bb
        freq3 = 392  # G
        
        wave = np.zeros(n_samples)
        third = n_samples // 3
        
        wave[:third] = np.sin(2 * np.pi * freq1 * t[:third])
        wave[third:2*third] = np.sin(2 * np.pi * freq2 * t[third:2*third])
        wave[2*third:] = np.sin(2 * np.pi * freq3 * t[2*third:])
        
        envelope = np.exp(-1 * t / duration)
        wave = wave * envelope * 0.3
        
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.mixer.Sound(stereo_wave)
    
    def play(self, sound_name: str):
        """Play a sound effect"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        sound = self.sounds[sound_name]
        sound.set_volume(self.volume)
        sound.play()
    
    def set_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
    
    def toggle(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
    
    def stop_all(self):
        """Stop all playing sounds"""
        pygame.mixer.stop()


# Global sound manager instance
_sound_manager: Optional[SoundManager] = None


def get_sound_manager() -> SoundManager:
    """Get the global sound manager instance"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
