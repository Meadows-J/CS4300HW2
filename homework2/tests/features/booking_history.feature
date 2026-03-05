Feature: Booking History
  As a user
  I want to view my booking history
  So that I can see all my previous bookings

  Scenario: View booking history
    Given I have made bookings
    When I navigate to the booking history page
    Then I should see all my bookings
    And I should see the movie title for each booking
    And I should see the seat number for each booking
    And I should see the booking date for each booking

  Scenario: Empty booking history
    Given I have not made any bookings
    When I navigate to the booking history page
    Then the booking history should be empty
