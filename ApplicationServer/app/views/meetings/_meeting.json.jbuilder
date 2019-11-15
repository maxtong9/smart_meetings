json.extract! meeting, :id, :name, :created_at, :updated_at
json.url meetings_url(meeting, format: :json)
