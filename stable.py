# Author: Emily Su
# Last Revised: February 2022

import prompt
import goody

match = 0   # Index 0 of list associated with name is match (str)
prefs = 1   # Index 1 of list associated with name is preference (list of str)
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    '''Reads a file of men and women and their preferences (from highest to lowest preference) for members of the opposite gender.
    Parameter:
    open_file (file object): open text file
    
    Return:
    pref_dict (dict): key (str) is a man/woman; value (list) contains the man/woman's match, initially None, and (nested list) their preferences 
    '''
    pref_dict = {}
    line_list = [line.rstrip('\n') for line in open_file]
    
    for p in line_list:
        person = p.split(';') 
        pref_dict[person[match]] = [None, list()]
        
        for i in range(1, len(person)):
            pref_dict[person[match]][prefs].append(person[i])
            
    return pref_dict


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    '''Returns a printed representation of the dictionary of men/women and their match and preferences.
    Parameters:
    d (dict): key (str) is a man/woman; value (list) contains the man/woman's match, initially None, and (nested list) their preferences
    key (callable function): ordering of printed dictionary
    reverse (bool): True/False to determine whether or not to reverse sorting 
    '''
    pref_str = ''
    
    for person in sorted(d, key=key, reverse=reverse):
        pref_str += '  ' + str(person) + ' -> ' + str(d[person]) + '\n'
        
    return pref_str
         

def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    '''Returns the person (p1 or p2) who is of higher preference in the preference list (order).
    Parameters:
    order (list of strs): list of a person's preferences
    p1 (str): person 1 to compare
    p2 (str): person 2 to compare
    '''
    p1_index = order.index(p1)
    p2_index = order.index(p2)
    
    if p1_index < p2_index:
        return p1
    else:
        return p2


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    '''Extracts a set of all men's matches.
    Parameter:
    men (dict): key (str) is a man; value (list) where index 0 (str) is the man's match, where index 1 (nested list) is the man's preferences
    
    Return:
    match_set (set of 2-tuples): set contains 2-tuples; in each 2-tuple, index 0 (str) is the man and index 1 (str) is the woman the man is matched with.
    '''
    match_set = set()
    
    for person, pref in men.items():
        match_set.add((person, pref[match]))
        
    return match_set


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    '''Use Gale/Shapley algorithm to match men and women based on their preferences.
    The Gale/Shapley algorithm is not symmetric: men propose to women; women accept/reject men. 
    
    Parameters:
    men (dict): key (str) is a man; value (list) where index 0 (str) is the man's match, where index 1 (nested list) is the man's preferences
    women (dict): key (str) is a woman; value (list) where index 0 (str) is the woman's match, where index 1 (nested list) is the woman's preferences
    trace (bool): True/False to print/not print trace of Gale/Shapley algorithm
    '''
    men_dict = {}
    unmatched = set()
    
    # create copy of men and unmatched set
    for k, v in men.items():
        pref_list = []
        
        for pref in v[prefs]:
            pref_list.append(pref)
            
        men_dict[k] = [v[match], pref_list]
        unmatched.add(k)
    
    if trace == True: print('Women Preferences (unchanging)\n' + str(dict_as_str(women)))
    
    # Gale/Shapley algorithm
    while True: 
        # terminate Gale/Shapley algorithm when all men are matched
        if len(unmatched) == 0:
            break
        
        if trace == True: print('Men Preferences (current)\n' + str(dict_as_str(men_dict)))
        if trace == True: print('unmatched men = ' + str(unmatched))
        
        bachelor = unmatched.pop()
        top_pref = men_dict[bachelor][prefs].pop(match)
        woman_matched = False
        
        # determine if woman is matched or unmatched
        for k1, v1 in men_dict.items():
            if v1[match] == top_pref:
                woman_matched = True
                woman_curr_match = k1
            
        #woman is currently matched    
        if woman_matched == True:
            woman_pref = who_prefer(women[top_pref][prefs], bachelor, woman_curr_match)
                
            # woman prefers bachelor over current match
            if woman_pref == bachelor:
                men_dict[woman_curr_match][match] = None
                unmatched.add(woman_curr_match)
                men_dict[bachelor][match] = top_pref
                
                if trace == True: print('\n' + str(bachelor) + ' proposes to ' + str(top_pref) + ', who is a matched woman who prefers her new match; so she accepts the proposal\n')
            
            # woman prefers current match over bachelor
            else:
                unmatched.add(bachelor)
                if trace == True: print('\n' + str(bachelor) + ' proposes to ' + str(top_pref) + ', who is a matched woman who prefers her current match; so she rejects the proposal\n')
        
        # woman is currently unmatched
        if woman_matched == False:
            men_dict[bachelor][match] = top_pref
            
            if trace == True: print('\n' + str(bachelor) + ' proposes to ' + str(top_pref) + ', who is an unmatched woman; so she accepts the proposal\n')
    
    return extract_matches(men_dict)
    
        
if __name__ == '__main__':
    men_file = input('Select a file storing the preferences of the men: ')
    women_file = input('Select a file storing the preferences of the women: ')
    
    print('\nMen Preferences')
    print(dict_as_str(read_match_preferences(open(men_file))))
    
    print('Women Preferences')
    print(dict_as_str(read_match_preferences(open(women_file))))
    
    trace = True if input('Select Tracing of Execution[True]: ').lower() == 'true' else False
    
    if trace == True:
        print('The calculated matches are ', make_match(read_match_preferences(open(men_file)), read_match_preferences(open(women_file)), trace))
    if trace == False: 
        print('\nThe calculated matches are ', make_match(read_match_preferences(open(men_file)), read_match_preferences(open(women_file)), trace))
    
    
    # print()
    # import driver
    # driver.default_file_name = "bsc2.txt"
    # # driver.default_show_traceback = True
    # # driver.default_show_exception = True
    # # driver.default_show_exception_message = True
    # driver.driver()
