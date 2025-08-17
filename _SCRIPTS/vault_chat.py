#!/usr/bin/env python3
"""
In-Vault Chat System - Sprint 1 MVI
Lightweight comment system for GM/Player discussions
"""

import os
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional
from common import ROOT_DIR, save_json, load_json

class VaultChatSystem:
    def __init__(self, vault_path: str = None):
        self.vault_path = vault_path or ROOT_DIR
        self.chat_dir = os.path.join(self.vault_path, "scripts", "chat_data")
        self.users_file = os.path.join(self.chat_dir, "users.json")
        self.messages_file = os.path.join(self.chat_dir, "messages.json")
        self.threads_file = os.path.join(self.chat_dir, "threads.json")
        
        os.makedirs(self.chat_dir, exist_ok=True)
        
        self.users = self._load_users()
        self.messages = self._load_messages()
        self.threads = self._load_threads()
    
    def _load_users(self) -> Dict[str, Any]:
        """Load user data"""
        default_users = {
            'admin': {
                'display_name': 'Game Master',
                'role': 'gm',
                'color': '#ff6b6b',
                'avatar': '🎲',
                'created': datetime.now().isoformat(),
                'last_active': datetime.now().isoformat()
            }
        }
        return load_json(self.users_file, default_users)
    
    def _load_messages(self) -> List[Dict[str, Any]]:
        """Load message history"""
        return load_json(self.messages_file, [])
    
    def _load_threads(self) -> Dict[str, Any]:
        """Load thread data"""
        return load_json(self.threads_file, {})
    
    def _save_users(self):
        """Save user data"""
        save_json(self.users_file, self.users)
    
    def _save_messages(self):
        """Save messages"""
        save_json(self.messages_file, self.messages)
    
    def _save_threads(self):
        """Save threads"""
        save_json(self.threads_file, self.threads)
    
    def add_user(self, username: str, display_name: str, role: str = 'player') -> bool:
        """Add a new user"""
        if username in self.users:
            return False
        
        colors = ['#4a90e2', '#50e3c2', '#f5a623', '#7ed321', '#bd10e0', '#b8e986']
        avatars = ['🧙‍♀️', '⚔️', '🛡️', '🏹', '🔮', '📚', '⚡', '🌊', '🔥', '❄️']
        
        user_count = len(self.users)
        
        self.users[username] = {
            'display_name': display_name,
            'role': role,
            'color': colors[user_count % len(colors)],
            'avatar': avatars[user_count % len(avatars)],
            'created': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat()
        }
        
        self._save_users()
        return True
    
    def create_thread(self, title: str, file_path: str, creator: str, description: str = "") -> str:
        """Create a new discussion thread"""
        thread_id = f"thread_{int(time.time())}_{len(self.threads)}"
        
        self.threads[thread_id] = {
            'title': title,
            'file_path': file_path,
            'creator': creator,
            'description': description,
            'created': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'message_count': 0,
            'participants': [creator],
            'tags': [],
            'status': 'active'  # active, resolved, archived
        }
        
        self._save_threads()
        return thread_id
    
    def post_message(self, thread_id: str, user: str, content: str, 
                    message_type: str = 'message', reply_to: str = None) -> str:
        """Post a message to a thread"""
        if thread_id not in self.threads:
            return None
        
        message_id = f"msg_{int(time.time())}_{len(self.messages)}"
        
        message = {
            'id': message_id,
            'thread_id': thread_id,
            'user': user,
            'content': content,
            'type': message_type,  # message, system, reaction
            'timestamp': datetime.now().isoformat(),
            'reply_to': reply_to,
            'reactions': {},
            'edited': False,
            'edit_history': []
        }
        
        self.messages.append(message)
        
        # Update thread info
        thread = self.threads[thread_id]
        thread['last_activity'] = datetime.now().isoformat()
        thread['message_count'] = thread.get('message_count', 0) + 1
        
        if user not in thread['participants']:
            thread['participants'].append(user)
        
        # Update user last active
        if user in self.users:
            self.users[user]['last_active'] = datetime.now().isoformat()
        
        self._save_messages()
        self._save_threads()
        self._save_users()
        
        return message_id
    
    def get_thread_messages(self, thread_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get messages for a thread"""
        thread_messages = [
            msg for msg in self.messages 
            if msg['thread_id'] == thread_id
        ]
        
        # Sort by timestamp
        thread_messages.sort(key=lambda x: x['timestamp'])
        
        # Apply pagination
        start = offset
        end = offset + limit
        
        return thread_messages[start:end]
    
    def get_threads_by_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Get all threads for a specific file"""
        file_threads = []
        
        for thread_id, thread_data in self.threads.items():
            if thread_data['file_path'] == file_path:
                thread_info = dict(thread_data)
                thread_info['id'] = thread_id
                file_threads.append(thread_info)
        
        # Sort by last activity
        file_threads.sort(key=lambda x: x['last_activity'], reverse=True)
        
        return file_threads
    
    def get_active_threads(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get most recently active threads"""
        active_threads = []
        
        for thread_id, thread_data in self.threads.items():
            if thread_data['status'] == 'active':
                thread_info = dict(thread_data)
                thread_info['id'] = thread_id
                active_threads.append(thread_info)
        
        # Sort by last activity
        active_threads.sort(key=lambda x: x['last_activity'], reverse=True)
        
        return active_threads[:limit]
    
    def add_reaction(self, message_id: str, user: str, emoji: str) -> bool:
        """Add reaction to a message"""
        for message in self.messages:
            if message['id'] == message_id:
                if emoji not in message['reactions']:
                    message['reactions'][emoji] = []
                
                if user not in message['reactions'][emoji]:
                    message['reactions'][emoji].append(user)
                else:
                    message['reactions'][emoji].remove(user)
                    if not message['reactions'][emoji]:
                        del message['reactions'][emoji]
                
                self._save_messages()
                return True
        
        return False
    
    def search_messages(self, query: str, user: str = None, thread_id: str = None) -> List[Dict[str, Any]]:
        """Search messages"""
        results = []
        query_lower = query.lower()
        
        for message in self.messages:
            if query_lower in message['content'].lower():
                if user and message['user'] != user:
                    continue
                if thread_id and message['thread_id'] != thread_id:
                    continue
                
                result = dict(message)
                
                # Add thread context
                if message['thread_id'] in self.threads:
                    result['thread_title'] = self.threads[message['thread_id']]['title']
                    result['thread_file'] = self.threads[message['thread_id']]['file_path']
                
                # Add user info
                if message['user'] in self.users:
                    result['user_display'] = self.users[message['user']]['display_name']
                    result['user_avatar'] = self.users[message['user']]['avatar']
                
                results.append(result)
        
        # Sort by timestamp, most recent first
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return results
    
    def get_user_activity(self, user: str, days: int = 7) -> Dict[str, Any]:
        """Get user activity summary"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.isoformat()
        
        user_messages = [
            msg for msg in self.messages 
            if msg['user'] == user and msg['timestamp'] > cutoff_str
        ]
        
        user_threads = [
            thread_id for thread_id, thread_data in self.threads.items()
            if user in thread_data['participants'] and thread_data['last_activity'] > cutoff_str
        ]
        
        return {
            'user': user,
            'period_days': days,
            'messages_posted': len(user_messages),
            'threads_participated': len(user_threads),
            'last_active': self.users.get(user, {}).get('last_active'),
            'recent_messages': user_messages[-5:]  # Last 5 messages
        }
    
    def export_thread(self, thread_id: str) -> Dict[str, Any]:
        """Export thread for backup/sharing"""
        if thread_id not in self.threads:
            return None
        
        thread_data = dict(self.threads[thread_id])
        thread_messages = self.get_thread_messages(thread_id, limit=1000)
        
        # Add user display names
        for message in thread_messages:
            if message['user'] in self.users:
                message['user_display'] = self.users[message['user']]['display_name']
        
        return {
            'thread': thread_data,
            'messages': thread_messages,
            'exported': datetime.now().isoformat(),
            'participants': {
                user_id: self.users.get(user_id, {})
                for user_id in thread_data['participants']
            }
        }

def main():
    parser = argparse.ArgumentParser(description='Vault Chat System')
    parser.add_argument('action', choices=[
        'add-user', 'create-thread', 'post-message', 'list-threads', 
        'show-messages', 'search', 'activity', 'export'
    ])
    parser.add_argument('--user', help='Username')
    parser.add_argument('--display-name', help='Display name for user')
    parser.add_argument('--role', default='player', help='User role')
    parser.add_argument('--thread-id', help='Thread ID')
    parser.add_argument('--title', help='Thread title')
    parser.add_argument('--file', help='File path')
    parser.add_argument('--content', help='Message content')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--limit', type=int, default=20, help='Result limit')
    
    args = parser.parse_args()
    
    chat = VaultChatSystem()
    
    if args.action == 'add-user':
        if not args.user or not args.display_name:
            print("--user and --display-name required")
            return
        
        success = chat.add_user(args.user, args.display_name, args.role)
        if success:
            print(f"Added user: {args.display_name} ({args.user})")
        else:
            print(f"User {args.user} already exists")
    
    elif args.action == 'create-thread':
        if not args.title or not args.file or not args.user:
            print("--title, --file, and --user required")
            return
        
        thread_id = chat.create_thread(args.title, args.file, args.user)
        print(f"Created thread: {thread_id}")
    
    elif args.action == 'post-message':
        if not args.thread_id or not args.user or not args.content:
            print("--thread-id, --user, and --content required")
            return
        
        message_id = chat.post_message(args.thread_id, args.user, args.content)
        if message_id:
            print(f"Posted message: {message_id}")
        else:
            print("Failed to post message")
    
    elif args.action == 'list-threads':
        if args.file:
            threads = chat.get_threads_by_file(args.file)
        else:
            threads = chat.get_active_threads(args.limit)
        
        print(f"Found {len(threads)} threads:")
        for thread in threads:
            print(f"  {thread['id']}: {thread['title']} ({thread['message_count']} messages)")
    
    elif args.action == 'show-messages':
        if not args.thread_id:
            print("--thread-id required")
            return
        
        messages = chat.get_thread_messages(args.thread_id, args.limit)
        print(f"Messages in thread {args.thread_id}:")
        
        for msg in messages:
            user_name = chat.users.get(msg['user'], {}).get('display_name', msg['user'])
            timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')
            print(f"  [{timestamp}] {user_name}: {msg['content']}")
    
    elif args.action == 'search':
        if not args.query:
            print("--query required")
            return
        
        results = chat.search_messages(args.query)
        print(f"Found {len(results)} messages:")
        
        for result in results[:args.limit]:
            user_name = result.get('user_display', result['user'])
            thread_title = result.get('thread_title', 'Unknown Thread')
            print(f"  {user_name} in '{thread_title}': {result['content']}")
    
    elif args.action == 'activity':
        if not args.user:
            print("--user required")
            return
        
        activity = chat.get_user_activity(args.user)
        print(f"Activity for {args.user}:")
        print(f"  Messages: {activity['messages_posted']}")
        print(f"  Threads: {activity['threads_participated']}")
        print(f"  Last active: {activity['last_active']}")
    
    elif args.action == 'export':
        if not args.thread_id:
            print("--thread-id required")
            return
        
        export_data = chat.export_thread(args.thread_id)
        if export_data:
            export_file = f"thread_export_{args.thread_id}.json"
            save_json(export_file, export_data)
            print(f"Exported thread to {export_file}")
        else:
            print("Thread not found")

if __name__ == "__main__":
    main()