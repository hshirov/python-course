import re

def get_dict_with_reactions_count(post, reaction_types):
    reaction_counts = {}
    for reaction in reaction_types:
        reaction_counts[reaction] = post.get_reaction_count(reaction)
    
    return reaction_counts

def extract_hashtags(text):
    """Extracts all hashtags from a string and returns them in a list."""
    hashtags = re.findall(r'#(\w+)', text)
    return hashtags