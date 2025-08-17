/**
 * Spotify Integration for TTRPG Sessions
 * Handles mood-based playlists, combat music, and atmospheric control
 */

class TTRPGSpotifyIntegration {
    constructor(app) {
        this.app = app;
        this.config = null;
        this.accessToken = null;
        this.deviceId = null;
        this.currentPlaylist = null;
        this.loadConfig();
    }

    async loadConfig() {
        try {
            const configFile = this.app.vault.getAbstractFileByPath('.obsidian/api_config.json');
            if (configFile) {
                const configContent = await this.app.vault.read(configFile);
                this.config = JSON.parse(configContent);
            }
        } catch (error) {
            console.warn('Spotify Config not found or invalid:', error);
        }
    }

    // OAuth 2.0 Authentication
    async authenticate() {
        if (!this.config?.spotify?.client_id) {
            throw new Error('Spotify client ID not configured');
        }

        const scopes = this.config.spotify.scopes;
        const redirectUri = this.config.spotify.redirect_uri;
        const clientId = this.config.spotify.client_id;

        const authUrl = `https://accounts.spotify.com/authorize?` +
            `client_id=${clientId}&` +
            `response_type=token&` +
            `redirect_uri=${encodeURIComponent(redirectUri)}&` +
            `scope=${encodeURIComponent(scopes)}`;

        // Open authentication in browser
        window.open(authUrl, '_blank');
        
        // Store token when user returns (simplified - would need proper OAuth flow)
        return new Promise((resolve, reject) => {
            new Notice('Complete Spotify authentication in the browser window, then click OK here when done.', 0);
            
            // In a real implementation, this would capture the OAuth callback
            setTimeout(() => {
                const token = prompt('Paste your access token here (from the URL after authentication):');
                if (token) {
                    this.accessToken = token;
                    resolve(token);
                } else {
                    reject(new Error('Authentication cancelled'));
                }
            }, 2000);
        });
    }

    // Get user's devices
    async getDevices() {
        if (!this.accessToken) {
            throw new Error('Not authenticated with Spotify');
        }

        try {
            const response = await fetch('https://api.spotify.com/v1/me/player/devices', {
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`
                }
            });

            if (!response.ok) {
                throw new Error(`Spotify API error: ${response.status}`);
            }

            const data = await response.json();
            return data.devices;
        } catch (error) {
            console.error('Error getting devices:', error);
            throw error;
        }
    }

    // Search for TTRPG-appropriate playlists
    async searchPlaylists(mood, genre = 'fantasy') {
        if (!this.accessToken) {
            throw new Error('Not authenticated with Spotify');
        }

        const searchTerms = {
            'exploration': 'ambient fantasy adventure exploration',
            'combat': 'epic battle combat fantasy orchestral',
            'tavern': 'medieval tavern folk acoustic',
            'mystery': 'dark ambient mysterious fantasy',
            'city': 'fantasy city urban medieval',
            'dungeon': 'dark dungeon ambient horror fantasy',
            'victory': 'triumphant victory fantasy orchestral',
            'rest': 'peaceful fantasy ambient calm'
        };

        const query = searchTerms[mood] || `${mood} ${genre} ambient`;
        
        try {
            const response = await fetch(
                `https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=playlist&limit=10`,
                {
                    headers: {
                        'Authorization': `Bearer ${this.accessToken}`
                    }
                }
            );

            const data = await response.json();
            return data.playlists.items;
        } catch (error) {
            console.error('Error searching playlists:', error);
            throw error;
        }
    }

    // Play a specific playlist
    async playPlaylist(playlistId, deviceId = null) {
        if (!this.accessToken) {
            throw new Error('Not authenticated with Spotify');
        }

        const targetDevice = deviceId || this.deviceId;
        const url = targetDevice ? 
            `https://api.spotify.com/v1/me/player/play?device_id=${targetDevice}` :
            'https://api.spotify.com/v1/me/player/play';

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    context_uri: `spotify:playlist:${playlistId}`
                })
            });

