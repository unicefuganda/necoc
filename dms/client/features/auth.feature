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