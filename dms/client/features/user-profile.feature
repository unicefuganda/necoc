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
    And I update by selecting my role as "Management Team"
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

  Scenario: Reset password not visible on current users profile
    Given I have no users
    And I am logged in as a NECOC admin
    When I navigate to the users page
    And I click "Test User" in the mobile users table
    Then I should not see the reset password button
    And I should see the change password button

  Scenario: Reset password visible on other users profiles
    Given I am logged out
    And I have no users
    And I am logged in as a NECOC admin
    And I have "Mukono" district and "Nabbaale" subcounty already registered
    When I navigate to the users page
    And I click the create new user button
    And I enter my "name" as "Solomon"
    And I enter my "email" as "solomon@gmail.com"
    And I enter my "phone" as "0775019449"
    And I select my "district" as "Mukono"
    And I select my "subcounty" as "Nabbaale"
    And I choose to grant web access
    And I enter my "username" as "solomon1990"
    And I select my role as "IT Assistant"
    And I click  save and close
    Given I log in with "can_manage_users" permission
    When I navigate to the users page
    And I click "Solomon" in the mobile users table
    Then I should see the reset password button
    And I should not see the change password button

  Scenario: Reset password
    Given I am logged out
    And I have no users
    And I am logged in as a NECOC admin
    And I am logged out
    And I log in with "can_manage_users" permission
    When I navigate to the users page
    And I click "Test User" in the mobile users table
    And I reset the password
    And I am logged out
    And I try to login in with username "test_user" and password "password"
    Then I should see "* Username or Password is invalid"

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
