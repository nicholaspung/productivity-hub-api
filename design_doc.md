# Design Document

## Front-End

Technologies:

(JavaScript)

- React
- Redux
- Firebase Authentication
- Emotion

## Back-End

Technologies:

(Python)

- Django
- SQLite3
- Firebase Admin SDK
- Cron

## Hosting

Technologies:

- VPS
- Linux
- Nginx
- CI/CD

## Future Considerations:

- Email service
- Abstracting away websites to scrape
- Max todos and habits in system?
- Pomodoro Timing System

### Database Schemas (In Django Model fields)

Habit Tracker

- Todo

  - ID (AutoField)
  - Name (CharField, max_length=280)
  - Description (TextField, optional)
  - Date Created (DateTimeField, auto_now_add=True)
  - Date Finished (DateTimeField, optional)
  - Finished (BooleanField, default=False)
  - Order (SmallIntegerField, default=grabLastNumberInUnfinishedTodos)
  - Priority (CharField, max_length=2, choices=ENUM_PRIORITY_CHOICES, default=NONE)
  - User UID (ForeignKey, 'User', on_delete=models.CASCADE)

- Habit

  - ID (AutoField)
  - Name (CharField, max_length=280)
  - Description (TextField, optional)
  - Date Created (DateTimeField, auto_now_add=True)
  - Order (SmallIntegerField, default=grabLastNumberInUnfinishedTodos)
  - User UID (ForeignKey, 'User', on_delete=models.CASCADE)

- Daily

  - ID (AutoField)
  - Date (DateField, auto_now_add=True, unique)
  - Habits ID (ForeignKey, 'Habit', on_delete=models.SET(get_sentinel_habit))
  - Finished (BooleanField, default=False)
  - User UID (ForeignKey, 'User', on_delete=models.CASCADE)

Post Saver

- Posts (Reddit, Websites)

  - ID (AutoField)
  - Reddit ID (TextField, optional)
  - Title (CharField, max_length=200)
  - URL (TextField, optional)

- Titles

  - ID (AutoField)
  - Title (CharField, max_length=200)
  - User UID (ForeignKey, 'User', on_delete=models.CASCADE)

- Saved Posts

  - ID (AutoField)
  - Post ID (ForeignKey, 'Post', on_delete=models.CASCADE, unique)
  - Seen (BooleanField, default=False)
  - User UID (ForeignKey, 'User', on_delete=models.CASCADE)

Users

- Users

  - ID (UUIDField, primary_key=True, default=uuid.uuid4, editable=False)
  - Provider ID (TextField, editable=False)
  - Services (CharField, max_length=5, choices=ENUM_SERVICES_CHOICES, default=ENUM_SERVICES_CHOICES_HABIT_TRACKER)

# User Actions

Habit Tracker

- Todos

  - Add todos
  - Edit todos
  - Delete todos
  - Finish todos
  - Unfinish todos
  - Order todos (up, down, drag up and down)
  - Prioritize todos (none, high, low)

- Habits

  - Add habits
  - Edit habits
  - Delete habits
  - Finish todos
  - Unfinish todos
  - Order habits (up, down, drag up and down)

- Daily Habits

  - Show habits for week, month, and year view

Post Saver

- Posts (Reddit, Websites)

  - View current posts
  - Refresh current posts
    - Cross out seen posts

- Titles

  - Add titles
  - Edit titles
  - Delete titles
  - Search titles
  - Sort titles

- Saved Posts

  - Read posts
  - Refresh saved posts

Users

- Users

  - Delete account
  - Add services
  - Delete services
