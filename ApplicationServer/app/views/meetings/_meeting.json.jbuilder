json.extract! meeting, :id, :name, :participants, :created_at, :updated_at
json.url meetings_url(meeting, format: :json)
