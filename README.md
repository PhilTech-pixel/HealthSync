This project focuses on enabling secure and efficient interoperability between two hospitals (Hospital A and Hospital B) using a Django-based web application. The system allows both hospitals to exchange patient biodata and medical records via a centralized API, improving continuity of care and reducing redundant data entry.

Each hospital maintains its own database with key models such as UserProfile, DoctorProfile, PatientProfile, MedicalRecord, and Hospital. An API interface enables authorized data requests based on patient ID, while a custom logic ensures unique identification to prevent conflicts due to duplicate patient IDs across hospitals.

The system includes a logging mechanism (DataExchangeLog) to track data access and queries for auditing and accountability. It is designed to support future enhancements for secure access control.
