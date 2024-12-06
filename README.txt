We are building a miniature version of Amazon, where sellers can create product listings and users can browse and purchase products using virtual currency. Users can review products and sellers, and transactions are conducted within the website.

## Progress Summary Since Milestone 1:
All contributed to combining our database and ER diagram.

- **William Chen (Users Guru)**:  Drafted the database schema for Accounts/Purchases and drew out relational tables and constraints. Worked on formalizing page-by-page mock-up. 

- **Prashamsa Koirala (Products Guru)**: Drafted the database schema for Products and drew out relational tables and constraints. Worked on formalizing page-by-page mock-up. 

- **Brian Kim (Cars Guru)**: Drafted the database schema for Cart/Order and drew out relational tables and constraints. Worked on formalizing page-by-page mock-up. 

- **Joanne Chae (Sellers Guru)**: Drafted the Inventory/Order Fulfillment database schema and drew out relational tables and the constraints. Worked on formalizing page-by-page mock-up. 

- **Kevin Lee (Social Guru)**: Drafted the database schema for Feedback/Messaging and drew out relational tables and constraints. Worked on formalizing page-by-page mock-up. 


## Progress Summary Since Milestone 2:

- Where to find the implementation of our progress:

Front end:
- Everything is under app/templates, there are .html files that have each page of our application as well as calling necessary API endpoints for the interaction/functionality with the data in our database

Back end:
- under create.sql we defined/implemented all our relations as planned in milestone 1 with some minor changes in the schema-
- Under app/models, there is a file that represents each model "object" for our application that holds specific attributes to that model as well as functions to interact with that model
- Under app/ there will be .py files that serve as controllers to define API endpoints/routes. these routes call functions in the model directory to perform necessary tasks.

Link to short video demo:
https://drive.google.com/file/d/1DgyEpF8W8QaoExLHqn26lzhSmPfWX3hA/view?usp=drive_link


## Progress Summary Since Milestone 3:

Front-End:
- Added a dynamic search bar and category filters on the homepage and improved the product listing view with pagination controls so users can efficiently browse larger sets of products.
- Integrated a review section under each product, allowing users to leave text reviews and star ratings.
- Displayed an average rating calculation on the product page based on submitted reviews.

Back-End:
- Created RESTful APIs to handle requests for user profile updates, product search, category management, cart operations, and reviews. 
- Integrated error handling mechanisms to return meaningful error messages for cases like duplicate emails or insufficient stock.
- Implemented pagination in API responses to handle large product datasets efficiently, only loading a subset of products per page.
- Implemented a review aggregation service to compute average ratings for products based on submitted reviews and included stock verification logic within the cart API, so users cannot add more items to the cart that is available in stock.

Link to short video demo:
https://drive.google.com/drive/folders/10dkpG4RA1bvF4scwr8mjEoF4dM2I1aGY?usp=drive_link


## Final Project Progress Summary:

Front-End:
- Added a temporary cart feature for unauthenticated users, allowing them to add products to a session-based cart
- Enhanced the product search with dynamic ranking and filters by category, price, and average ratings
- Added validation messages for registration errors (e.g., duplicate emails, invalid email formats)
- Included a user-friendly account update interface with real-time input validation
- Improved the cart view with a real-time total price calculation
- Added a checkout failure feedback mechanism for issues like insufficient balance or unavailable inventory
- Integrated interface for submitting, editing, and deleting reviews
- Added detailed order pages accessible from transaction history, showing fulfillment status and timestamps
- Designed an inventory management UI for adding, updating, and removing products
- Implemented fulfillment tools for marking items and orders as fulfilled

Backend:
- Added validation for email and password fields during registration
- Implemented unique email constraints to prevent duplicates
- Enforced inventory validation during cart operations and checkout
- Added balance verification logic to prevent insufficient balance transactions
- Enhanced error handling to provide precise feedback for checkout failures
- Implemented logic to validate and restrict users to a single review per product/seller
- Created APIs for fetching, updating, and deleting reviews
- Aggregated average ratings for products and sellers dynamically
- Added APIs for sellers to manage fulfillment statuses and timestamps
- Updated the backend logic to decrement inventory and adjust balances correctly during checkout

Link to short video demo:
https://drive.google.com/drive/folders/10dkpG4RA1bvF4scwr8mjEoF4dM2I1aGY?usp=drive_link
