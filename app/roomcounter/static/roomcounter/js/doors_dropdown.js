Vue.component('doors-dropdown', {
    data: function () {
        return {
            current_door: null,
            doors: [],
        }
    },
    template: `
<div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    {{ current_door ? current_door.name : "Select Door" }}
  </button>
  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
    <a v-for="door in doors" class="dropdown-item" href="#" v-bind:data-key="door.id" v-on:click="selected(door.id)">{{ door.name }}</a>
  </div>
</div>
    `,
    created: function() {
        $.get("/doors/")
            .done( (doors) => {
                this.doors = doors;
            })
            .fail( () => {
                console.error("Could not load doors.");
            });
    },
    methods: {
        selected: function(door_id) {
            let door = this.doors.find((door) => {return door.id == door_id});
            this.current_door = door;
            this.$emit("selected", door_id);
        },
    },
})
