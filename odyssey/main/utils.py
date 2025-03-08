# import ollama
from .models import Activity

# client = ollama.Client()

# model = "mistral"

# cities = [
#     'Bangkok', 'Paris', 'London', 'Dubai', 'Singapore', 'New York', 'Kuala Lumpur', 
#     'Istanbul', 'Tokyo', 'Antalya', 'Seoul', 'Osaka', 'Makkah', 'Hong Kong', 
#     'Milan', 'Barcelona', 'Pattaya', 'Bali', 'Shanghai', 'Las Vegas', 'Amsterdam', 
#     'Los Angeles', 'Miami', 'Vienna', 'Prague', 'Rome', 'Taipei', 'Guangzhou', 
#     'Delhi', 'Cairo', 'Berlin', 'Moscow', 'Madrid', 'Beijing', 'Ho Chi Minh City', 
#     'Munich', 'Dublin', 'Toronto', 'Jakarta', 'Lisbon', 'Sydney', 'Budapest', 
#     'Mexico City', 'Doha', 'Rio de Janeiro', 'Buenos Aires', 'Athens', 'Stockholm', 
#     'Warsaw', 'Edinburgh', 'Brussels', 'San Francisco', 'Florence', 'Chengdu', 
#     'Marrakech', 'Hanoi', 'Manila', 'Zurich', 'Geneva', 'Venice', 'Riyadh', 
#     'Johannesburg', 'Shenzhen', 'Boston', 'Copenhagen', 'Vancouver', 'Melbourne', 
#     'Abu Dhabi', 'Phuket', 'Nice', 'Krakow', 'Chennai', 'Cape Town', 'Brisbane', 
#     'Lyon', 'Lima', 'Bogotá', 'Montreal', 'Kolkata', 'Birmingham', 'Saint Petersburg', 
#     'Seattle', 'Nagoya', 'Kyoto', 'Macau', 'Hamburg', 'Frankfurt', 'Tel Aviv', 
#     'Munich', 'Marseille', 'Sao Paulo', 'Auckland', 'Porto', 'Valencia', 'Oslo', 
#     'Gothenburg', 'Bucharest', 'Belfast', 'Helsinki', 'Perth', 'Santiago', 'Taiyuan', 
#     'Nagoya', 'Athens', 'Christchurch', 'Colombo'
# ]

# all_activities = {}

# for i in cities:
#     prompt = f"""
#     I want you to list 30 popular tourist activity in the city of {i}. For each activity, provide the following details in this specific format:

#     | Title | Price (Always in the format £10, never any other format if it is free it would be £0) | Description (max 256 characters) | Shorter Description (max 64 characters) | Type, Only chose one of the following (Cultural, Family, Relaxation, Adventure, Sports) | Group Size (e.g., 1+, 2+, etc.) | Recommended Age (Only in the format 6+, 8+ or All ages with no extra details) | Duration (Always in one of the following formats '1 hour', '2 hours', '3-4 hours') | Popularity (whole numbers 1-5) | Accessibility (Limited, Partially, Fully) |

#     Example format (for 3 activities):

#     | Sagrada Família Tour | £25 | Explore Antoni Gaudí's masterpiece, known for its intricate architecture | Take a tour around the Sagrada Família | Cultural | 1+ | 8+ | 2 hours | 5/5 | Partially
#     | Tibidabo Amusement Park | £35 | Enjoy thrilling rides at this historic amusement park atop Mount Tibidabo | Enjoy a thrilling amusement park | Adventure | 2+ | 6+ | 3-4 hours | 4/5 | Fully
#     | Camp Nou Tour | £20 | Take a tour around one of the biggest stadiums in the world, the home of FC Barcelona | Tour FC Barcelona's iconic stadium | Sports | 1+ | All ages | 1 hour | 4/5 | Limited

#     Follow this exact format. Please provide only one activity per response. Don't skip any information. Do not make it into a table. I literarrly one the example Format precisely with no alteration other than the more activities. Do not include any intro or outro text before and after the data. You must have '|' Before you start each new activity, never start an new activity without the '|' at the start.
#     """
#     response = client.generate(model=model, prompt=prompt)

#     responses = response.response.split("|")
#     activity = []
#     total_activities = []
#     first = True
#     count = 0
#     for j in responses:
#         activity.append(j)
#         count += 1
#         if count == 10 and not first:
#             total_activities.append(activity)  
#             activity = []
#             count = 0
#         elif count == 11:
#             total_activities.append(activity)  
#             activity = []
#             first = False

#     all_activities[i] = total_activities

all_activities = {'Barcelona' : 
                  [[' ', ' Gothic Quarter Walking Tour ', ' €15 ', ' Discover the medieval heart of Barcelona, featuring stunning architecture and vibrant culture. ', ' Explore the Gothic Quarter with a knowledgeable guide. ', ' Cultural ', ' 1+ ', ' All ages ', ' 2-3 hours ', ' 4/5 ', ' Fully\n\n '],
                   [' Park Güell Tour ', ' €7 ', " Visit Antoni Gaudí's unique park, filled with colorful mosaics and iconic structures. ", ' Explore the whimsical creations of Gaudí in Park Güell. ', ' Cultural ', ' 1+ ', ' 8+ ', ' 1 hour ', ' 5/5 ', ' Partially\n\n '],
                   [' Barcelona Bike Tour ', ' €25 ', ' Ride through the city on a guided bike tour, taking in famous landmarks and hidden gems. ', " Cycle around Barcelona's highlights with a knowledgeable guide. ", ' Adventure ', ' 2+ ', ' 12+ ', ' 3-4 hours ', ' 4/5 ', ' Fully\n\n '],
                   [' Aquarium Barcelona ', ' €18 ', " Explore one of Europe's largest aquariums, home to thousands of marine creatures. ", ' Discover the wonders of the ocean at the Aquarium Barcelona. ', ' Family ', ' 1+ ', ' All ages ', ' 2-3 hours ', ' 5/5 ', ' Fully\n\n ']
                  ]}

for key, item in all_activities.items():
    all_activities[key][0].remove(' ')
    for activity in range(len(item)):
        for detail in range(len(all_activities[key][activity])):
            match detail:
                case 1:
                    all_activities[key][activity][detail] = all_activities[key][activity][detail][2:-1]

                case 2 | 3:
                    all_activities[key][activity][detail] = all_activities[key][activity][detail][1:-2]
              
                case 0 | 4 | 5 | 6 | 7:
                    all_activities[key][activity][detail] = all_activities[key][activity][detail][1:-1]
                
                case 8 | 9:
                    all_activities[key][activity][detail] = all_activities[key][activity][detail][1:-3]

        new_activity = Activity(activity_city = key, activity_title = item[activity][0], activity_price = item[activity][1], 
                                activity_desc = item[activity][2], activity_short_desc = item[activity][3], activity_type = item[activity][4], 
                                activity_group_size = item[activity][5], activity_age = item[activity][6], activity_duration = item[activity][7], 
                                activity_popularity = item[activity][8], activity_accessability = item[activity][9])
        new_activity.save()