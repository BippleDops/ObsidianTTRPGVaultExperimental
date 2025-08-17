# Vault Maintenance Schedule

## Daily Tasks (Before Sessions)
- [ ] Run session prep: `python3 _SCRIPTS/session_prep.py`
- [ ] Check for new files in root directory
- [ ] Review recent NPCs for upcoming session

## Weekly Tasks
- [ ] Run full automation: `python3 _SCRIPTS/vault_automation.py`
- [ ] Check link report: [[09_Performance/link_check_auto.json]]
- [ ] Organize new content: `python3 _SCRIPTS/auto_organizer.py`

## Monthly Tasks
- [ ] Full backup: `python3 _SCRIPTS/auto_backup.py`
- [ ] Review performance metrics: [[09_Performance/performance_report_phase7.md]]
- [ ] Clean duplicate files
- [ ] Archive old sessions (>6 months)

## Quarterly Tasks
- [ ] Comprehensive link check
- [ ] Image optimization review
- [ ] Update templates with new features
- [ ] Review and update automation scripts

## Annual Tasks
- [ ] Major vault cleanup
- [ ] Archive completed campaigns
- [ ] Update documentation
- [ ] Performance audit

## Emergency Procedures

### If Vault Corrupted
1. Check `08_Archive/automated_backups/` for recent backup
2. Run `python3 _SCRIPTS/EMERGENCY_RECOVERY.py` if exists
3. Restore from `vault_backup_*.tar.gz` if available

### If Mass File Loss
1. Check `08_Archive/` for moved files
2. Review `09_Performance/` for recent operations
3. Use git history if available: `git log --oneline`

### If Performance Degrades
1. Run performance analysis
2. Check for large files: >10MB
3. Remove duplicates
4. Optimize images

---
*Keep this schedule handy for vault maintenance*
