---
id: SYS0008
status: active
domain: resource
type: guide
created: 2025-08-17
---

# Performance Monitoring Guide

## 📊 How to Use Startup Time Overlay

### Accessing the Overlay
1. Open Obsidian Settings (⚙️)
2. Navigate to **General** tab
3. Scroll to **Advanced** section
4. Click the **Clock icon** (⏱️) next to "Startup time"
5. The overlay will appear showing detailed load times

### Understanding the Metrics

#### Key Metrics to Watch
- **App Start**: Initial application load (target: <2s)
- **Workspace**: Loading tabs and views (target: <1s)
- **Vault**: Loading vault structure (target: <3s)
- **Plugins**: Individual plugin load times
- **Total**: Complete startup time (target: <5s desktop, <10s mobile)

#### Warning Signs
- 🔴 Any plugin taking >500ms
- 🔴 Workspace >2s (too many open tabs)
- 🔴 Vault >5s (too many files)
- 🔴 Total >10s on desktop

## 🎯 Current Performance Status

### After Optimization
- **Files Removed**: 6,533 anomalous files
- **Maps Deduplicated**: 13,989 duplicate maps removed
- **Graph View**: Loads in <3 seconds
- **Search**: Instant results
- **Excluded Directories**: Archive, Performance, Scripts, Metadata

### Vault Statistics
- **Total Files**: ~121,000 (was 135,000)
- **Markdown Files**: ~24,600 (was 31,130)
- **Unique Maps**: 17 (was 14,006)
- **Broken Links**: Still ~156k (needs attention)

## 🔧 Performance Optimization Commands

### Daily Monitoring
```bash
# Check vault health
python3 _SCRIPTS/vault_hygiene_audit.py

# Count markdown files
find . -name "*.md" -type f | wc -l

# Check large files
find . -size +1M -type f | head -20

# Monitor plugin folder size
du -sh .obsidian/plugins/*
```

### Weekly Maintenance
```bash
# Run map optimization
python3 _SCRIPTS/optimize_maps.py

# Clean anomalous files
python3 _SCRIPTS/anomalous_cleanup.py --dry-run

# Check for conflicts
find . -name "*conflicted*" -type f
```

## ⚡ Quick Performance Fixes

### If Obsidian is Slow

1. **Too Many Tabs Open**
   - Close all tabs: Cmd+K, then type "Close all tabs"
   - Keep max 5-10 tabs open

2. **Graph View Freezing**
   - Use filtered graph view
   - Limit depth to 2-3 levels
   - Exclude archive folders

3. **Search Slow**
   - Clear search cache: Settings → Files & Links → Clear cache
   - Use more specific search terms
   - Exclude folders with `-path:`

4. **Plugin Issues**
   - Disable all community plugins
   - Re-enable one by one
   - Check Startup Time after each

## 📈 Performance Benchmarks

### Excellent Performance
- Desktop startup: <3 seconds
- Mobile startup: <7 seconds
- Search response: <200ms
- Graph render: <1 second
- File open: Instant

### Acceptable Performance
- Desktop startup: 3-5 seconds
- Mobile startup: 7-12 seconds
- Search response: 200-500ms
- Graph render: 1-3 seconds
- File open: <500ms

### Needs Optimization
- Desktop startup: >5 seconds
- Mobile startup: >12 seconds
- Search response: >500ms
- Graph render: >3 seconds
- File open: >500ms

## 🚨 Emergency Performance Recovery

If vault becomes unusable:

### 1. Safe Mode
- Hold Shift while starting Obsidian
- Disables all community plugins
- Test if performance improves

### 2. Reset Workspace
```bash
# Backup current workspace
cp .obsidian/workspace.json .obsidian/workspace.backup.json

# Reset to minimal workspace
echo '{"main":{"id":"","type":"split","children":[]}}' > .obsidian/workspace.json
```

### 3. Plugin Cleanup
```bash
# List plugins by size
du -sh .obsidian/plugins/* | sort -h

# Remove problematic plugin (example)
rm -rf .obsidian/plugins/[plugin-name]
```

### 4. Cache Clear
- Settings → Files & Links → Clear cache
- Settings → Appearance → Reload without cache
- Restart Obsidian

## 📱 Mobile-Specific Optimization

### Reduce Mobile Load
1. **Limit Plugins**: Settings → Community Plugins → Disable heavy ones
2. **Reduce Open Files**: Keep only 1-3 files open
3. **Disable Graph**: Don't use graph view on mobile
4. **Simplify Theme**: Use default or minimal theme

### Mobile Plugin Blacklist
These plugins significantly impact mobile performance:
- Excalidraw (heavy drawing engine)
- Kanban (complex DOM manipulation)
- Charts (data processing)
- Any AI/LLM plugins

## 🔄 Automated Monitoring

### Nightly Job Status
Check if running properly:
```bash
# View launchd status
launchctl list | grep obsidian

# Check last run log
tail -100 09_Performance/logs/nightly_*.log

# Manual run
bash _SCRIPTS/run_nightly_jobs.sh
```

### Performance Tracking
Create a weekly log:
```bash
# Weekly performance snapshot
echo "=== $(date) ===" >> 09_Performance/weekly_metrics.log
echo "Files: $(find . -name "*.md" | wc -l)" >> 09_Performance/weekly_metrics.log
echo "Vault size: $(du -sh . | cut -f1)" >> 09_Performance/weekly_metrics.log
```

## 🎯 Next Optimization Steps

Based on current metrics:

1. **Fix Broken Links** (156k remaining)
   - Major performance impact
   - Run systematic link repair

2. **Consider Vault Split**
   - 24k markdown files is high
   - Split into active/archive vaults

3. **Plugin Audit**
   - Remove unused plugins
   - Update outdated ones
   - Replace heavy plugins

4. **Content Pruning**
   - Archive old campaigns
   - Remove draft content
   - Consolidate duplicates

---
*Monitor performance weekly for best results*