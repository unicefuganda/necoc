Feature: Messages

  Scenario: View Messages
    Given I am logged in as a NECOC admin
    And I have "Kampala" district already registered
    And I have one Necoc Volunteer registered
    When I POST a message to the NECOC DMS
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
    When I POST a message to the NECOC DMS
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

  Scenario: Associate Messages to disaster
    Given I am logged in as a NECOC admin
    When I POST a message to the NECOC DMS
    And I have a disaster in "Mukono" registered
    And I visit the messages listing page
    And I check the message
    When I click on associate to disaster button
    And I search disaster by location
    And I click the add button
    Then I should see the message associated with the disaster

  Scenario: Associate Messages to disaster -- validations
    Given I am logged in as a NECOC admin
    When I POST a message to the NECOC DMS
    And I have a disaster in "Mukono" registered
    And I visit the messages listing page
    When I click on actions button
    Then I should not see the associate to disaster button
    When I check the message
    When I click on associate to disaster button
    And I click the add button
    Then I should see field required error message
    When I search disaster by location
    Then the error message disappear

