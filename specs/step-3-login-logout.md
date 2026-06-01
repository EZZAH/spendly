# Step 3: Login & Logout Enhancements

## Overview
Refine and enhance login/logout functionality with improved user experience, security, and session management features.

**Note**: Basic login/logout was implemented in Step 2. This step focuses on enhancements and polish.

## Objectives
1. Enhance logout with confirmation (optional)
2. Implement "Remember Me" functionality (optional)
3. Add session timeout/inactivity logout
4. Improve error messages and user feedback
5. Add password reset/recovery flow (future)
6. Implement logout from all devices (optional)

## Current State (Step 2 Completion)
✅ Login form with email/password validation
✅ Password verification with werkzeug hashing
✅ Session creation on successful login
✅ Generic error messages for security
✅ Logout route that clears session
✅ Protected routes with @login_required decorator
✅ Conditional navbar (logged in/out states)

## Scope for Step 3

### Login Enhancements
- **"Remember Me" Checkbox** (Optional):
  - If checked, extend session duration to 30 days
  - Store preference in database
  - Use persistent cookie instead of browser session
  
- **Failed Login Attempt Tracking** (Optional):
  - Track number of failed attempts
  - Lock account after 5 failed attempts (30 minutes)
  - Display warning on repeated failures
  
- **Redirect to Previous Page**:
  - After login, redirect to page user tried to access
  - Store `next` parameter in session
  - Default to `/expenses` if no previous page

### Logout Enhancements
- **Logout Confirmation** (Optional):
  - Modal/confirmation before logout
  - Prevent accidental logouts
  
- **Last Logged In Timestamp**:
  - Display "Last logged in: [date/time]" on login page
  - Update on each successful login
  
- **Logout from All Devices**:
  - Invalidate all sessions for user
  - Store session version in database
  - Increment on "logout all devices"

### Session Management Improvements
- **Session Timeout**:
  - Idle timeout: 30 minutes of inactivity
  - Absolute timeout: 24 hours maximum session
  - Warning before auto-logout (5 minute warning modal)
  
- **Session Activity Tracking**:
  - Update `last_activity` timestamp on each request
  - Check for timeout on before_request hook
  
- **Graceful Timeout Handling**:
  - Redirect to login with message: "Your session expired"
  - Show modal before redirect (optional)

### Security Enhancements
- **Rate Limiting** (Optional):
  - Limit login attempts to 5 per minute per IP
  - Use Flask-Limiter or similar
  
- **CSRF Protection**:
  - Add CSRF token to logout form (security best practice)
  - Use Flask-WTF or Flask-CSRF
  
- **Secure Session Cookie**:
  - Set HttpOnly flag (already default in Flask)
  - Set Secure flag for HTTPS (production)
  - Set SameSite=Lax (CSRF protection)

### User Feedback
- **Login Success Toast/Alert**:
  - "Welcome back, [name]!"
  - Auto-dismiss after 5 seconds
  
- **Logout Confirmation**:
  - "You've been signed out"
  - Show on landing page after logout

### Database Schema Updates (if needed)
```sql
-- Optional: Track login attempts
ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN last_login DATETIME;
ALTER TABLE users ADD COLUMN locked_until DATETIME;

-- Optional: Support multiple sessions per user
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT (datetime('now')),
    last_activity DATETIME DEFAULT (datetime('now')),
    expires_at DATETIME NOT NULL,
    ip_address TEXT,
    user_agent TEXT
);
```

## Testing

### Login Enhancement Tests
- [ ] User can check "Remember Me" and stay logged in for 30 days
- [ ] Failed login attempts are tracked (1-5 attempts)
- [ ] Account locks after 5 failed attempts
- [ ] Locked account shows error message
- [ ] After 30 minutes, lock is released
- [ ] User redirected to previous page after login
- [ ] If no previous page, redirect to expenses dashboard

### Logout Enhancement Tests
- [ ] Logout confirmation modal appears
- [ ] User can cancel logout
- [ ] User can confirm logout
- [ ] Last login time displays on login page
- [ ] "Logout all devices" invalidates all user sessions
- [ ] Other devices are logged out immediately

### Session Timeout Tests
- [ ] User idle for 30 minutes → session expires
- [ ] Warning modal appears 5 minutes before timeout
- [ ] User can click "Stay logged in" to extend session
- [ ] User auto-logged out after 24 hours max
- [ ] Expired session redirects to login with message

### Security Tests
- [ ] CSRF token required for logout
- [ ] Rate limiting prevents brute force (5 attempts/minute)
- [ ] Session cookie is HttpOnly
- [ ] Session cookie is Secure (HTTPS only in production)

## Files to Modify
- `app.py` — enhance login/logout routes, add session timeout logic
- `database/db.py` — add optional session tracking queries
- `templates/login.html` — add "Remember Me" checkbox, last login display
- `templates/base.html` — add logout confirmation modal (optional)
- `static/js/main.js` — handle logout confirmation, timeout warnings
- `static/css/style.css` — style logout modal and alerts

## Acceptance Criteria (MVP)
- ✅ Logout requires confirmation
- ✅ Sessions timeout after 30 minutes of inactivity
- ✅ User redirected to previous page after login
- ✅ Clear timeout warning displayed (5 min before logout)
- ✅ "Last logged in" timestamp shown on login page
- ✅ Failed attempts tracked and account locked at 5 attempts

## Acceptance Criteria (Optional Enhancements)
- ✅ "Remember Me" extends session to 30 days
- ✅ Logout from all devices supported
- ✅ Rate limiting prevents brute force
- ✅ CSRF protection on logout form
- ✅ Success toast messages on login/logout

## Implementation Priority
1. **High**: Session timeout with warning
2. **High**: Failed login tracking & account locking
3. **Medium**: Redirect to previous page
4. **Medium**: Logout confirmation
5. **Low**: "Remember Me" functionality
6. **Low**: Logout all devices

## Notes
- All changes should be backward compatible
- Existing tests from Step 2 should still pass
- Add new tests for all new features
- Consider performance impact of session tracking
