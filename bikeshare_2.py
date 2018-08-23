import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # Get user input for city (chicago, new york city, washington).
    # Collecting only a valid answer for city input using while loop, lower case answers acceptable
    city = input('Choose a city from: Chicago, New York City or Washington: ')
    city = city.lower();
    # Validate input to match file name with while loop
    while city not in ['chicago', 'new york city', 'washington']:
        print ('You may have a typo or an invalid city, please try again.')
        city = input('Choose a city from: Chicago, New York City or Washington: ')
        city = city.lower()

    # Get user input for month (all, january, february, ... , june)
    # Collecting only a valid answer for month input using while loop, lower case answers acceptable
    month = input('Choose a month from: January, February, March, April, May, June or choose All: ')
    month = month.lower();
    # Validate input to match file name with while loop
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print ('You may have a typo or an invalid month, please try again.')
        month = input('Choose a month from: January, February, March, April, May, June or choose All: ')
        month = month.lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    # Collecting only a valid answer for day input using while loop, lower case answers acceptable
    day = input('Choose a day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or choose All: ')
    day = day.lower();
    # Validate input to match file name with while loop
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print ('You may have a typo or an invalid selection, please try again.')
        day = input('Choose a day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or choose All: ')
        day = day.lower()
    # Printing the selection made by the user
    print("\nGreat, thanks for choosing this combination, City: {}, Month: {} and Day: {}!".format(city.title(),month.title(),day.title()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loads data file into a dataframe based on city selection from user
    df = pd.read_csv(CITY_DATA[city])

    # Converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable if selected by user
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        # Adding the +1 to from index to actual month
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable selected by user
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract and display the most common month using mode and the calendar import for name
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('The most common starting month is:', calendar.month_name[popular_month])

    # Extract and display the most common day of week using mode and the calendar import for name
    df['day'] = df['Start Time'].dt.weekday
    popular_day = df['day'].mode()[0]
    print('The most common starting day is:', calendar.day_name[popular_day])

    # Extract and display the most common hour from the Start Time column to create an hour column
    # Then use mode. Add .00 to end as string to make hour more readable
    df['hour'] = df['Start Time'].dt.hour.astype(str) + '.00'
    popular_hour = df['hour'].mode()[0]
    print('The most common starting hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # Display most commonly used start station using mode
    popular_start_station = df ['Start Station'].mode()[0]
    print('The most popular starting station is: ', popular_start_station)

    # Display most commonly used end station using mode
    popular_end_station = df ['End Station'].mode()[0]
    print('The most popular ending station is: ', popular_end_station)

    # Add a 'with ' to beginning of End station for user readability
    # Create a new column combining start and end station
    # Display most frequent combination of start station and end station trip
    # Additional note printed in case user is confused with same start and end station
    df ['End Station'] = ' with ' + df ['End Station'].astype(str)
    popular_combo_station = (df ['Start Station'] + df ['End Station']).mode()[0]
    print('The most popular combination of starting and ending stations is:', popular_combo_station)
    print('\nNote: If the combination of stations is the same, users may have taken rides in a loop.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time using sum and round to remove decimal points on seconds
    # Duration converted to days, hours, mins, secs for user readability using divmod
    total_travel_time = df ['Trip Duration'].sum().round().astype(int)
    print('The total duration of trips is: ', total_travel_time, 'seconds, or in a more reader friendly format:')
    m, s = divmod(total_travel_time, 60)
    h, m = divmod(m, 60)
    da, h = divmod(h, 24)
    print('%d days %02d hrs %02d mins %02d secs' % (da, h, m, s))

    # Display mean travel time using mean and round to remove decimal points on seconds
    # Mean time converted to mins, secs for user readability using divmod
    mean_travel_time = df ['Trip Duration'].mean().round().astype(int)
    print('\nThe mean duration of trips taken is: ',mean_travel_time, 'seconds, or in a more reader friendly format:')
    m, s = divmod(mean_travel_time, 60)
    print('%d mins %02d secs' % (m, s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types using value_counts
    user_types = df['User Type'].value_counts()
    print('The User Types are shown below:\n', user_types)

    # Display counts of gender with a while loop using KeyError to bypass the non-existent Washington data
    while True:
        try:
            gender = df['Gender'].value_counts()
            print('\nThe genders of users are shown below:\n', gender)
            break
        except KeyError:
            print ('\nGender data is not available for Washington')
            break

    # Display earliest, most recent, and most common year of birth
    # Again using a while loop with KeyError to bypass non-existent Washington data
    while True:
        try:
            birth_year_early = df['Birth Year'].min().round().astype(int)
            birth_year_recent = df['Birth Year'].max().round().astype(int)
            birth_year_most = df['Birth Year'].mode()[0].round().astype(int)

            print('\nThe earliest birth year of users is:', birth_year_early)
            print('The most recent birth year of users is:', birth_year_recent)
            print('The most common birth year of users is:', birth_year_most)
            break
        except KeyError:
            print ('\nBirth year data is not available for Washington')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # Defines the data and basis of a loop to see if the user wants to see the raw data in groups of 5 rows
    raw_question = ''
    i = 0
    while raw_question != 'no':
        raw_question = input('\nWould you like to see raw data for selected city? Enter yes or no. \n')
        raw_question = raw_question.lower()
        print(df.ix[i:i+4])
        i = i+5
def main():
    # Loading the dataframes based on the input from the user for each of the sections for stats
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Redefining original dataframe after minor manipulation in stats sections previously
        # Ensuring all city remains as a selection from user, month and day remain as all since that is the raw data
        df = load_data(city, month = "all", day = "all")
        raw_data(df)

        # Requests user to restart the program for new input values or quit
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

# Various searches in StackOverFlow, the Udacity forum and Slack channel provided valuable insight into how to modify code and incorporate to satisfy the criteria
