enyo.kind({
	name: "App",
	kind: "FittableRows",
	fit: true,
	components:[
		{kind: "onyx.Toolbar", style: "height:2em;padding:2px", components: [
            {kind: "onyx.MenuDecorator",style:"float:right;margin:0", onSelect: "itemSelected", components: [
                {content: "Wifi"},
                {name: "WifiMenu", classes: "wifi-menu", kind: "onyx.Menu", components: [
                    {content: "Ssid2"}
                ]}
            ]}
        ]},
		{kind: "enyo.Scroller", fit: true, components: [
			{name: "main", classes: "nice-padding", allowHtml: true}
		]}
	],
    constructor: function() {
        this.inherited(arguments);
        this.start();
    },
    start: function() {
        this.db = new SundayData("http://localhost:5984/wifi/");
    },
    create: function() {
        this.inherited(arguments);
        this.populateWifi();
    },
    populateWifi: function() {
        var parent = this;
        this.db.allDocs({include_docs: true}).done(function(value) {
            parent.$.WifiMenu.destroyClientControls();
            var lst = [];
            var now = Math.round(new Date().getTime()/1000);
            for(var i in value.rows) {
                var ap = value.rows[i];
                var time = ap.doc.time;
                if((now - 20) < time) {
                    lst.push({kind:"WifiMenuItem", ssid: ap.id,
                              signal: ap.doc.strength});
                } else {
                    console.log("old: ", ap.id);
                }
            }
            parent.$.WifiMenu.createComponents(lst);
            parent.$.WifiMenu.render();
        });
    }
});

enyo.kind({
    name: "WifiMenuItem",
    published: {
        ssid: "",
        signal: 0
    },
    create: function() {
        this.inherited(arguments);
        this.start();
    },
    start: function() {
        this.ssidChanged();
        this.signalChanged();
    },
    components: [
        {name: "ssidItem", classes: "wifi-ssd", content: "Ssid"},
        {name: "signalItem", classes: "wifi-signal", kind: "onyx.IconButton", src: "assets/nm-signal-100.svg"}
    ],
    ssidChanged: function() {
        this.$.ssidItem.setContent(this.ssid);
    },
    signalChanged: function() {
        var signal = this.getSignalNumber(this.signal);
        console.log("signal", signal);
        this.$.signalItem.setSrc("assets/nm-signal-"+signal+".svg");
    },
    getSignalNumber: function(num) {
        /*
        What this function does is splits the numbers into 4 segments that
        we have pictures for and uses the rounding function to assign them
        currectly
        */
        return Number(Math.round(num/25))*25
    }
});
