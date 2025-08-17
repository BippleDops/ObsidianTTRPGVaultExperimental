#!/usr/bin/env python3
"""
Text-to-Speech Narrator System - Sprint 1 MVI
Basic TTS for content reading with character voices
"""

import os
import re
import json
import argparse
import subprocess
from typing import Dict, List, Any, Optional
from common import ROOT_DIR, read_file, split_frontmatter

class TTSNarrator:
    def __init__(self, vault_path: str = None):
        self.vault_path = vault_path or ROOT_DIR
        self.voice_profiles = self._load_voice_profiles()
        self.output_dir = os.path.join(self.vault_path, "04_Resources", "Audio")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _load_voice_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Load character voice profiles"""
        return {
            'narrator': {
                'voice': 'Alex',  # macOS built-in voice
                'rate': 180,
                'pitch': 50,
                'description': 'Neutral narrator voice'
            },
            'queen_seraphina': {
                'voice': 'Samantha',
                'rate': 160,
                'pitch': 60,
                'description': 'Regal, crystalline queen'
            },
            'emperor_thalassius': {
                'voice': 'Daniel',
                'rate': 140,
                'pitch': 40,
                'description': 'Deep, authoritative ruler'
            },
            'vex_shadowthorn': {
                'voice': 'Victoria',
                'rate': 170,
                'pitch': 30,
                'description': 'Cold, calculating assassin'
            },
            'merchant': {
                'voice': 'Fred',
                'rate': 200,
                'pitch': 55,
                'description': 'Energetic trader'
            },
            'scholar': {
                'voice': 'Veena',
                'rate': 150,
                'pitch': 45,
                'description': 'Thoughtful academic'
            },
            'deep_mother': {
                'voice': 'Whisper',
                'rate': 100,
                'pitch': 20,
                'description': 'Ancient, otherworldly entity'
            }
        }
    
    def detect_character_voice(self, content: str, file_path: str) -> str:
        """Detect which character voice to use based on content"""
        content_lower = content.lower()
        file_lower = file_path.lower()
        
        # Character-specific detection
        if 'seraphina' in file_lower or 'queen' in file_lower:
            return 'queen_seraphina'
        elif 'thalassius' in file_lower or 'emperor' in file_lower:
            return 'emperor_thalassius'
        elif 'vex' in file_lower or 'shadowthorn' in file_lower:
            return 'vex_shadowthorn'
        elif 'deep mother' in content_lower or 'eldritch' in content_lower:
            return 'deep_mother'
        elif 'merchant' in file_lower or 'trader' in file_lower:
            return 'merchant'
        elif 'scholar' in file_lower or 'academy' in file_lower:
            return 'scholar'
        else:
            return 'narrator'
    
    def clean_text_for_speech(self, text: str) -> str:
        """Clean markdown and format text for speech synthesis"""
        # Remove frontmatter
        if text.startswith('---'):
            parts = text.split('---', 2)
            if len(parts) >= 3:
                text = parts[2]
        
        # Remove markdown formatting
        text = re.sub(r'#+\s*', '', text)  # Headers
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
        text = re.sub(r'`(.+?)`', r'\1', text)  # Inline code
        text = re.sub(r'\[\[(.+?)\]\]', r'\1', text)  # Wiki links
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Regular links
        text = re.sub(r'!\[.*?\]\(.+?\)', '', text)  # Images
        
        # Remove empty lines and extra whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        # Add natural pauses
        text = text.replace('\n\n', '. ... ')
        text = text.replace('\n', '. ')
        
        # Handle special terms
        replacements = {
            'Aquabyssos': 'Aqua-bis-sos',
            'Aethermoor': 'Ether-moor',
            'Seraphina': 'Sarah-fina',
            'Thalassius': 'Tha-las-ee-us',
            'Lumengarde': 'Lumen-garde'
        }
        
        for original, replacement in replacements.items():
            text = text.replace(original, replacement)
        
        return text
    
    def synthesize_speech(self, text: str, voice_profile: str, output_file: str) -> bool:
        """Synthesize speech using macOS say command"""
        try:
            profile = self.voice_profiles[voice_profile]
            voice = profile['voice']
            rate = profile['rate']
            
            # Clean text for speech
            clean_text = self.clean_text_for_speech(text)
            
            # Truncate if too long (say has limits)
            if len(clean_text) > 3000:
                clean_text = clean_text[:3000] + "... content continues in the text."
            
            # Build say command
            cmd = [
                'say',
                '-v', voice,
                '-r', str(rate),
                '-o', output_file,
                clean_text
            ]
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"Generated audio: {output_file}")
                return True
            else:
                print(f"Error generating audio: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
            return False
    
    def generate_content_audio(self, file_path: str, section: str = None) -> Optional[str]:
        """Generate audio for specific content file"""
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
            
        try:
            content = read_file(file_path)
            frontmatter, body = split_frontmatter(content)
            
            # Use section if specified, otherwise full body
            text_to_read = body
            if section:
                # Extract specific section
                section_pattern = rf"##\s*{re.escape(section)}\s*\n(.*?)(?=\n##|\n---|$)"
                match = re.search(section_pattern, body, re.DOTALL | re.IGNORECASE)
                if match:
                    text_to_read = match.group(1).strip()
                else:
                    print(f"Section '{section}' not found in {file_path}")
                    return None
            
            # Determine voice
            voice_profile = self.detect_character_voice(content, file_path)
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            if section:
                base_name += f"_{section.lower().replace(' ', '_')}"
            output_file = os.path.join(self.output_dir, f"{base_name}_{voice_profile}.aiff")
            
            # Generate audio
            success = self.synthesize_speech(text_to_read, voice_profile, output_file)
            
            if success:
                return output_file
            else:
                return None
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def generate_batch_audio(self, pattern: str = "*.md", limit: int = 10) -> List[str]:
        """Generate audio for multiple files matching pattern"""
        from glob import glob
        
        # Find matching files
        if not os.path.isabs(pattern):
            pattern = os.path.join(self.vault_path, "**", pattern)
        
        files = glob(pattern, recursive=True)[:limit]
        generated_files = []
        
        for file_path in files:
            # Skip certain directories
            if any(skip in file_path for skip in ['.git', 'backup', 'scripts']):
                continue
                
            print(f"Processing: {os.path.basename(file_path)}")
            output_file = self.generate_content_audio(file_path)
            
            if output_file:
                generated_files.append(output_file)
        
        return generated_files
    
    def create_audio_playlist(self, files: List[str], playlist_name: str) -> str:
        """Create a playlist file for audio files"""
        playlist_path = os.path.join(self.output_dir, f"{playlist_name}.m3u")
        
        with open(playlist_path, 'w') as f:
            f.write("#EXTM3U\n")
            for audio_file in files:
                file_name = os.path.basename(audio_file)
                f.write(f"#EXTINF:-1,{file_name}\n")
                f.write(f"{audio_file}\n")
        
        return playlist_path
    
    def list_available_voices(self) -> List[str]:
        """List available system voices"""
        try:
            result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
            if result.returncode == 0:
                voices = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        voice_name = line.split()[0]
                        voices.append(voice_name)
                return voices
            else:
                return []
        except Exception:
            return []

def main():
    parser = argparse.ArgumentParser(description='TTS Narrator System')
    parser.add_argument('action', choices=['generate', 'batch', 'voices', 'playlist'])
    parser.add_argument('--file', help='File path to generate audio for')
    parser.add_argument('--section', help='Specific section to read')
    parser.add_argument('--pattern', default='*.md', help='Pattern for batch processing')
    parser.add_argument('--limit', type=int, default=10, help='Limit for batch processing')
    parser.add_argument('--playlist', default='session_audio', help='Playlist name')
    
    args = parser.parse_args()
    
    narrator = TTSNarrator()
    
    if args.action == 'generate':
        if not args.file:
            print("--file required for generate action")
            return
        
        output_file = narrator.generate_content_audio(args.file, args.section)
        if output_file:
            print(f"Audio generated: {output_file}")
        else:
            print("Failed to generate audio")
    
    elif args.action == 'batch':
        generated_files = narrator.generate_batch_audio(args.pattern, args.limit)
        print(f"Generated {len(generated_files)} audio files")
        
        # Create playlist
        if generated_files:
            playlist = narrator.create_audio_playlist(generated_files, args.playlist)
            print(f"Playlist created: {playlist}")
    
    elif args.action == 'voices':
        voices = narrator.list_available_voices()
        print("Available voices:")
        for voice in voices[:20]:  # Show first 20
            print(f"  - {voice}")
    
    elif args.action == 'playlist':
        # Create playlist from existing audio files
        audio_files = [
            os.path.join(narrator.output_dir, f) 
            for f in os.listdir(narrator.output_dir) 
            if f.endswith('.aiff')
        ]
        
        if audio_files:
            playlist = narrator.create_audio_playlist(audio_files, args.playlist)
            print(f"Playlist created with {len(audio_files)} files: {playlist}")
        else:
            print("No audio files found")

if __name__ == "__main__":
    main()