Rails.application.routes.draw do
  get 'hello_world', to: 'hello_world#index'
  root 'static#index'
	namespace :v1, defaults: { format: 'json' } do
     get 'things', to: 'things#index'
  end 
end
