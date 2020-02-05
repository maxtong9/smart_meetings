class Meeting < ApplicationRecord
  has_many_attached :file
  
  attr_accessor :my_file
end
