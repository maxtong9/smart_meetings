class NotificationsMailer < ApplicationMailer

  # Subject can be set in your I18n file at config/locales/en.yml
  # with the following lookup:
  #
  #   en.notifications_mailer.meeting_processed.subject
  #

  def meeting_processed(user)
      mail to: user.email,
        subject: "Meeting Processed. Your analytics are ready."
  end

    @first_name = "name"
    @meeting_id = "123456789"
    # Get User from params to personalize email
    # Send to user.email
end
