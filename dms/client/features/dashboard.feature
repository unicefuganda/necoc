Feature: Dashboard

  Scenario: Open the message panel
    Given I am logged in as a NECOC admin
    When I navigate to map location "/admin/dashboard"
    And I click the messages panel chevron
    Then I should see the messages panel open
    When I click the messages panel chevron
    Then I should see the messages panel closed

  Scenario: Show messages on the message panel
    Given I am logged in as a NECOC admin
    And I have "Kampala" district already registered
    And I POST a message to the NECOC DMS
    When I navigate to map location "/admin/dashboard"
    And I click the messages panel chevron
    Then I should see my messages