Feature: Messages

  Scenario: View Messages
    Given I am logged in as a NECOC admin
    And I have a location
    And I have one Necoc Volunteer registered
    When I POST a message form that Volunteer to the NECOC DMS
    And I visit the messages listing page
    Then I should see my messages

  Scenario: Message Pagination
    Given I am logged in as a NECOC admin
    When I POST a list of messages to NECOC DMS
    And I visit the messages listing page
    Then I should see 10 messages in the first pagination
    When I click on the second pagination
    Then I should see 5 messages in the second pagination

  Scenario: Message Filter by location
    Given I am logged in as a NECOC admin
    And I have "Mukono" district already registered
    And I have one Necoc Volunteer registered
    When I POST a message form that Volunteer to the NECOC DMS
    When I POST a list of messages to NECOC DMS
    And I visit the messages listing page
    When I select my location as "Kampala"
    Then I should only see my message in that location
