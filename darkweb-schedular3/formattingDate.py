from datetime import datetime, timedelta
import re

def clndate(date,date_formats):
    try:
        
        result = re.search(r"^[A-Za-z]+\s\d{1,2},\s\d{4},\s\d{2}:\d{2}\s[A-Z]{2}", date).group()
        for date_format in date_formats:
            try:
                date_object = datetime.strptime(result, date_format)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                print(new_date_string)
                return new_date_string
            except:
                pass

    except:
        pass

def date_formating(date_string):
    date_formats = [ '%Y-%m-%d %H:%M:%S', '%Y-%m-%d','%m-%d-%Y', '%Y/%m/%d,%H:%M:%S', '%d-%m-%Y','%d-%m-%Y,%H:%M:%S','%m-%d-%Y,%H:%M:%S', '%d-%m-%Y %H:%M:%S', '%B %d, %Y, %I:%M %p', '%b %d, %Y, %I:%M %p', '%Y%m%dT%H%M%S.%fZ', '%Y%m%dT%H%M%S.%f%z', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S.%f', '%Y/%m/%d', '%d.%m.%Y', '%d.%m.%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %I:%M %p', '%m/%d/%y %I:%M:%S %p', '%m/%d/%y %I:%M %p', '%d %B %Y', '%d %b %Y', '%d %B %y', '%d %b %y', '%d,%m,%Y,%I:%M %p', '%m,%d,%Y,%I:%M:%S %p', '%Y,%m,%d,%H:%M:%S', '%m,%d,%y,%I:%M:%S %p', '%d,%b,%Y,%I:%M %p', '%d/%m/%Y %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f%z','%m-%d-%Y, %I:%M %p','%Y-%m-%dT%H:%M:%S+00:00','%Y-%m-%dT%H:%M:%S','%Y-%m-%dT%H:%MZ','%Y-%m-%dT%H:%M:%S+0000']

    for date_format in date_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            new_format="%Y-%m-%d %H:%M:%S"
            new_date_string = date_object.strftime(new_format)
            return new_date_string
        except :
            try:
                new_date_string = clndate(date_string,date_formats)
                if new_date_string:
                    return new_date_string
            except:
                pass  
                        
            #Today with hrs
            try:      
                match = re.search("(\d+) hours", date_string) or re.search("(\d+) Hours", date_string) or re.search("(\d+) hrs", date_string) or re.search("(\d+) Hrs", date_string) or re.search("(\d+) hrs.", date_string) or re.search("(\d+) Hrs.", date_string) or re.search("Today,(\d+) hours", date_string) or re.search("Today,(\d+) Hours", date_string) or re.search("Today,(\d+) hrs", date_string) or re.search("Today,(\d+) Hrs", date_string) or re.search("Today,(\d+) hrs.", date_string) or re.search("Today,(\d+) Hrs.", date_string)  or re.search("today,(\d+) hours", date_string) or re.search("today,(\d+) Hours", date_string) or re.search("today,(\d+) hrs", date_string) or re.search("today,(\d+) Hrs", date_string) or re.search("today,(\d+) hrs.", date_string) or re.search("today,(\d+) Hrs.", date_string)
                if match:
                    hours = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(hours=hours)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            #Days (25 Days ago)
            try:      
                match = re.search("(\d+) days", date_string) or re.search("(\d+) Days", date_string) or re.search("(\d+) day", date_string) or re.search("(\d+) Day", date_string) or re.search("(\d+) hrs.", date_string) 
                if match:
                    days = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(days=days)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            #Days (25 months ago)
            try:      
                match = re.search("(\d+) month", date_string) or re.search("(\d+) Month", date_string) or re.search("(\d+) months ago", date_string) or re.search("(\d+) Months", date_string) 
                if match:
                    months= int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(30*months)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
                               
            # today with minutes              
            try:      
                match = re.search("(\d+) minutes", date_string) or re.search("(\d+) Minutes", date_string) or re.search("(\d+) min", date_string) or re.search("(\d+) Min", date_string) or re.search("(\d+) min.", date_string) or re.search("(\d+) Min.", date_string) or re.search("Today,(\d+) minutes", date_string) or re.search("Today,(\d+) Minutes", date_string) or re.search("Today,(\d+) min", date_string) or re.search("Today,(\d+) Min", date_string) or re.search("Today,(\d+) min.", date_string) or re.search("Today,(\d+) Min.", date_string)  or re.search("today,(\d+) minutes", date_string) or re.search("today,(\d+) Minutes", date_string) or re.search("today,(\d+) min", date_string) or re.search("today,(\d+) Min", date_string) or re.search("today,(\d+) min.", date_string) or re.search("today,(\d+) Min.", date_string)
                if match:
                    minutes = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(minutes=minutes)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            # Seconds ago
            try:      
                match = re.search("(\d+) seconds", date_string) or re.search("(\d+) Seconds", date_string) or re.search("(\d+) sec", date_string) or re.search("(\d+) Sec", date_string) or re.search("(\d+) sec.", date_string) or re.search("(\d+) Sec.", date_string)
                if match:
                    second = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(seconds=second)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            # year ago
            try:      
                match = re.search("(\d+) year", date_string) or re.search("(\d+) Year", date_string) or re.search("(\d+) yrs", date_string) or re.search("(\d+) Yrs", date_string) or re.search("(\d+) yrs.", date_string) or re.search("(\d+) Yrs.", date_string)
                if match:
                    years = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(365*years)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            # week ago
            try:      
                match = re.search("(\d+) week", date_string) or re.search("(\d+) Week", date_string) or re.search("(\d+) weeks", date_string) or re.search("(\d+) Weeks", date_string) 
                if match:
                    week = int(match.group(1))
                else:
                    raise ValueError("Invalid date string format")
                now = datetime.now()
                date_object = now - timedelta(7*week)

                new_format="%Y-%m-%d %H:%M:%S"
                new_date_string = date_object.strftime(new_format)
                return new_date_string
            except:
                pass
            
            # sunday, 11pm
            try: 
                day_pattern = r'(mon|tue|wed|thu|fri|sat|sun|Mon|Tue|Wed|Thu|Fri|Sat|Sun)day'  
                time_pattern = r'(\d{1,2})(am|pm)' 

                match = re.match(f'{day_pattern},{time_pattern}', date_string) or re.match(f'{day_pattern}, {time_pattern}', date_string) or re.match(f'{day_pattern} ,{time_pattern}', date_string)
                day_of_week = match.group(1)
                hour = int(match.group(2))
                if match.group(3) == 'pm':
                    hour += 12

                now = datetime.now()
                days_until_next_day_of_week = (7 - now.weekday() + ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun' ,'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ].index(day_of_week)) % -7
                next_day_of_week = now + timedelta(days=days_until_next_day_of_week)

                final_datetime = next_day_of_week.replace(hour=hour, minute=0, second=0)
                final_string = final_datetime.strftime('%Y-%m-%d %H:%M:%S')

                return final_string  
                
            except:
                pass   


