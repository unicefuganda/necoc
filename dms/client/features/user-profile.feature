Feature: User Profile

  Scenario: Edit User Profile
    Given I have no users
    And I am logged in as a NECOC admin
    And I have "Mukono" district and "Nabbaale" subcounty already registered
    When I navigate to the users page
    And I click "Test User" in the mobile users table
    And I edit the user
    And I update my "name" as "Solomon"
    And I update my "email" as "solomon@gmail.com"
    And I update my "phone" as "0775019449"
    And I update by selecting my "district" as "Mukono"
    And I update by selecting my "subcounty" as "Nabbaale"
    And I save the updated user details
    Then I should see my updated profile

  Scenario: Change password
    Given I have no users
    And I am logged in as a NECOC admin
    When I navigate to the users page
    And I click "Test User" in the mobile users table
    And I change my password
    And I input my "old_password" as "password"
    And I input my "new_password" as "password1"
    And I input my "confirm_password" as "password1"
    And I proceed to click the save button
    When I logout
    And I try to login in with username "test_user" and password "password1"
    Then I should be logged In

  Scenario: Change Password validation
    Given I have no users
    And I am logged in as a NECOC admin
    When I navigate to the users page
    And I click "Test User" in the mobile users table
    And I change my password
    And I input my "old_password" as ""
    And I proceed to click the save button
    Then I see "old-password" number 0 error message "This field is required"
    And I input my "old_password" as "very wrong password"
    And I input my "new_password" as "password"
    And I input my "confirm_password" as "password"
    And I proceed to click the save button
    Then I see "old-password" number 1 error message "Current password incorrect."
    And I input my "old_password" as "password"
    And I input my "new_password" as "password1"
    And I input my "confirm_password" as "password1_not"
    And I proceed to click the save button
    Then I see "confirm-password" number 1 error message "The two password fields didn't match."
