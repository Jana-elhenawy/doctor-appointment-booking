"""Simple console Doctor Appointment Booking System.

R1-R4 are implemented. N = 3 future Pending + Accepted appointments per patient.
No third-party dependencies are required.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse


N = 3
DATE_FORMAT = "%Y-%m-%d %H:%M"


@dataclass
class Patient:
    patient_id: str
    name: str


@dataclass
class TimeSlot:
    slot_id: str
    start_time: datetime
    is_booked: bool = False


@dataclass
class Doctor:
    doctor_id: str
    name: str
    specialty: str
    available_slots: list[TimeSlot]


@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    slot_id: str
    start_time: datetime
    status: str = "Pending"


class AppointmentService:
    ACTIVE_LIMIT_STATUSES = {"Pending", "Accepted"}
    ALL_STATUSES = {"Pending", "Accepted", "Declined", "Cancelled"}

    def __init__(self, max_upcoming_appointments: int = N):
        if max_upcoming_appointments < 1:
            raise ValueError("The appointment limit must be at least 1.")
        self.max_upcoming_appointments = max_upcoming_appointments
        self.patients: dict[str, Patient] = {}
        self.doctors: dict[str, Doctor] = {}
        self.appointments: dict[str, Appointment] = {}
        self._next_appointment_number = 1

    def add_patient(self, patient: Patient) -> None:
        self.patients[patient.patient_id] = patient

    def add_doctor(self, doctor: Doctor) -> None:
        self.doctors[doctor.doctor_id] = doctor

    def get_available_slots(self, doctor_id: str) -> list[TimeSlot]:
        """R1: Return future, unbooked slots for a doctor."""
        doctor = self.doctors.get(doctor_id)
        if doctor is None:
            raise ValueError("Doctor not found.")
        now = datetime.now()
        return [
            slot for slot in doctor.available_slots
            if slot.start_time > now and not slot.is_booked
        ]

    def count_upcoming_appointments(self, patient_id: str) -> int:
        """R4: Count only future Pending and Accepted appointments."""
        now = datetime.now()
        return sum(
            1 for appointment in self.appointments.values()
            if appointment.patient_id == patient_id
            and appointment.start_time > now
            and appointment.status in self.ACTIVE_LIMIT_STATUSES
        )

    def book_appointment(self, patient_id: str, doctor_id: str, slot_id: str) -> Appointment:
        """R2/R4: Validate slot and limit, then create a Pending request."""
        if patient_id not in self.patients:
            raise ValueError("Patient not found.")
        doctor = self.doctors.get(doctor_id)
        if doctor is None:
            raise ValueError("Doctor not found.")

        slot = next((s for s in doctor.available_slots if s.slot_id == slot_id), None)
        if slot is None:
            raise ValueError("Slot not found for this doctor.")
        if slot.start_time <= datetime.now():
            raise ValueError("Cannot book a slot in the past.")
        if slot.is_booked:
            raise ValueError("This slot is no longer available.")

        if self.count_upcoming_appointments(patient_id) >= self.max_upcoming_appointments:
            raise ValueError(
                f"Appointment limit reached: maximum {self.max_upcoming_appointments} "
                "upcoming Pending/Accepted appointments."
            )

        appointment_id = f"A{self._next_appointment_number:03d}"
        self._next_appointment_number += 1
        appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            slot_id=slot.slot_id,
            start_time=slot.start_time,
            status="Pending",
        )
        self.appointments[appointment_id] = appointment
        slot.is_booked = True
        return appointment

    def review_appointment(self, doctor_id: str, appointment_id: str, decision: str) -> Appointment:
        """R3: Doctor accepts or declines a pending request."""
        if decision not in {"Accept", "Decline"}:
            raise ValueError("Decision must be Accept or Decline.")
        appointment = self.appointments.get(appointment_id)
        if appointment is None:
            raise ValueError("Appointment not found.")
        if appointment.doctor_id != doctor_id:
            raise ValueError("This appointment does not belong to this doctor.")
        if appointment.status != "Pending":
            raise ValueError("Only Pending appointments can be reviewed.")

        appointment.status = "Accepted" if decision == "Accept" else "Declined"
        if appointment.status == "Declined":
            self._release_slot(appointment)
        return appointment

    def cancel_appointment(self, patient_id: str, appointment_id: str) -> Appointment:
        appointment = self.appointments.get(appointment_id)
        if appointment is None:
            raise ValueError("Appointment not found.")
        if appointment.patient_id != patient_id:
            raise ValueError("This appointment does not belong to this patient.")
        if appointment.start_time <= datetime.now():
            raise ValueError("Only upcoming appointments can be cancelled.")
        if appointment.status not in self.ACTIVE_LIMIT_STATUSES:
            raise ValueError("Only Pending or Accepted appointments can be cancelled.")

        appointment.status = "Cancelled"
        self._release_slot(appointment)
        return appointment

    def _release_slot(self, appointment: Appointment) -> None:
        doctor = self.doctors[appointment.doctor_id]
        for slot in doctor.available_slots:
            if slot.slot_id == appointment.slot_id:
                slot.is_booked = False
                break


def create_demo_service() -> AppointmentService:
    """Create sample data with future slots so the demo can be run immediately."""
    service = AppointmentService(max_upcoming_appointments=N)
    service.add_patient(Patient("P001", "Alex Patient"))

    start = (datetime.now() + timedelta(days=1)).replace(
        hour=9, minute=0, second=0, microsecond=0
    )
    slots = [
        TimeSlot("S001", start),
        TimeSlot("S002", start + timedelta(hours=1)),
        TimeSlot("S003", start + timedelta(days=1)),
        TimeSlot("S004", start + timedelta(days=1, hours=1)),
        TimeSlot("S005", start + timedelta(days=2)),
    ]
    service.add_doctor(Doctor("D001", "Dr. Sara", "General Practice", slots))
    return service


def run_demo() -> None:
    service = create_demo_service()
    print("Doctor Appointment Booking System — Demo")
    print(f"Upcoming appointment limit N = {service.max_upcoming_appointments}")
    print("\nAvailable slots for Dr. Sara:")
    for slot in service.get_available_slots("D001"):
        print(f"  {slot.slot_id}: {slot.start_time.strftime(DATE_FORMAT)}")

    appointment = service.book_appointment("P001", "D001", "S001")
    print(f"\nCreated request {appointment.appointment_id}: {appointment.status}")
    service.review_appointment("D001", appointment.appointment_id, "Accept")
    print(f"Doctor decision: {appointment.status}")
    print("Demo completed successfully.")


def run_menu() -> None:
    service = create_demo_service()
    print("Doctor Appointment Booking System")
    print("Demo data: Patient P001; Doctor D001 (Dr. Sara).")
    while True:
        print("\n1. View available slots")
        print("2. Book an appointment")
        print("3. View appointments")
        print("4. Doctor: accept/decline request")
        print("5. Cancel an appointment")
        print("0. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                doctor_id = input("Doctor ID (D001): ").strip() or "D001"
                slots = service.get_available_slots(doctor_id)
                if not slots:
                    print("No available future slots.")
                else:
                    for slot in slots:
                        print(f"{slot.slot_id}: {slot.start_time.strftime(DATE_FORMAT)}")
            elif choice == "2":
                patient_id = input("Patient ID (P001): ").strip() or "P001"
                doctor_id = input("Doctor ID (D001): ").strip() or "D001"
                slot_id = input("Slot ID: ").strip()
                appointment = service.book_appointment(patient_id, doctor_id, slot_id)
                print(f"Request created: {appointment.appointment_id} ({appointment.status})")
            elif choice == "3":
                if not service.appointments:
                    print("No appointments yet.")
                for a in service.appointments.values():
                    print(
                        f"{a.appointment_id}: patient={a.patient_id}, doctor={a.doctor_id}, "
                        f"time={a.start_time.strftime(DATE_FORMAT)}, status={a.status}"
                    )
            elif choice == "4":
                doctor_id = input("Doctor ID (D001): ").strip() or "D001"
                appointment_id = input("Appointment ID: ").strip()
                decision = input("Type Accept or Decline: ").strip().capitalize()
                appointment = service.review_appointment(doctor_id, appointment_id, decision)
                print(f"Appointment status is now {appointment.status}.")
            elif choice == "5":
                patient_id = input("Patient ID (P001): ").strip() or "P001"
                appointment_id = input("Appointment ID: ").strip()
                appointment = service.cancel_appointment(patient_id, appointment_id)
                print(f"Appointment {appointment.appointment_id} cancelled.")
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Choose one of the listed options.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Doctor Appointment Booking System")
    parser.add_argument("--demo", action="store_true", help="run a short demonstration")
    args = parser.parse_args()
    run_demo() if args.demo else run_menu()
