Feature: Map

  Scenario: View Uganda Map
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    Then I should see a map of Uganda centered at latitude "1.436" and longitude "32.884"
    Then I should see a map of Uganda zoomed at level "7"

  @dev
  Scenario: Highlight district
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    And hover over "Lira"
    Then "Lira" should be highlighted

