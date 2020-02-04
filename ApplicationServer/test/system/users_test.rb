require "application_system_test_case"

class UsersTest < ApplicationSystemTestCase
  setup do
    @user = users(:one)
  end

  test "visiting the index" do
    visit users_url
    assert_selector "h1", text: "Users"
  end

  test "creating a User" do
    visit users_url
    click_on "New User"

    fill_in "Id", with: @user.id
    fill_in "Meeting 1", with: @user.meeting_1
    fill_in "Meeting 2", with: @user.meeting_2
    fill_in "Meeting 3", with: @user.meeting_3
    fill_in "Meeting 4", with: @user.meeting_4
    fill_in "Meeting 5", with: @user.meeting_5
    fill_in "Name", with: @user.first
    click_on "Create User"

    assert_text "User was successfully created"
    click_on "Back"
  end

  test "updating a User" do
    visit users_url
    click_on "Edit", match: :first

    fill_in "Id", with: @user.id
    fill_in "Meeting 1", with: @user.meeting_1
    fill_in "Meeting 2", with: @user.meeting_2
    fill_in "Meeting 3", with: @user.meeting_3
    fill_in "Meeting 4", with: @user.meeting_4
    fill_in "Meeting 5", with: @user.meeting_5
    fill_in "Name", with: @user.first
    click_on "Update User"

    assert_text "User was successfully updated"
    click_on "Back"
  end

  test "destroying a User" do
    visit users_url
    page.accept_confirm do
      click_on "Destroy", match: :first
    end

    assert_text "User was successfully destroyed"
  end
end
