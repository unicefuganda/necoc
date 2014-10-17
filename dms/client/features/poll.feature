Feature: Poll

  Scenario: Send Poll
    Given I am logged in as a NECOC admin
    And I have "Mukono" district already registered
    And I navigate to polls page
    And I click new poll button
    And I enter a poll name as "NECOC POLL"
    And I enter a poll question as "How many disasters have you had in your area"
    And I enter a poll keyword as "polls"
    And I select the target location as "Mukono"
    And I click the send poll button
    Then I should see poll successfully sent
    And I should see the poll in the poll-list
    When I click new poll button
    And I enter a poll name as "NECOC POLL"
    And I enter a poll question as "How many disasters have you had in your area"
    And I enter a poll keyword as "polls"
    And I select the target location as "Mukono"
    And I click the send poll button
    Then I should see key word must me unique

  Scenario: Send Poll --Validation
    Given I am logged in as a NECOC admin
    And I have "Mukono" district already registered
    And I navigate to polls page
    And I click new poll button
    And I click the send poll button
    Then I should see the polls fields required error messages
    And I enter a poll name as "NECOC POLL"
    And I enter a more than 130 characters "pollQuestionField"
    And I enter a more than 10 characters "pollKeywordField"
    Then I should see character limit errors


