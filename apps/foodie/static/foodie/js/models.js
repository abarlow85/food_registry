var RecipeModel = Backbone.Model.extend({
	idAttribute: "recipe_id",
	defaults: {

	}
});

var RecipeDetailModel = Backbone.Model.extend({
	idAttribute: "recipe_id",
	defaults: {

	},
});

var RecipeCategoryModel = Backbone.Model.extend({

});

var CookbookRecipeModel = Backbone.Model.extend({
	urlRoot: '/cookbooks',
	defaults: {
		notes : "Enter notes"
	}, 
});
