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

card_name = "Test Card"
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
