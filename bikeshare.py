import time
import pandas as pd
import datetime

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

"""
  A constant variable that stores a dictionary of valid inputs 
  for filtering the bikeshare data by city, month and day.
"""
VALID_USER_INPUTS = {
    "cities": ["chicago", "new york city", "washington"],

    "months": ["january",
               "february",
               "march",
               "april",
               "may",
               "june",
               "july",
               "august",
               "september",
               "october",
               "november",
               "december",
               "all"],

    "days": [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "all",
    ],
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    while True:
        city = input(
            "Please select Chicago, New York City, or Washington: "
        ).lower()
        if city in VALID_USER_INPUTS["cities"]:
            break
        print("Error! Valid options are Chicago, New York City, or Washington. ")

    while True:
        month = input(
            "Please select a month or 'all' :  "
        ).lower()
        if month in VALID_USER_INPUTS["months"]:
            break
        print(
            "Error! Valid options are months, or 'all'. ")

    while True:
        day = input(
            "Please select a day of the week, or 'all': "
        ).lower()
        if day in VALID_USER_INPUTS["days"]:
            break
        print("Error! Valid options are a day of the week or 'all'. ")

    print("-" * 40)
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
    df = pd.read_csv(CITY_DATA[city], parse_dates=[
                     "Start Time", "End Time"], infer_datetime_format=True)

    #  Create new column in the df for 'hour'
    df['hour'] = df['Start Time'].dt.hour

    #  Create new column in the df for 'day_of_week'
    df['day_of_week'] = df['Start Time'].dt.day_of_week

    #  Create new column in the df for 'month'
    df['month'] = df['Start Time'].dt.month

    # If a month has been specified then need to filter the df
    if month != 'all':
        specified_month = VALID_USER_INPUTS["months"].index(month)
        # months are not zero indexed in the df so need to add 1
        specified_month += 1

        df = df[df['month'] == specified_month]

    if day != 'all':
        specified_day = VALID_USER_INPUTS["days"].index(day)
        df = df[df['day_of_week'] == specified_day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    print('Most common month is ',
          VALID_USER_INPUTS["months"][most_common_month-1].capitalize())  # subtract 1 for indexing

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]

    print('Most common day is ',
          VALID_USER_INPUTS["days"][most_common_day].capitalize())

    # display the most common start hour
    most_common_starting_hour = df['hour'].mode()[0]
    print('Most popular starting hour is', most_common_starting_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_starting_station = df['Start Station'].mode()[0]
    print('Most Popular Starting Station', most_common_starting_station)

    # display most commonly used end station
    most_common_ending_station = df['End Station'].mode()[0]
    print('Most Popular Ending Station', most_common_ending_station)

    # display most frequent combination of starting and ending station
    most_common_station_combination = (
        df['Start Station'] + ','+df['End Station']).mode()[0]
    print('Most Popular Starting/Ending Combination',
          most_common_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    hours, remainder = divmod(total_travel_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("Total travel time: %d hours, %d minutes, %d seconds" %
          (hours, minutes, seconds))

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    avg_travel_time_delta = datetime.timedelta(seconds=average_travel_time)
    minutes, seconds = divmod(avg_travel_time_delta.seconds, 60)
    print("Average travel time: {} mins, {} secs".format(minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("-" * 40)
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame())
    print("-" * 40)

    # Display counts of gender
    try:
        df['Gender'].fillna("Not specified", inplace=True)
        gender_series = df['Gender'].value_counts()

        for key, value in gender_series.items():
            print("{}: {}".format(key, value))

    except KeyError:
        print("Error: Gender is not present in this dataset.")

    print("-" * 40)

    # Display earliest, most recent, and most common year of birth

    try:
        # Earliest year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year', int(earliest_birth_year))

        # Display most recent year of birth
        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year', int(most_recent_birth_year))
        print("-" * 40)

        # Display most common year of birth
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most common birth year', int(most_common_birth_year))
    except KeyError:
        print("Error: Birth Year is not present in this dataset.")

    print("-" * 40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def raw_data_display(df):
    """This function is used to display 10 rows of raw data from the dataframe at a time."""
    print("--------------------- Raw data display -------------------------")
    number_of_raw_data_items = 10

    start = 0
    end = number_of_raw_data_items

    while True:
        print(df[start:end])

        cont = user_continue_check(
            "\nWould you like the next " + str(number_of_raw_data_items) + " rows of raw data? Enter yes or no.\n")
        if cont == False:
            break

        start += number_of_raw_data_items
        end += number_of_raw_data_items


def user_continue_check(display_message):
    """Used to check for positive response from user"""
    result = False
    cont = input(display_message)
    if cont.lower() == "yes":
        result = True
    return result


def main():
    print("Starting program..")
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            restart = user_continue_check(
                "\n There is no data availabe, would you like to choose new options? Enter yes or no.\n")
            if restart == False:
                break
            else:
                continue

        raw_data_display(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = user_continue_check(
            "\nWould you like to restart? Enter yes or no.\n")
        if restart == False:
            break


if __name__ == "__main__":
    main()
