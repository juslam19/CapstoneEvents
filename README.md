# 🎉 CapstoneEvents ✨

## Table of contents
1. Distinctiveness and Complexity
2. Files and their contents
    1. HTML files
    2. JavaScript files
    2. CSS files
    2. Python files
3. Website Features
    1. For Both Accounts
    2. For Person Accounts
    3. For Organisation Accounts
4. How to Run Application
5. Acknowledgements


## 1. Distinctiveness and Complexity
CapstoneEvents has some of its minor concepts inspired from previous projects, but the overarching concepts are completely unique. It is an event booking website that enables event creation and event booking for organisations and persons respectively, and hence has the original implementation of multiple user types not seen in earlier projects. 

__CapstoneEvents is more complex than all of my previous 5 projects. The following are evidence for this claim:__

1. It differs from Project 4 Network by the following evidence:
    - The like function has additional utility added to it, such as sorting events by it. 
    - While events could appear to bear similarity to posts in social media, it has added complexity such as datetime formats, images, etc., has how users can interact with it limited by the users' account types, is organised by category, and also has the additonal related model of "TicketedEvents" to keep track of users who have signed up for that event. 
    - Moreover, accessibility to events / organisation profiles / personal profiles is limited by user account type and user identity for privacy purposes. 
2. The Application has 8 different models. This includes:
    - User (entity, for authentication purpose)
    - Person (entity, representing person information for person account)
    - Organisation (entity, representing organisation information for organisation account)
    - Event (entity, representing an organisation's event)
    - TicketedEvent (entity, representing a person's ticket to an event)
    - Like (relation, representing likes for an event)
    - Category (entity, representing the category of an event, and a person's possible interest)
3. The application uses HTML, CSS, and JavaScript for front-end user interaction. For the back-end, it uses Django, Python, and SQLite3 database.
4. Allows for multiple user account types that is unique to this project, each user account type has different website permissions, actions they are allowed to perform and exclusive website pages they can access. This has not been implemented in any of the earlier projects. Enforced by special decorators preventing unauthorised access of pages or functions.
5. Each account type and their features / actions:
    - Only organisations are allowed to create, update, view and delete (only their own) events -- trying to access other organisations' event pages will give a custom "access not allowed" page -- hence having full CRUD functionalities, but they are not allowed to like or book ticket to events, nor see other organisation accounts, nor accounts of persons not involved in their events -- will give them an "access not allowed" page.
    - Persons are not allowed to CRUD any events, but they can like and book events, and see all organisation accounts, but cannot see other persons' accounts. Moreover, person users can use the search page to comprehensively search through all events (excluding those booked by them), and they can sort events (not booked by them at the moment) by likes, start time, most participants, most capacity.


## 2. Files and contents
__Root directory is taken as /CapstoneEvents/.__

### 2.1. HTML files
#### 2.1.1. General templates
| Filename | Content |
| -------- | --------|
| `templates/base_p.html` | Provides navbar and footer for website |
| `templates/registration/login.html` | Login screen for both account types |
| `templates/registration/signup.html` | Select account type for sign up |
| `templates/registration/signup_form.html` | Sign up screen for both account types |

#### 2.1.2. Both Account Types Templates
| Filename | Content |
| -------- | --------|
| `capstone/templates/capstone/event_details.html` | Shows event details (accessibility of certain profiles depends on account type and user currently signed in) |
| `capstone/templates/capstone/home.html` | Shows "home" (informational) page when not signed in |
| `capstone/templates/capstone/org_profile.html` | Shows organisation profile (accessibility of certain profiles depends on account type and user currently signed in) |
| `capstone/templates/capstone/profile.html` | Shows person profile (accessibility of certain profiles depends on account type and user currently signed in) |

#### 2.1.3. Organisation Account Only Templates
| Filename | Content |
| -------- | --------|
| `capstone/templates/capstone/organisations/_header.html` | Top section of page used in many pages |
| `capstone/templates/capstone/organisations/_image_preview.html` | Image Preview section used in many form pages |
| `capstone/templates/capstone/organisations/_main_list.html` | Listing of events section used in many pages  |
| `capstone/templates/capstone/organisations/ended_change_list.html` | Listing of ended events  |
| `capstone/templates/capstone/organisations/event_add_form.html` | Page to add events |
| `capstone/templates/capstone/organisations/event_edit_form.html` | Page to edit events (accessibility of certain profiles depends on account type and user currently signed in) |
| `capstone/templates/capstone/organisations/event_change_list.html` | Listing of current events  |
| `capstone/templates/capstone/organisations/event_results.html` | Shows the participants that signed up / have attended an event (accessibility of certain profiles depends on account type and user currently signed in) |

#### 2.1.4. Person Account Only Templates
| Filename | Content |
| -------- | --------|
| `capstone/templates/capstone/persons/_header.html` | Template for sections used in 'Event' pages |
| `capstone/templates/capstone/persons/_header_my.html` | Template for sections used in 'Ticketed Event' pages |
| `capstone/templates/capstone/persons/_main_list.html` | Section of event listings used in 'Event' pages |
| `capstone/templates/capstone/persons/_main_ticketed.html` | Section of ticketed event listings used in 'Ticketed Event' pages |
| `capstone/templates/capstone/persons/_sort.html` | Sorting form used in many pages |
| `capstone/templates/capstone/persons/all_list.html` | Shows 'Explore' page in 'Event' pages |
| `capstone/templates/capstone/persons/ended_event_list.html` | Shows 'Ended Events' (ended events that user have ticket; probably attended already) page in 'Ticketed Event' pages |
| `capstone/templates/capstone/persons/event_list.html` | Shows 'Interests' page in 'Event' pages |
| `capstone/templates/capstone/persons/event_ticket.html` | Shows respective event ticket (accessibility of certain profiles depends on account type and user currently signed in) |
| `capstone/templates/capstone/persons/interests_form.html` | Displays interests form |
| `capstone/templates/capstone/persons/org_list.html` | Shows list of organisations |
| `capstone/templates/capstone/persons/past_event_list.html` | Shows 'Past Events' (events that have ended, excluding user ticketed ended events) page in 'Event' page  |
| `capstone/templates/capstone/persons/search_list.html` | Shows 'Search' page in 'Event' page |
| `capstone/templates/capstone/persons/ticketed_event_list.html` | Shows 'Ticketed Events' (current events that have ticket) page in 'Event' page |

### 2.2. JavaScript files
| Filename | Content |
| -------- | --------|
| `static/capstone/helper.js` | Contains functions for liking event, updating like button, and updating delete event button, confirm delete button and delete confirmation message |

### 2.3. CSS files
| Filename | Content |
| -------- | --------|
| `static/css/app.css` | Formats various elements on website |

### 2.4. Python files

#### 2.4.1. General files
| Filename | Content |
| -------- | --------|
| `capstone/__init__.py` | As required |
| `capstone/admin.py` | Tracks which models admin is allowed to perform CRUD |
| `capstone/apps.py` | Tracks apps used |
| `capstone/decorators.py` | Holds the permission decorators to ensure that methods that are organisation or person exclusive are exclusive |
| `capstone/forms.py` | Contains various forms/ part of forms used throughout website |
| `capstone/models.py` | Contains the models used in storign the website data |
| `capstone/urls.py` | Contains the various urls of the website, the functions associated with each, and the name of each url |

#### 2.4.2. Views
| Filename | Content |
| -------- | --------|
| `capstone/views/__init__.py` | As required |
| `capstone/views/capstone.py` | Views used when not logged in / just signing in / signing up |
| `capstone/views/persons.py` | Views used by Person Account Type |
| `capstone/views/organisations.py` | Views used by Organisation Account Type |


## 3. Website Features

### 3.1. Basic Requirements
---------------------------------------------------------------------------------------------------------
- Utilize Django (w/ many models) on back-end
- Mobile-responsive
    - Navbar collapses into dropdown
    - Pictures and text segments rearrange themselves when narrow width
- Utilize JavaScript on front-end
    - Like count updates live
        - When liked, count updates live to reflect the added like.
	- Using JavaScript, asynchronously let the server know to update the like count and then update event like count displayed without requiring a reload of the entire page.
        - Also, heart button remains red even after page refresh to show that person already liked that event.
    - Delete confirm button
        - Also, delete confirmation button uses JS to change text and hide/ show button and text

### 3.2. Website Features
--------------------------------------------------------------------------------------------------------
#### 3.2.1 For Both Accounts
- Multiple user sign-up and log-in
    - Person and Organisation has different functions for each user type
    - Special functions to not allow user to view organisation pages and vice versa
- Pictures upload implemented
    - Able to use pictures in accounts and events
- Datepicker implemented
    - Able to use datepicker in forms with date format input

#### 3.2.2. For Person Accounts
- Like and Unlike Events
    - Users can click like button to “like” an event.
- Privacy for other persons
    - Cannot see accounts of other person users
- Filter Events by Interests
    - Events filtered by one's interests - "Interests" tab in "Events" group
    - Can update Interests using a form
- Sort Events using Variables
    - Uses form to sort events – ALL tabs in "Events" group
    - Sorts by variables such as starting date, capacity, likes, tickets booked.
- Search Events by Variables 
    - Uses form to search events – "Search" tab in "Events" group
    - Searches by substring in name, earliest start and latest end date, categories, active or ended events.
- Search Organisations by Name
    - Uses form to search organisations – "Organisations" group
- Organisation Profiles
    - See Organisation details, and their events
- Event Details
    - See Event details
- Get and cancel ticket
    - Responds to booking number / capacity number:
        - When all available slots out:
            - If user has not booked, shows “Fully Booked” and does not allow user to get ticket
            - If user already has ticket, still gives user ability to cancel ticket
        - If event has passed (the end time):
            - User is not allowed to get / cancel ticket
    - Ticket page produces digital ticket of the event
        - Includes useful information like page access time, event last update, etc.

#### 3.2.3. For Organisation Accounts
- Privacy for other organisations
    - Cannot see accounts of other organisation users
- Can see results of events 
    - Shows list of persons participanting in table form, and links to their accounts
- Privacy for persons not participanting in organisation's events
    - Cannot see users who are not involved in your events
    - Privacy ensured, while still showing accounts of involved persons so can contact/ verify persons at events, or include personal info in logistical information
- Can CRUD own events (all fields except name)
    - Create events with pictures and start and end time etc. Also automatically generates time of event creation.
    - Can edit all fields included in event creation form (including image, start and end times) with exception of name
    - Updating event will show the number of updates done, and time of latest update done.
    - Delete event at event table, after pressing confirm button


## 4. How to Run Application
1. Clone or do other appropriate actions to get repository onto your local machine.
2. Install the requirements:
`pip install -r requirements.txt`
3. There is no need to create migrations and migrate, as this has already been done in order to have pre-existing content in website (to enhance website experience).
4. Finally, run the development server:
`python manage.py runserver`

5. Try out some of the existing accounts, so you can test out of the box! The existing users' usernames (which  also are their passwords) are:

	| Account Type | Usernames / Passwords |
	| -------- | --------|
	| PERSONS | 1, 2, 3, 4 |
	| ORGANISATIONS | q, w, e |
	| SUPERUSER** | 0 |

	__**WARNING: Log out of admin pages BEFORE accessing main website -- 0 is neither a person nor an organisation, so this causes issues if 0 visits the main website.__ 

## 5. Acknowledgements
- See CREDITS.txt for credits for graphics and images used throughout website for enhanced website demonstartive purposes.
- Credits where due to the external libraries I used, such as to Masonry, a JavaScript grid layout library, which has been used to make the events' card arrangement possible.
