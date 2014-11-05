Feature: Authenticationa and Authorization

  Scenario: Logging out
    Given I am logged in as a NECOC admin
    When I logout
    Then I should be redirected to login page
    When I navigate to "/admin/dashboard"
    Then I should be redirected to login page