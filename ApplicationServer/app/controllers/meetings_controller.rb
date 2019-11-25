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
      hostname = '169.231.51.177' # REPLACE THIS WITH YOUR PUBLIC IP ADDRESS FOR DOCKER
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
end
