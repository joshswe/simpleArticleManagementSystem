# Articles Management System 
This simple Articles Management System web app allows users to register their accounts and login to manage their articles. They are able to (1) view all the articles they created, and (2) add, update and edit any article in their dashboards. 

**Bootstrap (HTML, CSS and JavaScript)** was used for Front-End while **Flask** (a Python micro web framework) and **MySQL** was adapted to build the Back-End.

# Demo

## Authentication

![Authentication Demo](/ArticleManagementGif/Authentication.gif)


## Add, Edit and Delete an Article

![Add_Edit_Delete_Demo](/ArticleManagementGif/Add-Edit-Delete.gif)


# Libraries Involved
## Python
- Flask
- Flask-WTF
- Flask-MySQLdb
- passlib

# MySQL Database
- Create *articlesmanagement* database
CREATE DATABASE articlesmanagement;
- Create *users* table
CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), username VARCHAR(30), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
- Create *articles* table
CREATE TABLE articles (id INT(11) AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(100), body TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

# Useful Articles
- (MySQL Commands)[https://www.pantz.org/software/mysql/mysqlcommands.html]
- Resolve MySQL connection issue:
    - (Operational Error(2003, “Can't connect to MySQL server on 'XXXX' (111)”)[https://askubuntu.com/questions/272077/port-3306-appears-to-be-closed-on-my-ubuntu-server]
    - (Host 'xxxxxxx' is not allowed to connect to this MySQL server)[https://confluence.atlassian.com/jirakb/configuring-database-connection-results-in-error-host-xxxxxxx-is-not-allowed-to-connect-to-this-mysql-server-358908249.html]
    - (How to Grant All Privileges on a Database in MySQL)[https://chartio.com/resources/tutorials/how-to-grant-all-privileges-on-a-database-in-mysql/]

- (Python Tutorial on Database Interaction)[https://www.youtube.com/watch?v=VZMiDEUL0II]
