class NotificationsMailer < ApplicationMailer

  # Subject can be set in your I18n file at config/locales/en.yml
  # with the following lookup:
  #
  #   en.notifications_mailer.meeting_processed.subject
  #
  def meeting_processed
    @greeting = "Hi"
    # Get User from params to personalize email
    # Send to user.email
    mail to: "maxginier1@gmail.com",
      subject: "This is a test." 
  end
end