# -----------------------------------------------------------------------------------------

            # # February 22, 2022   #error 
            # try:      
            #     match = re.search(r"(\w+) (\d+), (\d+)") 
            #     if match:
            #         month = match.group(1)
            #         day = match.group(2)
            #         year = match.group(3)
            #     else:
            #         raise ValueError("Invalid date string format")
            #     # now = datetime.now()
            #     now = datetime.now()
            #     date_object = now - timedelta(7*week)
            #     new_format="%Y-%m-%d %H:%M:%S"
                
            #     date_object = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
            #     print(date_object)
            #     new_date_string = date_object.strftime("%Y-%m-%d %H:%M:%S")
            #     return new_date_string
            # except:
            #     pass

            # # December 3, 2022  #error
            # try:      
            #     date_pattern = r'(\w+?)\s+(\d{1,2}),\s+(\d{4})'
            #     time_pattern = r'(\d{1,2})(am|pm)'

            #     # Extract the date and time information from the string
            #     match = re.match(f'{date_pattern}\s+{time_pattern}', 'December 3, 2022 11pm')
            #     month = match.group(1)
            #     day = int(match.group(2))
            #     year = int(match.group(3))
            #     hour = int(match.group(4))
            #     if match.group(5) == 'pm':
            #         hour += 12

            #     # Create a datetime object with the extracted date and time information
            #     dt = datetime(year, datetime.strptime(month, '%B').month, day, hour, 0, 0)

            #     # Convert the datetime object into the desired format
            #     final_string = dt.strftime('%Y-%m-%d %H:%M:%S')

            #     return final_string
            # except:
            #     pass

             
            
def date_coverter(input_date):
    output = date_formating(input_date)
    # print(output)
    dt = datetime.strptime(output, "%Y-%m-%d %H:%M:%S")
    print(dt)
    timestamp = int(dt.timestamp())
    return timestamp

print(date_coverter("sunday,11pm")) #add input




# ----done ------

# 1 min ago
# "10-17-2020, 09:38 PM"
# "2023-01-17T17:40:42Z"
# "8 hours ago"
# "28-02-2023"
#2-02-2023
# 22-12-2023
# "12-22-2023,03:34:45"
# 25 days ago
# 1 hours ago
# 1 years ago
# 1 months ago
# February 22, 2022
# 2021-06-01T09:23:01+00:00
# 2023-03-03T17:46:12
# 2021-06-01T09:23:01+00:00
# 2023-01-04T01:15Z
# 2023-01-02T02:31:40+0000
# 01-21-2008, 03:35 PM
# Sunday,11pm


# -----done---

# 01-21-2008, 03:35 PM (This post was last modified: 01-21-2008, 04:18 PM by Kuroda_Shun.)
# This post was last modified: March 26, 2022, 12:12 AM by Ura.)
# Saturday at 01:25
# March 2
# February 3
# February 22, 2022
# November 2, 2022
# December 3, 2022
# January 29, 2023, 04:14
# Sep 6,2022
