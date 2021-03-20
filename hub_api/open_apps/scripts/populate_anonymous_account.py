from open_apps.models.habit_tracker import ENUM_PRIORITY_CHOICES, Todo, Habit
from open_apps.models.vice import Vice


def populate_anonymous_account(user):
    # Populating Todos
    todo_high = Todo(user=user, name="This is a high priority todo.",
                     description="When you want a todo to be high in mind, click on the double up arrow icon to make the todo a high priority.",
                     priority=ENUM_PRIORITY_CHOICES[1])
    todo_high.save()
    todo_high_explanation = Todo(user=user, name="Explanation for a high priority.",
                                 description="Please make sure that when you are assigning a high priority that it is a high priority. From experience, the longer a high priority stays undone, the longer it will stay undone. You don't want that. The goal is to complete high priority todos when they are marked.",
                                 priority=ENUM_PRIORITY_CHOICES[1])
    todo_high_explanation.save()
    todo_high_tips = Todo(user=user, name="Tips for High Priorities.",
                          description="Do these as soon as possible. When prioritizing, make sure these todos are the first things you need to finish, or make it front of mind.",
                          priority=ENUM_PRIORITY_CHOICES[1])
    todo_high_tips.save()

    todo_normal = Todo(user=user, name="This is a normal priority todo.",
                       description="The default todo when it's created. If you don't know the priority on this todo, leave it here.",
                       priority=ENUM_PRIORITY_CHOICES[0])
    todo_normal.save()
    todo_normal_explanation = Todo(user=user, name="Explanation for a normal priority.",
                                   description="This should be the most populated priority section. A todo should be normal priority and wait to be high/low priority before being done.",
                                   priority=ENUM_PRIORITY_CHOICES[0])
    todo_normal_explanation.save()
    todo_normal_tips = Todo(user=user, name="Tips for Normal Priorities.",
                            description="These todos should re-prioritized after a scheduled re-prioritization of todos. Check to see when a todo should be done, and act accordingly.",
                            priority=ENUM_PRIORITY_CHOICES[0])
    todo_normal_tips.save()

    todo_low = Todo(user=user, name="This is a low priority todo.",
                    description="When you have a todo that needs to be done, but it's not urgent, make it a low priority todo.",
                    priority=ENUM_PRIORITY_CHOICES[2])
    todo_low.save()
    todo_low_explanation = Todo(user=user, name="Explanation for a low priority.",
                                description="It's crucial that you notice when a todo is low priority. If a priority is kept in high/normal priorities, it will make you de-sensitized to the priorities of Todos.",
                                priority=ENUM_PRIORITY_CHOICES[2])
    todo_low_explanation.save()
    todo_low_tips = Todo(user=user, name="Tips for Low Priorities.",
                         description="You want to make sure that you re-visit these todos on a regular basis to see if they can be prioritized higher. You can also do these todos when you find you have no motivation to do anything else.",
                         priority=ENUM_PRIORITY_CHOICES[2])
    todo_low_tips.save()

    # Populating Habits
    habit1 = Habit(user=user, name="This is a habit, which created dailies.")
    habit1.save()

    habit2 = Habit(
        user=user, name="Dailies are used to be actions you want to do daily in order to make it a successful day.")
    habit2.save()

    habit3 = Habit(user=user, name="For example, below are examples of dailies that help you improve one day at a time.",
                   description="The goal is to be better than you were the day before.")
    habit3.save()

    habit4 = Habit(user=user, name="This only works if you aim to get a complete BLUE square week every week.",
                   description="Above, you'll see that there is a section with 7 boxes, which indicate the current week. Your goal every week is to complete all the dailies that were created.")
    habit4.save()

    habit5 = Habit(user=user, name="Tips: Archive a habit when you are done.",
                   description="If you decide to not use a habit anymore, try archiving the habit first. When you delete a habit, all the dailies history will also be deleted. The history of dailies make for a nice representation of what you accomplished every day.")
    habit5.save()

    habit6 = Habit(user=user, name="Tips: You can make a habit create dailies on specific days.",
                   description="Just click on the edit icon, and you'll be able to choose which days the dailies are created.")
    habit6.save()

    habit7 = Habit(user=user, name="Check hub.myexperiment.life once a day.",
                   description="If you don't know what habit to start, start off with this one! Make this website you keystone habit that will give you ideas for more habits in the future!")
    habit7.save()
