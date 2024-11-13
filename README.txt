We are building a miniature version of Amazon, where sellers can create product listings and users can browse and purchase products using virtual currency. Users can review products and sellers, and transactions are conducted within the website.

## Progress Summary Since Milestone 1:
All contributed in combininb our database and ER diagram

- **William Chen (Users Guru)**:  Drafted the database schema for Account/Purchases and drew out relational tables as well as the constraints. Worked on formalizing page by page mock up. 

- **Prashamsa Koirala (Products Guru)**: Drafted the database schema for Products and drew out relational tables as well as the constraints. Worked on formalizing page by page mock up. 

- **Brian Kim (Cars Guru)**: Drafted the database schema for Cart/Order and drew out relational tables as well as the constraints. Worked on formalizing page by page mock up. 

- **Joanne Chae (Sellers Guru)**: Drafted the database schema for Inventory/Order Fulfillment and drew out relational tables as well as the constraints. Worked on formalizing page by page mock up. 

- **Kevin Lee (Social Guru)**: Drafted the database schema for Feedback/Messaging and drew out relational tables as well as the constraints. Worked on formalizing page by page mock up. 

## Progress Summary Since Milestone 2:

- Where to find implementation of our progress:

Front end:
- Everything is under app/templates, there are .html files that have each page of our application as well as calling neccesary api endpoitns for the interaction/functionality with the data in our database

Back end:
- under create.sql we defined/implemented all our relations as planned in milestone 1 with some minor changes in the schema-
- Under app/models, there is a file that represents each model "object" for our application that holds specific attribuets to that model as well as functions to interact with that model
- Under app/ there will be .py files that serve as controllers to define api endpoints/routes. these routes call functions in the model directory to perform neccesary tasks.

Link to short video demo:
https://drive.google.com/file/d/1DgyEpF8W8QaoExLHqn26lzhSmPfWX3hA/view?usp=drive_link

## Progress Summary Since Milestone 3:

Front-End:
= Each page's load time was optimized by compressing images and enabling caching for frequently accessed components. 
- Enhanced navigation tools, such as a sidebar for product filters, were implemented to improve usability.
- Logged-in users now see a personalized recommendations section.

Back-End:
- A new search indexing service was integrated to improve search speed and accuracy.
- Enhanced error handling and logging were added to the checkout and payment processes to ensure smoother, more reliable transactions.

Link to short video demo:
https://drive.google.com/drive/folders/10dkpG4RA1bvF4scwr8mjEoF4dM2I1aGY?usp=drive_link
