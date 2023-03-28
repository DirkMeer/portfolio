## About the portfolio repository:
Django based DirkMeer.com portfolio to display my certifications and some projects I have worked on so far. Most are hosted externally but the Expense Tracker project is implemented directly into this Git repository and as such you can find it's source code under /expense_tracker/.

## About the expense tracker project:
A Django based app that allows the user to keep track of their expenses. It features user accounts with signup and account verification emails, the ability to reset a forgotten password and the ability to log in using either the chosen username or email-address.

The app allows the user to first input their base monthly income, and their base monthly expenses. This will be show in each months dashboard automatically so the user does not have to keep typing the same information each month. Then the user can add categories and add all their expenses per date and in a categorized manner. The dashboard then shows all this information in an easy to read format with graphs, allowing the user to switch back and forth between months.

**The login screen has a "Demo login" button which will allow you to quickly check out this project by skipping the account creation process and creating a logged in demo account prepopulated with semi-random data for you to play around with!**

This project uses the Django templating engine, custom template tags, the Django ORM with a postgreSQL database, backend customization, decorators, matplotlib, tokens and much more.

## Technology stack
- Python
- Django
- Javascript
- Html
- Css
- Matplotlib
- PostgreSQL