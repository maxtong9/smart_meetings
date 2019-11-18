class MeetingController < ApplicationController
  layout "meeting"
  before_action :set_user, only: [:show, :edit, :update, :destroy]
  def index
    @users = {users: User.all}
  end
end
