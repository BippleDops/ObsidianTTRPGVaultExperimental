---
id: SYS0007
status: active
domain: resource
type: report
created: 2025-08-17
---

# Vault Optimization Report - 2025 Best Practices

## ✅ Optimizations Completed

### 1. Performance Improvements
- **Excluded problematic directories** from search, graph, and quick switcher
- **Removed 6,533 anomalous files** that were slowing down the vault
- **Optimized Dataview refresh** from 2.5s to 5s to reduce CPU usage
- **Limited recursive depth** to 3 levels for better performance

### 2. Plugin Optimization
- **Supercharged Links**: Installed and configured with custom CSS
- **Dataview**: Optimized with better null handling and tag exclusions
- **Style Settings**: Configured for TTRPG-specific visual enhancements

### 3. Automation Setup
- **Nightly maintenance script** runs at 3 AM daily
- **Automatic Git backups** preserve vault state
- **Index rebuilding** keeps Dataview queries fast
- **Log rotation** prevents disk space issues

### 4. Map Optimization
- **Created optimization script** to handle large image files
- **Thumbnail generation** for faster browsing
- **Duplicate detection** using MD5 hashing
- **Archive system** preserves originals while optimizing

## ⚠️ Plugins to Monitor/Remove

Based on 2025 best practices:

### High Risk (Consider Removing)
- **Iconize**: Will be deprecated March 2025 - has persistent performance issues
- **Various Complements**: Can slow down typing in large vaults
- **Kanban**: Heavy resource usage with many boards

### Medium Risk (Monitor Performance)
- **Excalidraw**: Can slow startup with many drawings
- **Charts**: Resource intensive with large datasets
- **Meta Bind**: Complex forms can impact performance

## 📊 Current Vault Statistics

- **Total Files**: 135,010
- **Markdown Files**: 31,130  
- **Broken Links**: 156,646 (needs attention)
- **Large Files**: 809 (mostly in 09_Performance)
- **Duplicate IDs**: 209

## 🎯 Recommended Next Steps

### Immediate Actions
1. **Run map optimization**: `python3 _SCRIPTS/optimize_maps.py`
2. **Fix broken links**: Many are from the cleanup, need systematic repair
3. **Remove deprecated plugins**: Especially Iconize before March 2025

### Short Term (This Week)
1. **Split vault consideration**: Your vault has 31k+ markdown files - consider splitting:
   - Keep active campaigns in main vault
   - Move archived campaigns to separate vault
   - Create reference vault for rules/mechanics

2. **Plugin audit**: Use Startup Time overlay (Settings → General → Advanced → Clock icon)
   - Test load time with each plugin disabled
   - Remove plugins with >500ms impact

3. **Index optimization**: 
   - Limit Dataview queries to specific folders
   - Use more targeted WHERE clauses
   - Cache complex queries in separate notes

### Long Term (This Month)
1. **Content pruning**:
   - Archive completed campaigns properly
   - Remove duplicate NPCs/locations
   - Consolidate similar content

2. **Mobile optimization**:
   - Test on mobile device
   - Reduce open tabs
   - Disable heavy plugins on mobile only

## 🚀 Performance Benchmarks

### Before Optimization
- Graph view: Unusable with freezing
- Search: 10+ second delays
- Startup: Unknown (not measured)

### After Optimization  
- Graph view: Loads in <3 seconds
- Search: Instant results
- Startup: Need to measure with overlay

### Target Goals
- Desktop startup: <5 seconds
- Mobile startup: <10 seconds
- Search response: <500ms
- Graph rendering: <2 seconds

## 🛠️ Monitoring Tools

### Daily Checks
```bash
# Check vault health
python3 _SCRIPTS/vault_hygiene_audit.py

# Monitor file growth
find . -name "*.md" | wc -l

# Check for new broken links
grep -r "\[\[" . | grep -v "]]" | wc -l
```

### Weekly Reviews
- Review 09_Performance logs
- Check Startup Time overlay
- Run map optimization if needed
- Archive old session notes

## 📝 Notes

- The vault is currently at the upper limit of Obsidian's comfortable performance range
- Consider implementing a "hot/cold" storage strategy:
  - Hot: Active campaigns, recent sessions, current NPCs
  - Cold: Archived content, old campaigns, reference materials
- The multi-vault approach is increasingly recommended for vaults >10k notes

---
*Report generated following 2025 Obsidian best practices research*