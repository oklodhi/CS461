% OMER KHAN
% CS 461
% BRIAN HARE

solve(ROOMS) :-
	length(ROOMS, 5),                                            
	nth1(3,ROOMS,[computerscience,_,_,_,_]),
    	member([history,jazz,_,_,_],ROOMS),
    	member([_,_,toyota,yankees,_],ROOMS), 
    	member([accounting,_,_,_,coke],ROOMS),
    	member([engineering,_,_,_,coffee],ROOMS),
    	near([computerscience,_,_,_,_],[history,_,_,_,_],ROOMS), 
    	nth1(5,ROOMS,[_,classical,_,_,_]),
    	member([_,_,tesla,_,tea],ROOMS),
   	 near([_,classical,_,_,_],[_,jazz,_,_,_],ROOMS), 
    	\+ ROOMS = [[english,_,_,_,_],_,_,_,_],
	\+ ROOMS = [_,[english,_,_,_,_],_,_,_],
    	member([_,_,tesla,royals,_],ROOMS),
    	member([_,jazz,_,clubs,_],ROOMS),
    	member([engineering,_,_,chiefs,_],ROOMS),
    	nth1(1,ROOMS,[_,_,_,broncos,_]),
    	member([_,_,nissan,_,coke],ROOMS),
    	near([_,country,_,_,_],[_,techno,_,_,_],ROOMS), 
   	nth1(1,ROOMS,[accounting,_,_,_,_]),
    	near([_,_,_,chiefs,_],[_,_,_,royals,_],ROOMS), 
    	member([accounting,rock,_,_,_],ROOMS), 
    	member([_,_,_,yankees,milk],ROOMS),
    	member([_,country,chevy,_,_],ROOMS),
    	member([_,jazz,ford,_,_],ROOMS),  
    
    	member([_,_,_,_,water], ROOMS),
    
    	% what music does computer science student listen to and what does the english major drink
	member([computerscience,_,_,_,_], ROOMS),
	member([english,_,_,_,_], ROOMS),

	% There is only one solution.
	!
	.


% adjacent(A, B, List)
adjacent(A, B, [A, B|_]).
adjacent(A, B, [_|X]) :- adjacent(A, B, X).

% near(A, B, List)
% True if A and B are beside each other in List.
near(A, B, List) :- adjacent(A, B, List) ; adjacent(B, A, List).