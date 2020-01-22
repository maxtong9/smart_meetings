class CreateUsers < ActiveRecord::Migration[6.0]
  def change
    create_table :users do |t|
      t.string :name
      t.string :password
      t.integer :meeting_1
      t.integer :meeting_2
      t.integer :meeting_3
      t.integer :meeting_4
      t.integer :meeting_5

      t.timestamps
    end
  end
end
