#
# Code2College FormInput Template Example
#
# This branch uses the basic template form example to create a Stress-o-meter Analyzer.
# This example is an implementation of the original idea by Roberto S. in the class at PHS.
# This example collects form input data with questions (hrs sleep/night, hrs homework/night, # final exams next week)
# and uses the input provided to calculate a life stress score. It also asks for a free form text response on the question "How do you feel?".
# It then returns a different output message with advice based upon the calculated stress score.
#
# This python code illustrates how to turn inputs into calculated values a few different ways:
#   It uses dictionaries for input string key to value pairing for drop down fields
#   It uses counts of good/bad keyword string matching in a free-form input box.
# The code is here on the stress_test branch: https://github.com/gstearman/FormInputs.git
# See this link for the source change diff in GitHub: https://github.com/mough/FormInputs/compare/master...gstearman:stress_test
# The app may be running here:  http://gstearman.pythonanywhere.com
#

#
# Imports
#
from prettytable import PrettyTable  # This is new for capturing output from the site in a formatted table
from flask import Flask, request, render_template
app = Flask(__name__)

#
# Global Variables
#

# Words and lists used to look for clues about stress level in the freeform box field.
stress_red_flags = 'tired hungry worried afraid angry frustrated cranky mad sick'
stress_red_flag_list = stress_red_flags.split(" ")
stress_green_flags = 'rested happy peaceful calm'
stress_green_flag_list = stress_green_flags.split(" ")

stress_points = 0 # stress score counter

x = PrettyTable() # Table to hold formatted output received from the user
x.field_names = ["Name", "Hrs Sleep/Night", "Hrs Homework/Night", "Final Exams", "Freeform", "Stress Index Score"]


# Dictionaries used to assign points for values in the drop down input boxes
sleep_points = {'Less than 4 Hours': 50, '4-6 Hours': 50, '6-7 Hours': 40, '7-8 Hours': 30, 'More than 8 Hours': 10 }
sleep_list = ['Less than 4 Hours', '4-6 Hours', '6-7 Hours', '7-8 Hours', 'More than 8 Hours']
homework_points = {'Less than 1 Hour': 10, '1-2 Hours': 20, '2-3 Hours': 25, '3-4 Hours': 35, 'More than 4 Hours': 40 }
homework_list = ['Less than 1 Hour', '1-2 Hours', '2-3 Hours', '3-4 Hours', 'More than 4 Hours']

#
# Functions
#

def calc_stress_score(name, sleep, homework, final_exams_to_take, freeform):
    """This function calculates a stress score from 1-100 using the inputs."""
    freeform_list = freeform.split(" ") # create a list of all the words in the freeform text box (separated by spaces).

    score = sleep_points[sleep] + homework_points[homework] + (2 * int(final_exams_to_take)) # First part of calculation is here.

    # Look at red_flag list and the freeform field to count bad words. Add 1 for each bad stress indicating word.
    for w in stress_red_flag_list:
        if w in freeform_list:
            score += 1 # increment for a bad stress indicator word
    # Look at green_flag list and the freeform field and count good words. Subtract 1 for each good word.
    for w in stress_green_flag_list:
        if w in freeform_list:
            score -= 1 # decrement for a good stress indicator word

    return score
# calc_stress_score


@app.route('/', methods=['GET'])
def main():
    # found in ../templates/
    return render_template("main_page.html")
# main

# For web requests called via http:
@app.route('/process_inputs', methods=['POST'])
def process_inputs():
    # Get the input data from the form into variables
    name = request.form.get('input_name', '')
    sleep = request.form.get('input_sleep_dropdown', '')
    homework = request.form.get('input_homework_dropdown', '')
    final_exams_to_take = request.form.get('input_select', '')
    freeform = request.form.get('input_freeform', '')

    # Calculate stress score based upon fixed fields.
    score = calc_stress_score(name, sleep, homework, final_exams_to_take, freeform)

    # Log results to a file on the server using PrettyTable
    x.add_row([name, sleep, homework, final_exams_to_take, freeform,  score])
    g = open('results.txt', 'w')
    g.write(str(x))
    g.close

    message = 'Hello, ' + name + '. ' + 'Your life-stress index score is ' + str(score) + '.'
    if score > 70 :
        message = '* * * DANGER * * * ' + message + '  Your stress index is too high! Take a day off and play video games in your pajammas.'
    elif score > 40 :
        message = message + 'Your stress index is OK. Watch TV to relax after you finish your homework and go to bed by 11 PM.'
    else:
        message = message + 'Your stress index is great. You should stay up until midnight studying for final exams instead of watching TV tonight.'

#    return render_template("main_page.html", output=" %s " % str(x).replace('|+-','|+**-'))
#    return render_template("main_page.html", input_data=str(x), output=" %s " % message)
    return render_template("main_page.html", output=" %s " % message)
# process_inputs


# For local testing not called via http:
def process_test_inputs(name, sleep, homework, final_exams_to_take, freeform):
    # Calculate stress score based upon fixed fields.
    score = calc_stress_score(name, sleep, homework, final_exams_to_take, freeform)
    x.add_row([name, sleep, homework, final_exams_to_take, freeform,  score])
# process_test_inputs



#
# Execution starts here
#

# Open a file on the server for local test case results and write the heading to it.
#g = open('results.txt', 'w')
#g.write('Local Test Case Results:\n')
#g.close

# Just print to the console for local test results.
print('\n\n\nLocal Test Case Results:\n')

# Here we can put some test cases to call the process_inputs function and log the output.

# Local test #1
myname = 'Joe_beta_tester1'
# Loop through the inputs. NOTE: process-inputs already has the code to write the results to a file!
for s in sleep_list:
    for h in homework_list:
        for exams in [1, 2, 3, 4, 5, 6]:
            process_test_inputs(myname, s, h, exams, 'I feel mad.')
print(str(x))  # Print the completed table of test #1 results

# Local test #2
myname = 'Julie_beta_tester2'
x.clear_rows() # Remove the data from Joe_beta_tester1 from the table so we write a new table for this case
h = '2-3 Hours'
exams = 3
for s in sleep_list:
    process_test_inputs(myname, s, h, exams, 'I feel mad and hungry. I am also tired and calm.')
print(str(x))  # Print the completed table of test #2 results

x.clear_rows() # Remove the data from Julie_beta_tester2 from the table so web results are in a new table.

print('\nNow recording real data captured from the web site:\n')
# Open a file on the server for results and write the table header to it.
g = open('results.txt', 'w')
g.write('Now recording real data captured from the web site:\n')
g.close
print("Done.")


