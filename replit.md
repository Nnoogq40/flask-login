# Overview

This is a Flask web application for "Amasijos Arcabuco" that implements a comprehensive ERP-like system with PostgreSQL database integration. The application provides user authentication, product catalog with real-time stock management, shopping cart functionality, contact forms, and administrative panels. It features a complete MVC architecture with inventory control, order management, and responsive design for all devices.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask**: Core web framework handling routing, request processing, and response generation
- **Flask-Login**: Manages user sessions and authentication state
- **Jinja2 Templates**: Server-side rendering with template inheritance using base templates

## Database Layer
- **PostgreSQL**: Primary database for storing user information
- **psycopg2**: PostgreSQL adapter for Python database connectivity
- **Custom Database Connection Class**: Manages database connections with connection pooling logic
- **Model Layer**: Implements data access patterns with ModelUser class for user operations

## Authentication System
- **Password Security**: Uses Werkzeug's password hashing for secure password storage and verification
- **Session Management**: Flask-Login handles user session persistence and login state
- **User Entity**: UserMixin integration provides Flask-Login compatibility

## Frontend Architecture
- **Bootstrap 5**: CSS framework for responsive UI components
- **Template Structure**: Base template with block inheritance for consistent layout
- **Static Assets**: Organized CSS and JavaScript files for styling and interactions
- **Swiper.js**: JavaScript library for carousel/slider functionality

## Application Structure
- **MVC Pattern**: Separation of concerns with models, views (templates), and controllers (routes)
- **Configuration Management**: Environment-based configuration with development settings
- **Error Handling**: Flash messaging system for user feedback and error display

## Security Features
- **CSRF Protection**: Secret key configuration for session security
- **Password Hashing**: Secure password storage using Werkzeug utilities
- **Login Required Decorators**: Route protection for authenticated access

## Inventory Management System (ERP Features)
- **Real-time Stock Control**: Live inventory tracking with automatic stock updates
- **Product Database**: Complete product catalog with prices, descriptions, and stock levels
- **Purchase Validation**: Prevents overselling and validates stock availability before orders
- **Visual Stock Indicators**: Color-coded stock levels (Green: normal, Yellow: low, Red: out of stock)
- **Order Integration**: Automatic stock reduction when orders are processed
- **Stock API**: RESTful endpoints for real-time stock queries

## Recent Updates
- **September 8, 2025**: Implemented complete inventory management system
- **Key Features Added**:
  - Products table with stock tracking
  - Real-time stock validation
  - Visual stock indicators in UI
  - Automatic stock reduction on purchases
  - Stock availability API endpoints
  - Enhanced order processing with inventory control

# External Dependencies

## Database
- **PostgreSQL**: Primary database system accessible via DATABASE_URL environment variable
- **Default Connection**: Configured for Replit environment with helium database

## Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework loaded from CDN for responsive design
- **Swiper.js**: JavaScript carousel library for interactive components

## Python Packages
- **Flask**: Web framework
- **psycopg2**: PostgreSQL database adapter
- **Flask-Login**: User session management
- **Werkzeug**: WSGI utilities including password hashing

## Development Tools
- **VS Code**: Development environment configuration with JavaScript debugging support