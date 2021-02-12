# Palani's Ideas
 - [Version control idea](https://github.com/ideaconsult/etc/wiki/IDEA-Development-Collaboration-Best-Practices)

# Joel's Ideas
**ACTORS**  
*See Section 2 of Requirements_Definition.md where I've included most of this information in one form or another*
 * customer
 * parking lot attendant
 * parking lot owner
	* managing attendants
	managing lots (add, remove, etc)
 * supervisor
	* give permissions? 
		* request/grant permissions?  COULD?
		* rating system? 				COULD?

**FUNCTIONAL REQUIREMENTS**  
*Here I've compiled my notes from the several lectures in which Dan discussed the app with us*  

*Generic/unsorted requirements*
* The app will be a single system with one login method that presents different views to the user based on their user type/permissions (this can be accomplished with Django fairly easily)  
* COULD: Interface with local transit systems to show users transit they can take from potential parking lots to their destination
* The app needs to be mobile friendly
* COULD/WONT: Interface with actual USU events/calendar
* Include Aggie graphics/imagery
* May use AWS or localhost as hosting method for the project
	* MUST: localhost
	* WONT: AWS

*Reservation Timing*
* Allow clients to register for a parking spot for events several days in advance
* Parking registration for an event should stay available until the day after the event  
* Users may reserve as many parking spots as they want at a time, within what is available
* Sort reservations by event

*Payment features*
* Use fake money for payment features
* User account management should include a balance section
	* Button to add $100 (this is our method of implementing fake money)
* When users pay for parking spot reservations at checkout, deduct the required amount from their account balance. If not enough money is in their account, present an error message.  

*University Admin Features*
* Able to add upcoming events up to 6 months in advance
* Can remove events
	* WONT: Refund process

*Lot Owner Features*
* Do not allow parking lots without attendants assigned to them
* Allow multiple attendants per parking lot
* Lot owners can be attendants of their own lots
* Assign prices to each spot type in their respective lots
* SHOULD?: Each lot should have a map attached to it including it and the potential associated event locations, users can view lot map as they reserve spots
* COULD: Manually add attendant accounts?

*Lot Attendant Features*
* Has access to reservation list with user and parking spot number
* QR codes if implemented (or alternative validation method)
* COULD: Include a map of the parking lot
* SHOULD: Have users list the make/model of their car, maybe license plate #, for verification purposes. This would be part of the reservation application process for each spot

*Spot Reservation*
* Each spot in each lot should have an associated spot type(normal, compact, RV, Tailgate, etc)
* Each lot should have a distance from the event indicated

*Account/Login*  
* Require email
* Optional phone number
* 8+ digit password

**USE CASES DISCUSSION**  
Public user (new user, no account yet, anyone)
- Setup account
- Register as a lot owner (Request A)

Customer
- reserving a spot
- manage their reservations
- access a map to their parking lot
- Register/promote to lot owner (Request B)
????? Locate VS Reserve Spot ?????

Lot Attendant
- checking in reservations 

Lot Owner
- add a parking lot
	- add/define a spot (id (database), type, price)
	- set a pin/define location with Google Maps API
		- MUST: address
		- COULD: pin/enclosed area via Maps API
- manage lot attendants (promote, demote)

University Admin
- add events
- approve requests for lot owners
- demote/kick lot owners

TODO: Joel - change client to customer in Req Def

FUTURE FEATURE
- verify/prove ownership of lots



# Autumn's Ideas


# Lexy's Ideas

