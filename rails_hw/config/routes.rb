Rails.application.routes.draw do
  #get 'hello_world', to: 'hello_world#index'
  root 'hello_world#index'
  get 'about', to: 'about#index'
end
