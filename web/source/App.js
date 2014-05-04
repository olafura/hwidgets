enyo.kind({
	name: "App",
	kind: "FittableRows",
	fit: true,
    published: {
        //The access points
        wifiap: []
    },
	components:[
		{kind: "onyx.Toolbar", style: "height:2em;padding:2px", components: [
            {kind: "onyx.MenuDecorator",style:"float:right;margin:0", onSelect: "itemSelected", components: [
                //The battery icon that will be changed depending on the
                //battery level
                {name: "BatteryIcon", kind: "onyx.IconButton", src: "web/assets/gpm-battery-100.svg"},
                {name: "BatteryMenu", classes: "wifi-menu", kind: "onyx.Menu", components: [
                    {content: "Waiting for Battery"}
                ]}
            ]},
            {kind: "onyx.MenuDecorator",style:"float:right;margin:0", onSelect: "itemSelected", components: [
                //I update the wifi menu only when you click on the button
                //otherwise the we would always be doing interface updates
                {content: "Wifi", ontap: "updateWifi"},
                {name: "WifiMenu", classes: "wifi-menu", kind: "onyx.Menu", components: [
                    {content: "Waiting for Wifi"}
                ]}
            ]}
        ]},
        //Just a empty area
		{kind: "enyo.Scroller", fit: true, components: [
			{name: "main", classes: "nice-padding", allowHtml: true}
		]}
	],
    //As soon as the module is constructed I want to get the database set-up
    constructor: function() {
        this.inherited(arguments);
        this.start();
    },
    start: function() {
        this.wifidb = new SundayData("http://localhost:5984/wifi/");
        this.batterydb = new SundayData("http://localhost:5984/battery/");
    },
    //When everything is up and running I want to start polling
    create: function() {
        this.inherited(arguments);
        var parent = this;
        //I should be doing request animation frame, I can't use EventSource
        //because there are tomany updates going on
        var wifichange = new EventSource('http://localhost:5984/wifi/_changes?feed=eventsource');
        wifichange.addEventListener('message', function(e) {
            parent.populateWifi();
        });
        //With EventSource I only update it when I get a update
        var batterychange = new EventSource('http://localhost:5984/battery/_changes?feed=eventsource');
        batterychange.addEventListener('message', function(e) {
            parent.populateBattery();
        });

    },
    updateWifi: function() {
            this.$.WifiMenu.destroyClientControls();
            if(this.wifiap.length == 0) {
                this.$.WifiMenu.createComponents([{content: "Waiting for Wifi"}]);
            } else {
                this.$.WifiMenu.createComponents(this.wifiap);
            }
            this.$.WifiMenu.render();
    },
    populateBattery: function() {
        var parent = this;
        this.batterydb.get("battery").done(function(value) {
            //console.log(value);
            var timeremaining = value.TimeToEmpty.toString()+" sec";
            var percentage = value.Percentage.toString()+"%";
            var capacity = value.Capacity.toFixed(2)+" mAh";
            var percent_string = parent.getBatteryNumber(value.Percentage);
            parent.$.BatteryIcon.setSrc("web/assets/gpm-battery-"+percent_string+".svg");
            parent.$.BatteryMenu.destroyClientControls();
            parent.$.BatteryMenu.createComponents([
                {content: "Percentage: "+percentage},
                {content: "Time Remaining: "+timeremaining},
                {content: "Capacity: "+capacity},
            ]);
            parent.$.BatteryMenu.render();
        });
    },
    getBatteryNumber: function(num) {
        /*
        What this function does is splits the numbers into 4 segments that
        we have pictures for and uses the rounding function to assign them
        currectly
        */
        var percent = Number(Math.round(num/20))*20
        var percent_string = percent.toString();
        if(percent !== 100) {
            if(percent === 0) {
                percent_string = "00" + percent_string;
            } else {
                percent_string = "0" + percent_string;
            }
        }
        return percent_string
    },
    populateWifi: function() {
        var parent = this;
        this.wifidb.allDocs({include_docs: true}).done(function(value) {
            var lst = [];
            for(var i in value.rows) {
                var ap = value.rows[i];
                if(ap.doc.is_available) {
                    if(ap.doc.is_active) {
                        lst.unshift({content: "Available", classes: "wifi-head"});
                        lst.unshift({kind:"WifiMenuItem", ssid: ap.id,
                                  signal: ap.doc.strength});
                        lst.unshift({content: "Current", classes: "wifi-head"});
                    } else {
                        lst.push({kind:"WifiMenuItem", ssid: ap.id,
                                  signal: ap.doc.strength});
                    }
                } else {
                    //console.log("old: ", ap.id);
                }
            }
            parent.setWifiap(lst);
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
        {name: "signalItem", classes: "wifi-signal", kind: "onyx.IconButton", src: "web/assets/nm-signal-100.svg"}
    ],
    ssidChanged: function() {
        this.$.ssidItem.setContent(this.ssid);
    },
    signalChanged: function() {
        var signal = this.getSignalNumber(this.signal);
        //console.log("signal", signal);
        this.$.signalItem.setSrc("web/assets/nm-signal-"+signal+".svg");
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
