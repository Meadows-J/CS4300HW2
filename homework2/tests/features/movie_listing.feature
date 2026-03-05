Feature: Movie Listing
  As a user
  I want to view available movies
  So that I can browse and select movies to book seats for

  Scenario: View available movies
    Given there are movies available
    When I navigate to the movie listing page
    Then I should see all available movies
    And I should see the movie title
    And I should see the movie description
    And I should see the movie duration
    And I should see a "Book Now" button

  Scenario: No movies available
    Given there are no movies available
    When I navigate to the movie listing page
    Then I should see a message "No movies available at the moment"
