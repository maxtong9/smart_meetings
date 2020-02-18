class SessionsController < ApplicationController

  def new
  end

  def create
    user = User.find_by(email: params[:email])
    if user
      session[:user_id] = user.id
      # redirect_to user_path(:id => user.id)
      redirect_to '/users/'+(user.id).to_s(), notice: "You are logged in, "+ user.first
    else
      flash.now[:alert] = "Email or password is invalid"
      render "new"
    end
  end

  def destroy
    session[:user_id] = nil
    redirect_to '/', notice: "You are logged out"
  end
end
