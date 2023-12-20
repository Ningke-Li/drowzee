similar_works(WorkA, WorkB, Similarity) :-
    findall(SimilarityType,
            (common_director(WorkA, WorkB) -> SimilarityType = director;
             similar_type(WorkA, WorkB) -> SimilarityType = genre),
            Similarities),
    list_to_set(Similarities, Similarity).

awards_count(Film, Count) :-
    aggregate(count, award_received(Film, _), Count).

nominations_count(Film, Count) :-
    aggregate(count, nominated_for(Film, _), Count).

compare_film_influence(Film1, Film2, MoreInfluential) :-
    instance_of(Film1, 'film'),
    instance_of(Film2, 'film'),
    (   (nominations_count(Film1, Nominations1), nominations_count(Film2, Nominations2),
         awards_count(Film1, Awards1), awards_count(Film2, Awards2),
         Total1 is Nominations1 + Awards1, Total2 is Nominations2 + Awards2,
         (Total1 > Total2 -> MoreInfluential = Film1;
          Total1 < Total2 -> MoreInfluential = Film2))
    ).

same_climate(PlaceA, PlaceB) :-
    k_ppen_climate_classification(PlaceA, ClimateA),
    k_ppen_climate_classification(PlaceB, ClimateB),
    ClimateA == ClimateB,
    PlaceA \= PlaceB.
    
have_heritage(PlaceA, PlaceB) :-
    heritage_designation(PlaceA, heritageA),
    heritage_designation(PlaceA, heritageB),
    heritageA \= heritageB,
    PlaceA \= PlaceB.


similar_places(PlaceA, PlaceB, Similarities) :-
    findall(Similarity,
            ( (same_climate(PlaceA, PlaceB) -> Similarity = climate);
              (have_heritage(PlaceA, PlaceB) -> Similarity = heritage)
            ),
            SimilarityList),
    list_to_set(SimilarityList, Similarities).

is_battle(Event) :-
    instance_of(Event, 'battle').

strategically_important_location(Battle1, Battle2, Location) :-
    location(Battle1, Location),
    is_battle(Battle1),
    location(Battle2, Location),
    is_battle(Battle2),
    Battle1 \= Battle2.


extract_year_from_datetime(DateTime, Year) :-
    sub_atom(DateTime, 0, 4, _, YearString),
    atom_number(YearString, Year).

is_olympics(Event) :-
    sub_atom(Event, _, _, 0, '_Olympics').

experienced_sharing_olympics(CountryA, CountryB) :-
    hosted_olympics(CountryA, EventA, YearA),
    hosted_olympics(CountryB, EventB, YearB),
    EventA \= EventB,
    abs(YearA - YearB) =:= 4.

hosted_olympics(Country, Event, Year) :-
    is_olympics(Event),
    country(Event, Country),
    point_in_time(Event, DateTime),
    extract_year_from_datetime(DateTime, Year).

historically_important_place(Place) :-
    findall(Body, site_of_astronomical_discovery(Body, Place), Bodies),
    length(Bodies, Count),
    Count > 1.

collect_notable_works(Person, Works) :-
    findall(Work, notable_work(Person, Work), Works).

collect_positions_held(Person, Positions) :-
    findall(Position, position_held(Person, Position), Positions).

career_highlight_metric(Person, Metric) :-
    collect_positions_held(Person, Positions),
    collect_notable_works(Person, Works),
    length(Positions, NumPositions),
    length(Works, NumWorks),
    Metric is NumPositions + NumWorks.

compare_career(PersonA, PersonB, Winner) :-
    career_highlight_metric(PersonA, MetricA),
    career_highlight_metric(PersonB, MetricB),
    (  MetricA > MetricB -> Winner = PersonA
    ;  MetricB > MetricA -> Winner = PersonB
    ;  Winner = tie
    ).

related_employee(OrganizationA, OrganizationB) :- 
    includes_member(OrganizationA, PersonA), 
    includes_member(OrganizationB, PersonB), 
    same_country(OrganizationA, OrganizationB), 
    PersonA \= PersonB.

indirect_design_influence(ProductA, DesignerC) :- 
    designed_by(ProductA, DesignerB), 
    influenced_by(DesignerB, DesignerC).
