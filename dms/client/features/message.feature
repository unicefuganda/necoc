Feature: Messages

  Scenario: View Messages
    Given I am logged in as a NECOC admin
    When I POST messages to the NECOC DMS
    And I visit the messages listing page
    Then I should see my messages

