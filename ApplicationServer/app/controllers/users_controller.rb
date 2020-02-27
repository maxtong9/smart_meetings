class UsersController < ApplicationController
  before_action :set_user, only: [:show, :edit, :update, :destroy]

  # GET /users
  # GET /users.json
  def index
    @users = User.all
  end

  # GET /users/1
  # GET /users/1.json
  def show
    set_user
    name = @user.first

    # @user_hash["spoken"] returns hash of a user's spoken percentages, keyed by meeting #
    # @user_hash["spoken"][1] will return the percentage of the first meeting
    @user_hash = { "spoken" => {}, "hesitations" => {}, "interruptions" => {}, "action_items" => {}, "participants" => {} }

    meeting = Meeting.find_by(id: @user.meeting_1)
    if !meeting.nil?
      for file in meeting.file.attachments
        if file.content_type == 'application/json'
          download_file_from_s3('smartmeetingsbelieving', "./tmp/" + file.filename.to_s(), file.filename.to_s())
          json_from_file = File.read("tmp/" + file.filename.to_s())
          meeting_hash = JSON.parse(json_from_file, object_class: OpenStruct)

          for entry in meeting_hash.total_time_spoken do
            if entry[0] == name
              @user_hash["spoken"] = @user_hash["spoken"].merge({ 1 => entry[1] })
            end
          end

          for entry in meeting_hash.hesitation_analytics do
            if entry[0] == name
              @user_hash["hesitations"] = @user_hash["hesitations"].merge({ 1 => entry[1] })
            end
          end

          name_exists = false
          for entry in meeting_hash.interruption do
            if entry[0] == name
              name_exists = true
              @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 1 => entry[1] })
            end
          end
          if !name_exists
            @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 1 => 0 })
          end

          counter = 0
          for entry in meeting_hash.action_items do
            if entry[0] == name
              counter = counter + 1
            end
          end
          @user_hash["action_items"] = @user_hash["action_items"].merge({ 1 => counter })

          user_counter = 0
          if !meeting.user1.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user2.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user3.nil?
            user_counter = user_counter + 1
          end
          @user_hash['participants'] = @user_hash["participants"].merge({ 1 => user_counter })

        end
      end
    end

    meeting = Meeting.find_by(id: @user.meeting_2)
    if !meeting.nil?
      for file in meeting.file.attachments
        if file.content_type == 'application/json'
          download_file_from_s3('smartmeetingsbelieving', "./tmp/" + file.filename.to_s(), file.filename.to_s())
          json_from_file = File.read("tmp/" + file.filename.to_s())
          meeting_hash = JSON.parse(json_from_file, object_class: OpenStruct)

          for entry in meeting_hash.total_time_spoken do
            if entry[0] == name
              @user_hash["spoken"] = @user_hash["spoken"].merge({ 2 => entry[1] })
            end
          end

          for entry in meeting_hash.hesitation_analytics do
            if entry[0] == name
              @user_hash["hesitations"] = @user_hash["hesitations"].merge({ 2 => entry[1] })
            end
          end

          name_exists = false
          for entry in meeting_hash.interruption do
            if entry[0] == name
              name_exists = true
              @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 2 => entry[1] })
            end
          end
          if !name_exists
            @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 2 => 0 })
          end

          counter = 0
          for entry in meeting_hash.action_items do
            if entry[0] == name
              counter = counter + 1
            end
          end
          @user_hash["action_items"] = @user_hash["action_items"].merge({ 2 => counter })

          user_counter = 0
          if !meeting.user1.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user2.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user3.nil?
            user_counter = user_counter + 1
          end
          @user_hash['participants'] = @user_hash["participants"].merge({ 2 => user_counter })
        end
      end
    end

    meeting = Meeting.find_by(id: @user.meeting_3)
    if !meeting.nil?
      for file in meeting.file.attachments
        if file.content_type == 'application/json'
          download_file_from_s3('smartmeetingsbelieving', "./tmp/" + file.filename.to_s(), file.filename.to_s())
          json_from_file = File.read("tmp/" + file.filename.to_s())
          meeting_hash = JSON.parse(json_from_file, object_class: OpenStruct)

          for entry in meeting_hash.total_time_spoken do
            if entry[0] == name
              @user_hash["spoken"] = @user_hash["spoken"].merge({ 3 => entry[1] })
            end
          end

          for entry in meeting_hash.hesitation_analytics do
            if entry[0] == name
              @user_hash["hesitations"] = @user_hash["hesitations"].merge({ 3 => entry[1] })
            end
          end

          name_exists = false
          for entry in meeting_hash.interruption do
            if entry[0] == name
              name_exists = true
              @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 3 => entry[1] })
            end
          end
          if !name_exists
            @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 3 => 0 })
          end

          counter = 0
          for entry in meeting_hash.action_items do
            if entry[0] == name
              counter = counter + 1
            end
          end
          @user_hash["action_items"] = @user_hash["action_items"].merge({ 3 => counter })
          user_counter = 0
          if !meeting.user1.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user2.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user3.nil?
            user_counter = user_counter + 1
          end
        @user_hash['participants'] = @user_hash["participants"].merge({ 3 => user_counter })
        end
      end
    end

    meeting = Meeting.find_by(id: @user.meeting_4)
    if !meeting.nil?
      for file in meeting.file.attachments
        if file.content_type == 'application/json'
          download_file_from_s3('smartmeetingsbelieving', "./tmp/" + file.filename.to_s(), file.filename.to_s())
          json_from_file = File.read("tmp/" + file.filename.to_s())
          meeting_hash = JSON.parse(json_from_file, object_class: OpenStruct)

          for entry in meeting_hash.total_time_spoken do
            if entry[0] == name
              @user_hash["spoken"] = @user_hash["spoken"].merge({ 4 => entry[1] })
            end
          end

          for entry in meeting_hash.hesitation_analytics do
            if entry[0] == name
              @user_hash["hesitations"] = @user_hash["hesitations"].merge({ 4 => entry[1] })
            end
          end

          name_exists = false
          for entry in meeting_hash.interruption do
            if entry[0] == name
              name_exists = true
              @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 4 => entry[1] })
            end
          end
          if !name_exists
            @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 4 => 0 })
          end

          counter = 0
          for entry in meeting_hash.action_items do
            if entry[0] == name
              counter = counter + 1
            end
          end
          @user_hash["action_items"] = @user_hash["action_items"].merge({ 4 => counter })
          user_counter = 0
          if !meeting.user1.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user2.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user3.nil?
            user_counter = user_counter + 1
          end
          @user_hash['participants'] = @user_hash["participants"].merge({ 4 => user_counter })
        end
      end
    end

    meeting = Meeting.find_by(id: @user.meeting_5)
    if !meeting.nil?
      for file in meeting.file.attachments
        if file.content_type == 'application/json'
          download_file_from_s3('smartmeetingsbelieving', "./tmp/" + file.filename.to_s(), file.filename.to_s())
          json_from_file = File.read("tmp/" + file.filename.to_s())
          meeting_hash = JSON.parse(json_from_file, object_class: OpenStruct)

          for entry in meeting_hash.total_time_spoken do
            if entry[0] == name
              @user_hash["spoken"] = @user_hash["spoken"].merge({ 5 => entry[1] })
            end
          end

          for entry in meeting_hash.hesitation_analytics do
            if entry[0] == name
              @user_hash["hesitations"] = @user_hash["hesitations"].merge({ 5 => entry[1] })
            end
          end

          name_exists = false
          for entry in meeting_hash.interruption do
            if entry[0] == name
              name_exists = true
              @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 5 => entry[1] })
            end
          end
          if !name_exists
            @user_hash["interruptions"] = @user_hash["interruptions"].merge({ 5 => 0 })
          end

          counter = 0
          for entry in meeting_hash.action_items do
            if entry[0] == name
              counter = counter + 1
            end
          end
          @user_hash["action_items"] = @user_hash["action_items"].merge({ 5 => counter })
          user_counter = 0
          if !meeting.user1.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user2.nil?
            user_counter = user_counter + 1
          end
          if !meeting.user3.nil?
            user_counter = user_counter + 1
          end
          @user_hash['participants'] = @user_hash["participants"].merge({ 5 => user_counter })
        end
      end
    end

  end

  # GET /users/new
  def new
    @user = User.new
  end

  # GET /users/1/edit
  def edit
  end

  # POST /users
  # POST /users.json
  def create
    @user = User.new(user_params)

    respond_to do |format|
      if @user.save
        format.html { redirect_to @user, notice: 'User was successfully created.' }
        format.json { render :show, status: :created, location: @user }
      else
        format.html { render :new }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /users/1
  # PATCH/PUT /users/1.json
  def update
    respond_to do |format|
      if @user.update(user_params)
        format.html { redirect_to @user, notice: 'User was successfully updated.' }
        format.json { render :show, status: :ok, location: @user }
      else
        format.html { render :edit }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /users/1
  # DELETE /users/1.json
  def destroy
    @user.destroy
    respond_to do |format|
      format.html { redirect_to users_url, notice: 'User was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_user
      @user = User.find(params[:id])
    end

    def download_file_from_s3(bucket, file_path, object_key)
      require 'aws-sdk-s3'  # v2: require 'aws-sdk'

      #Aws.config(:access_key_id => Rails.application.credentials.production[:aws][:access_key_id], :secret_access_key => Rails.application.credentials.production[:aws][:secret_access_key])
      s3 = Aws::S3::Resource.new(:access_key_id => Rails.application.credentials.dig(:aws, :access_key_id), :secret_access_key => Rails.application.credentials.dig(:aws, :secret_access_key), region: 'us-west-1')
      # Create the object to retrieve
      obj = s3.bucket(bucket).object(object_key)
      # Get the item's content and save it to a file
      obj.get(response_target: file_path)
    end
    helper_method :download_file_from_s3

    # Never trust parameters from the scary internet, only allow the white list through.
    def user_params
      params.require(:user).permit(:first, :last, :email, :trello)
    end
end
