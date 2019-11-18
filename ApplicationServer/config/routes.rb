Rails.application.routes.draw do
  resources :users
  #get 'hello_world', to: 'hello_world#index'
  root 'hello_world#index'
  get 'about', to: 'about#index'
  get 'meeting', to: 'meeting#index'
  #match '*path', to: 'hello_world#index' via :all
end
