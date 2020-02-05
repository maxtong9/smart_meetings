class NotificationsMailer < ApplicationMailer

  # Subject can be set in your I18n file at config/locales/en.yml
  # with the following lookup:
  #
  #   en.notifications_mailer.meeting_processed.subject
  #

  def meeting_processed(meeting)
    if !meeting.user1.nil?
      user1 = User.find(meeting.user1)
      mail to: user1.email,
        subject: "Meeting Processed. Your analytics are ready."
    end
    if !meeting.user2.nil?
      user2 = User.find(meeting.user2)
      mail to: user2.email,
        subject: "Meeting Processed. Your analytics are ready."
    end
    if !meeting.user3.nil?
      user3 = User.find(meeting.user3)
      mail to: user3.email,
        subject: "Meeting Processed. Your analytics are ready."
    end

    @first_name = "name"
    @meeting_id= "123456789"
    # Get User from params to personalize email
    # Send to user.email
  end
end
