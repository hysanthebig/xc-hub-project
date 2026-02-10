
import pandas as pd


file = r"/storage/emulated/0/pythondata/data.csv"
df = pd.read_csv(file)


#display options
pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.max_rows',None)

#sort by name and date
df["Date_dt"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
df = df.sort_values(by=["Runner","Date_dt"])
df["Date"] = df["Date_dt"].dt.strftime("%m/%d/%Y")



#useful-----------------------------------------------

def calc_avg_split(time,x):
       mint, sec = map(float, time.split(":"))
       tsec = mint * 60 + sec
       d_s = tsec / x
       nm = int(d_s / 60)
       ns = int(d_s % 60)
       if ns <= 10:
           ns = f"0{ns}"
           return f"{nm}:{ns}"
       else:
           return f"{nm}:{ns}"
  
def time_in_seconds(time):
       mint, sec = map(float, time.split(":"))
       tsec = mint * 60 + sec
       return(tsec)
  
df["time_seconds"] = df["Time"].apply(time_in_seconds)

def seconds_to_mintunes(seconds):
	mint = int(seconds//60)
	sec = round(seconds % 60,1)
	if sec < 10:
		sec = f"0{sec}"
	time = f"{mint}:{sec}"
	return(time)

#not as useful---------------------------------------

#specfic to comparison module
def race_ask_comparison():
   		try:
   			name, race, year,length = input("Enter race as format runner,race,year,length ".ljust(50)+ "|").strip().split(',')
   		except:
   			return
   
   	#mask for all
   		readmask = pd.Series(True, index = df.index)
	   	
   		col_data = df["Date"].astype(str)
   		single_year_mask = col_data.str.contains(year.strip(), case=False, na=False)
   		
   		col_data = df["Race"].astype(str)
   		single_race_mask = col_data.str.contains(race.strip(), case=False, na=False)
 		  		
 	  	col_data = df["Runner"].astype(str)
   		single_runner_mask = col_data.str.contains(name.strip(), case=False, na=False)
   		
   		col_data = df["Length"].astype(str)
   		single_length_mask = col_data.str.contains(length.strip(), case=False, na=False)
   		
	   	readmask = readmask & single_runner_mask & single_race_mask & single_year_mask & single_length_mask
	   	return(readmask)
       
#modules----------------------------------------------------
def read():
   read1 = input("Enter search: ")
   testlist = df.columns.tolist()
   for col in testlist:
       col_data = df[col].astype(str)
       readmask = col_data.str.contains(read1, case=False)
       if readmask.any() == True:
           print('')
           print(df.loc[readmask].drop(columns = ["time_seconds","Date_dt"]))
           print('')
           return
   return
   
def search_by_time():
   user_search_by_time_choice = input("Faster/Slower than MM:SS, or custom time range. FS for faster/slower, Range for custom        ").strip().lower()
   
   if user_search_by_time_choice == "fs":
   	time_input = input("Enter time as MM:SS: ")
   	time_input_sec = time_in_seconds(time_input)
   	great_o_less_o_equal = input(f"Time faster or slower than {time_input}? ").lower().strip()
   	if great_o_less_o_equal == "faster":
	       time_mask = df['time_seconds'] < time_input_sec
	       return time_mask
   	elif great_o_less_o_equal == "slower":
	       time_mask =df["time_seconds"] > time_input_sec
	       return time_mask
   
   elif user_search_by_time_choice == "range":
       print("Enter the range as MM:SS".ljust(40)+ "|")
       low_range = time_in_seconds(input("Enter lower range".ljust(40)+ "|"))
       high_range = time_in_seconds(input("Enter higher range".ljust(40)+ "|"))
       time_seconds = df["Time"].apply(time_in_seconds)
       time_mask = (low_range <= time_seconds) & (high_range >= time_seconds)
       return(time_mask)
   else:
       print("Not understood, please print FS or Range")
       search_by_time()
       
def new_race():
   new_row = {}

   new_row["Runner"] = input("Runner?".ljust(20)+ "|")
   new_row["Race"] = input("Race Name?".ljust(20)+ "|")
   new_row["Date"] = input("Date?".ljust(20)+ "|")
   new_row["Time"] = input("Time".ljust(20)+ "|")
   new_row["Placement"] = input("Placement?".ljust(20)+ "|")
   new_row["Length"] = input("Length of race".ljust(20)+ "|")


   if new_row["Length"].lower() == "3 miles":
       time = new_row["Time"]
       x = 3
       new_row["Avr spilts"] = calc_avg_split(time,x)
   else:
       new_row["Avr spilts"] = input("Average splits?".ljust(20)+ "|")


   new_row["Sport"] = input("Sport?".ljust(20)+ "|")
   new_row["Grade"] = input("Grade?".ljust(20)+"|")
   
   print('')
   df.loc[len(df)] = new_row
   print(df.tail(1))
   confirm = input("Does this match? Y/N: ")
   if confirm == "Y":
       df.to_csv(file, index=False)
       return
   else:
       print("Restarting")
       return

def advanced_search():
   
   	print("Advanced search:")
   	print("Please enter critera or press enter if no critera")
   	print("-"*100)
   
   	sport = input("XC or Track?".ljust(50)+ "|").strip()
   	season = input("Enter Seasons(Years)seperated by a comma:?".ljust(50)+ "|").strip().split(',')
   	grades = input("Enter Grades seperated by a comma:?".ljust(50)+"|").strip().split(',')
   	race_name = input ("Enter Races seperated by a comma:?".ljust(50)+ "|").strip().split(',')
   	names = input("Enter runners seperated by a comma:".ljust(50)+ "|").strip().split(',')
   	lengths = input("Enter length seperated by a comma:".ljust(50)+ "|").strip().split(',')
  
   
   	#mask for all
   	readmask = pd.Series(True, index = df.index)
   	runner_mask = pd.Series(False,index = df.index)
   	race_mask = pd.Series(False,index = df.index)
   	year_mask = pd.Series(False,index = df.index)
   	grade_mask = pd.Series(False,index = df.index)
   	length_mask = pd.Series(False,index = df.index)
 
   	if season == '':
   		year_mask = pd.Series(True,index = df.index)
   	else:
   		for year in season[0:]:
   			col_data = df["Date"].astype(str)
		   	single_year_mask = col_data.str.contains(year.strip(), case=False, na=False)
	   		year_mask = year_mask | single_year_mask
   	if grades == '':
   		grade_mask = pd.Series(True,index = df.index)
   	else :
   		for grade in grades[0:]:
  	 		col_data = df["Grade"].astype(str)
	   		single_grade_mask = col_data.str.contains(grade.strip(), case=False, na=False)
	   		grade_mask = grade_mask | single_grade_mask
   	if race_name == '':
   		race_mask = pd.Series(True,index = df.index)
   	else:
   		for race in race_name[0:]:
   			col_data = df["Race"].astype(str)
   			single_race_mask = col_data.str.contains(race.strip(), case=False, na=False)
 	  		race_mask = race_mask | single_race_mask
   	if names == '':
   		runner_mask = pd.Series(True,index = df.index)
   	else:
   		for name in names[0:]:
   				col_data = df["Runner"].astype(str)
   				single_runner_mask = col_data.str.contains(name.strip(), case=False, na=False)
   				runner_mask = runner_mask | single_runner_mask
   				
   	if lengths == '':
   		length_mask = pd.Series(True,index = df.index)
   	else:
   		for length in lengths[0:]:
   				col_data = df["Length"].astype(str)
   				single_length_mask = col_data.str.contains(length.strip(), case=False, na=False)
   				length_mask = length_mask | single_length_mask  		
   	
   	#runner sort
  
	    
   	print("Runner mask matches:", runner_mask.sum())
   	print("Race mask matches:", race_mask.sum())
   	print("Grade mask matches:", grade_mask.sum())
   	print("Year mask matches:", year_mask.sum())
   	print("Length mask matches:",length_mask.sum())
   

   	readmask = readmask & runner_mask & race_mask & grade_mask & year_mask & length_mask
   	
   	#singlesort cus normal sort wasnt working
   	if sport != '':
   		col_data = df["Sport"].astype(str)
	   	readmask = readmask & col_data.str.contains(sport, case=False)
   	      	 		
   	time_input = input("Filter by Time? Y/N".ljust(50)+ "|").lower()	
   	print("-"*100)		
   	if time_input == "y":
      	 time_mask = search_by_time()
      	 print("-"*100)
      	 readmask = readmask & time_mask
      	 print(df.loc[readmask].drop(columns = ["time_seconds","Date_dt"]))
      	 return
       	
   	else:
   	   	print(df.loc[readmask].drop(columns = ['time_seconds',"Date_dt"]))
   	   	return

def show_pr():
	print('')
	print('-'*75,'PERSONAL RECORDS', '-'*75)
	df_pr = df.copy()
	df_pr['time_seconds'] = df_pr["Time"].apply(time_in_seconds)

	df_pr = df_pr.sort_values(by=["time_seconds"])

	pr_df = df_pr.groupby("Runner")['time_seconds'].min().copy()

	pr_rows = df_pr[df_pr["time_seconds"] == df_pr["Runner"].map(pr_df)]

	
	pr_rows = pr_rows.drop(columns = ['time_seconds','Date_dt'])

	print(pr_rows)
	
	
def comparison():  
	   
	   race_ask_1 = race_ask_comparison()
	   race_ask_2 = race_ask_comparison()
	   try:
   		readmask = race_ask_1 | race_ask_2
	   except:
   		print('')
   		print("Please input runner,race,year,length all seperated by a comma")
   		print('')
   		return
	   print('')
 
	   df_comparison = df.loc[readmask].copy()
	   total_rows = len(df_comparison)
	   if total_rows < 2:
   		print("Certain races not found, check inputs")
   		print('')
   		print(df_comparison)
   		return
	   elif total_rows > 2:
   		print("Multiple races detected, outputs may be incorrect, please specfiy race")	
	   df_comparison = df_comparison.sort_values(by=["time_seconds"], ascending = False)
	   time_difference_seconds = df_comparison.loc[df_comparison.index[0], "time_seconds"] - df_comparison.loc[df_comparison.index[1], "time_seconds"]
	  	
	   time_difference = seconds_to_mintunes(time_difference_seconds)
   	
	   time_since = df_comparison.loc[df_comparison.index[0], "Date_dt"] - df_comparison.loc[df_comparison.index[1], "Date_dt"]
   	
	   if time_since.days != 0:
   		average_time_gain_per_day = round((abs(time_difference_seconds)/abs(time_since.days)),4)
	   else:
   		average_time_gain_per_day = 0
   	
	   print('-'*70)
	   print(f"{average_time_gain_per_day} average seconds change per day | {abs(time_since.days)} days in between races | {time_difference} time difference")
   	
	   print("-"*70)
	   print('')
	   print(df_comparison.drop(columns =['Date_dt']))
	   print('')
	   return
	   
def average_time_per_season():
	
	readmask = pd.Series(True, index = df.index)
	year_mask = pd.Series(False,index = df.index)
	
	print('')
	print('-'*100)
	name = input("Enter Runner's name".ljust(70)+ "|").strip()
	season = input("Enter all seasons to include, seperate each year with a comma:?".ljust(70)+ "|").strip().split(',')
	print('')
			
	for year in season:
   			col_data = df["Date"].astype(str)
		   	single_year_mask = col_data.str.contains(year.strip(), case=False, na=False)
	   		year_mask = year_mask | single_year_mask
	   
	col_data = df["Runner"].astype(str)
	single_runner_mask = col_data.str.contains(name.strip(), case=False, na=False)
	
	readmask = year_mask & single_runner_mask
	
	df_averagetime = df.loc[readmask].copy()
	total_rows = len(df_averagetime)
	if total_rows < 1:
   		print("Races not found, check inputs")
   		print('')
   		print(df_averagetime)
   		print('')
   		return
	name_tag = df_averagetime.loc[df_averagetime.index[0], 'Runner']
	total_seconds_over_season = df_averagetime['time_seconds'].sum()
	averageseconds = round(total_seconds_over_season / total_rows,3)
	average_time = seconds_to_mintunes(averageseconds)
	
	print('-'*50)		
	print(f'{name_tag} had an average time of {average_time} over {total_rows} races.')
	print('-'*50)
	print('')
	return
		
while True:
	navigate_menu = ["1. Add New Race ", "2. Search for Race ","3. Search with Filter ", "4. Show PRs","5. Compare Races",'6. Average time per races', "", "or enter break to exit"]
	print("Select Item:")
	print("-"*20)
	print("\n".join(navigate_menu))
	print("-"*20)	
	print('')
	try:
		check = input("")
		if check == "break":
			break
		else:
			selection = int(check)
		menu_selection = [new_race, read, advanced_search,show_pr, comparison,average_time_per_season]
		menu_selection[selection-1]()
	except:
		print('')
		print("Please only input from the menu")
		print('')

