Preliminary Design Doc for log color coding program


Object of this program: 
	It will be able to color code the log files that it is provided. Each of the log files have lines that look something like this:

	2016-03-07 23:08:51.748 27883 DEBUG oslo_service.service [-] keystone_authtoken.check_revocations_for_cached = False log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2341

	There are different sections of these lines, such as date/time, the PID, DEBUG, the module (oslo_service.service) etc. The goal is to make a program the colors each of these components a different color. 


Inputs to the program could be:
	We would be passing in multiple log files into the program. 
	Two ways to do that. One would be to pass the log files in as an argument like this:
		./color_log_file.py hello.txt world.txt ....
	Another way would be to pipe the output of the the previous log parsing file into this program like this:
		cat hello.txt | color_log_file.py

Output of the program could be:
	It could just output the contents of the file(s) to stdout with all lines properly colored. 
	Or it could output a seperate txt file, and that file would be a colored. 





These are the functions I'm planning for the program right now. Things may change later. Need to think about the inputs and outputs of each of the functions more. But this is a basic prelim outline.


# It could take in a line as input, and output all of the different sections (like the ones said above) of this line as a tuple perhaps. Using 
# regex matching.
# Need to use the re python library. Don't know too much amount regular expressions in general so will need to research this. Since this is the 
# bulk of the work. 
get_all_tokens(line) 

# This function would simply just read the file, and maybe output a list of lines in that file that it just opened and read.
read_file()

# This function could process the list of lines of the file. On each line, the get_all_tokens function would be called. 
process_lines()

# There could also be a simple function that processes user inputs. We can have the -f and have them specify which files they want to color code
process_user_inputs()

# A main for calling each of the functions above.
main()
	read_file()
	process_user_inputs()
	process_lines()....get_all_tokens() called inside here perhaps?



Possible test cases for unit testing the above functions, and possible edge cases. 

get_all_tokens()
Since this function would actually parse the line using regex, we would need unit tests for each section of the lines. 
For example, one for the date/time, one for the module, etc. 
1. Datetime check
2. Module name check
3. Flag type check
4. Also try lines with no date/time, or none of any of these sections. 
etc


read_file()
Since this function reads the files, its difficult to unit test. Maybe won't have any for this function. 


process_lines()
For this we can pass in a chuck on lines as input for the test functions.
The cases for different types of lines can be things like:
1. Lines with no date/time the beginning
2. Lines with and without the req number.
3. Lines with the req number that start with different character. 


process_user_inputs()
1. When user puts in no files to be processed. 
2. When user puts in a random string.
3. When user forgets an option, if options are even allowed. 
