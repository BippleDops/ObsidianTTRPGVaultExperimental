#!/bin/bash

# Nightly Vault Maintenance Script
# Runs at 3 AM daily

VAULT_PATH="/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVaultExperimental"
LOG_DIR="$VAULT_PATH/09_Performance/logs"
DATE=$(date +%Y%m%d)

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_DIR/nightly_$DATE.log"
}

log "Starting nightly maintenance..."

cd "$VAULT_PATH"

# 1. Git backup
log "Running Git backup..."
git add -A >> "$LOG_DIR/nightly_$DATE.log" 2>&1
git commit -m "Automated nightly backup $(date '+%Y-%m-%d')" >> "$LOG_DIR/nightly_$DATE.log" 2>&1

# 2. Vault hygiene audit
log "Running vault hygiene audit..."
python3 _SCRIPTS/vault_hygiene_audit.py >> "$LOG_DIR/nightly_$DATE.log" 2>&1

# 3. Clean up old logs (keep 30 days)
log "Cleaning old logs..."
find "$LOG_DIR" -name "*.log" -mtime +30 -delete

# 4. Rebuild indexes
log "Rebuilding indexes..."
python3 _SCRIPTS/rebuild_indexes.py >> "$LOG_DIR/nightly_$DATE.log" 2>&1

# 5. Optimize images (if script exists)
if [ -f "_SCRIPTS/optimize_images.py" ]; then
    log "Optimizing images..."
    python3 _SCRIPTS/optimize_images.py >> "$LOG_DIR/nightly_$DATE.log" 2>&1
fi

log "Nightly maintenance complete!"

# Send notification (optional - requires terminal-notifier)
if command -v terminal-notifier &> /dev/null; then
    terminal-notifier -title "Obsidian Vault" -message "Nightly maintenance complete"
fi