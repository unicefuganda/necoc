Feature: Sorting

  Scenario: Sorting Messages
    Given I am logged in as a NECOC admin
    And I have a "Fire" disaster in "Gulu" district, "Awach" subcounty already registered
    And I have a "Flood" disaster in "Mukono" district, "Goma" subcounty already registered
    And I have the following messages in the NECOC DMS:
    | phone      | text                          | time                        |
    | 111111     | NECOC.Goma Disasters!         | 2014-11-25T12:00:01.000000Z |
    | 222222     | NECOC.Awach. 1                | 2014-11-25T12:00:00.000000Z |
    | 333333     | NECOC.Mukono.Goma Disasters!  | 2014-11-24T12:00:00.000000Z |
    | 444444     | NECOC.Awach. 2                | 2014-11-23T12:00:00.000000Z |
    And I visit the messages listing page
    And I check message 2
    And I click on associate to disaster button
    And I search disaster by location
    And I click the add button
    And I sort by "Date Time" ascending
    Then I should see the messages in the following order:
    | text                          |
    | NECOC.Awach. 2                |
    | NECOC.Mukono.Goma Disasters!  |
    | NECOC.Awach. 1                |
    | NECOC.Goma Disasters!         |
    And I sort by "Date Time" descending
    Then I should see the messages in the following order:
    | text                          |
    | NECOC.Goma Disasters!         |
    | NECOC.Awach. 1                |
    | NECOC.Mukono.Goma Disasters!  |
    | NECOC.Awach. 2                |
    When I sort by "Status" ascending
    Then I should see the messages in the following order:
    | text                          |
    | NECOC.Awach. 1                |
    | NECOC.Goma Disasters!         |
    | NECOC.Mukono.Goma Disasters!  |
    | NECOC.Awach. 2                |
    When I sort by "Status" descending
    Then I should see the messages in the following order:
    | text                          |
    | NECOC.Goma Disasters!         |
    | NECOC.Mukono.Goma Disasters!  |
    | NECOC.Awach. 2                |
    | NECOC.Awach. 1                |
    When I sort by "Source" ascending
    Then I should see the messages in the following order:
    | text                          |
    | NECOC.Goma Disasters!         |
    | NECOC.Awach. 1                |
    | NECOC.Mukono.Goma Disasters!  |
    | NECOC.Awach. 2                |
    When I sort by "Source" descending
    Then I should see the messages in the following order:
    | text                          |
    | NECOC.Awach. 2                |
    | NECOC.Mukono.Goma Disasters!  |
    | NECOC.Awach. 1                |
    | NECOC.Goma Disasters!         |
    When I sort by "SMS Body" ascending
    Then I should see the messages in the following order:
    | text                          |
    | NECOC.Awach. 1                |
    | NECOC.Awach. 2                |
    | NECOC.Goma Disasters!         |
    | NECOC.Mukono.Goma Disasters!  |