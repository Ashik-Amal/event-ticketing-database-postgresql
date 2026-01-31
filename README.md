# Event Ticketing Database – PostgreSQL

## Overview
This project implements a relational database for managing events, spectators, ticket sales, and ticket cancellations.  
It was developed using PostgreSQL and pgAdmin as part of an academic mini-project.

## Features
- Entity–Relationship (ER) modeling
- Primary key and foreign key constraints
- CHECK constraints for data validation
- Transactional SQL queries
- Reporting queries using JOIN, GROUP BY, and subqueries

## Database Schema
Entities:
- Event
- Spectator
- Ticket
- Cancel

Relationships:
- One spectator can attend many events
- One event can have many spectators
- Each ticket may be cancelled at most once

## Transactions Implemented
- Insert spectator and event
- Issue tickets with capacity and uniqueness checks
- Delete spectators and events with business rules
- Reports for ticket counts, schedules, and cancellations
- Ticket validity checking

## Tools & Technologies
- PostgreSQL
- pgAdmin
- SQL
- GitHub
  
## Python Integration
The database was integrated with Python using the psycopg2 library.

Python scripts were developed to:
- Connect to the PostgreSQL database
- Execute transactional SQL queries
- Generate analytical reports
- Check ticket validity and cancellation status



  



