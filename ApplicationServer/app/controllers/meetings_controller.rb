class MeetingsController < ApplicationController
  before_action :set_meeting, only: [:show, :edit, :update, :destroy]

  # GET /meetings
  # GET /meetings.json
  def index
    @user_meeting1 = Meeting.find_by(id: current_user.meeting_1)
    @user_meeting2 = Meeting.find_by(id: current_user.meeting_2)
    @user_meeting3 = Meeting.find_by(id: current_user.meeting_3)
    @user_meeting4 = Meeting.find_by(id: current_user.meeting_4)
    @user_meeting5 = Meeting.find_by(id: current_user.meeting_5)
  end

  # GET /meetings/1
  # GET /meetings/1.json
  def show
    @meeting = Meeting.find(params[:id])
    @json_from_file = 0
    for file in @meeting.file.attachments
      if file.content_type == 'application/json'
        download_file_from_s3('smartmeetingsbelieving', "./tmp/" + file.filename.to_s(), file.filename.to_s())
        @json_from_file = File.read("tmp/" + file.filename.to_s())
      end
    end
  end

  # GET /meetings/new
  def new
    @meeting = Meeting.new
  end

  # GET /meetings/1/edit
  def edit
  end

  # POST /meetings
  # POST /meetings.json
  def create
    @meeting = Meeting.new(create_params)
    respond_to do |format|
      if @meeting.save
        format.html { redirect_to @meeting, notice: 'Meeting was successfully created.' }
        format.json { render :show, status: :created, location: @meeting }
      else
        format.html { render :new }
        format.json { render json: @meeting.errors, status: :unprocessable_entity }
      end
    end
    add_user_meeting_relation
  end

  def analyze
    @meeting = Meeting.find_by(id: params[:id])
    send_to_socket(@meeting)
    create_trello_cards()
    send_email()
    # redirect_to @meeting
  end

  # PATCH/PUT /meetings/1
  # PATCH/PUT /meetings/1.json
  def update
    respond_to do |format|
      if @meeting.update(edit_params)
        @meeting.file.attach(params[:meeting][:my_file])
        format.html { redirect_to @meeting, notice: 'Meeting was successfully updated.' }
        format.json { render :show, status: :ok, location: @meeting }
        analyze
      else
        format.html { render :edit }
        format.json { render json: @meeting.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /meetings/1
  # DELETE /meetings/1.json
  def destroy
    delete_meetings_from_users
    @meeting.destroy
    respond_to do |format|
      format.html { redirect_to meetings_url, notice: 'Meeting was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_meeting
      @meeting = Meeting.find(params[:id])
    end

    def add_user_meeting_relation
      params[:user_ids].each do |user_id|
        add_meeting_foreign_key(User.find(user_id))
        add_user_foreign_key(user_id)
      end
    end

    def add_user_foreign_key(user_id)
      if @meeting.user1.nil?
        @meeting.update(user1: user_id)
      elsif @meeting.user2.nil?
        @meeting.update(user2: user_id)
      elsif @meeting.user3.nil?
        @meeting.update(user3: user_id)
      end
    end

    def add_meeting_foreign_key(user)
      if user.meeting_1.nil?
        user.update(meeting_1: @meeting.id)
      elsif user.meeting_2.nil?
        user.update(meeting_2: @meeting.id)
      elsif user.meeting_3.nil?
        user.update(meeting_3: @meeting.id)
      elsif user.meeting_4.nil?
        user.update(meeting_4: @meeting.id)
      elsif user.meeting_5.nil?
        user.update(meeting_5: @meeting.id)
      end
    end

    def delete_meetings_from_users
      if !@meeting.user1.nil?
        delete_meeting_foreign_key(User.find(@meeting.user1))
      end
      if !@meeting.user2.nil?
        delete_meeting_foreign_key(User.find(@meeting.user2))
      end
      if !@meeting.user3.nil?
        delete_meeting_foreign_key(User.find(@meeting.user3))
      end
    end

    def delete_meeting_foreign_key(user)
      if user.meeting_1 == @meeting.id
        user.update(meeting_1: nil)
      elsif user.meeting_2 == @meeting.id
        user.update(meeting_2: nil)
      elsif user.meeting_3 == @meeting.id
        user.update(meeting_3: nil)
      elsif user.meeting_4 == @meeting.id
        user.update(meeting_4: nil)
      elsif user.meeting_5 == @meeting.id
        user.update(meeting_5: nil)
      end
    end
    # Never trust parameters from the scary internet, only allow the white list through.
    def edit_params
      params.require(:meeting).permit(:name, file: [])
    end

    def create_params
      params.require(:meeting).permit(:name, :participants)
    end

    def send_to_socket(meeting)
      require 'open-uri'
      # hostname = 'localhost' # COMMENT THIS OUT FOR DOCKER
      hostname = open('https://api.ipify.org').read
      # hostname = '107.77.213.153' # REPLACE THIS WITH YOUR PUBLIC IP ADDRESS FOR DOCKER
      puts hostname
      port = 9999

      s = TCPSocket.open(hostname, port)
      info_string = meeting.participants.to_s + meeting.name
      for file in meeting.file.attachments do
          info_string = info_string + '|' + file.key + ';' + file.filename.to_s
      end
      puts "INFO STRING: #{info_string}"
      s.write(info_string)

      recv_from_socket(s, meeting)

      s.close
    end

    def recv_from_socket(s, meeting)
      key = s.gets
      directory = "./tmp/"
      download_file_from_s3('smartmeetingsbelieving', directory + key, key)
      meeting.file.attach(io: File.open(directory + key), filename: key, content_type: 'application/json')
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

    def create_trello_cards
      require 'uri'
      require 'net/http'
      require 'openssl'
      require 'json'

      trello_key = ENV['TRELLO_PUBLIC_KEY']
      trello_token = ENV['TRELLO_MEMBER_TOKEN']
      trello_url = 'https://api.trello.com/1'

      username = 'christinatao31'

      # get the id of the board to add the new card to
      boards_url = "#{trello_url}/members/#{username}/boards?key=#{trello_key}&token=#{trello_token}"
      boards_uri = URI(boards_url)
      boards_json = Net::HTTP.get(boards_uri)
      boards = JSON.parse(boards_json)
      board_id = boards.find {|b| b['name']=='Weekly Meetings'}['id']

      # get the id of the list within the board to add the new card to
      lists_url = "#{trello_url}/boards/#{board_id}/lists?key=#{trello_key}&token=#{trello_token}"
      lists_uri = URI(lists_url)
      lists_json = Net::HTTP.get(lists_uri)
      lists = JSON.parse(lists_json)
      list_id = lists.find {|l| l['name']=='Tasks from Meetings'}['id']

      json_from_file = File.read("tmp/" + @meeting.file.attachments.last.filename.to_s())
      hash = JSON.parse(json_from_file, object_class: OpenStruct)

      for i in hash.action_items
        card_name = i[1][0...-1]
        card_description = "created by SmartMeetings"
        card_member_username = User.find_by(first: i[0]).trello

         # get id of the card member
        member_url = "#{trello_url}/members/#{card_member_username}?key=#{trello_key}&token=#{trello_token}"
        member_uri = URI(member_url)
        member_json = Net::HTTP.get(member_uri)
        member = JSON.parse(member_json)
        member_id = member['id']

        if i.size() == 3
          deadline = i[2][0]
          dl_index = i[2][1]
          # puts dl_index
          # card_name = i[1][0...dl_index]
          # puts card_name.split(' ')
          # puts card_name.split(' ')[0...dl_index]
          card_name = (card_name.split(' ')[0...dl_index]).join(' ')
          # puts card_name
          # puts "RUBY DEADLINE: " + deadline
          url = URI("#{trello_url}/cards?name=#{card_name}&desc=#{card_description}&idList=#{list_id}&idMembers=#{member_id}&due=#{deadline}&key=#{trello_key}&token=#{trello_token}")
        else
          url = URI("#{trello_url}/cards?name=#{card_name}&desc=#{card_description}&idList=#{list_id}&idMembers=#{member_id}&key=#{trello_key}&token=#{trello_token}")
        end

        http = Net::HTTP.new(url.host, url.port)
        http.use_ssl = true
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE

        request = Net::HTTP::Post.new(url)

        response = http.request(request)

        puts response
      end
    end
    def send_email
      @notifications_mailer = NotificationsMailer

      if !@meeting.user1.nil?
        @notifications_mailer.meeting_processed(User.find_by(id: @meeting.user1), @meeting.id).deliver_now
      end
      if !@meeting.user2.nil?
        @notifications_mailer.meeting_processed(User.find_by(id: @meeting.user2), @meeting.id).deliver_now
      end
      if !@meeting.user3.nil?
        @notifications_mailer.meeting_processed(User.find_by(id: @meeting.user3), @meeting.id).deliver_now
      end
    end
end
