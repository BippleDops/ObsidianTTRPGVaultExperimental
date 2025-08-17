# Vault Performance Optimization

## Dataview Optimization
- Use WHERE clauses to filter results
- Add LIMIT to large queries
- Prefer TABLE over LIST for better performance
- Use specific folder paths in FROM clauses

## Image Optimization
- Compress large images before embedding
- Use WebP format when possible
- Resize images to appropriate dimensions
- Consider using thumbnails for galleries

## Plugin Performance
- Disable unused plugins
- Use canvas sparingly for large graphs
- Limit real-time preview for large files
- Consider using cached views for complex queries

## File Organization
- Keep individual files under 1MB
- Limit deeply nested folder structures
- Use consistent naming conventions
- Archive old content regularly

## Indexing Optimization
```json
{
  "indexingSettings": {
    "excludePaths": [
      "08_Archive",
      "_BACKUPS",
      "09_Performance"
    ],
    "indexImages": false,
    "indexAudio": false
  }
}
```

## Memory Usage
- Close unnecessary tabs
- Restart Obsidian weekly
- Clear cache periodically
- Monitor plugin memory usage
