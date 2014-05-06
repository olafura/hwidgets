enyo.kind({
	name: "AppQt",
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
    //When everything is up and running I want to start polling
    create: function() {
        this.inherited(arguments);
        battery.on_battery_status.connect(enyo.bind(this, this.populateBattery));
        battery.getCurrentBattery("");
        //wifi.on_wifi_status.connect(function(value){console.log("value",value);});
        wifi.on_wifi_status.connect(enyo.bind(this, this.populateWifi));
        wifi.checkAccessPoints("");
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
    populateBattery: function(value) {
        value = JSON.parse(value);
        //console.log("value",value);
        var timeremaining = value.TimeToEmpty.toString()+" sec";
        var percentage = value.Percentage.toString()+"%";
        //console.log("percentage",percentage);
        var capacity = value.Capacity.toFixed(2)+" mAh";
        var percent_string = this.getBatteryNumber(value.Percentage);
        this.$.BatteryIcon.setSrc("web/assets/gpm-battery-"+percent_string+".svg");
        this.$.BatteryMenu.destroyClientControls();
        this.$.BatteryMenu.createComponents([
            {content: "Percentage: "+percentage},
            {content: "Time Remaining: "+timeremaining},
            {content: "Capacity: "+capacity},
        ]);
        this.$.BatteryMenu.render();
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
    populateWifi: function(value) {
        value = JSON.parse(value);
        //console.log("value",value);
        if(value.length > 1) {
            var lst = [];
            var length1 = value.length;
            for(var i1=0; i1 < length1; i1++) {
                //console.log("i",i1);
                var ap = value[i1];
                //console.log("ap",ap);
                if(ap.is_available) {
                    if(ap.is_active) {
                        lst.unshift({content: "Available", classes: "wifi-head"});
                        lst.unshift({kind:"WifiMenuItem", ssid: ap.ssid,
                                     signal: ap.strength});
                        lst.unshift({content: "Current", classes: "wifi-head"});
                    } else {
                        lst.push({kind:"WifiMenuItem", ssid: ap.ssid,
                                     signal: ap.strength});
                    }
                } else {
                }
            }
            this.setWifiap(lst);
        } else {
            var ap = value[0];
            if(ap.is_available) {
                this.wifiap.push({kind:"WifiMenuItem", ssid: ap.ssid,
                             signal: ap.strength});
            } else {
                var length2 = this.wifiap.length;
                for(var i2=0; i2 < length2; i2++) {
                    if(this.wifiap[i2].ssid == ap.ssid) {
                        //console.log("remove", i2, ap.ssid);
                        this.wifiap.remove(i2);
                        break;
                    }
                }
            }
        }
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

// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

