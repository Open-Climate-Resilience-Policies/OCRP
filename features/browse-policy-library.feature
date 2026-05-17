Feature: Browse policy library pages
  In order to review many policies without overload
  As a site visitor
  I want to navigate policy library pagination controls

  Scenario: BDD-003 visitor can move from page 1 to page 2 in the policy library
    Given the policy site is available
    When the visitor opens the policy library
    Then the first page of policy listings is shown
    When the visitor activates the next-page control
    Then the second page of policy listings is shown
    And the browser URL reflects the selected page

