enyo.kind({
	name: "App",
	kind: "FittableRows",
	fit: true,
	components:[
		{kind: "onyx.Toolbar", style: "height:2em;padding:2px", components: [
            {kind: "onyx.MenuDecorator", style:"float:right;margin:0", onSelect: "itemSelected", components: [
                {content: "Wifi"},
                {kind: "onyx.Menu", components: [
                    {components: [
                        {content: "Ssid", fit: true},
                        {kind: "onyx.IconButton", classes: "wifi-signal", src: "assets/nm-signal-100.svg"}
                    ]},
                    {content: "Ssid2"}
                ]}
            ]}
        ]},
		{kind: "enyo.Scroller", fit: true, components: [
			{name: "main", classes: "nice-padding", allowHtml: true}
		]}
	],
    getSignalNumber: function(num) {
        /*
        What this function does is splits the numbers into 4 segments that
        we have pictures for and uses the rounding function to assign them
        currectly
        */
        return Number(Math.round(num/25))*25
    }
});
