Rails.application.routes.draw do
  resources :users
  resources :meetings
  #get 'hello_world', to: 'hello_world#index'
  root 'hello_world#index'
  get 'about', to: 'about#index'
  #match '*path', to: 'hello_world#index' via :all

  resources :sessions, only: [:new, :create, :destroy]
  get 'signup', to: 'users#new', as: 'signup'
  get 'login', to: 'sessions#new', as: 'login'
  post 'login', to: 'sessions#create'
  get 'welcome', to: 'sessions#welcome'
  get 'logout', to: 'sessions#destroy', as: 'logout'

  post 'meetings/analyze'

end
