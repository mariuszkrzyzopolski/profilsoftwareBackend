# profilsoftwareBackend

# Installation
- import environment from environment.yml for anaconda or from requirements.txt for pip
- activate new environment
- in project directory initialize script(python script.py --start web/local)

# Commands
## --start [web/local]
start program and import data from local(option=local) person.json or from the api(option=web).Needed run first to initialize, after that not necessary and will overwrite last database

## -percentage-sex [all]
show percentage of men and women in database

## -average-age [all/men/women]
show average age of all people,men or women

## -popular-city [number_of_results]
list the most popular cities from database

## -popular-password [number_of_results]
list the most popular passwords from database

## -start-birth [Start_date] -end-birth [End_date]
The range of users born after start date and before end date.Format is YYYY-MM-DD

## -best-password [number_of_results]
List of best password meet that criteria:
- 1 point - have at least one lowercase letter
- 2 points - have at least one uppercase letter
- 1 point - have at least on digit
- 5 points - it is at least 8 length
- 3 points - have a special character

