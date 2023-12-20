:- use_module(library(aggregate)).

% transitive rules in various works
common_author(WorkA, WorkB) :-
    author(WorkA, PersonA),
    author(WorkB, PersonB),
    PersonA == PersonB,
    WorkA \= WorkB.


common_director(WorkA, WorkB) :-
    director(WorkA, PersonA),
    director(WorkB, PersonB),
    PersonA == PersonB,
    WorkA \= WorkB.

common_screenwriter(WorkA, WorkB) :-
    screenwriter(WorkA, PersonA),
    screenwriter(WorkB, PersonB),
    PersonA == PersonB,
    WorkA \= WorkB.

common_cast_member(WorkA, WorkB) :-
    cast_member(WorkA, PersonA),
    cast_member(WorkB, PersonB),
    PersonA == PersonB,
    WorkA \= WorkB.

same_series(WorkA, WorkB) :-
    part_of_the_series(WorkA, SeriesA),
    part_of_the_series(WorkB, SeriesB),
    SeriesA == SeriesB,
    WorkA \= WorkB.

similar_type(WorkA, WorkB) :-
    genre(WorkA, TypeA),
    genre(WorkB, TypeB),
    TypeA == TypeB,
    WorkA \= WorkB.

settlement_near_body_of_water(PlaceA, PlaceB, PlaceC) :-
    contains_settlement(PlaceA, PlaceB),
    located_in_or_next_to_body_of_water(PlaceA, PlaceC),
    PlaceB \= PlaceC,
    PlaceA \= PlaceC,
    PlaceA \= PlaceB.

indirectly_shares_border_with(Place1, Place2, Place3) :-
    shares_border_with(Place1, Place2),
    shares_border_with(Place1, Place3),
    Place1 \= Place3,
    Place2 \= Place1,
    Place2 \= Place3.

genetic_link(DiseaseA, DiseaseB) :-
    genetic_association(DiseaseA, GeneA),
    genetic_association(DiseaseB, GeneB),
    GeneA == GeneB,
    DiseaseA \= DiseaseB.

similar_symptoms_and_signs(DiseaseA, DiseaseB) :-
    symptoms_and_signs(DiseaseA, SymptomA),      
    symptoms_and_signs(DiseaseB, SymptomB),
    SymptomA == SymptomB,
    DiseaseA \= DiseaseB.

similar_drug_or_therapy_used_for_treatment(DiseaseA, DiseaseB) :-     
    drug_or_therapy_used_for_treatment(DiseaseA, TheropyA),
    drug_or_therapy_used_for_treatment(DiseaseB, TheropyB),
    TheropyA == TheropyB,
    DiseaseA \= DiseaseB. 

same_medical_examination(DiseaseA, DiseaseB) :-
    medical_examination(DiseaseA, ExaminationA),
    medical_examination(DiseaseB, ExaminationB),
    ExaminationA == ExaminationB,
    DiseaseA \= DiseaseB.

same_health_specialty(DiseaseA, DiseaseB) :-        
    health_specialty(DiseaseA, SpecialtyA),
    health_specialty(DiseaseB, SpecialtyB),
    SpecialtyA == SpecialtyB,
    DiseaseA \= DiseaseB.

same_subclass_event(EventA, EventB) :-
    part_of(EventA, Event),
    part_of(EventB, Event),
    EventA \= EventB.

same_participant(EventA, EventB) :-
    participant(EventA, Person),
    participant(EventB, Person),
    EventA \= EventB.

use_same_signal(TheoremA, TheoremB) :-
    used_by(TheoremA, Signal),
    used_by(TheoremB, Signal),
    TheoremA \= TheoremB.

influential_research(Research, Field) :-
    studied_by(Research, Field).

named_after_same_person(TheoremA, TheoremB) :-
    named_after(TheoremA, Person),                    
    named_after(TheoremB, Person),                    
    TheoremA \= TheoremB.                             

same_asteroid_spectral_type(BodyA, BodyB) :- 
    asteroid_spectral_type(BodyA, TypeA),
    asteroid_spectral_type(BodyB, TypeB),
    TypeA == TypeB,
    BodyA \= BodyB.

same_minor_planet_group(BodyA, BodyB) :- 
    minor_planet_group(BodyA, GroupA),
    minor_planet_group(BodyB, GroupB),
    GroupA == GroupB,
    BodyA \= BodyB.

same_political_party(PersonA, PersonB) :- 
    member_of_political_party(PersonA, PartyA), 
    member_of_political_party(PersonB, PartyB),
    PartyA == PartyB,
    PersonA \= PersonB.

same_award_received(PersonA, PersonB) :- 
    award_received(PersonA, AwardA), 
    award_received(PersonB, AwardB),
    AwardA == AwardB,
    PersonA \= PersonB.

same_country(OrganizationA, OrganizationB) :- 
    country(OrganizationA, PlaceA), 
    country(OrganizationB, PlaceB),
    PlaceA == PlaceB,
    OrganizationA \= OrganizationB.

same_operating_system(TechA, TechB) :- 
    operating_system(TechA, SystemA), 
    operating_system(TechB, SystemB),
    SystemA == SystemB,
    TechA \= TechB.

used_in_platform(TechA, TechB) :- 
    platform(TechA, PlatformA), 
    platform(TechB, PlatformB),
    PlatformA == PlatformB,
    TechA \= TechB.

similar_distributed_by(TechA, TechB) :- 
    distributed_by(TechA, X), 
    distributed_by(TechB, X),
    TechA \= TechB.
