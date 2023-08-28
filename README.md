# AspireLoan

## Installation

- Built on python 3.9
- > cd AspireLoan/src
- > python3 -m venv AspireLoanVenv
- > source AspireLoanVenv/bin/activate
- > pip3 install -r app/src/requirements.txt
- > python main.py
- Or using docker deploy the dockerfile on Docker Engine bound on port 8000
- Access the swagger page on http://localhost:8000/docs

## User token/User login to view schedule or create loans

- For user identification user needs to use a user_token (something like JWT/SSO)
- User logs in with API `/user/login` using their email and password
- The API returns a token which will identify the user for the rest of the active server session(this token is reset
  when server restarts)
- The user is expected to use this token for all APIs which have `user_token` as a parameter

## Usage Examples

### Create new user

**API**: `/user/create/`

**Request**

`
curl -X 'POST' \
'http://localhost:8000/user/create/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"name": "Ahmed",
"email": "ahmed@example.com",
"password": "pass"
}'
`

**Response**

`{
"name": "Ahmed",
"email": "ahmed@example.com",
"user_id": 1
}`

### Login

**API**: `/user/login/`

**Request**

`
curl -X 'GET' \
'http://localhost:8000/user/login/?email=ahmed%40example.com&password=pass' \
-H 'accept: application/json'
`

**Response**

`"2645744402625122793"`

### Create new loan

**API**: `/user/new_loan`

**Request**

`
curl -X 'POST' \
'http://localhost:8000/user/new_loan' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"amount": 110,
"term": 2,
"start_date": "2023-08-28",
"user_token": "2645744402625122793"
}'
`

**Response**

`{
"amount": 110,
"term": 2,
"start_date": "2023-08-28",
"loan_id": 1
}`

