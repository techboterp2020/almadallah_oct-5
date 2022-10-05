Accept and Deny button in Helpdesk ticket list view
---------------

- Extend ListView.buttons and added new two buttons Accept and Deny after create button
- Added classes for both buttons
- Added willStart method in js and return a rpc call. Pass the value to template 
- Initially willStart methods runs, so we can hide button based on return value.
- The class added on button works while clicking on the button and set the user_available value on user.
