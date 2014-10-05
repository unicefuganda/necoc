Feature: Disasters

  Scenario: Add Disaster
    Given I am logged in as a NECOC admin
    And I have "Mukono" district already registered
    And I have "Flood" registered as a disaster type
    When I navigate to "/admin/disasters"
    And I click add disaster button
    And I select the disaster type as "Flood"
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