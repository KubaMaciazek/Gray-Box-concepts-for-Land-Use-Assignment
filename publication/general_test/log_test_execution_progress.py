import time


def log_test_execution_progress(test_nr, starting_time, nr_of_tests, thread_nr):
    test_nr = test_nr + 1
    hours, minutes = format_hours_minutes(time.time() - starting_time)
    print('Seed: ' + str(thread_nr) + ' test: ' + str(test_nr) + '/' + str(nr_of_tests) + ' | ' + f"Duration: {hours} hours and {minutes} minutes")
    return test_nr

def format_hours_minutes(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes
