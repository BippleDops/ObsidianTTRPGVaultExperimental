#!/usr/bin/env python3
"""
Player Engagement Metrics System - Sprint 1 MVI
Track most-visited content and session activity
"""

import os
import json
import time
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
from common import ROOT_DIR, load_json, save_json

class EngagementTracker:
    def __init__(self, vault_path: str = None):
        self.vault_path = vault_path or ROOT_DIR
        self.metrics_file = os.path.join(self.vault_path, "scripts", "engagement_data.json")
        self.session_file = os.path.join(self.vault_path, "scripts", "session_data.json")
        self.data = self._load_data()
        self.session_data = self._load_session_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load engagement metrics data"""
        default_data = {
            'content_visits': {},  # {file_path: {'count': int, 'last_visit': str, 'total_time': int}}
            'daily_stats': {},     # {date: {'visits': int, 'unique_files': int, 'session_time': int}}
            'search_queries': [],  # [{'query': str, 'timestamp': str, 'results_count': int}]
            'user_sessions': [],   # [{'start': str, 'end': str, 'pages_viewed': int}]
            'hot_content': {},     # Top content by category
            'last_updated': datetime.now().isoformat()
        }
        
        return load_json(self.metrics_file, default_data)
    
    def _load_session_data(self) -> Dict[str, Any]:
        """Load current session data"""
        default_session = {
            'session_id': None,
            'start_time': None,
            'current_file': None,
            'file_start_time': None,
            'pages_in_session': [],
            'active': False
        }
        
        return load_json(self.session_file, default_session)
    
    def _save_data(self):
        """Save engagement data"""
        self.data['last_updated'] = datetime.now().isoformat()
        save_json(self.metrics_file, self.data)
    
    def _save_session_data(self):
        """Save session data"""
        save_json(self.session_file, self.session_data)
    
    def start_session(self, session_id: str = None) -> str:
        """Start a new tracking session"""
        session_id = session_id or f"session_{int(time.time())}"
        
        self.session_data = {
            'session_id': session_id,
            'start_time': datetime.now().isoformat(),
            'current_file': None,
            'file_start_time': None,
            'pages_in_session': [],
            'active': True
        }
        
        self._save_session_data()
        return session_id
    
    def end_session(self):
        """End current session and save stats"""
        if not self.session_data['active']:
            return
            
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.session_data['start_time'])
        session_duration = int((end_time - start_time).total_seconds())
        
        # Save session to history
        session_record = {
            'session_id': self.session_data['session_id'],
            'start': self.session_data['start_time'],
            'end': end_time.isoformat(),
            'duration': session_duration,
            'pages_viewed': len(self.session_data['pages_in_session']),
            'unique_files': len(set(self.session_data['pages_in_session']))
        }
        
        self.data['user_sessions'].append(session_record)
        
        # Update daily stats
        date_key = end_time.strftime('%Y-%m-%d')
        if date_key not in self.data['daily_stats']:
            self.data['daily_stats'][date_key] = {'visits': 0, 'unique_files': 0, 'session_time': 0}
        
        self.data['daily_stats'][date_key]['visits'] += len(self.session_data['pages_in_session'])
        self.data['daily_stats'][date_key]['unique_files'] += len(set(self.session_data['pages_in_session']))
        self.data['daily_stats'][date_key]['session_time'] += session_duration
        
        # Mark session as inactive
        self.session_data['active'] = False
        self._save_session_data()
        self._save_data()
    
    def track_file_visit(self, file_path: str, duration: int = None):
        """Track a visit to a specific file"""
        if not self.session_data['active']:
            self.start_session()
        
        # End previous file if exists
        if self.session_data['current_file'] and self.session_data['file_start_time']:
            self._finalize_file_visit()
        
        # Start tracking new file
        self.session_data['current_file'] = file_path
        self.session_data['file_start_time'] = datetime.now().isoformat()
        self.session_data['pages_in_session'].append(file_path)
        
        # Initialize file in metrics if not exists
        if file_path not in self.data['content_visits']:
            self.data['content_visits'][file_path] = {
                'count': 0,
                'total_time': 0,
                'last_visit': None,
                'first_visit': datetime.now().isoformat()
            }
        
        # Update visit count
        self.data['content_visits'][file_path]['count'] += 1
        self.data['content_visits'][file_path]['last_visit'] = datetime.now().isoformat()
        
        if duration:
            self.data['content_visits'][file_path]['total_time'] += duration
        
        self._save_session_data()
        self._save_data()
    
    def _finalize_file_visit(self):
        """Finalize the current file visit with duration"""
        if not self.session_data['current_file'] or not self.session_data['file_start_time']:
            return
        
        start_time = datetime.fromisoformat(self.session_data['file_start_time'])
        duration = int((datetime.now() - start_time).total_seconds())
        
        file_path = self.session_data['current_file']
        if file_path in self.data['content_visits']:
            self.data['content_visits'][file_path]['total_time'] += duration
    
    def track_search(self, query: str, results_count: int):
        """Track a search query"""
        search_record = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results_count': results_count,
            'session_id': self.session_data.get('session_id')
        }
        
        self.data['search_queries'].append(search_record)
        
        # Keep only recent searches (last 1000)
        if len(self.data['search_queries']) > 1000:
            self.data['search_queries'] = self.data['search_queries'][-1000:]
        
        self._save_data()
    
    def get_engagement_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate engagement report for specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Top visited content
        recent_visits = {
            path: data for path, data in self.data['content_visits'].items()
            if data['last_visit'] and datetime.fromisoformat(data['last_visit']) > cutoff_date
        }
        
        top_by_visits = sorted(
            recent_visits.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:20]
        
        top_by_time = sorted(
            recent_visits.items(),
            key=lambda x: x[1]['total_time'],
            reverse=True
        )[:20]
        
        # Daily activity
        recent_daily = {
            date: stats for date, stats in self.data['daily_stats'].items()
            if datetime.fromisoformat(date + 'T00:00:00') > cutoff_date
        }
        
        # Search trends
        recent_searches = [
            search for search in self.data['search_queries']
            if datetime.fromisoformat(search['timestamp']) > cutoff_date
        ]
        
        search_terms = Counter([s['query'].lower() for s in recent_searches])
        
        # Session stats
        recent_sessions = [
            session for session in self.data['user_sessions']
            if datetime.fromisoformat(session['start']) > cutoff_date
        ]
        
        avg_session_duration = 0
        avg_pages_per_session = 0
        if recent_sessions:
            avg_session_duration = sum(s['duration'] for s in recent_sessions) / len(recent_sessions)
            avg_pages_per_session = sum(s['pages_viewed'] for s in recent_sessions) / len(recent_sessions)
        
        return {
            'period_days': days,
            'total_unique_content': len(recent_visits),
            'total_visits': sum(data['count'] for data in recent_visits.values()),
            'total_time_spent': sum(data['total_time'] for data in recent_visits.values()),
            'top_content_by_visits': [
                {
                    'file': os.path.basename(path),
                    'path': path,
                    'visits': data['count'],
                    'total_time': data['total_time'],
                    'last_visit': data['last_visit']
                } for path, data in top_by_visits
            ],
            'top_content_by_time': [
                {
                    'file': os.path.basename(path),
                    'path': path,
                    'total_time': data['total_time'],
                    'visits': data['count']
                } for path, data in top_by_time
            ],
            'daily_activity': recent_daily,
            'search_trends': dict(search_terms.most_common(10)),
            'session_stats': {
                'total_sessions': len(recent_sessions),
                'avg_duration': int(avg_session_duration),
                'avg_pages_per_session': round(avg_pages_per_session, 1)
            },
            'recent_searches': recent_searches[-10:]  # Last 10 searches
        }
    
    def get_content_popularity_score(self, file_path: str) -> float:
        """Calculate popularity score for content (0-100)"""
        if file_path not in self.data['content_visits']:
            return 0.0
        
        visit_data = self.data['content_visits'][file_path]
        
        # Factors: visit count (40%), time spent (40%), recency (20%)
        visit_score = min(visit_data['count'] / 10, 1.0) * 40  # Max 10 visits = full score
        time_score = min(visit_data['total_time'] / 600, 1.0) * 40  # Max 10 minutes = full score
        
        recency_score = 0
        if visit_data['last_visit']:
            days_ago = (datetime.now() - datetime.fromisoformat(visit_data['last_visit'])).days
            recency_score = max(0, (30 - days_ago) / 30) * 20  # Recent = higher score
        
        return round(visit_score + time_score + recency_score, 1)

def main():
    parser = argparse.ArgumentParser(description='Player Engagement Metrics')
    parser.add_argument('action', choices=['start', 'end', 'visit', 'search', 'report', 'score'])
    parser.add_argument('--file', help='File path for visit tracking')
    parser.add_argument('--duration', type=int, help='Duration in seconds')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--results', type=int, default=0, help='Number of search results')
    parser.add_argument('--days', type=int, default=30, help='Days for report')
    parser.add_argument('--session-id', help='Session ID')
    
    args = parser.parse_args()
    
    tracker = EngagementTracker()
    
    if args.action == 'start':
        session_id = tracker.start_session(args.session_id)
        print(f"Started session: {session_id}")
    
    elif args.action == 'end':
        tracker.end_session()
        print("Session ended")
    
    elif args.action == 'visit':
        if not args.file:
            print("--file required for visit tracking")
            return
        tracker.track_file_visit(args.file, args.duration)
        print(f"Tracked visit to {args.file}")
    
    elif args.action == 'search':
        if not args.query:
            print("--query required for search tracking")
            return
        tracker.track_search(args.query, args.results)
        print(f"Tracked search: {args.query}")
    
    elif args.action == 'report':
        report = tracker.get_engagement_report(args.days)
        print(json.dumps(report, indent=2))
    
    elif args.action == 'score':
        if not args.file:
            print("--file required for popularity score")
            return
        score = tracker.get_content_popularity_score(args.file)
        print(f"Popularity score for {args.file}: {score}/100")

if __name__ == "__main__":
    main()