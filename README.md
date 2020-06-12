## Bespoke Newsdesk
### Capstone Project by Austin Serif

https://bespokenews.us
[NewsAPI](https://newsapi.org/)

### Stack Description

#### Languages/Libraries
Bespoke is built on-top of [Flask](https://flask.palletsprojects.com/en/1.1.x/), [PostgreSQL](https://www.postgresql.org/), and [SQLAlchemy](https://www.sqlalchemy.org/), with [Bcrypt](https://pypi.org/project/bcrypt/) encryption. For quick, out of the box responsivenss, design patterns from [Material Design Lite](https://getmdl.io/) and [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction/) were utilized on the front-end.

#### Server Configuration
...TODO: Explain server config process.


### Features
- Search Bar
- Add-able/Removable Search Items
- Tag Items 

The project is a light-weight news tracking and analysis tool, providing users with a dashboard for searching keywords and from them creating tags. In addition to the feed tab and search tab, there is a profile tab, where (in the future) users will be able to configure settings related to their personal information, as well as feature preferences, such as whether or not they wish to recieve a daily email will all headlines related the keywords they are tracking. Tags can be deleted, and users can search and browse many terms before choosing to make it a tag. The application offers a simple, mobile friendly environment for currating news intake by personal topics of interest.

### User-flow
The user-flow is straight forward: Login to your Bespoke dashboard and immediately view all saved tags. To view articles related to a tag, select that tag. Want to add something new? Using the dashaboard tab just below the header, navigate to the search page. Here you can search anything, and it's immediately prepended to your search history just below the search bar. For instance, you might want to track articles related to Elon Musk. Naturally, you test out some queries like "Elon Musk", "Tesla", "SpaceX", "The Boring Company", each of which is populated to your history. But since you are only interested in space-related Musk news, neither "The Boring Company" nor "Tesla" would be useful tags. To get rid of them, go ahead and select the cancel button on the right-hand side of trash-can-bound search item (its just an "X"). Now you want to make tags of your other two search queries. Click the green "+" button to the left-hand side, you can't miss it. Select it once and a tag will be created from the search keyword. Select it again and you will be reminded that a tag for this already exists. To view your tags, navigate back over to the home/feed tab of your dashboard, and simply select the desired tag.