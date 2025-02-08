# Konsultasi_Web

![Project Status](https://img.shields.io/badge/status-completed-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue)

This project is a case study for the **NoSQL Database** course, implemented using **Python 3.12.3**, the **Flask** framework, and **MongoDB** as the database.

## Technologies Used
- **Python 3.12.3**: Backend logic and API development.
- **Flask**: Web framework for handling HTTP requests.
- **MongoDB**: NoSQL database for storing consultation data.
- **HTML, CSS, JavaScript**: Frontend technologies for UI development.
- **Bootstrap 5**: Responsive design and UI components.

## Features
- **User Authentication**: Login and registration system.
- **Profile Management**: Users can update their profile information.
- **Consultation Management**: Schedule and manage consultations.
- **CRUD Operations**:
  - **Departments**
  - **Students**
  - **Competencies**
  - **Lecturers**
  - **Users**
- **User-Friendly Interface**: Clean and responsive UI for easy navigation.

## Demo

### Landing Page
- The homepage of the application.

  <img src="https://github.com/user-attachments/assets/769758e1-f7f8-4a16-b05a-ef0aaf3ae626" alt="Landing Page" width="600">
  <img src="https://github.com/user-attachments/assets/a7e2ef31-f7c8-48dd-a696-c9b4ad526686" alt="Landing Page Alt" width="600">

### Login/Register
- User authentication system.

  <img src="https://github.com/user-attachments/assets/f23d1e01-e7a1-471b-9d23-b3de73f5c8db" alt="Login/Register" width="600">

### Edit Profile
- Users can update their personal information.

  <img src="https://github.com/user-attachments/assets/40562aad-889b-4063-8ad6-4feeb42fe723" alt="Edit Profile" width="600">

### Consultation Data
- Displays a list of all scheduled consultations.

  <img src="https://github.com/user-attachments/assets/4ba3bb4e-c5d5-44c4-85fa-e5f68e4e963c" alt="Consultation Data" width="600">

### Create Consultation
- Users can create a new consultation session.

  <img src="https://github.com/user-attachments/assets/1c46358a-fa39-4e6b-abe5-ed79d3d0ed17" alt="Create Consultation" width="600">

### CRUD Features

#### Departments
  <img src="https://github.com/user-attachments/assets/811c7c4a-7dfa-4e9e-8939-d5d9f2b3cb1a" alt="CRUD Departments" width="600">

#### Students
  <img src="https://github.com/user-attachments/assets/b90ca4cd-06f2-44b3-91aa-0821221269b3" alt="CRUD Students" width="600">

#### Competencies
  <img src="https://github.com/user-attachments/assets/1a396f47-4d59-41d8-8542-2770d175416c" alt="CRUD Competencies" width="600">

#### Lecturers
  <img src="https://github.com/user-attachments/assets/85bae017-0a36-46ff-a69b-91a9c9866853" alt="CRUD Lecturers" width="600">

#### Users
  <img src="https://github.com/user-attachments/assets/9759b880-11d0-4267-9be3-f5227161bffa" alt="CRUD Users" width="600">

## Setup

1. **Install Python 3.12.3**  
   Download Python from the [official Python website](https://www.python.org/).

2. **Clone the Repository**  
   Open your terminal and execute:
   ```bash
   git clone <repository_url>
   cd Konsultasi_Web
   
3. Set up a virtual environment and activate it:
   ```
   python -m venv env
   cd env/Scripts
   activate
   cd ../..
   ```
4. Install the required Python packages:
   ```
   pip install flask pymongo
   ```
5. Run the application:
   ```
   py app.py
   ```

## Usage
1. Open a browser and navigate to `localhost:5000`.
2. Register or log in to access the features.
3. Manage consultations, edit profiles, and use CRUD functionalities.
4. All data is stored in the MongoDB database.

## Project Status
This project is **completed** and will not be further developed.

## Contributions
Feel free to submit issues or contribute by creating pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
