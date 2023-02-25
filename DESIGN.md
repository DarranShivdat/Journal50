Darran Shivdat
Journal50 Design Walkthrough


I emulated a lot of the structure and design for journal50 from cs50 finance. I used a styles.css file inside
of a static folder for the styling and design of the site. I have html files in a template folder. I created a
database with 2 tables to store the information. I used a helpers.py file to render an apology for errors and
to decorate routes. Lastly, I used an app.py file.
Let's break it down.

Starting with the app.py file:

Using flask I configured the application. I defined my database. The first route I created was the home page.
This is linked to the home.html file and you have to login to reach it. The next route adapted from cs50 finance was the
login route. In this route I cleared any sessions so I could log in fresh and be logged out of another account.
I then made sure that the username and password fields were filled. I then grabbed the username from my users table.
I then checked the password hashes to ensure the correct password was entered. I then set set my session[user_id]
to the username from the users table. If the file was reach by post then it was directed to the home page, otherwise
it rendered the login.html file. After the login route I used the register route (adapted from CS50 finance). I checked
if the username and password fields were empty and if the confirmaiton passwords were the same. I then entered the
new user information into the users table (they can now log in). I redirected them to the home directory, otherwise,
the username was already taken and an apology was rendered. The next route I created was the journal route.
I made sure a journal and title was provided recorded the inputs and incremented entries by one. I then checked if the
seven questions were answered and rendered apologies if they were. I casted the values as intgers and added them together;
this is the numerical DRA score. I flashed that it was successful and redirected them to the history page.
The next route I created was the history route. This route went through the entries table and pulled all of the
journal entries. If there were no previous entries, It rendered empty.html, otherwise it passed entries on to history.html.
The next route I created was the view post route which takes in an id. It renderes everyhting from entries and passes
it on to viewpost.html. Lastly, I used the logout and error catching from cs50 finance.

Next we will look at the templates.
The apology template renderes an apology with a gif of a cat (cs50 finance).
The empty.html template was returned if there were no journal entries.
The history.html template creates a table of entries by incrementing through entries using a for loop.
The home.html template is the home template and introduces journal50.
Journal.html creates a bulleted list of prompted questions. It then takes in a title using a text form and the entry
using a textarea form. The template then asks the DRA questions allowing only numbers from 1-10.
Layout.html provides the overall layout of all of the html files. This is adapted from cs50 finance. I used this for
the navbar, the javascript button, the alert flashes (cs50 finance).
The login template takes in a username and password as a form.
The register templates take in username, password and a confirmation password as a form.
The viewpost template creates a text area where the entry is shown. It also creates a route using /viewpost/ and
then the id of the message.

Next we will look at the journal database. This databse has two tables: users and entries.
The users table holds an id, username, password hash, and an entries number for each user.
The entries table holds an id, a user_id from users, a title, journal entry (text), a time and the DRA score.

Lastly we will look the styles.css file.
This css file provided the style for all of the html files.
It contains color customization for the links.
It has helper classes like left align that were implemented to help with alignment.
It has the nav bar colors from cs50 finance.
It has classes such as questionitem that help with margins.
It has a form control section where it specifies the height, width, and alignment of forms.
It has classes such as small, textbox, and center classes which help with suze ans allginemnt when called.
Lastly it specifies the main sections such as image, table, and tfoot.

