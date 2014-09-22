Feature: Messages

  Scenario: View Messages
    Given I am logged in as a NECOC admin
    When I POST messages to the NECOC DMS
    And I visit the messages listing page
    Then I should see my messages

  Scenario: Message Pagination
    Given I am logged in as a NECOC admin
    When I POST a list of messages to NECOC DMS
    And I visit the messages listing page
    Then I should see 10 messages in the first pagination
    When I click on the second pagination
    Then I should see 6 messages in the second pagination

