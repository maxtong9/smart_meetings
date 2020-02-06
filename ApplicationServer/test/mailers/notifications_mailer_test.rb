require 'test_helper'

class NotificationsMailerTest < ActionMailer::TestCase
  test "meeting_processed" do
    mail = NotificationsMailer.meeting_processed
    assert_equal "Meeting processed", mail.subject
    assert_equal ["to@example.org"], mail.to
    assert_equal ["from@example.com"], mail.from
    assert_match "Hi", mail.body.encoded
  end

end
