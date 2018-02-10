## Bina Rywards

### Components
- Users
- Organisations (companies)
- Rewards

### Quick Docs
|End Point|Method|Parameters|Result|Complete|
|---------|------|----------|------|--------|
|api|any| |Returns a small documentation of the api, better than this one|Yes|
|api/redeem|POST|redemptionCode, phoneNumber|Redeems a token to a specific user|Yes|
|api/user_add|POST|phone_number, password, [name, email]|Adds a user/ Logs in if registered|Yes|
|api/user_login|POST|phone_number, password|Logs in the user if registered|No|
|api/user_exists|GET|phone|Get details of a user if exists|Yes|
|api/user_update|PUT|user_id, key, value|Update details of a user account|No|
|api/user_remove|DELETE|user_id|Delete a user|No|
|api/companies|GET| |Returns a list of all registered organisations|
|api/company_add|POST|email, phone_number, password, name, company_code|Registers a new organisation|
|api/company_details|GET|user_name|Get details of a specific company|
|api/company_update|PUT|user_name, key, value|Update details of a company|
|api/company_campaigns|GET|user_name|List of rewards offered by an organisation|
|api/company_campaign|GET|user_name, campaign_id|A single campaign launched by an organization|
|api/company_new_campaign|POST|user_name, campaign_id, description|Adds a campaign by the organisation|
|api/company_update_campaign|PUT|user_name, campaign_id, key, value|Updates details of a campaign|
|api/company_delete_campaign|DELETE|user_name, campaign_id|Updates details of a campaign|
|api/ussd_callback|POST|sessionid, phoneNumber, serviceCode, text|Handles USSD requests and responses|
