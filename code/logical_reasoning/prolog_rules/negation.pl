not_same_creator(WorkA, WorkB) :-
    creator(WorkA, CreatorA),
    creator(WorkB, CreatorB),
    WorkA \= WorkB,
    \+ CreatorA = CreatorB.


not_awarded(Work) :-
    \+ award_received(Work, _).


not_male_character(CharacterA) :-
    instance_of(CharacterA, Type),
    string_concat(_, "character", Type),
    sex_or_gender(CharacterA, Gender),
    Gender \= male. 

not_same_country(City1, City2) :-
    country(City1, Country1),
    country(City2, Country2),
    \+ Country1 = Country2.

not_genetically_associated(Disease, Gene) :-
    \+ genetic_association(Disease, Gene).

not_occurred_in(Event, Location) :- 
    \+ location(Event, Location).

no_proved_by(TheoremA, Person) :- 
    \+ proved_by(TheoremA, Person).

not_parent_body(BodyA, BodyB) :- 
    \+ parent_astronomical_body(BodyA, BodyB).

not_shared_worldview(PersonA, PersonB) :-
    PersonA \= PersonB,                                 
    \+ (religion_or_worldview(PersonA, Worldview),      
        religion_or_worldview(PersonB, Worldview)).

not_a_member(Member, Organization) :- 
    \+ member_of(Member, Organization).

not_designed_by(Product, Designer) :- 
    \+ designed_by(Product, Designer).
