enyo.kind({
	name: "App",
	kind: "FittableRows",
	fit: true,
	components:[
		{kind: "onyx.Toolbar", style: "height:2em;padding:2px", components: [
            {kind: "onyx.MenuDecorator", style:"float:right;margin:0", onSelect: "itemSelected", components: [
                {content: "Bookmarks menu"},
                {kind: "onyx.Menu", components: [
                    {components: [
                        {kind: "onyx.IconButton", src: "assets/menu-icon-bookmark.png"},
                        {content: "Bookmarks"}
                    ]},
                    {content: "Favorites"},
                    {classes: "onyx-menu-divider"},
                    {content: "Recents"}
                ]}
            ]}
        ]},
		{kind: "enyo.Scroller", fit: true, components: [
			{name: "main", classes: "nice-padding", allowHtml: true}
		]}
	],
    getSignalNumber(num) {
        /*
        What this function does is splits the numbers into 4 segments that
        we have pictures for and uses the rounding function to assign them
        currectly
        */
        return Number(Math.round(num/25))*25
    }
});
