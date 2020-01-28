class MeetingsController < ApplicationController
  before_action :set_meeting, only: [:show, :edit, :update, :destroy]

  # GET /meetings
  # GET /meetings.json
  def index
    @meetings = Meeting.all
  end

  # GET /meetings/1
  # GET /meetings/1.json
  def show
    @meeting = Meeting.find(params[:id])
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
  end

  # PATCH/PUT /meetings/1
  # PATCH/PUT /meetings/1.json
  def update
    respond_to do |format|
      if @meeting.update(edit_params)
        send_to_socket(@meeting)
        create_trello_cards()
        format.html { redirect_to @meeting, notice: 'Meeting was successfully updated.' }
        format.json { render :show, status: :ok, location: @meeting }
      else
        format.html { render :edit }
        format.json { render json: @meeting.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /meetings/1
  # DELETE /meetings/1.json
  def destroy
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

    # Never trust parameters from the scary internet, only allow the white list through.
    def edit_params
      params.require(:meeting).permit(:name, file: [])
    end

    def create_params
      params.require(:meeting).permit(:name, :participants)
    end

    def send_to_socket(meeting)
      # hostname = 'localhost' # COMMENT THIS OUT FOR DOCKER
      hostname = '169.231.41.182' # REPLACE THIS WITH YOUR PUBLIC IP ADDRESS FOR DOCKER
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
      board_id = boards.find {|b| b['name']=='Demo Board'}['id']
      puts "board_id=#{board_id}"

      # get the id of the list within the board to add the new card to
      lists_url = "#{trello_url}/boards/#{board_id}/lists?key=#{trello_key}&token=#{trello_token}"
      lists_uri = URI(lists_url)
      lists_json = Net::HTTP.get(lists_uri)
      lists = JSON.parse(lists_json)
      list_id = lists.find {|l| l['name']=='Demo List'}['id']
      puts "list_id=#{list_id}"

      json_from_file = File.read("tmp/" + @meeting.file.attachments.last.filename.to_s())
      hash = JSON.parse(json_from_file, object_class: OpenStruct)

      for i in hash.action_items
        card_name = i[1]
        card_description = "Test Description"
        card_member_username = "christinatao31"

         # get id of the card member
        member_url = "#{trello_url}/members/#{card_member_username}?key=#{trello_key}&token=#{trello_token}"
        member_uri = URI(member_url)
        member_json = Net::HTTP.get(member_uri)
        member = JSON.parse(member_json)
        member_id = member['id']
        puts "member_id=#{member_id}"

        url = URI("#{trello_url}/cards?name=#{card_name}&desc=#{card_description}&idList=#{list_id}&idMembers=#{member_id}&key=#{trello_key}&token=#{trello_token}")

        http = Net::HTTP.new(url.host, url.port)
        http.use_ssl = true
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE

        request = Net::HTTP::Post.new(url)

        response = http.request(request)
        puts response.read_body
      end
    end
end
