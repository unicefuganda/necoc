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