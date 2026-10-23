# API request examples

Use `emptrackai.http` with the VS Code REST Client extension. Start the backend first, then run the requests in order:

1. Register an admin. This succeeds once for the chosen email; on later runs, use the existing account and skip registration.
2. Log in to get a fresh access token.
3. Request the admin profile.
4. Create an employee. The API derives `admin_id` and `company_name` from the access token and the admin record; do not send those fields yourself.

Change the sample email, passwords, company, or `baseUrl` at the top of the request file for your environment. Use test credentials only, and do not commit real credentials or access tokens.

Endpoints covered:

- `POST /api/register/`
- `POST /api/login/`
- `GET /api/profile/` (Bearer access token required)
- `POST /api/employees/` (Bearer access token required)
- `GET /api/employees/` (Bearer access token required; lists only the current admin's employees)
