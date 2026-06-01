# Step 2: Authentication & Session Management

## Overview
Implement user registration, login, and session management to allow secure user authentication and maintain logged-in state.

## Objectives
1. Handle form submissions for registration and login
2. Validate user input (email, password, confirm password)
3. Hash passwords securely using Werkzeug
4. Create and manage user sessions
5. Protect routes that require authentication
6. Implement logout functionality

## Scope

### Register (`/register`)
- **Form**: Collect name, email, password, confirm password
- **Validation**:
  - Email must be valid format
  - Email must be unique (check database)
  - Password must match confirm password
  - Password must be at least 8 characters
  - All fields required
- **Processing**:
  - Hash password using `werkzeug.security.generate_password_hash()`
  - Insert user into `users` table
  - Create session
  - Redirect to dashboard or profile
- **Error Handling**: Display validation errors on form

### Login (`/login`)
- **Form**: Collect email and password
- **Validation**:
  - Both fields required
  - Email must exist in database
  - Password must match hash in database
- **Processing**:
  - Use `werkzeug.security.check_password_hash()` to verify password
  - Create session
  - Redirect to dashboard or profile
- **Error Handling**: Display "Invalid email or password" on failure

### Session Management
- **Implementation**: Flask sessions (using `session` from `flask`)
- **Data**: Store `user_id` in session
- **Security**: Use `app.secret_key` for session signing
- **Duration**: Browser session (cleared on close)

### Logout (`/logout`)
- Clear session
- Redirect to landing page
- Route: `POST /logout` (or `GET /logout` with confirmation)

### Authentication Helper
- **`login_required` decorator**: Protect routes that need authentication
  - Check if `user_id` in session
  - Redirect to login if not authenticated
  - Pass current user to template
- **Global template variable**: `current_user` available in all templates

## Database
**No schema changes needed** — `users` table already exists with:
- `id`, `name`, `email`, `password_hash`, `created_at`

## Template Updates
- **register.html**: Add form fields, display validation errors
- **login.html**: Add form fields, display validation errors
- **base.html**: Update navbar to show logout link when logged in, login/register when not

## Testing
- Test successful registration
- Test duplicate email rejection
- Test password mismatch rejection
- Test successful login
- Test invalid password rejection
- Test session persistence across page navigation
- Test logout clears session
- Test protected routes redirect to login

## Files to Modify
- `app.py` — update `/register`, `/login`, `/logout` routes
- `templates/register.html` — add form
- `templates/login.html` — add form
- `templates/base.html` — add conditional navbar logic

## Acceptance Criteria
- ✅ User can register with valid email, password
- ✅ Registration prevents duplicate emails
- ✅ User can log in with correct credentials
- ✅ User remains logged in across page navigation
- ✅ User can log out
- ✅ Protected routes redirect unauthenticated users to login
- ✅ All validation errors display clearly
