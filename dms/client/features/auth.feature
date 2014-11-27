Feature: Authentication and Authorization

  Scenario: Logging out
    Given I am logged in as a NECOC admin
    When I logout
    Then I should be redirected to login page
    When I navigate to "/admin/dashboard"
    Then I should be redirected to login page

  Scenario: Login validation
    Given I am logged out
    When I try to login in with username "" and password ""
    Then I should see "username" error message "* This field is required."
    And I should see "password" error message "* This field is required."
    When I try to login in with username "test_user" and password "wrong_password"
    Then I should see "* Username or Password is invalid"

  Scenario: Manage Users Authorization
    Given I am logged out
    And I log in with "" permission
    Then I should not see the users tab
    And I should not route to "/admin/mobile-users"
    Given I log in with "can_manage_users" permission
    Then I should see the users tab
    And I can route to "/admin/mobile-users"

  Scenario: Manage Users Authorization - Reset Password
    Given I am logged out
    And I have no users
    And I am logged out
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
#    And I should not see the change password button

  Scenario: Manage Disasters Authorization
    Given I am logged out
    And I log in with "" permission
    Then I should not see the disasters tab
    And I should not route to "/admin/disasters"
    Given I log in with "can_manage_disasters" permission
    Then I should see the disasters tab
    And I can route to "/admin/disasters"

  Scenario: Manage Messages Authorization
    Given I am logged out
    And I log in with "" permission
    Then I should not see the messages tab
    And I should not route to "/admin/messages"
    Given I log in with "can_manage_messages" permission
    Then I should see the messages tab
    And I can route to "/admin/messages"

  Scenario: Manage Polls Authorization
    Given I am logged out
    And I log in with "" permission
    And I navigate to polls page
    Then I should not see the new poll button
    Given I log in with "can_manage_polls" permission
    And I navigate to polls page
    Then I should see the new poll button