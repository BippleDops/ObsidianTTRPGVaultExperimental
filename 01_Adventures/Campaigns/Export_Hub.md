---
tags: [export, conversion, multi-format]
---

# 📤 Multi-Format Export System

## Available Export Formats

### 📄 PDF Export
```python
class PDFExporter:
    def export_campaign(self):
        sections = [
            "cover_page",
            "table_of_contents",
            "world_overview",
            "npcs",
            "locations",
            "quests",
            "items",
            "rules_reference",
            "appendices"
        ]

        pdf = PDFDocument()
        for section in sections:
            pdf.add_section(self.format_section(section))

        return pdf.save("campaign_guide.pdf")
```

**Options:**
- [ ] Include images
- [ ] Include stat blocks
- [ ] Player-safe version
- [ ] Print-friendly format

### 🎲 Roll20 Package
```javascript
// Roll20 API Compatible Format
const campaignData = {
  characters: [],
  handouts: [],
  maps: [],
  macros: [],
  rollableTables: []
};

function exportToRoll20() {
  convertNPCs();
  convertMaps();
  convertHandouts();
  createMacros();
  packageAsZip();
}
```

**Includes:**
- Character sheets
- Token markers
- Map layers
- Handout formatting
- Macro scripts

### 🏰 Foundry VTT Module
```json
{
  "name": "campaign-vault",
  "title": "Campaign Vault Export",
  "description": "Complete campaign content",
  "version": "1.0.0",
  "minimumCoreVersion": "0.8.0",
  "compatibleCoreVersion": "9.0.0",
  "author": "VaultSystem",
  "scripts": [],
  "styles": [],
  "packs": [
    {
      "name": "actors",
      "label": "NPCs",
      "path": "packs/actors.db",
      "entity": "Actor"
    },
    {
      "name": "scenes",
      "label": "Maps",
      "path": "packs/scenes.db",
      "entity": "Scene"
    }
  ]
}
```

### 🌍 World Anvil Export
```yaml
world:
  name: Campaign World
  description: Exported from Obsidian Vault

categories:
  - npcs:
      type: character
      template: person
  - locations:
      type: geography
      template: settlement
  - quests:
      type: plot
      template: storyline
```

### 📱 Web App Export
```html
<!DOCTYPE html>
<html>
<head>
    <title>Campaign Vault</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <nav id="sidebar">
        <!-- Navigation menu -->
    </nav>
    <main id="content">
        <!-- Dynamic content -->
    </main>
    <script src="app.js"></script>
</body>
</html>
```

## Export Presets

### Quick Exports
- **Player Handouts**: Safe content only
- **DM Screen**: Quick reference sheets
- **Session Pack**: Everything for next session
- **Campaign Bible**: Complete documentation

### Custom Export
Select content to include:
- [ ] NPCs
- [ ] Locations
- [ ] Quests
- [ ] Items
- [ ] Rules
- [ ] Maps
- [ ] Handouts
- [ ] Audio

## Format Conversion Matrix

| From | To PDF | To Roll20 | To Foundry | To Web |
|------|--------|-----------|------------|--------|
| Markdown | ✅ | ✅ | ✅ | ✅ |
| Images | ✅ | ✅ | ✅ | ✅ |
| Tables | ✅ | ✅ | ✅ | ✅ |
| Links | Convert | Convert | Update | Update |

---
*Export maintains all improvements and formatting*
