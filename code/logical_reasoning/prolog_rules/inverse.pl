successor_style(WorkB, WorkA) :- 
    influenced_by(WorkA, WorkB),
    WorkA \= WorkB.

predecessor(WorkA, WorkB) :- 
    followed_by(WorkB, WorkA),
    WorkA \= WorkB.

original_work(DerivativeWork, OriginalWork) :- 
    derivative_work(OriginalWork, DerivativeWork),
    OriginalWork \= DerivativeWork.

country_of(City, Country) :- 
    capital_of(Country, City).

administrative_territorial_entity_of(PlaceB, PlaceA) :-
    located_in_the_administrative_territorial_entity(PlaceA, PlaceB).

influenced_by_disease(Gene, Disease) :- 
    genetic_association(Disease, Gene).

killer(PersonA, PersonB) :- 
    killed_by(PersonB, PersonA).

parent(Child, Parent) :- 
    child(Parent, Child).

child_of_mother(PersonA, PersonB) :- 
    mother(PersonB, PersonA).

child_of_father(Father, Child) :- 
    father(Child, Father).

give_name_to(PersonA, TheoremA) :- 
    named_after(TheoremA, PersonA).

discovered_by(Body, Scientist) :- 
    discoverer_or_inventor(Body, Scientist).

preceded_by(BodyB, BodyA) :- 
    followed_by(BodyA, BodyB).

teacher(PersonB, PersonA) :- 
    student(PersonA, PersonB).

includes_member(Organization, Member) :- 
    member_of(Member, Organization).

found_person(PersonA, OrganizationA) :- 
    founded_by(OrganizationA, PersonA).

headquarters_of(Location, Organization) :- 
    headquarters_location(Organization, Location).
