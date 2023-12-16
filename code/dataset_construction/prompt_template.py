# prompt_template.py
import random
import json
from tqdm import tqdm



new_predicate_list = ['common_author', 'predecessor', 'common_director', 'same_series', 'common_cast_member', 'common_screenwriter', 'similar_type', 'successor_style', 'original_work', 'not_male_character', 'indirectly_shares_border_with', 'not_same_country', 'administrative_territorial_entity_of', 'settlement_near_body_of_water', 'country_of', 'similar_places', 'parent', 'same_subclass_event', 'same_participant', 'child_of_father', 'child_of_mother', 'not_occurred_in', 'killer', 'strategically_important_location', 'compare_career', 'same_political_party', 'same_award_received', 'teacher', 'not_shared_worldview', 'same_country', 'not_a_member', 'found_person', 'includes_member', 'same_operating_system', 'similar_distributed_by', 'not_designed_by', 'used_in_platform', 'named_after_same_person', 'discover', 'influential_research', 'no_proved_by', 'same_health_specialty', 'not_genetically_associated', 'influenced_by_disease', 'similar_symptoms_and_signs', 'same_medical_examination', 'similar_drug_or_therapy_used_for_treatment', 'not_parent_body', 'same_minor_planet_group', 'same_asteroid_spectral_type', 'preceded_by']


