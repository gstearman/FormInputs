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

from prettytable import PrettyTable
#from flask import Flask, request, render_template
#app = Flask(__name__)

# Words and lists used to look for in the freeform box for clues about stress level.
stress_red_flags = 'tired hungry worried afraid angry frustrated cranky mad sick'
stress_red_flag_list = stress_red_flags.split(" ")
stress_green_flags = 'rested happy peaceful calm'
stress_green_flag_list = stress_green_flags.split(" ")


stress_points = 0 # stress score counter
x = PrettyTable() # Table for output
x.field_names = ["Name", "Hrs Sleep/Night", "Hrs Homework/Night", "Final Exams", "Freeform", "Stress Index Score"]

# Dictionaries used to assign points for values in the drop down input boxes
sleep_points = {'Less than 4 Hours': 50, '4-6 Hours': 50, '6-7 Hours': 40, '7-8 Hours': 30, 'More than 8 Hours': 10 }
sleep_list = ['Less than 4 Hours', '4-6 Hours', '6-7 Hours', '7-8 Hours', 'More than 8 Hours']
homework_points = {'Less than 1 Hour': 10, '1-2 Hours': 20, '2-3 Hours': 25, '3-4 Hours': 35, 'More than 4 Hours': 40 }
homework_list = ['Less than 1 Hour', '1-2 Hours', '2-3 Hours', '3-4 Hours', 'More than 4 Hours']

"""@app.route('/', methods=['GET'])
def main():
    # found in ../templates/
    return render_template("main_page.html")
"""

"""@app.route('/process_inputs', methods=['POST'])
def process_inputs():
    # Get the input data from the form into variables
    name = request.form.get('input_name', '')
    sleep = request.form.get('input_sleep_dropdown', '')
    homework = request.form.get('input_homework_dropdown', '')
    final_exams_to_take = request.form.get('input_select', '')
    freeform = request.form.get('input_freeform', '')
"""
def process_inputs(name, sleep, homework, final_exams_to_take, freeform):
    freeform_list = freeform.split(" ") # create a list of all the words separated by spaces

    # Calculate stress score based upon fixed fields.
    score = sleep_points[sleep] + homework_points[homework] + (2 * int(final_exams_to_take))

    # Look at freeform field and count bad words. Add 1 for each bad stress indicating words.
    for w in freeform_list:
        if w in stress_red_flag_list:
            score += 1 # increment for a bad stress indicator word
        if w in stress_green_flag_list:
            score -= 1 # decrement for a good stress indicator word


#    message = "Hello, " + name + '. Life-stress index score: ' + str(score) + '. ' + str(sleep) + ' Hours sleep, ' + str(homework) + ' Hours homework, ' + str(final_exams_to_take) + ' Final exams to study for. '
    message = "Hello, " + name + '. '
    message = message + 'Your life-stress index score is ' + str(score) + '.  '

    if score > 70 :
#        message = '* * * DANGER * * * ' + message + ' Your stress index is too high! Take a day off and play video games in your pajammas.'
        message = '* * * DANGER * * * ' + message + ' Your stress index is too high!'
    elif score > 40 :
#        message = message + 'Your stress index is OK.    Watch TV to relax after you finish your homework and go to bed by 11 PM.'
        message = message + 'Your stress index is OK.'
    else:
#        message = message + 'Your stress index is great. You should stay up until midnight studying for final exams instead of watching TV tonight.'
        message = message + 'Your stress index is great.'

#    return render_template("main_page.html", input_data=str("Hello, " + name + '.'), output="%s" % message)
#    return message
    return str(score)

myname = 'Joe'

for s in sleep_list:
    for h in homework_list:
        for exams in [1, 2, 3, 4, 5, 6]:
            x.add_row([myname, s, h, exams, "mad",  process_inputs(myname, s, h, exams, 'mad')])

#print(process_inputs('Greg', 'Less than 4 Hours', 'More than 4 Hours', 5, 'I feel tired, sad, a little bit angry, mad, and sick'))
print(x)

x.clear_rows()
for s in sleep_list:
    for h in homework_list:
        for exams in [1, 2, 3, 4, 5, 6]:
            x.add_row([myname, s, h, exams, "mad angry",  process_inputs(myname, s, h, exams, 'mad angry')])
print(x)


print('Done.')

