Project Plan

# Big Blue's Parking Genie

## Project Overview
This project’s objective is to provide a system for providing and reserving parking spots at Utah State University.

The system will be designed for large events on the campus such as sporting events, musical productions, graduation, etc. Owners of large parking lots as well as single parking spaces will be able to list various types of parking spots available through the system. Customers looking for a parking spot on or near USU’s campus will be able to purchase one or more spots and receive their confirmation ticket through the system. Other users will be able to use the system as well, such as university admin and parking lot attendants. The browser-based system will be capable of running through the web on a PC, Android, and iOS mobile device.

## Team Organization

Our team is made up of four software developers/designers and two project managers, Dan Watson and Bradley Payne. The project managers will oversee the project and interact with the client. As the designers and developers, we will work together to design and build the system (front and back end) according to the requirements given from the managers.

For each milestone/phase in the project, there will be a different project leader, from the four developers, who will help divide the work out for each team member. Each phase, the work will be evenly distributed to each person. The phase tasks have assigned point values, which will help the leader in delegating them out.

## Software Development Process

The development will be broken up into four phases.  Each phase will be a little like a Sprint in an Agile method and a little like an iteration in a Spiral process.  Specifically, each phase will be like a Sprint, in that work to be done will be organized into small tasks, placed into a “backlog”, and prioritized.   Then, using on time-box scheduling, the team will decide which tasks the phase (Sprint) will address.  The team will use a Scrum Board to keep track of tasks in the backlog, those that will be part of the current Sprint, those in progress, and those that are done.

Each phase will also be a little like an iteration in a Spiral process, in that each phase will include some risk analysis and that any development activity (requirements capture, analysis, design, implementation, etc.) can be done during any phase.  Early phases will focus on understanding (requirements capture and analysis) and subsequent phases will focus on design and implementation.  Each phase will include a retrospective.

| **Phase** | **Iteration** |
|-----------|---------------|
| 1. | Phase 1 - Requirements Capture |
| 2. | Phase 2 - Analysis, Architectural, UI, and DB Design |
| 3. | Phase 3 - Implementation, and Unit Testing |
| 4. | Phase 4 - More Implementation and Testing  |

We will use Unified Modeling Language (UML) to document user goals, structural concepts, component interactions, and behaviors.

## Communication Policies, Procedures, and Tools
Our team will mainly use text messaging and Zoom to communicate about the project. Outside of regular class time, we will meet at least once a week for updates on the project and plans moving forward. We will all be working on the same Git repository, so we will communicate about details there as well. We have sections of the repo that contain our brainstorming/idea documents and other collaborations. We have a Slack channel set up for us to share documents and have meetings as well. It will help us keep track of our progress on each phase of the project.

## Risk Analysis

1. **Task:** Add independent lot owners
    - **Likelihood:** Medium
    - **Severity:** Medium
    - **Consequences:** Loss of revenue. Without independent lot owners, there won't be as many parking spots for sale.
    - **Workaround:** List independent parking spots through university parking lots
        - **Difficulty:** Medium
        - **Impact:** This would create an hour of two of work for the developers to add the functionality to the university lot owners' page to add parking spots that aren't in their specified lots.
        - **Pros:** The university would be able to control who they allow to sell parking spots.
        - **Cons:** The ease of listing a parking spot would become more difficult, requiring the independent owners to go through the university.
2. **Task:** Extend system to Andriod and iOS mobile devices
    - **Likelihood:** Medium
    - **Severity:** Medium
    - **Consequences:** The system will be very limited in its accessibility. We need to get it running on mobile devices so it can be accessed wherever.
    - **Workaround:** Use desktop browser to access Parking Genie.
        - **Difficulty:** Easy. This is already the plan for the system.
        - **Impact:** This won't add much work, because itwill be implemented already.
        - **Pros:** All of the system's features can be used on a desktop browser.
        - **Cons:** Customers will not be able to access the system when they are on the go, making it difficult to reserve parking spots and access reservation info anytime.
3. **Task:** Use Google Maps API for the parking spot navigation
    - **Likelihood:** Medium
    - **Severity:** High
    - **Consequences:** Specific directions to locate parking spots will be limited. 
    - **Workaround:** Use a pdf map of the campus and surrounding streets and allow lot owners to mark the locations of their parking spots.
        - **Difficulty:** Medium
        - **Impact:** This will create extra work for the developer. They will need to add functionality to the map where lot owners can mark their locations.
        - **Pros:** Customers will be able to see the general area of their reserved parking spots.
        - **Cons:** The map is not as versatile and does not use GPS to guide users to the marked locations.

## Configuration Management
See the README.md in the Git repository.

