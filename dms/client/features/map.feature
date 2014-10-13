Feature: Map

  Scenario: View Uganda Map
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    Then I should see a map of Uganda centered at latitude "1.436" and longitude "32.884"
    Then I should see a map of Uganda zoomed at level "7"


  Scenario: Highlight district
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    And hover over "Lira"
    Then "Lira" should be highlighted

  Scenario: Zoom into districts on click
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    And click "Lira" district
    Then I should see Uganda map zoomed into "Lira" district

  Scenario: Navigate to district
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard/lira"
    Then I should see Uganda map zoomed into "Lira" district

