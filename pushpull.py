#!/usr/bin/env python3
import subprocess
import sys
import os
from datetime import datetime

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def get_smart_commit_message():
    """Generate a smart commit message based on changed files"""
    success, stdout, stderr = run_command("git diff --name-only --cached")
    if not success:
        return f"Update sportsbot workspace - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    changed_files = stdout.strip().split('\n') if stdout.strip() else []

    # Categorize changes
    sports_files = [f for f in changed_files if any(sport in f.lower() for sport in ['nfl', 'mlb', 'nba', 'nhl', 'cfb', 'soccer'])]
    data_files = [f for f in changed_files if 'data' in f.lower() or 'mapping' in f.lower()]
    script_files = [f for f in changed_files if f.endswith('.py')]
    config_files = [f for f in changed_files if any(cfg in f.lower() for cfg in ['.env', 'config', 'claude.md'])]

    if sports_files:
        sports = list(set([sport for f in sports_files for sport in ['NFL', 'MLB', 'NBA', 'NHL', 'CFB', 'Soccer'] if sport.lower() in f.lower()]))
        return f"Update {', '.join(sports)} sports data and scripts"
    elif data_files:
        return "Update sports data mappings and configurations"
    elif script_files:
        return "Update Python scripts and utilities"
    elif config_files:
        return "Update project configuration"
    else:
        return f"Update sportsbot workspace - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

def git_status():
    """Check git status"""
    success, stdout, stderr = run_command("git status --porcelain")
    if success:
        return stdout.strip() != ""
    return False

def git_pull(branch="main"):
    """Pull from specified branch"""
    print(f"Pulling from {branch} branch...")
    success, stdout, stderr = run_command(f"git pull origin {branch}")
    if success:
        print("Pull successful!")
        print(stdout)
    else:
        print("Pull failed!")
        print(stderr)
    return success

def git_push(branch="main"):
    """Push to specified branch"""
    # Check if there are uncommitted changes first
    has_changes = git_status()
    
    if has_changes:
        print("Changes detected. Adding and committing files...")
        
        # Add all changes
        success, stdout, stderr = run_command("git add .")
        if not success:
            print("Failed to add files!")
            print(stderr)
            return False
        
        # Get commit message with better context
        commit_msg = get_smart_commit_message()
        success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"')
        if not success:
            print("Failed to commit changes!")
            print(stderr)
            return False
        
        print(f"Changes committed with message: '{commit_msg}'")
    
    # Try to push first - if it fails due to being behind, we'll pull and push again
    print(f"Attempting to push to {branch} branch...")
    success, stdout, stderr = run_command(f"git push origin {branch}")
    
    if success:
        print("Push successful!")
        print(stdout)
        return True
    
    # If push failed, check if it's because we're behind the remote
    if "fetch first" in stderr or "rejected" in stderr:
        print("Push rejected - remote has newer commits. Pulling and merging...")
        
        # Pull with rebase to maintain clean history
        success, stdout, stderr = run_command(f"git pull --rebase origin {branch}")
        if not success:
            print("Failed to pull and rebase!")
            print(stderr)
            print("You may need to resolve conflicts manually.")
            return False
        
        print("Successfully pulled and rebased. Attempting push again...")
        
        # Try push again after rebase
        success, stdout, stderr = run_command(f"git push origin {branch}")
        if success:
            print("Push successful!")
            print(stdout)
        else:
            print("Push failed even after pull!")
            print(stderr)
        
        return success
    else:
        print("Push failed for unknown reason!")
        print(stderr)
        return False