            if (response.ok) {
                this.currentPlaylist = playlistId;
                return true;
            } else {
                throw new Error(`Failed to play playlist: ${response.status}`);
            }
        } catch (error) {
            console.error('Error playing playlist:', error);
            throw error;
        }
    }

    // Control playback
    async pausePlayback() {
        if (!this.accessToken) return;

        try {
            await fetch('https://api.spotify.com/v1/me/player/pause', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`
                }
            });
        } catch (error) {
            console.error('Error pausing playback:', error);
        }
    }

    async resumePlayback() {
        if (!this.accessToken) return;

        try {
            await fetch('https://api.spotify.com/v1/me/player/play', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`
                }
            });
        } catch (error) {
            console.error('Error resuming playback:', error);
        }
    }

    async setVolume(volume) {
        if (!this.accessToken) return;

        try {
            await fetch(`https://api.spotify.com/v1/me/player/volume?volume_percent=${volume}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`
                }
            });
        } catch (error) {
            console.error('Error setting volume:', error);
        }
    }

    // TTRPG-specific mood management
    async setSessionMood(mood, options = {}) {
        const { volume = 30, fadeIn = true } = options;
        
        try {
            // Search for appropriate playlists
            const playlists = await this.searchPlaylists(mood);
            
            if (playlists.length === 0) {
                throw new Error(`No playlists found for mood: ${mood}`);
            }

            // Select best playlist (first result for now)
            const selectedPlaylist = playlists[0];
            
            // Set volume if requested
            if (fadeIn) {
                await this.setVolume(5);
                await this.playPlaylist(selectedPlaylist.id);
                // Gradually increase volume
                for (let v = 10; v <= volume; v += 5) {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    await this.setVolume(v);
                }
            } else {
                await this.setVolume(volume);
                await this.playPlaylist(selectedPlaylist.id);
            }

            return {
                mood,
                playlist: selectedPlaylist.name,
                volume,
                success: true
            };

        } catch (error) {
            console.error('Error setting session mood:', error);
            return {
                mood,
                error: error.message,
                success: false
            };
        }
    }

    // Session-based music tracking
    async logMusicToSession(sessionFile, musicData) {
        try {
            const file = this.app.vault.getAbstractFileByPath(sessionFile);
            if (!file) return;

            const content = await this.app.vault.read(file);
            
            // Add music tracking to frontmatter
            const musicLog = {
                timestamp: new Date().toISOString(),
                mood: musicData.mood,
                playlist: musicData.playlist,
                volume: musicData.volume
            };

            // Simple append to file (in real implementation, would parse and update YAML)
            const musicEntry = `\n## 🎵 Music Log - ${new Date().toLocaleTimeString()}\n` +
                `**Mood**: ${musicData.mood}\n` +
                `**Playlist**: ${musicData.playlist}\n` +
                `**Volume**: ${musicData.volume}%\n`;

            await this.app.vault.modify(file, content + musicEntry);
            
        } catch (error) {
            console.error('Error logging music to session:', error);
        }
    }

    // Quick mood presets for common TTRPG scenarios
    getMoodPresets() {
        return {
            'Session Start': { mood: 'exploration', volume: 25, description: 'Light ambient exploration music' },
            'Entering Town': { mood: 'city', volume: 20, description: 'Urban fantasy atmosphere' },
            'Tavern Scene': { mood: 'tavern', volume: 30, description: 'Folk music and chatter' },
            'Investigation': { mood: 'mystery', volume: 15, description: 'Mysterious, tense atmosphere' },
            'Combat Ready': { mood: 'combat', volume: 40, description: 'Epic battle music' },
            'Dungeon Exploration': { mood: 'dungeon', volume: 20, description: 'Dark, ominous ambience' },
            'Victory Celebration': { mood: 'victory', volume: 35, description: 'Triumphant orchestral' },
            'Long Rest': { mood: 'rest', volume: 15, description: 'Peaceful, restorative music' }
        };
    }

    // Create a custom TTRPG playlist
    async createTTRPGPlaylist(name, tracks) {
        if (!this.accessToken) {
            throw new Error('Not authenticated with Spotify');
        }

        try {
            // Get user profile
            const profileResponse = await fetch('https://api.spotify.com/v1/me', {
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`
                }
            });
            const profile = await profileResponse.json();

            // Create playlist
            const playlistResponse = await fetch(`https://api.spotify.com/v1/users/${profile.id}/playlists`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: `TTRPG: ${name}`,
                    description: 'Created by TTRPG Vault Ultra for tabletop gaming sessions',
                    public: false
                })
            });

            const playlist = await playlistResponse.json();

            // Add tracks if provided
            if (tracks && tracks.length > 0) {
                await fetch(`https://api.spotify.com/v1/playlists/${playlist.id}/tracks`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.accessToken}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        uris: tracks
                    })
                });
            }

            return playlist;
        } catch (error) {
            console.error('Error creating playlist:', error);
            throw error;
        }
    }
}

// Global instance
window.ttrpgSpotify = new TTRPGSpotifyIntegration(app);

// Utility functions for MetaBind buttons
window.setSessionMood = async (mood, volume = 25) => {
    try {
        if (!window.ttrpgSpotify.accessToken) {
            await window.ttrpgSpotify.authenticate();
        }
        
        const result = await window.ttrpgSpotify.setSessionMood(mood, { volume });
        
        if (result.success) {
            new Notice(`🎵 Now playing: ${result.playlist} (${mood} mood)`, 3000);
        } else {
            new Notice(`🎵 Music error: ${result.error}`, 5000);
        }
        
        return result;
    } catch (error) {
        new Notice(`🎵 Spotify connection failed: ${error.message}`, 5000);
        throw error;
    }
};

window.pauseMusic = async () => {
    try {
        await window.ttrpgSpotify.pausePlayback();
        new Notice('🎵 Music paused');
    } catch (error) {
        new Notice(`🎵 Error pausing music: ${error.message}`);
    }
};

window.resumeMusic = async () => {
    try {
        await window.ttrpgSpotify.resumePlayback();
        new Notice('🎵 Music resumed');
    } catch (error) {
        new Notice(`🎵 Error resuming music: ${error.message}`);
    }
};

window.setMusicVolume = async (volume) => {
    try {
        await window.ttrpgSpotify.setVolume(volume);
        new Notice(`🎵 Volume set to ${volume}%`);
    } catch (error) {
        new Notice(`🎵 Error setting volume: ${error.message}`);
    }
};

console.log('TTRPG Spotify Integration loaded successfully'); 