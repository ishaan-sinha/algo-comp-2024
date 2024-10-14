import random

import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    N = len(scores)


    def is_compatible(proposer_id, receiver_id):
        proposer_gender = gender_id[proposer_id]
        receiver_gender = gender_id[receiver_id]
        proposer_pref = gender_pref[proposer_id]
        receiver_pref = gender_pref[receiver_id]

        if proposer_gender=="Male":
            if proposer_pref=="Women" and receiver_gender=="Female" and receiver_pref=="Men":
                return True
            if proposer_pref=="Men" and receiver_gender=="Male" and receiver_pref!="Women":
                return True
            if proposer_pref=="Bisexual" and (receiver_pref=="Bisexual" or receiver_pref==proposer_gender):
                return True
        elif proposer_gender=="Female":
            if proposer_pref=="Men" and receiver_gender=="Male" and receiver_pref=="Women":
                return True
            if proposer_pref=="Women" and receiver_gender=="Female" and receiver_pref!="Male":
                return True
            if proposer_pref=="Bisexual" and (receiver_pref=="Bisexual" or receiver_pref==proposer_gender):
                return True
        elif proposer_gender=="Nonbinary":
            if receiver_pref=="Bisexual":
                return True
        return False

    for i in range(N):
        for j in range(N):
            if not is_compatible(i, j):
                scores[i][j] = 0

    proposers = random.sample(range(N), N//2)
    receivers = list(set(range(N)) - set(proposers))

    proposer_prefs = {p: sorted(range(N), key=lambda x: scores[p][x], reverse=True) for p in proposers}
    receiver_prefs = {r: sorted(range(N), key=lambda x: scores[x][r], reverse=True) for r in receivers}

    free_proposers = proposers[:]
    matches = {}
    proposed = {p: [] for p in proposers}

    while free_proposers:
        proposer = free_proposers.pop(0)
        receiver = proposer_prefs[proposer].pop(0)
        if receiver not in matches:
            matches[receiver] = proposer
        else:
            current_match = matches[receiver]
            if receiver_prefs[receiver].index(proposer) < receiver_prefs[receiver].index(current_match):
                matches[receiver] = proposer
                free_proposers.append(current_match)
            else:
                free_proposers.append(proposer)

    matches = [(proposer, receiver) for receiver, proposer in matches.items()]
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
    print(gs_matches)
