Feature: API Testing

    Scenario: Attempt to retrieve specific user details
        When I request specific user details

    Scenario: Attempt to retrieve specific user details with an incorrect ID
        When I request specific user details using the incorrect ID

    Scenario: Attempt to create a new user
        When I attempt to create a new user

    Scenario: Attempt to create a user with an email that is already taken
        When I attempt to create a new user with that email alredy taken

    Scenario: Attempt to create a new user with an invalid authentication token
        When I attempt to create a new user using the invalid token

    Scenario: Attempt to update specific user details
        When I attempt to update specific user details

    Scenario: Attempt to update specific user details with an incorrect ID
        When I attempt to update specific user details using the incorrect ID

    Scenario: Attempt to delete specific user
        When I attempt to delete specific user

    Scenario: Attempt to delete a specific user with an incorrect ID
        When I attempt to delete the user with the incorrect ID
