import os
import frontmatter
import datetime
# Sample frontmatter
# ---
# layout: ../layouts/BlogPost.astro
# title: Hello, world!
# slug: hello-world
# description: >-
#   This is an example blog!
# tags:
#   - personal
# added: "May 01 2024"
# ---

# Existing frontmatter

# title: Airflow Operators - A Comparison
# sub_title: Comparison between Python, Docker and Kubernetes Airflow Operator
# slug: airflow-operators-comparison
# tags:
#   - apache-airflow
# featuredImgPath: https://i.imgur.com/UvlPSAW.png
# isexternal: true
# published_date: '2021-01-12'
# created_date: '2021-01-10'
# draft: false
# description: >-
#   Airflow provides a variety of operators to couple your business logic into
#   executable tasks in a workflow. Often times it is confusing to decide when to
#   use what. In this article we will discuss the p

import subprocess
from datetime import datetime

import re

def extract_h1_title(markdown_file_path):
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Match the line that starts with a single '#' followed by a space
            match = re.match(r'^# (.*)', line)
            if match:
                return match.group(1)
    return None


def get_file_creation_time(repo_path, file_path):
    # Move to the repository path
    command = ["git", "log", "--diff-filter=A", "--follow", "--format=%ct", "--", file_path]
    
    result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)
    
    # Get the first commit timestamp
    timestamps = result.stdout.strip().splitlines()
    
    if not timestamps:
        raise FileNotFoundError(f"File {file_path} does not exist in the repository.")
    
    # The earliest timestamp is the file creation time
    creation_timestamp = int(timestamps[-1])
    creation_time = datetime.fromtimestamp(creation_timestamp)
    
    return creation_time


posts_path = '/Users/bhavaniravi/projects/til'

# walk the folder and find markdown files at all level

def get_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith(".md")]:
            yield os.path.join(dirpath, filename)
        
mapping = {
    'published_date': 'added',
    'featuredImgPath': 'image',
    'draft': 'draft',
    'sub_title': 'description',
}

# mapping = {
#     'added': 'published_date',
#     'image': 'featuredImgPath',
#     'draft': 'draft',
#     'description': 'sub_title',
# }

def construct_default_metadata(file):
    metadata = {}
    metadata['title'] = extract_h1_title(file)
    metadata['layout'] = '../layouts/BlogPost.astro'
    metadata['slug'] = file.split('/')[-1].split('.')[0]
    metadata['description'] = None
    metadata['tags'] = [file.split('/')[-2]]
    file_created_date = get_file_creation_time(posts_path, file)
    # format = "May 01 2024"
    metadata['added'] = file_created_date.strftime("%b %d %Y")
    return metadata


required_metadata = ['title', 'layout', 'slug', 'description', 'tags', 'added']

def map_existing_metadata(metadata):
    default_metadata = construct_default_metadata(file)
    for key in required_metadata:
        if key not in metadata:
            if key in mapping:
                metadata[key] = metadata[mapping[key]]
            else:
                metadata[key] = default_metadata[key]
    return metadata
        

for dirs in os.listdir(posts_path):
    for file in get_files(f"{posts_path}/{dirs}"):
        print (file)
        # airflow-operators-comparison.md
        front_matter = frontmatter.load(file)
        if not front_matter.metadata:
            front_matter.metadata = construct_default_metadata(file)
            frontmatter.dump(front_matter, file)
        # else:
        #     front_matter.metadata = map_existing_metadata(front_matter.metadata)

        
        # if not frontmatter.get('title'):
        #     print(f"Adding title to {file}")
        #     frontmatter['title'] = file.split('/')[-1].split('.')[0]
        # if not frontmatter.get('layout'):
        #     print(f"Adding layout to {file}")
        #     frontmatter['layout'] = '../layouts/BlogPost.astro'
        # if not frontmatter.get('slug'):
        #     print(f"Adding slug to {file}")
        #     frontmatter['slug'] = file.split('/')[-1].split('.')[0]
        # if not frontmatter.get('description'):
        #     print(f"Adding description to {file}")
        #     frontmatter['description'] = file.seek(0, 100)
        # if not frontmatter.get('tags'):
        #     print(f"Adding tags to {file}")
        #     dir_name = file.split('/')[-2]
        #     frontmatter['tags'] = dir_name
        # if frontmatter.get('published_date'):
        #     print(f"Adding added to {file}")
        #   frontmatter['added'] = "May 01 2024"