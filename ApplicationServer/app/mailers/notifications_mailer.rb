class NotificationsMailer < ApplicationMailer

  # Subject can be set in your I18n file at config/locales/en.yml
  # with the following lookup:
  #
  #   en.notifications_mailer.meeting_processed.subject
  #

  def meeting_processed(user, meeting_id)
    @meeting_id = meeting_id
    @first_name = user.first
    mail to: user.email,
      subject: "Meeting Processed. Your analytics are ready."
  end

end
