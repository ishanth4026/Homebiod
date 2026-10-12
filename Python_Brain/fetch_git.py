import subprocess

def get_git_stats(repo_path="."):
    """
    Fetches the current status of a Git repository.
    Returns a dictionary with branch name, unpushed commits, and modified files.
    """
    stats = {
        "branch": "Unknown",
        "unpushed_commits": 0,
        "modified_files": 0,
        "error": None
    }

    try:
        # We removed the strict os.path.exists check!
        # Now we just run the command and let Git's native folder-searching take over.
        result = subprocess.run(
            ["git", "status", "--porcelain=v1", "-b"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.split('\n')
        
        for line in lines:
            if not line.strip():
                continue 
            
            if line.startswith('##'):
                stats['branch'] = line[3:].split('...')[0].strip()
                
                if '[ahead' in line:
                    # Extract the number of unpushed commits
                    # We add .split(',')[0] just in case it says "[ahead 2, behind 1]"
                    part = line.split('[ahead ')[1]
                    stats['unpushed_commits'] = int(part.replace(']', '').split(',')[0])
            
            else:
                stats['modified_files'] += 1

        return stats

    except subprocess.CalledProcessError:
        # If Git searches all the way to the top of your hard drive and still
        # can't find a .git folder, it will crash. We catch that crash here safely.
        stats["error"] = "Not inside a Git repository."
        return stats
    except FileNotFoundError:
        stats["error"] = "Git is not installed or not in PATH."
        return stats

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Testing Git Fetcher...")
    
    current_repo_stats = get_git_stats(".")
    print(f"Stats: {current_repo_stats}")