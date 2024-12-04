import subprocess
import os
import unittest

def run_tests():
    result = subprocess.run(['python', '-m', 'unittest', 'discover'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Tests failed")
    else:
        print("Tests passed.")

def build_and_push_docker_image(image_name):
    subprocess.run(['docker', 'build', '-t', image_name, '.'], check=True)
    subprocess.run(['docker', 'push', image_name], check=True)
    print(f"Docker image {image_name} pushed successfully.")

def main():
    repo_url = "https://github.com/your-repo/project.git"
    image_name = "yourdockerhubuser/project:latest"
    
    # Clone the GitHub repository
    subprocess.run(['git', 'clone', repo_url], check=True)
    
    # Navigate to the project directory
    project_dir = repo_url.split('/')[-1].replace('.git', '')
    os.chdir(project_dir)
    
    try:
        # Run unit tests
        run_tests()
        
        # Build and push Docker image
        build_and_push_docker_image(image_name)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

# Run the pipeline
main()
