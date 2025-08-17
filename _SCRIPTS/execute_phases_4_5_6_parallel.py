#!/usr/bin/env python3
"""
Master Executor for Phases 4-6 of Vault Improvement
Runs Phase 4 (Metadata Enhancement), Phase 5 (Database Creation), and Phase 6 (Automation Setup) in parallel
"""

import os
import sys
import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

# Add the scripts directory to Python path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

# Import phase modules
from phase_4_metadata_enhancement import MetadataEnhancer
from phase_5_database_creation import DatabaseCreator
from phase_6_automation_setup import AutomationSetup

class PhaseExecutor:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.start_time = datetime.now(timezone.utc)
        self.results = {}
        self.progress = {
            'phase_4': {'status': 'pending', 'progress': 0, 'improvements': []},
            'phase_5': {'status': 'pending', 'progress': 0, 'improvements': []},
            'phase_6': {'status': 'pending', 'progress': 0, 'improvements': []}
        }
        
    def execute_phase_4(self) -> Dict[str, Any]:
        """Execute Phase 4: Metadata Enhancement"""
        try:
            print("🎯 Starting Phase 4: Metadata Enhancement")
            self.progress['phase_4']['status'] = 'running'
            
            enhancer = MetadataEnhancer(str(self.vault_path))
            improvements = enhancer.run_phase_4()
            
            self.progress['phase_4']['status'] = 'completed'
            self.progress['phase_4']['progress'] = 100
            self.progress['phase_4']['improvements'] = improvements
            
            return {
                'phase': 4,
                'status': 'success',
                'improvements': improvements,
                'steps_completed': enhancer.steps_completed,
                'duration': str(datetime.now(timezone.utc) - self.start_time)
            }
            
        except Exception as e:
            self.progress['phase_4']['status'] = 'failed'
            print(f"❌ Phase 4 failed: {e}")
            return {
                'phase': 4,
                'status': 'failed',
                'error': str(e),
                'improvements': [],
                'steps_completed': 0
            }

    def execute_phase_5(self) -> Dict[str, Any]:
        """Execute Phase 5: Database Creation"""
        try:
            print("🗄️ Starting Phase 5: Database Creation")
            self.progress['phase_5']['status'] = 'running'
            
            creator = DatabaseCreator(str(self.vault_path))
            improvements = creator.run_phase_5()
            
            self.progress['phase_5']['status'] = 'completed'
            self.progress['phase_5']['progress'] = 100
            self.progress['phase_5']['improvements'] = improvements
            
            return {
                'phase': 5,
                'status': 'success',
                'improvements': improvements,
                'steps_completed': creator.steps_completed,
                'duration': str(datetime.now(timezone.utc) - self.start_time)
            }
            
        except Exception as e:
            self.progress['phase_5']['status'] = 'failed'
            print(f"❌ Phase 5 failed: {e}")
            return {
                'phase': 5,
                'status': 'failed',
                'error': str(e),
                'improvements': [],
                'steps_completed': 0
            }

    def execute_phase_6(self) -> Dict[str, Any]:
        """Execute Phase 6: Automation Setup"""
        try:
            print("⚙️ Starting Phase 6: Automation Setup")
            self.progress['phase_6']['status'] = 'running'
            
            automation = AutomationSetup(str(self.vault_path))
            improvements = automation.run_phase_6()
            
            self.progress['phase_6']['status'] = 'completed'
            self.progress['phase_6']['progress'] = 100
            self.progress['phase_6']['improvements'] = improvements
            
            return {
                'phase': 6,
                'status': 'success',
                'improvements': improvements,
                'steps_completed': automation.steps_completed,
                'duration': str(datetime.now(timezone.utc) - self.start_time)
            }
            
        except Exception as e:
            self.progress['phase_6']['status'] = 'failed'
            print(f"❌ Phase 6 failed: {e}")
            return {
                'phase': 6,
                'status': 'failed',
                'error': str(e),
                'improvements': [],
                'steps_completed': 0
            }

    def run_parallel_execution(self) -> Dict[str, Any]:
        """Run all three phases in parallel"""
        print("🚀 Starting Parallel Execution of Phases 4-6")
        print("=" * 60)
        
        # Create thread pool for parallel execution
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all phase tasks
            future_to_phase = {
                executor.submit(self.execute_phase_4): 'phase_4',
                executor.submit(self.execute_phase_5): 'phase_5',
                executor.submit(self.execute_phase_6): 'phase_6'
            }
            
            # Monitor progress
            self.monitor_progress(future_to_phase)
            
            # Collect results as they complete
            for future in as_completed(future_to_phase):
                phase_name = future_to_phase[future]
                try:
                    result = future.result()
                    self.results[phase_name] = result
                    print(f"✅ {phase_name.replace('_', ' ').title()} completed successfully")
                except Exception as e:
                    self.results[phase_name] = {
                        'phase': phase_name,
                        'status': 'failed',
                        'error': str(e)
                    }
                    print(f"❌ {phase_name.replace('_', ' ').title()} failed: {e}")
        
        return self.generate_final_report()

    def monitor_progress(self, future_to_phase: Dict) -> None:
        """Monitor and display progress of all phases"""
        monitoring_thread = threading.Thread(target=self._progress_monitor, daemon=True)
        monitoring_thread.start()

    def _progress_monitor(self) -> None:
        """Background thread to monitor progress"""
        while True:
            all_completed = all(
                status['status'] in ['completed', 'failed'] 
                for status in self.progress.values()
            )
            
            if all_completed:
                break
            
            # Print progress update
            self._print_progress_update()
            time.sleep(5)  # Update every 5 seconds

    def _print_progress_update(self) -> None:
        """Print current progress of all phases"""
        print("\n📊 Progress Update:")
        for phase_name, progress in self.progress.items():
            status_icon = {
                'pending': '⏳',
                'running': '🔄',
                'completed': '✅',
                'failed': '❌'
            }.get(progress['status'], '❓')
            
            improvement_count = len(progress['improvements'])
            print(f"  {status_icon} {phase_name.replace('_', ' ').title()}: {progress['status']} ({improvement_count} improvements)")

    def generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        end_time = datetime.now(timezone.utc)
        total_duration = end_time - self.start_time
        
        # Aggregate results
        total_improvements = 0
        total_steps = 0
        successful_phases = 0
        failed_phases = 0
        
        for phase_name, result in self.results.items():
            if result['status'] == 'success':
                successful_phases += 1
                total_improvements += len(result.get('improvements', []))
                total_steps += result.get('steps_completed', 0)
            else:
                failed_phases += 1
        
        # Create comprehensive report
        report = {
            'execution_summary': {
                'start_time': self.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'total_duration': str(total_duration),
                'successful_phases': successful_phases,
                'failed_phases': failed_phases,
                'total_improvements': total_improvements,
                'total_steps_completed': total_steps
            },
            'phase_results': self.results,
            'improvements_by_phase': {
                'phase_4_metadata': len(self.results.get('phase_4', {}).get('improvements', [])),
                'phase_5_database': len(self.results.get('phase_5', {}).get('improvements', [])),
                'phase_6_automation': len(self.results.get('phase_6', {}).get('improvements', []))
            },
            'files_created': [
                '_METADATA/vault_metadata.db',
                '_METADATA/vault_database.db',
                '_METADATA/tag_taxonomy.json',
                '_METADATA/npc_relationship_analysis.json',
                '_METADATA/location_hierarchy.json',
                '_METADATA/faction_network_analysis.json',
                '_METADATA/campaign_timeline.json',
                '_METADATA/relationship_graphs.json',
                '.obsidian/snippets/',
                '.obsidian/workspaces/',
                '_SCRIPTS/automation/',
                '00_System/Templates/Quick_Capture/',
                '00_System/Quick_Capture_Inbox/'
            ],
            'features_implemented': [
                'Standardized frontmatter across vault',
                'Comprehensive tag taxonomy',
                'CSS snippets for enhanced visualization',
                'Complete NPC relationship database',
                'Hierarchical location mapping',
                'Item and spell cataloging',
                'Faction network analysis',
                'Timeline and event tracking',
                'Quest interconnection mapping',
                'Session data indexing',
                'Daily notes automation',
                'Quick capture system',
                'Auto-linking between content',
                'Template triggers',
                'Optimized hotkeys',
                'Workspace layouts',
                'Smart bookmarks',
                'Content generators',
                'Maintenance automation'
            ],
            'next_steps': [
                'Run the automation scripts regularly',
                'Use the quick capture system during sessions',
                'Explore the database with SQL queries',
                'Customize CSS snippets for your preferences',
                'Set up cron jobs for maintenance',
                'Import data into the relationship graphs',
                'Create custom workspaces for different activities'
            ]
        }
        
        # Save comprehensive report
        report_file = self.vault_path / "_SCRIPTS" / f"phases_4_5_6_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.write_text(json.dumps(report, indent=2))
        
        # Print final summary
        self.print_final_summary(report, report_file)
        
        return report

    def print_final_summary(self, report: Dict[str, Any], report_file: Path) -> None:
        """Print final execution summary"""
        print("\n" + "=" * 80)
        print("🎉 PHASES 4-6 EXECUTION COMPLETE!")
        print("=" * 80)
        
        summary = report['execution_summary']
        print(f"⏱️  Total Duration: {summary['total_duration']}")
        print(f"✅ Successful Phases: {summary['successful_phases']}/3")
        print(f"📈 Total Improvements: {summary['total_improvements']}")
        print(f"🎯 Total Steps Completed: {summary['total_steps_completed']}")
        
        if summary['failed_phases'] > 0:
            print(f"❌ Failed Phases: {summary['failed_phases']}")
        
        print("\n📊 Improvements by Phase:")
        improvements = report['improvements_by_phase']
        print(f"  🎯 Phase 4 (Metadata): {improvements['phase_4_metadata']} improvements")
        print(f"  🗄️ Phase 5 (Database): {improvements['phase_5_database']} improvements")
        print(f"  ⚙️ Phase 6 (Automation): {improvements['phase_6_automation']} improvements")
        
        print("\n🎁 Key Features Implemented:")
        for feature in report['features_implemented'][:10]:  # Show first 10
            print(f"  ✨ {feature}")
        if len(report['features_implemented']) > 10:
            print(f"  ... and {len(report['features_implemented']) - 10} more features!")
        
        print(f"\n📋 Detailed report saved to:")
        print(f"   {report_file}")
        
        print("\n🚀 Your vault is now supercharged with:")
        print("  • Comprehensive metadata system")
        print("  • Relationship databases")
        print("  • Automation tools")
        print("  • Enhanced visualization")
        print("  • Quick capture workflows")
        
        print("\n" + "=" * 80)

def main():
    """Main execution function"""
    vault_path = Path(__file__).parent.parent
    
    print("🎲 Obsidian TTRPG Vault Enhancement")
    print("🚀 Executing Phases 4-6 in Parallel")
    print(f"📁 Vault Path: {vault_path}")
    print(f"🕐 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create backup before starting
    print("\n💾 Creating backup before enhancement...")
    backup_path = vault_path.parent / "Vault_Backups" / f"pre_phases_4_5_6_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        import shutil
        shutil.copytree(vault_path, backup_path, ignore=shutil.ignore_patterns('.DS_Store', 'Vault_Backups'))
        print(f"✅ Backup created: {backup_path}")
    except Exception as e:
        print(f"⚠️ Backup creation failed: {e}")
        response = input("Continue without backup? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Execute phases
    executor = PhaseExecutor(str(vault_path))
    final_report = executor.run_parallel_execution()
    
    print("\n🎉 All phases completed! Check the reports for detailed results.")

if __name__ == "__main__":
    main()