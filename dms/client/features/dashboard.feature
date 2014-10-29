Feature: Dashboard

  Scenario: Open the message panel
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    And I click the messages panel chevron
    Then I should see the messages panel open
    When I click the messages panel chevron
    Then I should see the messages panel closed