def promote_to_production():
    """Promote main branch to production-stable with manual confirmation"""
    print("PRODUCTION DEPLOYMENT")
    print("=" * 40)
    print("This will update production-stable branch with current main branch.")
    print("WARNING: This affects your live Discord bot and MCP servers!")
    print()
    
    # Show current branch status
    success, stdout, stderr = run_command("git branch --show-current")
    if success:
        current_branch = stdout.strip()
        print(f"Current branch: {current_branch}")
    
    # Show what will be deployed
    success, stdout, stderr = run_command("git log --oneline -5")
    if success:
        print("\nRecent commits on main:")
        print(stdout)
    
    print("\n" + "="*40)
    confirmation = input("Type 'DEPLOY TO PRODUCTION' to confirm: ").strip()
    
    if confirmation != "DEPLOY TO PRODUCTION":
        print("Deployment cancelled!")
        return False
    
    print("\nStarting production deployment...")
    
    # Switch to production-stable branch
    success, stdout, stderr = run_command("git checkout production-stable")
    if not success:
        print("Failed to switch to production-stable!")
        print(stderr)
        return False
    
    # Merge main into production-stable
    success, stdout, stderr = run_command("git merge main")
    if not success:
        print("Failed to merge main into production-stable!")
        print(stderr)
        return False
    
    # Push to remote
    success, stdout, stderr = run_command("git push origin production-stable")
    if not success:
        print("Failed to push production-stable!")
        print(stderr)
        return False
    
    # Switch back to main
    success, stdout, stderr = run_command("git checkout main")
    
    print("PRODUCTION DEPLOYMENT SUCCESSFUL!")
    print("production-stable branch updated with latest main")
    return True

def backup_sports_data():
    """Create backup of critical sports data before major operations"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Check if data directories exist
    data_dirs = ["data", "mapping", "new/mapping_backup*"]
    backup_needed = False

    for pattern in data_dirs:
        success, stdout, stderr = run_command(f'find . -name "{pattern}" -type d 2>/dev/null || dir /s /b *{pattern.replace("*", "")}* 2>nul')
        if success and stdout.strip():
            backup_needed = True
            break

    if backup_needed:
        print(f"Creating sports data backup: backup_{timestamp}")
        run_command(f"mkdir -p backup_{timestamp}")
        run_command(f"cp -r data backup_{timestamp}/ 2>/dev/null || xcopy /e /i data backup_{timestamp}\\data\\ >nul 2>&1")
        run_command(f"cp -r mapping backup_{timestamp}/ 2>/dev/null || xcopy /e /i mapping backup_{timestamp}\\mapping\\ >nul 2>&1")
        print("Backup created successfully!")

    return backup_needed

def main():
    print("SportsBot Git Helper")
    print("===================")
    print("🏈 Sports Data Management Tool")

    while True:
        print("\nChoose an option:")
        print("1. Pull from main branch")
        print("2. Push to main branch (with smart sports commit)")
        print("3. Pull from production-stable")
        print("4. DEPLOY to production-stable (with confirmation)")
        print("5. Check git status")
        print("6. Backup sports data before major changes")
        print("7. Quick status check (files + recent commits)")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            git_pull("main")
            print("\nOperation completed. Press Enter to exit...")
            input()
            sys.exit(0)
        elif choice == "2":
            git_push("main")
            print("\nOperation completed. Press Enter to exit...")
            input()
            sys.exit(0)
        elif choice == "3":
            git_pull("production-stable")
            print("\nOperation completed. Press Enter to exit...")
            input()
            sys.exit(0)
        elif choice == "4":
            promote_to_production()
            print("\nOperation completed. Press Enter to exit...")
            input()
            sys.exit(0)
        elif choice == "5":
            success, stdout, stderr = run_command("git status")
            if success:
                print(stdout)
            else:
                print("Failed to get git status!")
                print(stderr)
            print("\nStatus check completed. Press Enter to exit...")
            input()
            sys.exit(0)
        elif choice == "6":
            backup_sports_data()
            print("\nBackup completed. Press Enter to exit...")
            input()
            sys.exit(0)
        elif choice == "7":
            print("\n🔍 QUICK STATUS CHECK")
            print("=" * 30)

            # Show modified files
            success, stdout, stderr = run_command("git status --porcelain")
            if success and stdout.strip():
                print("📝 Modified files:")
                for line in stdout.strip().split('\n'):
                    print(f"   {line}")
            else:
                print("✅ No modified files")

            print()

            # Show recent commits
            success, stdout, stderr = run_command("git log --oneline -5")
            if success:
                print("📊 Recent commits:")
                print(stdout)

            print("\nQuick check completed. Press Enter to exit...")
            input()
            sys.exit(0)
        elif choice == "8":
            print("Goodbye! 🏈")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()
