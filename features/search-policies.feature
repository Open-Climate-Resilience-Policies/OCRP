Feature: Search policies
  In order to discover relevant climate policy content quickly
  As a site visitor
  I want to use the search page to query the policy library

  Scenario: BDD-001 visitor can perform a policy search from the search page
    Given the policy site is available
    When the visitor opens the search page
    Then the search interface is visible
    And the visitor can submit a query
    And the visitor receives search results for matching policies

