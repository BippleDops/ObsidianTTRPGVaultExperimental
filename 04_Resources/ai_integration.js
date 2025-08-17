/**
 * AI Integration Utilities for Obsidian TTRPG Vault
 * Handles OpenAI (text/image generation) and Unsplash (photo search)
 */

class TTRPGAIIntegration {
    constructor(app) {
        this.app = app;
        this.config = null;
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
            console.warn('AI Config not found or invalid:', error);
        }
    }

    // OpenAI Text Generation
    async generateNPCDescription(npcData) {
        if (!this.config?.openai?.api_key) {
            throw new Error('OpenAI API key not configured');
        }

        const prompt = `Create a detailed D&D NPC description for:
        
Name: ${npcData.name}
Race: ${npcData.race}
Occupation: ${npcData.occupation}
Location: ${npcData.location}
Personality Traits: ${npcData.personality || 'Unknown'}

Provide:
1. Physical appearance (2-3 sentences)
2. Personality quirks and mannerisms
3. A secret they're hiding
4. How they speak and interact with others
5. A potential quest hook they could provide

Keep it concise but engaging, suitable for immediate use in a D&D session.`;

        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.config.openai.api_key}`
                },
                body: JSON.stringify({
                    model: this.config.openai.model,
                    messages: [
                        {
                            role: 'system',
                            content: 'You are a professional D&D content creator specializing in memorable NPCs for tabletop gaming.'
                        },
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    max_tokens: this.config.openai.max_tokens,
                    temperature: this.config.openai.temperature
                })
            });

            const data = await response.json();
            return data.choices[0].message.content;
        } catch (error) {
            console.error('OpenAI API Error:', error);
            throw error;
        }
    }

    // OpenAI DALL-E Image Generation
    async generateNPCPortrait(npcData) {
        if (!this.config?.openai?.api_key) {
            throw new Error('OpenAI API key not configured');
        }

        const prompt = `High-quality fantasy D&D character portrait: ${npcData.age}-year-old ${npcData.gender} ${npcData.race} ${npcData.occupation}. ${npcData.appearance || 'Distinctive features'}. Professional digital painting style, detailed character art, fantasy setting, head and shoulders portrait.`;

        try {
            const response = await fetch('https://api.openai.com/v1/images/generations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.config.openai.api_key}`
                },
                body: JSON.stringify({
                    model: this.config.openai.dalle_model,
                    prompt: prompt,
                    size: "1024x1024",
                    quality: "standard",
                    n: 1
                })
            });

            const data = await response.json();
            return data.data[0].url;
        } catch (error) {
            console.error('DALL-E API Error:', error);
            throw error;
        }
    }

    // Unsplash Location Images
    async searchLocationImage(searchTerms) {
        if (!this.config?.unsplash?.access_key) {
            throw new Error('Unsplash API key not configured');
        }

        const query = encodeURIComponent(searchTerms);
        const url = `${this.config.unsplash.base_url}/search/photos?query=${query}&orientation=${this.config.unsplash.orientation}&per_page=${this.config.unsplash.per_page}`;

        try {
            const response = await fetch(url, {
                headers: {
                    'Authorization': `Client-ID ${this.config.unsplash.access_key}`
                }
            });

            const data = await response.json();
            
            if (data.results && data.results.length > 0) {
                const image = data.results[0];
                return {
                    url: image.urls.regular,
                    download_url: image.urls.full,
                    attribution: `Photo by ${image.user.name} on Unsplash`,
                    description: image.alt_description,
                    id: image.id
                };
            } else {
                throw new Error('No images found for search terms');
            }
        } catch (error) {
            console.error('Unsplash API Error:', error);
            throw error;
        }
    }

    // Save image from URL to vault
    async saveImageToVault(imageUrl, fileName, folder = 'z_Assets') {
        try {
            const response = await fetch(imageUrl);
            const blob = await response.blob();
            const arrayBuffer = await blob.arrayBuffer();
            
            const filePath = `${folder}/${fileName}`;
            await this.app.vault.createBinary(filePath, arrayBuffer);
            return filePath;
        } catch (error) {
            console.error('Error saving image:', error);
            throw error;
        }
    }

    // Generate complete NPC with AI
    async generateCompleteNPC(basicInfo) {
        try {
            // Generate description
            const description = await this.generateNPCDescription(basicInfo);
            
            // Generate portrait
            const portraitUrl = await this.generateNPCPortrait(basicInfo);
            
            // Save portrait to vault
            const fileName = `${basicInfo.name.toLowerCase().replace(/\s+/g, '-')}-portrait-${Date.now()}.png`;
            const imagePath = await this.saveImageToVault(portraitUrl, fileName, 'z_Assets/Characters');
            
            return {
                description,
                imagePath,
                portraitUrl
            };
        } catch (error) {
            console.error('Complete NPC generation failed:', error);
            throw error;
        }
    }

    // Generate quest hooks using AI
    async generateQuestHook(context) {
        if (!this.config?.openai?.api_key) {
            throw new Error('OpenAI API key not configured');
        }

        const prompt = `Create a compelling D&D quest hook for the following context:

Setting: ${context.setting || 'Fantasy city of Shadowhaven'}
NPCs involved: ${context.npcs || 'Unknown'}
Current events: ${context.events || 'Political tensions and missing ships'}
Party level: ${context.level || '3-5'}
Desired tone: ${context.tone || 'Investigation with political intrigue'}

Provide:
1. A compelling opening scenario (2-3 sentences)
2. The main mystery or problem to solve
3. 3 possible investigation paths
4. Potential complications or obstacles
5. Estimated rewards and consequences

Format as a complete quest brief ready for immediate use.`;

        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.config.openai.api_key}`
                },
                body: JSON.stringify({
                    model: this.config.openai.model,
                    messages: [
                        {
                            role: 'system',
                            content: 'You are an expert D&D Dungeon Master creating engaging quest content for tabletop gaming.'
                        },
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    max_tokens: this.config.openai.max_tokens,
                    temperature: this.config.openai.temperature
                })
            });

            const data = await response.json();
            return data.choices[0].message.content;
        } catch (error) {
            console.error('Quest generation error:', error);
            throw error;
        }
    }
}

// Global instance
window.ttrpgAI = new TTRPGAIIntegration(app);

// Utility functions for MetaBind buttons
window.generateAINPC = async (basicInfo) => {
    try {
        const result = await window.ttrpgAI.generateCompleteNPC(basicInfo);
        new Notice('AI NPC generated successfully!');
        return result;
    } catch (error) {
        new Notice(`AI Generation failed: ${error.message}`, 5000);
        throw error;
    }
};

window.generateLocationImage = async (searchTerms) => {
    try {
        const result = await window.ttrpgAI.searchLocationImage(searchTerms);
        const fileName = `location-${searchTerms.replace(/\s+/g, '-')}-${Date.now()}.jpg`;
        const imagePath = await window.ttrpgAI.saveImageToVault(result.url, fileName, 'z_Assets/Locations');
        
        new Notice(`Location image saved: ${fileName}`);
        return { ...result, localPath: imagePath };
    } catch (error) {
        new Notice(`Image search failed: ${error.message}`, 5000);
        throw error;
    }
};

window.generateQuestAI = async (context) => {
    try {
        const quest = await window.ttrpgAI.generateQuestHook(context);
        new Notice('AI quest generated successfully!');
        return quest;
    } catch (error) {
        new Notice(`Quest generation failed: ${error.message}`, 5000);
        throw error;
    }
};

console.log('TTRPG AI Integration loaded successfully'); 