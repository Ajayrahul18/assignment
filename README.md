# assignment
Degin - https://app.diagrams.net/#G1meskhgktO0Uxs_gGQSXUJYAmn33Cmt8h

In the above I have desgined database schema 
    Implemented the fields in the model

models.py:

    1. Created the User class to store the information of the users.
    
    2. Created the Expense class to store the data while creating the expense.
    
              1. In the Expense model one of the field is a choise filed to select between "EXACT", "EQUAL", "PERCENTAGE", which helps in creating the share amount for each user.
              
              2. Also Implemented the function "calculate_exact_amount" - which check with choise field and calculates the share for each user and updates in the data base field.
                 
    3. Created the IndividualExpense class which saves the data that is calculated for the each user and the paid user

views.py:

    1. created a function "home_page" which gets the data of users form the database and pass it to the "home.html"(basic html) page which shows the data in 
    
       table format  which also shows the how much the user owes to the other users.
    2. create a function "create_expense" which get the data after the user filled the form  fields ("Amount", "Paid by", "Expense Type", "Users") when the save 
    
       button is clicked the function save it to the database and updates the user share amount.
       
Email:

    1 Used Celery and a message broker to send the message through the mail implimented in the "task.py" file modeified the "calcualte_exact_amount" function to send mail to the users.
    
    2. used "schedule" package to send the weekly mail to the users
