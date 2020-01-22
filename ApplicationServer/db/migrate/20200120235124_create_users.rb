class CreateUsers < ActiveRecord::Migration[6.0]
  def change
    create_table :users, :id => false do |t|
      t.integer :id
      t.string :name
      t.integer :meeting_1
      t.integer :meeting_2
      t.integer :meeting_3
      t.integer :meeting_4
      t.integer :meeting_5

      t.timestamps
    end
  end
end
