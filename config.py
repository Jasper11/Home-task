from datetime import datetime
date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

url_login = 'https://qa-int-brand.vm.cogniance.com/np/login'
url_workouts_categories = 'https://qa-int-brand.vm.cogniance.com/np/workout/categories'
url_view_workout = 'https://qa-int-brand.vm.cogniance.com/np/exerciser/'
credentials = {'username': 55445544, 'password': 1212}
workout_id = 4240912
wrong_workout_id = 4240912312
view_workouts_parameters = '?interval=single&intervalCount=1&startDate=19910101'
view_workouts_invalid_parameters = '?interval=single&startDate=19910101'
header = {'Content-Type': 'multipart/form-data'}
files = {'file': open('Untitled-1.jpg', 'rb')} # jpeg file should be in same directory where script is.
invalid_manual_parameters = '?workoutDateTimeNoTz=' + date + 'timezone=US/Pacific&category=1&duration=170'
create_workout_params = '?workoutDateTimeNoTz=' + date + '&timezone=Europe/Kiev&category=15&duration=45&calories=450&distance=5&comment=created&equipmentType=Treadmill'