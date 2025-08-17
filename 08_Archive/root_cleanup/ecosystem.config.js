module.exports = {
  apps: [
    {
      name: 'vault-automation',
      script: './scripts/continuous_vault_automation.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production'
      },
      error_file: './09_Performance/continuous_logs/pm2-error.log',
      out_file: './09_Performance/continuous_logs/pm2-out.log',
      log_file: './09_Performance/continuous_logs/pm2-combined.log',
      time: true,
      cron_restart: '0 0 * * *', // Restart daily at midnight
    },
    {
      name: 'link-resolver',
      script: './scripts/continuous_link_resolver.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '*/5 * * * *', // Every 5 minutes
      error_file: './09_Performance/continuous_logs/link-resolver-error.log',
      out_file: './09_Performance/continuous_logs/link-resolver-out.log',
    },
    {
      name: 'content-enhancer',
      script: './scripts/continuous_content_enhancer.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '*/10 * * * *', // Every 10 minutes
      error_file: './09_Performance/continuous_logs/content-enhancer-error.log',
      out_file: './09_Performance/continuous_logs/content-enhancer-out.log',
    },
    {
      name: 'asset-generator',
      script: './scripts/continuous_asset_generator.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '*/15 * * * *', // Every 15 minutes
      error_file: './09_Performance/continuous_logs/asset-generator-error.log',
      out_file: './09_Performance/continuous_logs/asset-generator-out.log',
    },
    {
      name: 'metadata-optimizer',
      script: './scripts/continuous_metadata_optimizer.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '*/20 * * * *', // Every 20 minutes
      error_file: './09_Performance/continuous_logs/metadata-optimizer-error.log',
      out_file: './09_Performance/continuous_logs/metadata-optimizer-out.log',
    },
    {
      name: 'git-sync',
      script: './scripts/continuous_git_sync.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '*/30 * * * *', // Every 30 minutes
      error_file: './09_Performance/continuous_logs/git-sync-error.log',
      out_file: './09_Performance/continuous_logs/git-sync-out.log',
    },
    {
      name: 'index-builder',
      script: './scripts/continuous_index_builder.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '0 * * * *', // Every hour
      error_file: './09_Performance/continuous_logs/index-builder-error.log',
      out_file: './09_Performance/continuous_logs/index-builder-out.log',
    },
    {
      name: 'quality-monitor',
      script: './scripts/continuous_quality_monitor.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '0 */2 * * *', // Every 2 hours
      error_file: './09_Performance/continuous_logs/quality-monitor-error.log',
      out_file: './09_Performance/continuous_logs/quality-monitor-out.log',
    },
    {
      name: 'backup-manager',
      script: './scripts/continuous_backup.js',
      cwd: process.cwd(),
      instances: 1,
      autorestart: false,
      cron_restart: '0 */6 * * *', // Every 6 hours
      error_file: './09_Performance/continuous_logs/backup-manager-error.log',
      out_file: './09_Performance/continuous_logs/backup-manager-out.log',
    }
  ]
};
