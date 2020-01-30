class CreateMeetings < ActiveRecord::Migration[6.0]
  def change
    create_table :meetings do |t|
      t.string :name
      t.integer :participants
      t.integer :user1
      t.integer :user2
      t.integer :user3

      t.timestamps
    end
  end
end
