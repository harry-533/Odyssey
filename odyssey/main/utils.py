# import ollama
from .models import Activity
import re

cities = [
        'Bangkok', 'Paris', 'London', 'Singapore', 'New York', 
        'Istanbul', 'Tokyo', 'Seoul', 'Milan', 'Barcelona', 
        'Shanghai', 'Amsterdam', 'Los Angeles', 'Cairo', 
        'Berlin', 'Moscow', 'Madrid', 'Beijing', 
        'Rio de Janeiro', 'Venice','Copenhagen',
        'Abu Dhabi', 'Cape Town'
    ]

# Function that queries the LLM and then stores the response in the database
def get_activities():
    # Ollama ran localy with the mistral model
    client = ollama.Client()
    model = "mistral"

    # Loops through all the cities to seperateley store the activities for each city
    for i in cities:
        all_activities = {}
        # Prompt used to get the specific activities
        prompt = f"""
        I want you to list 30 popular tourist activity in the city of {i}. For each activity, provide the following details in this specific format:

        | Title | Price (Always in the format £10, never any other format if it is free it would be £0) | Description (max 256 characters) | Shorter Description (max 64 characters) | Type, Only chose one of the following (Cultural, Family, Relaxation, Adventure, Sports) | Group Size (e.g., 1+, 2+, etc.) | Recommended Age (Only in the format 6+, 8+ or All ages with no extra details) | Duration (Always in one of the following formats '1 hour', '2 hours', '3-4 hours') | Popularity (whole numbers 1-5) | Accessibility (Limited, Partially, Fully) |

        Example format (for 3 activities):

        | Sagrada Família Tour | £25 | Explore Antoni Gaudí's masterpiece, known for its intricate architecture | Take a tour around the Sagrada Família | Cultural | 1+ | 8+ | 2 hours | 5/5 | Partially
        | Tibidabo Amusement Park | £35 | Enjoy thrilling rides at this historic amusement park atop Mount Tibidabo | Enjoy a thrilling amusement park | Adventure | 2+ | 6+ | 3-4 hours | 4/5 | Fully
        | Camp Nou Tour | £20 | Take a tour around one of the biggest stadiums in the world, the home of FC Barcelona | Tour FC Barcelona's iconic stadium | Sports | 1+ | All ages | 1 hour | 4/5 | Limited

        Follow this exact format. Please provide only one activity per response. Don't skip any information. Do not make it into a table. I literarrly one the example Format precisely with no alteration other than the more activities. Do not include any intro or outro text before and after the data. You must have '|' Before you start each new activity, never start an new activity without the '|' at the start.
        """
        response = client.generate(model=model, prompt=prompt)

        # Splits the response so it can be easily stored
        responses = response.response.split("|")
        activity = []
        total_activities = []
        first = True
        count = 0
        # Loops through the split response and groups the acitvities details
        for j in responses:
            if not first:
                activity.append(j)
                count += 1
            else:
                first = False
            if count == 10:
                total_activities.append(activity)  
                activity = []
                count = 0

        all_activities[i] = total_activities

        # Loops through the activities and stores them in the database
        for key, item in all_activities.items():
            for activity in range(len(item)):
                # Loops through the activitiy details and gets rid of certian chars
                for detail in range(len(all_activities[key][activity])):
                    if detail == 9:
                        all_activities[key][activity][detail] = all_activities[key][activity][detail].lstrip().rstrip()
                    else:
                        all_activities[key][activity][detail] = all_activities[key][activity][detail].lstrip().rstrip()
                    try:
                        index = all_activities[key][activity][detail].index('(')
                        all_activities[key][activity][detail] = all_activities[key][activity][detail][:index-1]
                    except:
                        pass

                # Adds the activity to the database assuming no errors
                try:
                    new_activity = Activity(city = key, title = item[activity][0], image = item[activity][0].replace(" ", "").lower(), price = item[activity][1], 
                                        desc = item[activity][2], short_desc = item[activity][3], category = item[activity][4], 
                                        group_size = item[activity][5], age = item[activity][6], duration = item[activity][7], 
                                        popularity = item[activity][8], accessibility = item[activity][9])
                    new_activity.save()
                    print('success')
                except:
                    print('fail')

# Function used to clean the database to remove errors
def fix_database():
    activities = Activity.objects.all()

    # Loops through the activities to remove errors in details
    for activity in activities:
        if (v_index := activity.title.find('visit')) != -1:
            activity.title = activity.title[:v_index - 1]

        if (v_index := activity.image.find('visit')) != -1:
            activity.image = activity.image[:v_index]
        
        if not activity.image:
            activity.image = activity.title.replace(" ", "").lower()

        if (space_index := activity.accessibility.find(' ')) != -1:
            activity.accessibility = activity.accessibility[:space_index]

        if (space_index := activity.category.find(' ')) != -1:
            activity.category = activity.category[:space_index]
        if (comma_index := activity.category.find(',')) != -1:
            activity.category = activity.category[:comma_index]

        if (pound_index := activity.price.find('£')) != -1:
            if pound_index > 0:
                pound_index -= 1
                activity.price = activity.price[pound_index:].rstrip()
        if (space_index := activity.price.find(' ')) != -1:
            activity.price = activity.price[:space_index]
        if (to_index := activity.price.find('-')) != -1:
            activity.price = activity.price[:to_index]
        if (free_index := activity.price.lower().find('free')) != -1:
            activity.price = activity.price[:free_index] + '0'

        if (more_index := activity.duration.find(' or more')) != -1:
            activity.duration = activity.duration[:more_index] + '+'

        if activity.accessibility == "Limited":
            activity.accessibility += ' accessibility'
        else:
            activity.accessibility += ' accessible'

        popularity = int(activity.popularity[0])
        activity.popularity = '⭐' * popularity + '☆' * (5-popularity)

        activity.image = re.sub(r'[^a-zA-Z0-9 ]', '', activity.image)

        city_dict = {"Cape Town": "South Africa", "Abu Dhabi": "UAE", "Melbourne": "Australia", "Venice": "Italy",
                     "Rio de Janeiro": "Brazil", "Beijing": "China", "Madrid": "Spain", "Moscow": "Russia",
                     "Berlin": "Germany", "Cairo": "Egypt", "Los Angeles": "USA", "Amsterdam": "Netherlands",
                     "Shanghai": "China", "Barcelona": "Spain", "Milan": "Italy", "Seoul": "South Korea",
                     "Tokyo": "Japan", "Istanbul": "Turkey", "New York": "USA", "Singapore": "Singapore",
                     "London": "UK", "Paris": "France", "Bangkok": "Thailand"
                    }
        country = city_dict[activity.city]
        activity.country = country

        activity.save()