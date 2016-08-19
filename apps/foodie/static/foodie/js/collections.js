var RecipeCollection = Backbone.Collection.extend({
	model: RecipeModel,
	url: '/recipes',
	parse: function(recipes){
		return recipes.recipes
	}

});

var RecipeCategoryCollection = Backbone.Collection.extend({
	model: RecipeCategoryModel,
});


var CookbookCollection = Backbone.Collection.extend({
	model: CookbookRecipeModel,
	url: '/cookbooks',
	parse: function(cookbook){
		this.categories = cookbook.categories;
		return cookbook.recipes
	}
});


