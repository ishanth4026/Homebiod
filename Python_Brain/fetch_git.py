import subprocess
import os
import re

def get_git_stats(repo_path):
    """
    Fetches the status of a single Git repository, including cloud updates,
    and breaks down file modifications into staged and unstaged categories.
    """
    project_name = os.path.basename(os.path.abspath(repo_path))
    
    stats = {
        "name": project_name,
        "branch": "Unknown",
        "unpushed": 0,
        "unpulled": 0,
        "staged": 0,      # Ready to be committed
        "unstaged": 0,    # Modified or Untracked, not yet staged
        "error": None
    }

    try:
        # 1. The Reconnaissance Mission
        subprocess.run(
            ["git", "fetch"],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
            check=False 
        )
        
        # 2. Check the local status
        result = subprocess.run(
            ["git", "status", "--porcelain=v1", "-b"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.split('\n')
        
        for line in lines:
            if not line: # Skip empty lines
                continue 
            
            # Parse Branch and Commits
            if line.startswith('##'):
                stats['branch'] = line[3:].split('...')[0].strip()
                
                ahead_match = re.search(r'ahead (\d+)', line)
                if ahead_match:
                    stats['unpushed'] = int(ahead_match.group(1))
                    
                behind_match = re.search(r'behind (\d+)', line)
                if behind_match:
                    stats['unpulled'] = int(behind_match.group(1))
            
            # Parse Staged vs Unstaged Files
            else:
                # Porcelain output guarantees the first two characters represent the status
                x = line[0] # The Index (Staged)
                y = line[1] # The Working Tree (Unstaged)

                # If X is M (Modified), A (Added), D (Deleted), R (Renamed), or C (Copied)
                if x in 'MADRC':
                    stats['staged'] += 1
                
                # If Y is M or D, or if the file is completely untracked (??)
                if y in 'MD' or x == '?':
                    stats['unstaged'] += 1

        return stats

    except subprocess.CalledProcessError:
        stats["error"] = "Not a valid Git repo."
        return stats
    except Exception as e:
        stats["error"] = f"Error: {e}"
        return stats

def get_all_projects_stats(repo_paths):
    results = []
    for path in repo_paths:
        results.append(get_git_stats(path))
    return results

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Testing Staged vs Unstaged Git Fetcher...")
    
    target_projects = ["."]
    all_stats = get_all_projects_stats(target_projects)
    
    for project_stat in all_stats:
        print(project_stat)