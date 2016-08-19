$(document).ready(function(){
	(function() {
		user = $('meta[name="auth"]').attr('content');
		if (user != "None") {
			$('#logout-link').css('display', 'inherit');
		} else {
			$('#logout-link').css('display', 'none');
		}
	})();

	var RecipeView = Backbone.View.extend({
		tagName: 'div',
		className: 'recipe',
		template: _.template($('#recipe-collection').html()),
		initialize: function(){
			this.render();
		},
		render: function() {
			this.$el.html(this.template(this.model.toJSON()));
			this.$el.css('background-image', 'linear-gradient(rgba(0,0,0,0.33),rgba(0,0,0,0.33)), url("'+this.model.get("image_url")+'")')
			return this
		},
		events: {
			'click' : 'getRecipeDetails'
		},
		loadingGif : loadingGifSrc,

		getRecipeDetails : function() {
			
			if (renderRecipeDetails.lastClicked != this.model) {
				renderRecipeDetails.lastClicked = this.model;
				$('.recipe').css("border","4px solid rgba(0,0,0,0)");
				this.$el.css('border', "4px solid #F44336");
				$('#details').html(this.loadingGif);
				
				this.model.fetch().success(function(response){
					recipeDetails.clear({silent:true})
					recipeDetails.set(response.recipe);
				});
			}
		}, 

	});

	var RecipeDetailView = Backbone.View.extend({
		el: '#details',
		template: _.template($('#recipe-details-template').html()),
		render: function() {
			this.$el.empty()
			this.$el.html(this.template(this.model.toJSON()));
			if ($('#recipe_tab_left').css('display') == 'none') {
				$('#openAddBook').hide();
			} else {
				$('#removeRecipe-btn').hide();
			}
			if (user == "None") {
				$('#openAddBook').prop('disabled',true);
			}

			return this;
		},
		initialize: function(){
			this.listenTo(this.model, 'change', this.render)
		},
		events: {
			'click #openAddBook' : 'getCategories',
			'submit #add-recipe-form' : 'addToCookbook',
			'click #add-book-btn' : 'addToCookbook',
			'click #removeRecipe-btn' : 'removeFromCookbook',
		},

		getCategories: function() {
			if (user != "None") {
				var categories = cookbookCategories.collection.models;
				for (idx in categories) {
					var c = categories[idx].get('category');
					if (c != "None"){
						$('#select-category').append('<option value="'+c+'">'+c+'</option>')
					}
				}
				
			}
		},

		addToCookbook : function(e) {
			e.preventDefault()
			var recipe_cat = this.$el.find('input[name="new_category"]').val().trim();
			if (recipe_cat == '') {
				recipe_cat = this.$el.find('select[name="category"]').val();
			}

			this.model.set('category', recipe_cat, {silent:true});
			var recipeToAdd = new CookbookRecipeModel(this.model.attributes);
			recipeToAdd.save().success(function(response){

				$('#add-book-modal-body .form-group').hide();
				$('#add-book-success').show();	

				cookbookCollection.reset(response.recipes);
				if (response.categories.length != renderCookbook.categories.length) {
					renderCookbook.categories.reset(response.categories);
				}
				setTimeout(function(){
					$('#add-book-modal').modal('toggle');
					$('#add-book-success').hide();	
					$('#add-book-modal-body .form-group').show();
					$('#openAddBook').hide();
					$('#removeRecipe-btn').show();
				}, 1000);

			});
			this.$el.find('input[name="new_category"]').val('')
			


		},
		removeFromCookbook : function() {
			var remove = cookbookCollection.findWhere({recipe_id:this.model.id});
			self=this
			remove.destroy({wait: true}).success(function(response){
				if (response.reset_cat != renderCookbook.categories.length) {
					renderCookbook.categories.reset(response.categories);
				}				
				self.$el.empty();
				self.lastClicked = undefined
				// self.model.clear({silent: true});
				renderRecipeList.render()

			});
		},
		lastClicked : undefined,
		
		

	});

	var RecipeListView = Backbone.View.extend({
		el: '#wrapper',
		render: function() {
			var $list = this.$('div#search_content').empty();

			this.collection.each(function(recipe){
				var recipeView = new RecipeView({model: recipe});
				try {
					$list.append(recipeView.render().$el);
				} catch (err) {
					
					console.log(err);
				
				}
				
			}, this);
		},
		initialize: function(){
			if (user != "None") {
				cookbookCollection = new CookbookCollection()
				cookbookCollection.fetch().then(function(response){
					renderCookbook = new CookbookListView({collection: cookbookCollection});
				});
			}

		},
		events: {
			'submit #search-form' : 'newSearch',
			'submit #register-user-form' : 'registerUser',
			'click #cookbook-link' : 'toggleSearch',
			'submit #login-user-form' : 'loginUser',
		},

		newSearch: function(e) {
			e.preventDefault()
			var params = this.$el.find('input[name="food-search"]').val()
			if (this.recentSearchParams[this.recentSearchParams.length-1] == params || params == '') {
				return
			}
			$('#search_content').html(this.loadingGif);
			this.recentSearchParams.push(params)
			self=this
			this.collection.fetch({data : {s:params}}).then(function(){
				self.render();
			})
			
			
		},
		registerUser: function(e){
			e.preventDefault()
			$('.form_errors').text('');
			$.post('accounts/register/', $('#register-user-form').serialize(), function(response){
				if (response.errors) {
					var errors = JSON.parse(response.errors);
					if (errors.email) {
						$('#id_email_errors').text(errors.email[0].message);
					}
					if (errors.username) {
						$('#id_username_errors').text(errors.username[0].message);
					}
					if (errors.password1) {
						$('#id_password1_errors').text(errors.password1[0].message);
					}
					if (errors.password2) {
						$('#id_password2_errors').text(errors.password2[0].message);
					}
				} else if (response.status == true) {
					$('#register-user-form').html("<h4 class='text-info'>Thank you for registering!</h4><h5 class='text-info'>You can now add recipes to your cookbook.</h5>");
					$('#register-link').css('display', 'none');
					$('#login-link').css('display', 'none');
					$('#logout-link').css('display', 'inherit');
					$('#user-register-btn').css('display', 'none');
					cookbookCollection = new CookbookCollection()
					cookbookCollection.fetch().then(function(response){
						user = response.user;
						renderCookbook = new CookbookListView({collection: cookbookCollection});
					});
					setTimeout(function(){
						$('#user-register-modal').modal('toggle');
					}, 2000);
					
				}
			}, 'json');
		},

		loginUser: function(e){
			e.preventDefault()
			$('.form_errors').text('');
			$.post('accounts/login/', $('#login-user-form').serialize(), function(response){
				if (response.status == true) {
					$('#login-user-form').html("<h4 class='text-info'>Welcome back!</h4>");
					$('#register-link').css('display', 'none');
					$('#login-link').css('display', 'none');
					$('#logout-link').css('display', 'inherit');
					$('#user-login-btn').css('display', 'none');
					cookbookCollection = new CookbookCollection()
					cookbookCollection.fetch().then(function(response){
						user = response.user;
						renderCookbook = new CookbookListView({collection: cookbookCollection});
					});
					setTimeout(function(){
						$('#user-login-modal').modal('toggle');
					}, 1000);
				} else {
					$('#login_errors').text(response.errors)
				}
				

			}, 'json');
		},

		toggleSearch: function(){
			if (user == "None") {
				$('#user-register-modal').modal('toggle');
				return
			}
			if (this.showSearch) {
				$('#search-bar, #recipe_tab_left').css('display', 'none');
				$('#myCookbook_tab').css('display', 'inherit');
				$('#cookbook-link a').text('Back to Search');
				this.showSearch = false;
			} else {
				$('#myCookbook_tab').css('display', 'none');
				$('#search-bar, #recipe_tab_left').css('display', 'inherit');
				$('#cookbook-link a').text('Open my cookbook');
				this.showSearch = true;
			}
		},

		recentSearchParams : [],
		loadingGif : loadingGifSrc,
		showSearch: true,

	});

	var RecipeCategoryView = Backbone.View.extend({
		tagName: 'div',
		className: 'panel panel-default',
		template: _.template($('#cookbook-categories').html()),
		render: function() {
			this.$el.html(this.template(this.model.toJSON()));
			return this;
		},
	});

	var RecipeCategoryListView = Backbone.View.extend({
		el: '#accordion',
		render: function(){
			this.$el.empty();
			this.collection.each(function(category){
				var categoryView = new RecipeCategoryView({
					model: category,
					id: "category-row-"+category.get('id')
				});
				this.$el.append(categoryView.render().$el);
			}, this);

			try {
				renderCookbook.render();
			} catch (err) {
			}
		},
		initialize: function(){
			this.listenTo(this.collection, 'reset', this.render);
			this.render();
		}
	});

	var CookbookListView = Backbone.View.extend({
		el: '#wrapper',
		render: function() {
			var $list = this.$('div#accordion.panel.panel-default').empty();
			this.$('.panel-collapse.collapse').empty();
			this.collection.each(function(recipe){
				$list = this.$('#collapse'+recipe.get('category_id'));
				var recipeView = new RecipeView({model: recipe});
				$list.append(recipeView.render().$el);

			}, this);
		},
		initialize: function(){
			this.categories = new RecipeCategoryCollection(this.collection.categories);
			cookbookCategories = new RecipeCategoryListView({collection: this.categories});
			this.listenTo(this.collection, 'reset', this.render);
			this.listenTo(this.collection, 'remove', this.render);
			this.render();
		},
		

		

	});

	var recipeCollection = new RecipeCollection()
	var renderRecipeList = new RecipeListView({collection: recipeCollection})

	var recipeDetails = new RecipeDetailModel()
	var renderRecipeDetails = new RecipeDetailView({model : recipeDetails})
});