def geography_template(fact):
    subject = fact['subject']
    predicate = fact['predicate']
    if 'object' in fact.keys():
        object_ = fact['object']
    if 'PlaceA' in fact.keys():
        place_a = fact['PlaceA']
    if predicate == 'indirectly_shares_border_with':
        question_template = [f"If place_a shares borders with place_b and place_b shares borders with placec, then we define place_a indirectly shares borders with place_c. Does {subject} indirectly share border with {object_} through {place_a}?", 
        f"If place_a shares borders with place_b and place_b shares borders with placec, then we define place_a indirectly shares borders with place_c. Is it true that {subject} has no relation with {object_} according to their borders through {place_a}?", 
        f"If place_a shares borders with place_b and place_b shares borders with placec, then we define place_a indirectly shares borders with place_c. Is it possible for {subject} to indirectly share border with {object_} through {place_a}?"]
        answer_template = ['Yes.', 'No.', 'Yes.']
    elif predicate == 'not_same_country':
        question_template = [f"Is it true that {subject} and {object_} are not in the same country?", f"Is it true that {subject} and {object_} are in the same country?", f"{subject} and {object_} are in the same country. Please judge the truth of this statement.", f"Is it possible for {subject} and {object_} to be in the different country?", f"Is it possible for {subject} and {object_} to be in the same country?"]
        answer_template = ['Yes.', 'No.', 'No.', 'Yes.', 'No.']
    elif predicate == 'administrative_territorial_entity_of':
        question_template = [f"Is it true that {subject} is the administrative territorial of {object_}?", f"Does {subject} contains {object_} from the aspect of administrative territory?", f"Is it possible for {subject} to be the administrative territorial entity of {object_}?", f"{subject} is not associated with {object_}. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'Yes.', 'Yes.', 'No.']
    elif predicate == 'settlement_near_body_of_water':
        question_template = [f"Is it true that {subject} is a settlement near {object_}?", f"Is it true that {subject} is not a settlement near {object_}?", f"Is it possible for {subject} to be a settlement near {object_}", f"There are no near relationship between {subject} and {object_}. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'country_of':
        question_template = [f"Is it true that the center of {subject} is {object_}?", f"Is {subject} the located area of {object_}?", f"Is it possible for {subject} that {object_} is the location for its important government apparatus?", f"{subject} is far away from {object_}. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'Yes.', 'Yes.', 'No.']
    elif predicate == 'similar_places':
        question_template = [f"Is it true that {subject} and {object_} are similar places according to their climate and world heritage designation numbers?", f"Is it true that {subject} and {object_} are not similar on climate?", f"Is it possible for {subject} and {object_} to be similar places according to their climate?", f"{subject} and {object_} totally differ from climate and world heritage designation numbers. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer


def culture_template(fact):
    subject = fact['subject']
    predicate = fact['predicate']
    if 'object' in fact.keys():
        object_ = fact['object']
    if predicate in ['common_author', 'common_director', 'common_screenwriter', 'common_cast_member']:
        key = ' '.join(predicate.split('_')[1:])
        question_template = [f"Is it true that {subject} and {object_} are of the same {key} according to their {key} lists?", f"Dose {subject} and {object_} have the same {key} according to their {key} lists?", f"Dose {subject} and {object_} have completely separate {key} according to their {key} lists?", f"Dose {subject} and {object_} share totally different {key}?", f"Is there any possibility for the {key} of {subject} also participate in conducting or writing {object_} according to their {key} lists?", f"It's not true that {subject} and {object_} have the same {key} according to their {key} lists. Am I right?", f"It's not true that {subject} and {object_} have totally different {key} according to their {key} lists. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'Yes.', 'No.', 'No.', 'Yes.', 'No.', 'Yes.']
    elif predicate == 'similar_type':
        question_template = [f"Considering the specific category of various films/books/channels/series such as horror movies, comedies and so on, is {subject} the same type of work as {object_}?", f"Considering the specific category of various films/books/channels/series such as horror movies, comedies and so on, is {subject} the different type of work as {object_}?", f"Considering the specific category of various films/books/channels/series such as horror movies, comedies and so on, {subject} and {object_} are the same type of work. Am I right?", f"Considering the specific category of various films/books/channels/series such as horror movies, comedies and so on, {subject} and {object_} are quite similar according to their types. Do you think so?", f"Considering the specific category of various films/books/channels/series such as horror movies, comedies and so on, {subject} and {object_} are quite different according to their types. Do you think so?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'Yes.', 'No.']
    elif predicate == 'same_series':
        question_template = [f"Is it true that {subject} and {object_} are both part of the same series?", f"Is it true that {subject} and {object_} are from two different series?", f"Did {subject} and {object_} belong to the same series?", f"Did {subject} and {object_} belong to the different series?", f"Is it possible for {subject} and {object_} to belong to the same series?", f"Is it possible for {subject} and {object_} to belong to the different series?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.', 'Yes.', 'No.']
    elif predicate in ['successor_style', 'predecessor', 'original_work']:
        key = ' '.join(predicate.split('_'))
        question_template = [f"Is it true that {subject} is the {key} of {object_}?", f"Is it true that {subject} is not the {key} of {object_}?", f"Is it possible for {subject} to be the {key} of {object_}?", f"I think {subject} is not the {key} of {object_}, do you think so?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'not_male_character':
        key = ' '.join(predicate.split('_'))
        question_template = [f"Is it true that {subject} is {key}?", f"Someone holds the opinion that {subject} is {key}, but I support the opposite one. Is my view right?", f"Is it possible for {subject} to be a {key}?", f"I think {subject} is {key}, do you think so?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'Yes.']
    
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer


def history_template(fact):
    if type(fact['subject']) == list:
        event1 = fact['subject'][0]
        event2 = fact['subject'][1]
    else:
        subject = fact['subject']
    subject = fact['subject']
    predicate = fact['predicate']
    if 'object' in fact.keys():
        object_ = fact['object']
    if predicate == 'parent':
        question_template = [f"Is it true that {subject} has the parent of {object_}?", f"Is it true that {subject} and {object_} are child and parent?", f"{subject}'s parent does not include {object_}. Please judge the truth of this statement.", f"Is it possible {subject}'s parent does not include {object_}?"]
        answer_template = ['Yes.', 'Yes.', 'Yes.', 'No.']
    elif predicate == 'same_subclass_event':
        question_template = [f"Is it true that {subject} and {object_} are both subclass of the same event?", f"Is it true that {subject} and {object_} are both subclass of different events?", f"Is it possible for {subject} and {object_} to be both subclass of the same event?", f"Is it possible for {subject} and {object_} to be both subclass of different events?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'same_participant':
        question_template = [f"Is it true that {subject} and {object_} have same participants?", f"Is it true that {subject} and {object_} have totally distinct participants", f"Is it possible for someone to be both participants of two various events {subject} and {object_}?", f"Is there an participant overlap betwen {subject} and {object_}?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'Yes.']
    elif predicate == 'child_of_father':
        question_template = [f"Is it true that {subject} has a child named {object_}?", f"{subject} is not the father of {object_}. Please judge the truth of this statement.", f"Is it possible for {subject} to be the mother of {object_}?", f"Is it possible for {subject} to be the father of {object_}?"]
        answer_template = ['Yes.', 'No.', 'No.', 'Yes.']
    elif predicate == 'child_of_mother':
        question_template = [f"Is it true that {subject} gave birth to {object_}?", f"{subject} is not the mother of {object_}. Please judge the truth of this statement.", f"Is it possible for {subject} to be the mother of {object_}?", f"Is it possible for {subject} to be the father of {object_}?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'not_occurred_in':
        question_template = [f"Is it true that {subject} occurred in {object_}?", f"Is it true that {subject} did not occur in {object_}?", f"{object_} is not the memorial site for the historical event {subject}. Please judge the truth of this statement.", f"Is it possible for {subject} to not occur in {object_}?"]
        answer_template = ['No.', 'Yes.', 'No.', 'No.']
    elif predicate == 'killer':
        question_template = [f"Is it right that {subject} did not need to take responsibility for the death of {object_}?", f"Is it true that {subject} did not kill {object_}?", f"Is it possible for {subject} to kill {object_}?", f"{subject} is a murderer as he/she killed {object_}. Please judge the truth of this statement."]
        answer_template = ['No.', 'No.', 'Yes.', 'Yes.']
    elif predicate == 'strategically_important_location':
        question_template = [f"Is {object_} strategically significant according to the many times of battle events ever happened in this place?", f"{object_} is strategically significant since more than one battle event took place at this location. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'Yes.']

    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer


def people_template(fact):
    if type(fact['subject']) == list:
        person1 = fact['subject'][0]
        person2 = fact['subject'][1]
    else:
        subject = fact['subject']
    subject = fact['subject']
    predicate = fact['predicate']
    if 'object' in fact.keys():
        object_ = fact['object']
    if predicate == 'compare_career':
        question_template = [f"Compare the career of different people according to the number of their notable works and positions they've held, so is it true that {person1} and {person2} have the same career?", f"Compare the career of different people according to the number of their notable works and positions they've held, so is it true that {person1} have better career than {person2}?", f"{person1} have worse career than {person2} simply according to the number of their notable works and positions they've held. Please judge the truth of this statement."]
        answer_template = ['Yes.' if object_ == "tier" else 'No.', 'Yes.' if object_ == person1 else 'No.', 'No.' if object_ == person1 else 'Yes.']
    elif predicate == 'same_political_party':
        question_template = [f"Is it true that {subject} and {object_} are both members of the same political party?", f"Is it true that {subject} and {object_} are both members of different political parties?", f"Is it possible for {subject} and {object_} to share similar political views?", f"Is it possible for {subject} and {object_} to be both members of different political parties?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'same_award_received':
        question_template = [f"Is it true that {subject} and {object_} have both received the same award?", f"Is it true that {subject} and {object_} never recieved same awards?", f"Is it possible for {subject} and {object_} to have both received the same award?", f"Is it possible for {subject} and {object_} to share experience of winning the same award?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'Yes.']
    elif predicate == 'teacher':
        question_template = [f"Is it true that {object_} is the teacher of {subject}?", f"Is it true that {subject} have taught {object_} important knowledge and lessons?", f"Is it possible for {subject} to never meet {object_}?", f"Is it possible for {subject} to learn from {object_} a lot?"]
        answer_template = ['Yes.', 'Yes.', 'No.', 'Yes.']
    elif predicate == 'not_shared_worldview':
        question_template = [f"Is it true that {subject} and {object_} share the same worldview or religion belief?", f"Is it true that {subject} and {object_} do not share the same worldview or religion belief?", f"Is it possible for {subject} and {object_} to share the same worldview or religion belief?", f"{subject} has highly different worldview or religion belief from {object_}. Please judge the truth of this statement."]
        answer_template = ['No.', 'Yes.', 'No.', 'Yes.']
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer


def health_template(fact):
    subject = fact['subject']
    predicate = fact['predicate']
    if 'object' in fact.keys():
        object_ = fact['object']
    if predicate in ['same_health_specialty', 'similar_symptoms_and_signs', 'same_medical_examination', 'similar_drug_or_therapy_used_for_treatment']:
        key_list = predicate.split('_')
        key = ' '.join(predicate.split('_'))
        question_template = [f"Is it true that {subject} and {object_} have {key}?", f"Is it true that {subject} and {object_} have totally different {key_list[1:]}?", f"Is there any {key_list[1:]} both useful for {subject} and {object_}?", f"Is it possible for {subject} and {object_} to have completely different {key_list[1:]}?"]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'not_genetically_associated':
        question_template = [f"Is it true that {subject} and {object_} are genetically associated?", f"Is it true that {subject} and {object_} are not genetically associated?", f"Is it possible for {subject} and {object_} to be genetically associated?", f"{subject} has nothing to do with {object_} from the aspect of genetic association. Please judge the truth of this statement."]
        answer_template = ['No.', 'Yes.', 'No.', 'Yes.']
    elif predicate == 'influenced_by_disease':
        question_template = [f"Is it true that {subject} can be influenced by {object_}?", f"Is it true that {subject} may not be influenced by {object_} according to genetic association?", f"Is it possible for {subject} to be influenced by {object_}?", f"{subject} is not influenced by {object_} according to genetic association. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer


def math_template(fact):
    subject = fact['subject']
    predicate = fact['predicate']
    object_ = fact['object']
    if predicate == 'named_after_same_person':
        question_template = [f"Is it true that {subject} and {object_} are both named after the same person?", f"Is it true that {subject} and {object_} are named after different people?", f"A admirable scientist named both {subject} and {object_}, is this true?", f"{subject} and {object_} are named after different people. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'discover':
        question_template = [f"{subject} named {object_}. Please judge the truth of this statement.", f"Is it true that {subject} named {object_}?", f"Is it true that {subject} did not give name to {object_}?"]
        answer_template = ['Yes.', 'Yes.', 'No.']
    elif predicate == 'influential_research':
        question_template = [f"Is it true that {subject} has made influential impact on {object_}?", f"Is it true that {subject} has not made influential impact on {object_} since no one from {object_} studied it?"]
        answer_template = ['Yes.', 'No.']
    elif predicate == 'no_proved_by':
        question_template = [f"{object_} is not the one that proved {subject}. Please judge the truth of this statement.", f"Is it true that {subject} has been proved by {object_}?"]
        answer_template = ['Yes.', 'No.']
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer



def tech_template(fact):
    subject = fact['subject']
    predicate = fact['predicate']
    object_ = fact['object']
    if predicate == 'same_operating_system':
        question_template = [f"Is it true that {subject} and {object_} are used in the same operating system?", f"Is it true that {subject} and {object_} are used in different operating systems?", f"Is it possible for {subject} and {object_} to fit the same operating system?", f"{subject} and {object_} can not be used in the same system. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'similar_distributed_by':
        question_template = [f"Is it true that {subject} and {object_} are both distributed by the same company?", f"Is it true that {subject} and {object_} are distributed by different companies?", f"Is it possible for {subject} and {object_} to be both distributed by the same company?", f"We can not get distributions of both {subject} and {object_} from the same company. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'not_designed_by':
        question_template = [f"{subject} is not designed by {object_}. Please judge the truth of this statement.", f"Is it true that {subject} is designed by {object_}?", f"Is it possible for {subject} to be designed by {object_}?"]
        answer_template = ['Yes.', 'No.', 'No.']
    elif predicate == 'used_in_platform':
        question_template = [f"Is it true that {subject} and {object_} are used in the same platform?", f"Is it true that {subject} and {object_} are used in different platforms?", f"Is it possible for {subject} and {object_} to fit the same platform?", f"{subject} and {object_} can not fit the same platform. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer


def nature_template(fact):
    subject = fact['subject']
    predicate = fact['predicate']
    object_ = fact['object']
    if predicate == 'not_parent_body':
        question_template = [f"Is it true that {subject} is not the parent astronomical body of {object_}?", f"Is it true that {subject} is the parent astronomical body of {object_}?", f"Is it possible for {subject} to be the parent astronomical body of {object_}?", f"{subject} is the parent astronomical body of {object_}. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    elif predicate == 'same_minor_planet_group':
        question_template = [f"Is it true that {subject} and {object_} are both members of the same minor planet group?", f"Is it true that {subject} and {object_} are from different minor planet groups?", f"{subject} and {object_} are from different minor planet groups. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'No.']
    elif predicate == 'same_asteroid_spectral_type':
        question_template = [f"Is it true that {subject} and {object_} are similar asteroid spectral type?", f"Is it true that {subject} and {object_} are different in asteroid spectral types?", f"{subject} and {object_} are different in asteroid spectral types. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'No.']
    elif predicate == 'preceded_by':
        question_template = [f"Is it true that {subject} is preceded by {object_}?", f"Is it true that {subject} is not preceded by {object_}?", f"Is it possible for {subject} to be preceded by {object_}?", f"{subject} is not preceded by {object_}. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer


# 'same_country', 'not_a_member', 'found_person', 'includes_member',
def society_template(fact):
    subject = fact['subject']
    predicate = fact['predicate']
    object_ = fact['object']
    if predicate == 'same_country':
        question_template = [f"Is it true that {subject} and {object_} are in the same country?", f"Is it true that {subject} and {object_} came from two different country?", f"{subject} and {object_} are two famous organizations from two different coutries. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'No.']
    elif predicate == 'not_a_member':
        question_template = [f"Is it true that {subject} is not the member of {object_}?", f"Is it true that {subject} is a member of {object_}?", f"{subject} is a member of {object_}. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'No.']
    elif predicate == 'found_person':
        question_template = [f"Is it true that {subject} is the founder of {object_}?", f"Is it true that {subject} is not the founder of {object_}?", f"{subject} founded {object_}. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.']
    elif predicate == 'includes_member':
        question_template = [f"Is it true that {subject} includes {object_} as its member?", f"Is it true that {object_} has never been on the member list of {subject}?", f"Is it possible for {object_} to appear as the member of {subject}", f"{subject} does not include {object_} as its member. Please judge the truth of this statement."]
        answer_template = ['Yes.', 'No.', 'Yes.', 'No.']
    question = random.choice(question_template)
    answer = answer_template[question_template.index(question)]
    return question, answer

function_mapping = {
    'culture': culture_template,
    'geography': geography_template,
    'history': history_template,
    'people': people_template,
    'society': society_template,
    'tech': tech_template,
    'math': math_template,
    'health': health_template,
    'nature': nature_template
}

def generate_qa_pairs(fact, collection):
    subject = fact['subject']
    predicate = fact['predicate']
    if 'object' in fact.keys():
        object_ = fact['object']
    else:
        object_ = ''
    # question, answer = culture_template(fact)
    # question, answer = function_mapping[collection](fact)
    # question, answer = geography_template(fact)
    # question, answer = history_template(fact)
    # question, answer = people_template(fact)
    # question, answer = health_template(fact)
    # question, answer = math_template(fact)
    # question, answer = tech_template(fact)
    # question, answer = nature_template(fact)
    # question, answer = society_template(fact)
    question, answer = function_mapping[collection](fact)
    return question, answer
