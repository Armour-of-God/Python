# Hospital Management System / # Course: ITT103 - Programming Techniques
#============================================================

#importing the necessary libraries
import random

import re
from datetime import datetime

# This function checks for the validity of names
def is_valid_name(name):
    return bool(name) and name.replace(" ", "").isalpha()

# This function checks for the validity of gender input types
def is_valid_gender(gender):
    return gender.lower() in ['male', 'female', 'm', 'f', 'others']

# This function checks for the validity of date input types
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%m/%d/%Y")
        return True
    except ValueError:
        return False

# This function checks for the validity of time input types
def is_valid_time(time_str):
    return bool(re.match(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$", time_str))

# This function checks if a given date and time is available in the schedule
def is_the_available(schedule, date, time):
    return (date, time) not in schedule

# This function generates a unique ID for patients, doctors, and appointments
def generate_id(prefix):
    return f"{prefix}{random.randint(1000, 99999)}"
#------------------------------------------------------
# CLASS: Person ( Parent Class)
# Represents a generic person with their name, age and gender.
#--------------------------------------------------------------------------------------------
class Person: # Person Attributes
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def display(self):# Display the person's information
        print(f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}")

#------------------------------------------------------
# CLASS: Patient Management( inherits from the Person Class)
# Adds patient_id and appointment_list
#--------------------------------------------------------------------------------------------
class Patient(Person):
    def __init__(self, name, age, gender): # Patient Attributes
        super().__init__(name, age, gender)
        self.patient_id = generate_id("P")
        self.appointment_list = []


    def add_appointment(self, appointment): # Add an appointment to the patient's appointment list
        self.appointment_list.append(appointment)

    def profile_view(self): # View Patient Profile information
        print("\n******* Patient Profile Information*******")
        self.display()
        print(f"Patient ID: {self.patient_id}")
        print("Appointments: ")
        if self.appointment_list:
            for appt in self.appointment_list:
                print(f"Assign to Dr. {appt.doctor.name} on {appt.date} at {appt.time}")
        else:
            print("No appointments scheduled, Please contact the hospital for an appointment.")
#------------------------------------------------------
# CLASS: Doctor Management (inherits from the Person Class)
# Adds doctor_id, speciality, and schedule
#--------------------------------------------------------------------------------------------
#class inherits from the main class Person
class Doctor(Person): # Doctor Attributes being inherited from Person Class
    def __init__(self, name, age, gender, speciality): # Doctor speciality
        super().__init__(name, age, gender)
        self.doctor_id = generate_id("D")
        self.speciality = speciality
        self.schedule = []

    def is_available (self, date, time): # Check if the doctor is available on a given date and time
        return is_the_available(self.schedule, date, time)

    def view_schedule(self): # View Doctor Schedule information
        print(f" === Schedule for Dr. {self.name} ===")
        if self.schedule:
            for date,time in self.schedule:
                print(f"{date} at {time}")
        else:
            print("No appointments scheduled or available at this time.")


#------------------------------------------------------
# CLASS: Appointment Scheduling (inherits from the Person Class)
# Appointment between a patient and a doctor
#--------------------------------------------------------------------------------------------

class Appointment: # Appointment Attributes
    def __init__(self, patient, doctor, date, time):
        self.appointment_id = generate_id("A")
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Confirmed"


    def confirm (self): # confirming the appointment being scheduled
        print(f"\nAppointment Confirmed for Dr. {self.doctor.name} - Your Appointment ID is: {self.appointment_id}")

    def cancel(self): # cancelling the scheduled appointment
        self.status = "Cancelled"
        print(f"\nAppointment {self.appointment_id} has been cancelled.")

#------------------------------------------------------
# CLASS: System for the Hospital
# This section manages the system for (patients, doctors and appointments)
#--------------------------------------------------------------------------------------------

class Hospital_Management_System_Interface_Setup:
    def __init__(self):
        self.patient       = {}
        self.doctor        = {}
        self.appointment   = {}


    def add_patient(self, name, age, gender): # registering a new patient
        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            print("Invalid age. Please enter a valid number.") # error message displayed if the age is not a number or is zero
            return

        patient = Patient(name, age, gender.capitalize()) #displaying the patient ID and registration completion message
        self.patient[patient.patient_id] = patient
        print(f"\n ******* Patient Registration Completed Successfully! *******")
        print(f"Patient Registration ID # is: {patient.patient_id} \n ")
        print()

    def add_doctor(self, name, age,gender, speciality): # registering a new doctor
        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            print("Invalid age. Please enter a valid number") # error message displayed if the age is not a number or is zero
            return

        doctor = Doctor(name, age, gender.capitalize(), speciality)
        self.doctor[doctor.doctor_id] = doctor
        print(f"\n Doctor Profile Created Successfully, Your ID # is: {doctor.doctor_id}") # displaying the doctor ID and registration completion message

    def book_appointment(self,patient_id,doctor_id, date, time):
        patient = self.patient.get(patient_id)
        doctor = self.doctor.get(doctor_id)

        if not patient or not doctor: # checking if the patient and doctor information exist
            print("Invalid Patient or Doctor Information. Please check and try again.")
            return

        if not doctor.is_available(date, time): # checking if the doctor is available
            print(f"Dr. {doctor.name} is not available on {date} at {time}. Please choose another time.")
            return

        appointment = Appointment(patient, doctor, date, time) #updating the appointment information
        self.appointment[appointment.appointment_id] = appointment
        patient.add_appointment(appointment)
        doctor.schedule.append((date, time))
        appointment.confirm()


    def cancel_appointment(self, appointment_id): # cancelling an appointment
        appointment = self.appointment.get(appointment_id)
        if appointment:
            appointment.cancel()
        else:
            print("This appointment does not exist. Please check the appointment ID and try again.") # error message displays, if the appointment does not exist


    def generate_bill(self, appointment_id): # generating a bill for the appointment
        appointment = self.appointment.get(appointment_id)
        if not appointment or appointment.status != "Confirmed":
            print("Invalid or cancelled appointment. Please check the appointment ID and try again.")
            return

        print("\n       ******* Marvell Service hospital Bill Receipt *******")
        print("             123 Marvell Avenue, Montego Bay, Jamaica ")
        print("Telephone: (876) 555-1234 | Fax: (876) 555-1345 | Email:MSHospital@gmai.com")
        print("*******-------*******-------*******-------*******-------*******-------******* \n")
        print("Please wait while we generate your bill...")
        print(f"Patient: {appointment.patient.name} ")
        print(f"Doctor: {appointment.doctor.name} ")
        print(f"Date & Time: {appointment.date} at {appointment.time} ")
        print("*******-------*******-------*******-------*******-------*******-------******* \n")

        consultation_fee = 3000 # Fixed cost for consultation
        print(f"Service Provided: Consultation Fee JMD ${consultation_fee}")
        try:
            additional_services = float(input("Please enter the additional services provided (if any tests/medication): JMD $"))
            if additional_services < 0:
                raise ValueError
        except ValueError:
            print("Invalid input. additional services cannot be zero.") # error message displayed if the input is not a number or is zero
            additional_services = 0
            return

        total_bill = consultation_fee + additional_services # Total bill calculation
        print(f"TOTAL BILL AMOUNT: JMD ${total_bill}")
        print()
        print("******* Thank you for choosing MS hospital. We wish you a speedy recovery! ******* \n")

#------------------------------------------------------
# Main Program Loop options
# Display the main menu and handle user input options
#--------------------------------------------------------------------------------------------

def main():
    hospital = Hospital_Management_System_Interface_Setup()  # Linking the main menu with the main functions

    while True:
        print(" \n*******===== Marvell Service Hospital Management System =====******* \n")
        print("==============================================================================")
        print("Please select an option from the menu listing below to continue \n")
        print("1. New Patient Registration")
        print("2. New Doctor Registration")
        print("3. Book Appointment")
        print("4. Cancel Appointment")
        print("5. View Patient Profile")
        print("6. View Doctor Schedule")
        print("7. Generate Billing Statement")
        print("8. Exit Menu \n")
        print("*******===M===*******===S===*******===H===*******===M===*******===S===*******")

        option = input("\nOption Selected: ").strip()

        # New Patient Registration
        if option == "1":
            name = input("Patient Name: ").strip()
            if not is_valid_name(name):
                print("Invalid name. Only letters and spaces allowed.")
                continue
            age = input("Patient Age: ").strip()
            gender = input("Patient Gender (Male/Female/Others): ").strip()
            if not is_valid_gender(gender):
                print("Invalid gender. Please enter Male, Female, or Others.")
                continue
            hospital.add_patient(name, age, gender)

        # New Doctor Registration
        elif option == "2":
            name = input("Doctor Name: ").strip()
            if not is_valid_name(name):
                print("Invalid name. Only letters and spaces allowed.")
                continue
            age = input("Doctor Age: ").strip()
            gender = input("Doctor Gender (Male/Female/Others): ").strip()
            if not is_valid_gender(gender):
                print("Invalid gender. Please enter Male, Female, or Others.")
                continue
            speciality = input("Doctor Speciality: ").strip()
            if not speciality:
                print("Speciality cannot be empty.")
                continue
            hospital.add_doctor(name, age, gender, speciality)

        # Book Appointment
        elif option == "3":
            pid = input("Enter Patient ID: ").strip()
            did = input("Enter Doctor ID: ").strip()
            date = input(" Date (mm/dd/yyyy: ").strip()
            time = input("Time (HH:MM AM/PM): ").strip()
            if not is_valid_date(date):
                print("Invalid date format MM/DD/YYYY")
                continue
            time = input("Time (HH:MM AM/PM): ").strip()
            if not is_valid_time(time):
                print("Invalid time format HH:MM AM/PM")
                continue
            hospital.book_appointment(pid, did, date, time)

        # Cancelling an Appointment
        elif option == "4":
            appointment_id = input("Enter Appointment ID to cancel: ").strip()
            hospital.cancel_appointment(appointment_id)

        # View Patient Profile
        elif option == "5":
            patient_id = input("Enter Patient ID to view profile: ").strip()
            patient = hospital.patient.get(patient_id)
            if patient:
                patient.profile_view()
            else:
                print("Invalid Patient ID. Please check and try again.")

        # View Doctor Schedule
        elif option == "6":
            doctor_id = input("Enter Doctor ID to view schedule: ").strip()
            doctor = hospital.doctor.get(doctor_id)
            if doctor:
                doctor.view_schedule()
            else:
                print("No doctor schedule found. Please check and try again.")

        # Generate Billing Statement
        elif option == "7":
            appointment_id = input("Enter Appointment ID to generate bill: ").strip()
            hospital.generate_bill(appointment_id)

        # Exit the program
        elif option == "8":
            print("Thank you for using the Marvell Service Hospital Management System. Goodbye!")

            break

        else:
            print("Invalid option selected. Select a number from 1 to 8 in the list and try again.")  # error message displayed if the option is not valid


# This is to execute the program code
if __name__ == "__main__":
    main()