# P1 — Requirements Classification

Chosen value: **N = 3** upcoming appointments per patient.

## Functional requirements

- **R1:** A patient can view the days and times when a doctor is available.
- **R2:** A patient can book an appointment during an available time slot.
- **R3:** A doctor can accept or decline an appointment request.
- **R4:** A patient can have at most N upcoming appointments at any given time. For this project, N = 3. Only future appointments with `Pending` or `Accepted` status count toward the limit. `Declined`, `Cancelled`, and past appointments do not count.

## Non-functional requirements

- **R5 — Security:** Patient medical data shall be accessible only to authorized staff. In a production system, this would be addressed with authentication, role-based authorization, least-privilege access, and secure storage. Full medical-record access control is outside this simple console implementation.
- **R6 — Performance:** Available appointment times shall be displayed within 2 seconds. In a production system, efficient queries, indexes, and performance monitoring would help meet this target. This assignment does not require performance testing.
- **R7 — Usability:** The application shall be usable on mobile phone screens. A production web interface would use responsive design and mobile-device testing. The assignment permits a console application, so mobile UI implementation is not required.
