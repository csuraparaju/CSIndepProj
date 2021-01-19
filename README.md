# Automatic Dementia Detection Through Voice
An Amazon Web Services based python program that takes in user speech recordings and produces a score indicating whether their voice show early signs of dementia or
not. There are two parts to the program, both consisting of their own score. Part one prompts the user to describe a memory or experience that relates to a certain
topic. From this speech recordings, the program analyzes for specific biomarkers of demetia (such as slow speech rate, high pause rate, low syllable count, simple 
vocabulary, etc). The main rational behind this process is because research has shown that people with dementia often pause mid sentence when speaking in a casual 
conversations. Additionally, research has also shown that their vocabulary often reverts to a simpler version.

The score for part two comes from a modified version of the MMSE (Mini Mental Status Examination). This step assesses the user's current mental status and 
datermines if there is anything abnormal. The user is asked a set of questions, and their responses are recorded in the format of a .wav file. These speech 
recordings are then converted to a text output and are checked for the correct response. Each question correct grants the user with one point. Their final score 
will be the sum of score for part 1 and part 2.


# Dependencies:
   • Aws Boto3 library\
   • Flask Web Application Framework\
   • Inflect Engine\
   • Natural Language Toolkit (NLTK)\
   • Pydub  

Note: The user interface for this program is still a work in progress. Check back later to view the final version.
