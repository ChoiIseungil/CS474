# Written by Seungil Lee, Nov 30, 2021

input("""
    Welcome to Korean Issue Tracker 2015-2017,
    Developed by Seungil Lee, Yunho Lee and Hyeann Lee

    This is implemented for a term project of the course: 2021 Fall CS474 Text Mining, instructed by Prof. Sung-Hyon Myaeng
    Please contact silly5921@kaist.ac.kr if you have any feedback

    Press Enter to continue
    Press Ctrl+C any time you want to exit"""
    )

while True:
    YEAR = input("""
         
    Choose the year you want to investigate among 2015, 2016, 2017
    Input: """)

    if YEAR not in ['2015','2016','2017']:
        print("""
    Only 2015, 2016, and 2017 are available years
            """)

    else: break

while True:
    MODE = input("""
         
    Choose the mode
        1. Issue Trend Analysis
        2. On-issue Event Tracking
        3. Related-issue Event Tracking 
        Input: """)

    if MODE not in ['1','2','3']:
        print("""
    Input is not valid, please check once again
        """)

    else: break

if MODE == 1:
    year = input("""
    Choose the mode
        1. Issue Trend Analysis
        2. On-issue Event Tracking
        3. Related-issue Event Tracking 
    Input: """)
    
elif MODE == 2:
    pass
elif MODE == 3:
    pass