---
enhanced: true

title: deployment report
type: report
tags:
- active
- report

created: '2025-08-14'
modified: '2025-08-14'

--- # TTRPG Asset Generation System - Deployment Report

## Description

Detailed description pending.

Generated: Thu Aug 14 15:32:03 CDT 2025 ## System Status | Component | Status | Port | PID |

|-----------|--------|------|-----|
| Comfy UI | running | 8188 | N/A |

*Sounds of [relevant sounds] echo in the distance.*| Orchestrator | stopped | 5679 | N/A | ## Asset Statistics - Total PNGs: 583

- Total Videos: 0
- Recent (1hr): 583 ## Recent Generations```/Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/04_Resources/Assets/Pasted image 20240607151510.png

/Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/04_Resources/Assets/Pasted image 20240627201658.png
/Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/04_Resources/Assets/Pasted image 20240630204305.png
/Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/04_Resources/Assets/Pasted image 20240630203442.png
/Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/04_Resources/Assets/Pasted Image 20240630230819_217.png```## Logs - Comfy UI: /Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/09_Performance/logs/comfyui.log

- Orchestrator: /Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/09_Performance/logs/orchestrator.log
- Security Audit: /Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/09_Performance/security_audit_report.json
- Quality Tests: /Users/jongosussmango/Library/Mobile Documents/i Cloud~md~obsidian/Documents/Obsidian TTRPGVault Experimental/09_Performance/test_report.json ## Quick Commands```bash

# Generate batch of images

node scripts/simple_batch_gen.js 5 # Run security audit

node scripts/security_audit.js # Run quality tests

node scripts/test_comfyui_quality.js # Generate video from image

node scripts/video_generation.js --image path/to/image.png # Check system status

curl http://127.0.0.1:8188/system_stats | jq```## Connections - See also: [[Master_Timeline

- Related: [Recent Events]]
- Connected to: [[Side Adventures ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes

## Notes

*Additional notes*

## Visual References
![04_Resources/maps/world_reports_bidirectional_links_gm.png]]
![[04_Resources/maps/world_reports_bidirectional_links_player.png
![04_Resources/maps/world_witness_reports_gm.png]]
