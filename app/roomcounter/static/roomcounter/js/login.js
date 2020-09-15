// Define a new component called button-counter
Vue.component('login', {
    props: {
        "me_url": {default: "/auth/me"},
        "login_url": {default: "/auth/login"},
        "logout_url": {default: "/auth/logout"}
    },
    data: function () {
        return {
            initialized: false,
            user: null,
            username: "",
            password: "",
        }
    },
    template: `
<ul class="navbar-nav mr-auto">
  <li v-if="user" class="nav-item">
    <a class="nav-link"><span class="fa fa-user"></span>&nbsp;{{ user.username }}</a>
  </li>
  <li v-if="user" class="nav-item" id='nav_item_logout'>
    <a class="nav-link" v-bind:href="logout_url" @click.prevent="logout"><span class="fa fa-power-off"></span>&nbsp;Logout</a>
  </li>

  <li v-if="!user && initialized" class="nav-item">
    <form class="form-signin" method="post" v-bind:action="login_url" @submit.prevent="login">
      <input type="text" class="input-block-level" placeholder="Login" name="username" v-model="username">
      <input type="password" class="input-block-level" placeholder="Password" name="password" v-model="password">
      <button class="btn btn-large btn-dark" type="submit" name="form.submitted">Log in</button>
    </form>
  </li>
</ul>
    `,
    methods: {
        login: function() {
            $.post(this.login_url, $(this.$el).find("form").serialize())
                .done( (data) => {
                    location.reload();
                })
                .fail( (a,b,c, d) => {
                    alert("Failed to login: " + c);
                });
        },
        logout: function() {
            $.get(this.logout_url)
                .done( (data) => {
                    location.reload();
                })
                .fail( (a,b,c) => {
                    console.log("Failed to logout:", c);
                });
        },
    },
    created: function () {
        $.get(this.me_url)
            .done( (data) => {
                this.user = data;
                this.initialized = true;
            });
    },
})
