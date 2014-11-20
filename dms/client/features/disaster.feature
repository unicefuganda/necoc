Feature: Disasters

  Scenario: Add and Edit Disaster
    Given I am logged in as a NECOC admin
    And I have "Flood" registered as a disaster type
    And I have "Fire" registered as a disaster type
    And I have "Mukono" district and "Nabbaale" subcounty already registered
    And I have "BUGIRI" district and "Bulesa" subcounty already registered
    When I navigate to "/admin/disasters"
    And I click add disaster button
    And I select the disaster type as "Flood"
    And I select district as "Mukono"
    And I select subcounty as "Nabbaale"
    And I enter disaster description as "Big flood"
    And I select disaster status as "Assessment"
    And I enter disaster date as "2014/10/08 00:03"
    And I click save and close
    Then I should see the disaster in the disasters table
    When I click the disaster in "Mukono"
    And I click edit disaster button
    And I select the disaster type as "Fire"
    And I select district as "BUGIRI"
    And I select subcounty as "Bulesa"
    And I enter disaster description as "Bigger flood"
    And I select disaster status as "Response Team Deployed"
    And I enter disaster date as "2014/10/08 00:04"
    And I click save disaster
    Then I should see my disaster information

  Scenario: Add Disaster with un registered Disaster Type
    Given I am logged in as a NECOC admin
    And I have "Mukono" district already registered
    When I navigate to "/admin/disasters"
    And I click add disaster button
    And I enter the disaster type as "Fire"
    And I select district as "Mukono"
    And I enter disaster description as "Big flood"
    And I select disaster status as "Assessment"
    And I enter disaster date as "2014/10/08 00:03"
    And I click save and close
    Then I should see the disaster in the disasters table

  Scenario: Add Disaster --Validation
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/disasters"
    And I click add disaster button
    And I click save
    Then I should see required fields error messages