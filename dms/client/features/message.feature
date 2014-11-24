Feature: Messages

  Scenario: View Messages
    Given I am logged in as a NECOC admin
    And I have "Kampala" district already registered
    And I have one Necoc Volunteer registered
    When I POST a message to the NECOC DMS
    And I visit the messages listing page
    Then I should see my messages

  Scenario: Refresh Messages
    Given I am logged in as a NECOC admin
    And I have "Kampala" district already registered
    And I have one Necoc Volunteer registered
    When I POST a message to the NECOC DMS
    And I visit the messages listing page
    Then I should see my messages
    When I POST "necoc.gulu.awach. Second message" to the NECOC DMS
    And I refresh my messages
    Then I should see 2 message
    When I select my location as "Kampala"
    And I POST "necoc. kampala. third message" to the NECOC DMS
    And I refresh my messages
    Then I should see 2 message

  Scenario: Message Pagination
    Given I am logged in as a NECOC admin
    When I POST a list of messages to NECOC DMS
    And I visit the messages listing page
    Then I should see 10 messages in the first pagination
    When I click on the second pagination
    Then I should see 5 messages in the second pagination
    And I should see the total number of messages displayed

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
    And I navigate to messages page
    And I click send bulk sms button
    And I enter a sender number as "+256775019449"
    And I enter the message as "Hello"
    And I click the send button
    Then I should see message successfully sent

  Scenario: Send Bulk SMS --Validation
    Given I am logged in as a NECOC admin
    And I navigate to messages page
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
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    And I visit the messages listing page
    Then I should see one message uncategorized
    And I check the message
    When I click on associate to disaster button
    And I search disaster by location
    And I click the add button
    Then I should see the message associated with the disaster
    And I should see zero message uncategorized
    And I POST "NECOC GULU Fire" to the NECOC DMS
    When I navigate to "/admin/disasters"
    And I click the disaster in "Mukono"
    Then I should see the associated message

  Scenario: Associate Messages to disaster -- Validations
    Given I am logged in as a NECOC admin
    When I POST a message to the NECOC DMS
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    And I visit the messages listing page
    When I click on actions button
    Then I should not see the associate to disaster button
    When I check the message
    When I click on associate to disaster button
    And I click the add button
    Then I should see field required error message
    When I search disaster by location
    Then the error message disappear

  Scenario: Show uncategorized message count on admin panel
    Given I am logged in as a NECOC admin
    When I POST a message to the NECOC DMS
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    And I visit the messages listing page
    Then I should see 1 uncategorized message on the admin panel
    When I check the message
    And I click on associate to disaster button
    And I search disaster by location
    And I click the add button
    Then I should see 0 uncategorized message on the admin panel
