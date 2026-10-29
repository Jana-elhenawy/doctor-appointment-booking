# P4 — Candidate Classes

| Candidate class | Evidence from requirements/use cases | Classification | Decision |
|---|---|---|---|
| `Patient` | Patient views slots, requests/cancels appointments, and has an upcoming appointment limit (R1, R2, R4). | Explicit | Keep |
| `Doctor` | Doctor availability and accept/decline actions are required (R1, R3). | Explicit | Keep |
| `Appointment` | A booking request has a time and status and may be Pending, Accepted, Declined, or Cancelled (R2–R4). | Inferred | Keep |
| `TimeSlot` | R1 requires available days and times; R2 requires booking a specific slot. | Inferred | Keep |
| `AppointmentService` | Booking validation, availability checks, limit checks, and status updates are coordinated operations. | Inferred | Keep |
| `Payment` | No requirement mentions payment or fees. | Rejected | Do not implement |
| `MedicalRecord` | R5 mentions protection of medical data, but the required working flow does not include medical-record operations. | Rejected for core workflow | Explain R5 in design/README; do not add unnecessary scope |
| `Notification` | No requirement asks for notifications. | Rejected | Do not implement |
