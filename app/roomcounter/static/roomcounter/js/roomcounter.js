// Define a new component called button-counter
Vue.component('room-counter', {
    props: ["door_id", "ws_url"],
    data: function () {
        return {
            name: "Door",
            count_left_to_right: 0,

            left_name: "Left",
            left_utilization: 0,
            left_capacity: 0,

            right_name: "Right",
            right_utilization: 0,
            right_capacity: 0,

            critical_thresh: 2,
        }
    },
    template: `
<div>
<div class="row">
  <div class="col-sm-6">
    <div class="card text-center" v-bind:class="{'border-danger': left_room_critical}">
      <h3 class="card-header" v-bind:class="{'bg-danger': left_room_critical}">{{ left_name }}</h3>
      <div class="card-body" v-bind:class="{'bg-danger': left_room_full}">

        <span v-if="left_capacity > 0" style="font-size: 2em;">{{ left_utilization }} / {{ left_capacity }}</span>
        <span v-else style="font-size: 2em;">Keine Beschränkung</span>
        <br>
        <br>
        <button class="btn btn-lg btn-secondary" v-bind:class="{'btn-danger': left_room_critical, 'btn-secondary': !left_room_critical}" v-on:click="pass_door(-1)">Enter</button>

      </div>
    </div>
  </div>

  <div class="col-sm-6">
    <div class="card text-center" v-bind:class="{'border-danger': right_room_critical}">
      <h3 class="card-header" v-bind:class="{'bg-danger': right_room_critical}">{{ right_name }}</h3>
      <div class="card-body" v-bind:class="{'bg-danger': right_room_full}">
        <span v-if="right_capacity > 0" style="font-size: 2em;">{{ right_utilization }} / {{ right_capacity }}</span>
        <span v-else style="font-size: 2em;">Keine Beschränkung</span>
        <br>
        <br>
        <button class="btn btn-lg" v-bind:class="{'btn-danger': right_room_critical, 'btn-secondary': !right_room_critical}" v-on:click="pass_door(1)">Enter</button>

      </div>
    </div>
  </div>
</div>
</div>
              `,
    methods: {
        pass_door: function (val) {
            this.count_left_to_right += val;

            // keep local value of room counts in line with observed door pass
            if (this.left_capacity > 0)
                this.left_utilization -= val;
            if (this.right_capacity > 0)
                this.right_utilization += val;

            this.send();
        },
        refresh: function (send=false) {
            if(send && this.count_left_to_right != 0) {
                this.send();
            };
            $.get("/doors/{0}".format(this.door_id))
                .done(data => {
                    this.name = data.name;

                    this.left_name = data.left_room.name;
                    this.left_utilization = data.left_room.utilization;
                    this.left_capacity = data.left_room.capacity;

                    this.right_name = data.right_room.name;
                    this.right_utilization = data.right_room.utilization;
                    this.right_capacity = data.right_room.capacity;
                });
        },
        send: function () {
            let value_to_send = this.count_left_to_right;

            // reset counter to zero (if there was another count
            // in the meantime, account for it -> subtract value to send)
            this.count_left_to_right -= value_to_send;

            $.post("/activities/pass_door", JSON.stringify({door_id: this.door_id, count_left_to_right: value_to_send}))
                .done( () => {
                    this.refresh(false);
                })
                .fail( () => {
                    // remember not sent counters for next try
                    this.count_left_to_right += value_to_send;
                });
        },
    },
    computed: {
        left_room_critical: function() {
            if (this.left_capacity == 0)
                return false;
            return this.left_utilization >= this.left_capacity - this.critical_thresh;
        },
        right_room_critical: function() {
            if (this.right_capacity == 0)
                return false;
            return this.right_utilization >= this.right_capacity - this.critical_thresh;
        },
        left_room_full: function() {
            if (this.left_capacity == 0)
                return false;
            return this.left_utilization >= this.left_capacity;
        },
        right_room_full: function() {
            if (this.right_capacity == 0)
                return false;
            return this.right_utilization >= this.right_capacity;
        },
    },
    watch: {
        door_id: function() {
            this.refresh();
        },
    },
    created: function () {
        this.refresh();
        let _this = this;

        console.log("Starting connection to WebSocket Server")
        this.connection = new WebSocket(this.ws_url);

        this.connection.onmessage = function(event) {
            let data = event.data;
            if (data == "pass_door") {
                _this.refresh();
            }
        }

        this.connection.onopen = function(event) {
            console.log("Successfully connected to WebSocket server...")
        }
    },
})
