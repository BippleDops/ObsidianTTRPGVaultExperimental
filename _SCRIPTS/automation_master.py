#!/usr/bin/env python3
"""
Automation Master Control Script
Unified interface for all Phase 4 automation systems
Part of Phase 4: Advanced Automation & Dynamic Systems
"""

import os
import sys
import json
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class AutomationMaster:
    """Master controller for all vault automation systems."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.scripts_path = self.vault_path / "scripts"
        
        # Available automation systems
        self.systems = {
            "validator": {
                "script": "content_validator.py",
                "description": "Content validation and quality assurance",
                "status": "available"
            },
            "backup": {
                "script": "backup_automation.py", 
                "description": "Automated backup and versioning",
                "status": "available"
            },
            "links": {
                "script": "auto_link_suggester.py",
                "description": "Automatic link suggestion system",
                "status": "available"
            },
            "notifications": {
                "script": "update_notification_system.py",
                "description": "Update monitoring and notifications",
                "status": "available"
            },
            "ai_generator": {
                "script": "ai_content_generator.py",
                "description": "AI-assisted content generation",
                "status": "available"
            },
            "random_generator": {
                "script": "random_generator_engine.py",
                "description": "Random content generation",
                "status": "available"
            },
            "quest_tracker": {
                "script": "dynamic_quest_tracker.py",
                "description": "Dynamic quest state tracking",
                "status": "available"
            }
        }
        
        self.check_system_availability()
        
    def check_system_availability(self):
        """Check which automation systems are available."""
        for system_id, system_info in self.systems.items():
            script_path = self.scripts_path / system_info["script"]
            if script_path.exists():
                system_info["status"] = "ready"
            else:
                system_info["status"] = "missing"
                
    def run_command(self, system: str, command: List[str]) -> Dict[str, Any]:
        """Run a command for a specific system."""
        if system not in self.systems:
            return {"error": f"Unknown system: {system}"}
            
        system_info = self.systems[system]
        if system_info["status"] != "ready":
            return {"error": f"System {system} is not available"}
            
        script_path = self.scripts_path / system_info["script"]
        full_command = ["python", str(script_path), "--vault-path", str(self.vault_path)] + command
        
        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out after 5 minutes"}
        except Exception as e:
            return {"error": f"Failed to run command: {e}"}
            
    def system_status(self) -> Dict[str, Any]:
        """Get status of all automation systems."""
        status = {
            "timestamp": datetime.now().isoformat(),
            "vault_path": str(self.vault_path),
            "systems": {}
        }
        
        for system_id, system_info in self.systems.items():
            status["systems"][system_id] = {
                "description": system_info["description"],
                "status": system_info["status"],
                "script": system_info["script"]
            }
            
        return status
        
    def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check on all systems."""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {}
        }
        
        checks = [
            ("validator", ["--vault-path", str(self.vault_path)], "Content validation check"),
            ("backup", ["list", "--limit", "5"], "Backup system check"),
            ("links", ["--report"], "Link analysis check"),
            ("quest_tracker", ["list"], "Quest tracking check")
        ]
        
        for system, command, description in checks:
            print(f"Running {description}...")
            result = self.run_command(system, command)
            
            health_report["checks"][system] = {
                "description": description,
                "success": result.get("success", False),
                "error": result.get("error", ""),
                "output_length": len(result.get("stdout", ""))
            }
            
            if not result.get("success", False):
                health_report["overall_status"] = "issues_detected"
                
        return health_report
        
    def initialize_vault_automation(self) -> Dict[str, Any]:
        """Initialize all automation systems for a vault."""
        print("Initializing vault automation systems...")
        
        initialization_steps = [
            ("Creating full backup", "backup", ["backup", "--type", "full"]),
            ("Running content validation", "validator", ["report"]), 
            ("Analyzing links", "links", ["--report"]),
            ("Checking quest states", "quest_tracker", ["list"]),
        ]
        
        results = []
        
        for step_name, system, command in initialization_steps:
            print(f"  {step_name}...")
            result = self.run_command(system, command)
            
            results.append({
                "step": step_name,
                "system": system,
                "success": result.get("success", False),
                "error": result.get("error", "")
            })
            
            if not result.get("success", False):
                print(f"    ⚠️ {step_name} had issues: {result.get('error', 'Unknown error')}")
            else:
                print(f"    ✅ {step_name} completed")
                
        success_count = sum(1 for r in results if r["success"])
        print(f"\nInitialization complete: {success_count}/{len(results)} steps successful")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_steps": len(results),
            "successful_steps": success_count,
            "results": results
        }
        
    def start_monitoring_services(self) -> Dict[str, Any]:
        """Start background monitoring services."""
        services = [
            ("Update notifications", "notifications", []),
            ("Backup scheduler", "backup", ["schedule"])
        ]
        
        started_services = []
        
        for service_name, system, command in services:
            print(f"Starting {service_name}...")
            
            # Start service in background
            script_path = self.scripts_path / self.systems[system]["script"]
            full_command = ["python", str(script_path), "--vault-path", str(self.vault_path)] + command
            
            try:
                process = subprocess.Popen(
                    full_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                started_services.append({
                    "name": service_name,
                    "system": system,
                    "pid": process.pid,
                    "command": " ".join(command)
                })
                
                print(f"  ✅ {service_name} started (PID: {process.pid})")
                
            except Exception as e:
                print(f"  ❌ Failed to start {service_name}: {e}")
                
        return {
            "timestamp": datetime.now().isoformat(),
            "started_services": started_services
        }
        
    def generate_sample_content(self, count: int = 3) -> Dict[str, Any]:
        """Generate sample content using available generators."""
        print(f"Generating {count} pieces of sample content...")
        
        generation_tasks = [
            ("NPCs", "random_generator", ["--type", "npc", "--count", str(count), "--realm", "Both"]),
            ("Encounters", "random_generator", ["--type", "encounter", "--count", str(count), "--realm", "Both"]),
            ("Loot Items", "random_generator", ["--type", "loot", "--count", str(count)])
        ]
        
        results = []
        
        for content_type, system, command in generation_tasks:
            print(f"  Generating {content_type}...")
            result = self.run_command(system, command)
            
            results.append({
                "type": content_type,
                "success": result.get("success", False),
                "output_length": len(result.get("stdout", "")),
                "error": result.get("error", "")
            })
            
            if result.get("success", False):
                print(f"    ✅ Generated {content_type}")
            else:
                print(f"    ❌ Failed to generate {content_type}: {result.get('error', 'Unknown error')}")
                
        return {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
    def run_maintenance(self) -> Dict[str, Any]:
        """Run comprehensive maintenance tasks."""
        print("Running vault maintenance...")
        
        maintenance_tasks = [
            ("Content validation", "validator", ["--auto-fix"]),
            ("Link suggestions", "links", ["--report"]),
            ("Backup cleanup", "backup", ["cleanup"]),
            ("Quest state sync", "quest_tracker", ["scan"])
        ]
        
        results = []
        
        for task_name, system, command in maintenance_tasks:
            print(f"  {task_name}...")
            result = self.run_command(system, command)
            
            results.append({
                "task": task_name,
                "success": result.get("success", False),
                "output": result.get("stdout", "")[:200] + "..." if len(result.get("stdout", "")) > 200 else result.get("stdout", ""),
                "error": result.get("error", "")
            })
            
            if result.get("success", False):
                print(f"    ✅ {task_name} completed")
            else:
                print(f"    ⚠️ {task_name} had issues")
                
        return {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
    def generate_automation_report(self) -> str:
        """Generate comprehensive automation status report."""
        status = self.system_status()
        
        lines = [
            "# Vault Automation Status Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Vault Path: {self.vault_path}",
            "",
            "## System Status",
            ""
        ]
        
        for system_id, system_info in status["systems"].items():
            status_icon = {
                "ready": "✅",
                "missing": "❌", 
                "available": "⚠️"
            }.get(system_info["status"], "❓")
            
            lines.append(f"- {status_icon} **{system_id.title()}**: {system_info['description']}")
            lines.append(f"  - Script: `{system_info['script']}`")
            lines.append(f"  - Status: {system_info['status']}")
            lines.append("")
            
        # Add quick start commands
        lines.extend([
            "## Quick Start Commands",
            "",
            "### Initialize Automation",
            "```bash",
            f"python {self.scripts_path}/automation_master.py --vault-path '{self.vault_path}' init",
            "```",
            "",
            "### Start Monitoring",
            "```bash", 
            f"python {self.scripts_path}/automation_master.py --vault-path '{self.vault_path}' monitor",
            "```",
            "",
            "### Run Health Check",
            "```bash",
            f"python {self.scripts_path}/automation_master.py --vault-path '{self.vault_path}' health",
            "```",
            "",
            "### Generate Content",
            "```bash",
            f"python {self.scripts_path}/automation_master.py --vault-path '{self.vault_path}' generate --count 5",
            "```",
            "",
            "### Run Maintenance",
            "```bash",
            f"python {self.scripts_path}/automation_master.py --vault-path '{self.vault_path}' maintenance",
            "```"
        ])
        
        return '\n'.join(lines)

def main():
    """Command-line interface for automation master."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vault Automation Master Control")
    parser.add_argument("--vault-path", default=".", help="Path to vault root")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show system status")
    
    # Health check command
    health_parser = subparsers.add_parser("health", help="Run health check")
    
    # Initialize command
    init_parser = subparsers.add_parser("init", help="Initialize vault automation")
    
    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Start monitoring services")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate sample content")
    generate_parser.add_argument("--count", type=int, default=3, help="Number of items to generate")
    
    # Maintenance command
    maintenance_parser = subparsers.add_parser("maintenance", help="Run maintenance tasks")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate automation report")
    
    # Run system command
    run_parser = subparsers.add_parser("run", help="Run specific system command")
    run_parser.add_argument("system", help="System to run")
    run_parser.add_argument("args", nargs="*", help="Command arguments")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    master = AutomationMaster(args.vault_path)
    
    if args.command == "status":
        status = master.system_status()
        
        print("Vault Automation Systems Status")
        print("=" * 40)
        
        for system_id, system_info in status["systems"].items():
            status_icon = {
                "ready": "✅",
                "missing": "❌",
                "available": "⚠️"
            }.get(system_info["status"], "❓")
            
            print(f"{status_icon} {system_id.ljust(15)} - {system_info['description']}")
            
    elif args.command == "health":
        health_report = master.run_health_check()
        
        print(f"\nHealth Check Results: {health_report['overall_status'].upper()}")
        print("=" * 50)
        
        for system, check_info in health_report["checks"].items():
            status_icon = "✅" if check_info["success"] else "❌"
            print(f"{status_icon} {system}: {check_info['description']}")
            
            if check_info["error"]:
                print(f"   Error: {check_info['error']}")
                
    elif args.command == "init":
        result = master.initialize_vault_automation()
        print(f"\nInitialization Summary: {result['successful_steps']}/{result['total_steps']} successful")
        
    elif args.command == "monitor":
        result = master.start_monitoring_services()
        print(f"\nStarted {len(result['started_services'])} monitoring services")
        print("Services are running in background. Use 'ps aux | grep python' to see processes.")
        
    elif args.command == "generate":
        result = master.generate_sample_content(args.count)
        successful = sum(1 for r in result["results"] if r["success"])
        print(f"\nGeneration Summary: {successful}/{len(result['results'])} types successful")
        
    elif args.command == "maintenance":
        result = master.run_maintenance()
        successful = sum(1 for r in result["results"] if r["success"])
        print(f"\nMaintenance Summary: {successful}/{len(result['results'])} tasks successful")
        
    elif args.command == "report":
        report = master.generate_automation_report()
        
        report_path = Path(args.vault_path) / f"automation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        
        print(f"Automation report generated: {report_path}")
        print()
        print(report[:1000] + "..." if len(report) > 1000 else report)
        
    elif args.command == "run":
        result = master.run_command(args.system, args.args)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            if result.get("success", False):
                print("Command executed successfully")
            else:
                print(f"Command failed with return code: {result.get('returncode', 'unknown')}")
                
            if result.get("stdout"):
                print("\nOutput:")
                print(result["stdout"])
                
            if result.get("stderr"):
                print("\nErrors:")
                print(result["stderr"])

if __name__ == "__main__":
    main()