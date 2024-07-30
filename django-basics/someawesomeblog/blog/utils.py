def get_dict_with_reactions_count(post, reaction_types):
    reaction_counts = {}
    for reaction in reaction_types:
        reaction_counts[reaction] = post.get_reaction_count(reaction)
    
    return reaction_counts
