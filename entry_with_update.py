import os
import sys

# Set the root to the directory containing this script
root = os.path.dirname(os.path.abspath(__file__))
# Add this directory to the system path so that modules from this directory can be imported
sys.path.append(root)
# Change the current working directory to the root
os.chdir(root)

try:
    # Import the pygit2 library
    import pygit2
    # Set a Git option for owner validation to 0 (disabling it)
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    # Open the Git repository located in the directory of this script
    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    # Get the name of the current branch
    branch_name = repo.head.shorthand

    # Define the name of the remote repository (commonly "origin" for the primary remote)
    remote_name = 'origin'
    # Get the remote object using the name
    remote = repo.remotes[remote_name]

    # Fetch the latest changes from the remote
    remote.fetch()

    # Construct a string for the local branch reference
    local_branch_ref = f'refs/heads/{branch_name}'
    # Get the reference object for the local branch
    local_branch = repo.lookup_reference(local_branch_ref)

    # Construct a string for the remote branch reference
    remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
    # Get the commit object for the remote branch
    remote_commit = repo.revparse_single(remote_reference)

    # Analyze the merge possibilities with the fetched remote commit
    merge_result, _ = repo.merge_analysis(remote_commit.id)

    # Check merge possibilities and perform appropriate actions
    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        # No updates needed - the local branch is up-to-date with the remote
        print("Already up-to-date")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        # A fast-forward merge is possible. This means the local branch is behind the remote, 
        # but there are no diverging changes.
        local_branch.set_target(remote_commit.id)       # Update the local branch reference to the remote commit
        repo.head.set_target(remote_commit.id)          # Update HEAD to point to the remote commit
        repo.checkout_tree(repo.get(remote_commit.id))  # Checkout the contents of the remote commit
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD) # Reset the working directory and index
        print("Fast-forward merge")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        # A merge is needed, which means both local and remote branches have diverged. 
        # This script doesn't handle this scenario, but it notifies the user.
        print("Update failed - Did you modified any file?")
        
except Exception as e:
    # If any exception occurs during the Git operations, notify the user
    print('Update failed.')
    print(str(e))
else:
    # This block will execute if no exceptions occurred inside the try block
    print('Update succeeded.')
    
    # It appears to run a script or module named 'launch' after updating. 
    # Details of what this does are not present in the provided code.
    from launch import *
