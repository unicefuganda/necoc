Feature: Messages

  Scenario: View Messages
    Given I am logged in as a NECOC admin
    And I have "Kampala" district already registered
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
    And I have "Kampala" district already registered
    And I have one Necoc Volunteer registered
    When I POST a message form that Volunteer to the NECOC DMS
    When I POST a list of messages to NECOC DMS
    And I visit the messages listing page
    When I select my location as "Kampala"
    Then I should only see my message in "Kampala"

  Scenario: Send Bulk SMS
    Given I am logged in as a NECOC admin
    And I visit the dashboard
    And I click send bulk sms button
    And I enter a sender number as "+256775019449"
    And I enter the message as "Hello"
    And I click the send button
    Then I should see message successfully sent

  Scenario: Send Bulk SMS --Validation
    Given I am logged in as a NECOC admin
    And I visit the dashboard
    And I click send bulk sms button
    And I click the send button
    Then I should see the sms fields required error messages
    And I enter a sender number as "+256775019449"
    And I enter a more than 160 characters message
    Then I should not see the fields required error messages
    And I should see please enter not more that 160 characters
