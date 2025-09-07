# Overview

This is a Flask web application for "Amasijos Arcabuco" that implements a basic authentication system with PostgreSQL database integration. The application provides user login functionality with session management using Flask-Login. It features a simple MVC architecture with user authentication, template rendering, and database connectivity for managing user accounts.

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